import os
import signal
import subprocess
import threading
import time
from typing import List, Optional

from .config import ServerConfig
from .logger import get_logger


logger = get_logger("openvpn")


class OpenVPNProcessManager:
    def __init__(self) -> None:
        self._process: Optional[subprocess.Popen] = None
        self._stdout_lines: List[str] = []
        self._stderr_lines: List[str] = []
        self._reader_thread: Optional[threading.Thread] = None
        self._stop_read_event = threading.Event()

    def is_running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def _build_command(self, server: ServerConfig) -> List[str]:
        cmd: List[str] = []
        if server.use_sudo:
            cmd.extend(["sudo", "-n"])  # -n: non-interactive; fail if password is needed
        cmd.append(server.openvpn_path)
        cmd.extend(["--config", server.ovpn_config_path])
        if server.auth_user_pass_path:
            cmd.extend(["--auth-user-pass", server.auth_user_pass_path])
        cmd.extend(["--verb", "3"])  # moderate verbosity for logs
        # Do not daemonize, we want to capture stdout to detect readiness
        # Accept extra args
        if server.extra_args:
            cmd.extend(server.extra_args)
        return cmd

    def _reader(self, pipe, buffer: List[str], name: str) -> None:
        try:
            while not self._stop_read_event.is_set():
                line = pipe.readline()
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace").rstrip()
                buffer.append(decoded)
                if name == "stdout":
                    logger.info("ovpn: %s", decoded)
                else:
                    logger.error("ovpn-err: %s", decoded)
        except Exception as exc:
            logger.exception("Reader thread error: %s", exc)

    def start(self, server: ServerConfig, connect_timeout_seconds: int = 90) -> bool:
        if self.is_running():
            logger.info("OpenVPN already running; stopping existing instance before starting new.")
            self.stop()

        cmd = self._build_command(server)
        logger.info("Starting OpenVPN: %s", " ".join(cmd))

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
            )
        except FileNotFoundError:
            logger.error("OpenVPN executable not found: %s", server.openvpn_path)
            return False
        except subprocess.CalledProcessError as exc:
            logger.error("Failed to start OpenVPN: %s", exc)
            return False
        except Exception as exc:
            logger.exception("Unexpected error starting OpenVPN: %s", exc)
            return False

        assert self._process.stdout is not None
        assert self._process.stderr is not None

        self._stop_read_event.clear()
        self._stdout_lines.clear()
        self._stderr_lines.clear()
        self._reader_thread = threading.Thread(
            target=self._reader, args=(self._process.stdout, self._stdout_lines, "stdout"), daemon=True
        )
        self._reader_thread.start()
        threading.Thread(
            target=self._reader, args=(self._process.stderr, self._stderr_lines, "stderr"), daemon=True
        ).start()

        # Wait for success marker or failure/timeout
        start_time = time.time()
        while time.time() - start_time < connect_timeout_seconds:
            if self._process.poll() is not None:
                logger.error("OpenVPN exited early with code %s", self._process.returncode)
                return False

            # Success marker printed by OpenVPN when tunnel is established
            if any("Initialization Sequence Completed" in ln for ln in self._stdout_lines):
                logger.info("OpenVPN connection established.")
                return True

            # Detect common failure patterns early
            failure_markers = [
                "AUTH_FAILED",
                "TLS Error",
                "Connection reset",
                "Inactivity timeout",
                "Exiting due to fatal error",
                "Cannot ioctl TUNSETIFF",
                "ERROR: Cannot open TUN/TAP dev",
                "ERROR: You must define TUN/TAP device",
                "sudo: a password is required",
                "AUTH: Received control message: AUTH_FAILED",
            ]
            if any(any(marker in ln for marker in failure_markers) for ln in (self._stdout_lines + self._stderr_lines)):
                logger.error("Detected error during OpenVPN startup. Stopping.")
                self.stop()
                return False

            time.sleep(1)

        logger.error("Timed out waiting for OpenVPN to connect after %s seconds", connect_timeout_seconds)
        return False

    def stop(self, force_kill_after_seconds: int = 5) -> None:
        if not self._process:
            return
        try:
            if self.is_running():
                logger.info("Stopping OpenVPN (SIGTERM)...")
                self._process.terminate()
            # Wait a bit, then kill if needed
            try:
                self._process.wait(timeout=force_kill_after_seconds)
            except subprocess.TimeoutExpired:
                if self.is_running():
                    logger.warning("OpenVPN did not stop in time; sending SIGKILL")
                    self._process.kill()
        finally:
            self._stop_read_event.set()
            self._process = None
            self._reader_thread = None

    def collect_logs(self) -> List[str]:
        return list(self._stdout_lines + self._stderr_lines)
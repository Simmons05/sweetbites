import argparse
import signal
import sys
import time
from typing import Optional

from .config import AppConfig, ServerConfig, load_config
from .health_check import is_connection_healthy
from .logger import get_logger, setup_logging
from .openvpn_manager import OpenVPNProcessManager


logger = get_logger("cli")


class FailoverVPNClient:
    def __init__(
        self,
        app_config: AppConfig,
        connection_timeout_seconds: int,
        health_check_interval_seconds: int,
        require_country_match: bool,
        expected_country_code: str,
        health_timeout_seconds: int,
    ) -> None:
        self._config = app_config
        self._connection_timeout_seconds = connection_timeout_seconds
        self._health_check_interval_seconds = health_check_interval_seconds
        self._require_country_match = require_country_match
        self._expected_country_code = expected_country_code
        self._health_timeout_seconds = health_timeout_seconds
        self._openvpn = OpenVPNProcessManager()
        self._stop = False
        self._active_index: Optional[int] = None

    def _connect_to_server(self, idx: int) -> bool:
        server = self._config.servers[idx]
        logger.info("Attempting connection to server %d/%d: %s", idx + 1, len(self._config.servers), server.name)
        ok = self._openvpn.start(server, connect_timeout_seconds=self._connection_timeout_seconds)
        if not ok:
            logger.error("Connection to server %s failed.", server.name)
            return False
        # Post-connect health validation
        if not is_connection_healthy(
            expected_country_code=self._expected_country_code,
            require_country_match=self._require_country_match,
            timeout_seconds=self._health_timeout_seconds,
        ):
            logger.error("Health check failed after connecting to %s. Disconnecting.", server.name)
            self._openvpn.stop()
            return False
        logger.info("Connected and healthy on server: %s", server.name)
        self._active_index = idx
        return True

    def _disconnect(self) -> None:
        self._openvpn.stop()
        self._active_index = None

    def _next_index(self, current: int) -> int:
        return (current + 1) % len(self._config.servers)

    def run(self, start_index: int = 0) -> None:
        # Failover loop
        idx = start_index % len(self._config.servers)
        while not self._stop:
            if not self._connect_to_server(idx):
                idx = self._next_index(idx)
                continue

            # Monitor health periodically
            while not self._stop:
                time.sleep(self._health_check_interval_seconds)
                if not self._openvpn.is_running():
                    logger.error("OpenVPN process is not running; switching to next server.")
                    break
                healthy = is_connection_healthy(
                    expected_country_code=self._expected_country_code,
                    require_country_match=self._require_country_match,
                    timeout_seconds=self._health_timeout_seconds,
                )
                if not healthy:
                    logger.error("Health check failed; switching to next server.")
                    break
                logger.info("Health check passed.")

            self._disconnect()
            idx = self._next_index(idx)

    def request_stop(self) -> None:
        self._stop = True
        self._disconnect()


def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple VPN client with automatic US server failover (OpenVPN)")
    parser.add_argument(
        "--config",
        dest="config_path",
        default="/workspace/servers/servers.yml",
        help="Path to YAML configuration containing server entries.",
    )
    parser.add_argument(
        "--connect-timeout",
        dest="connect_timeout",
        type=int,
        default=90,
        help="Seconds to wait for OpenVPN to establish the tunnel before failing over.",
    )
    parser.add_argument(
        "--health-interval",
        dest="health_interval",
        type=int,
        default=60,
        help="Seconds between health checks while connected.",
    )
    parser.add_argument(
        "--health-timeout",
        dest="health_timeout",
        type=int,
        default=6,
        help="Per-request timeout for health check HTTP requests.",
    )
    parser.add_argument(
        "--expected-country",
        dest="expected_country",
        default="US",
        help="Expected country ISO code for the VPN egress IP.",
    )
    parser.add_argument(
        "--no-country-enforce",
        dest="no_country_enforce",
        action="store_true",
        help="Do not require IP geolocation to match expected country (only checks internet reachability).",
    )
    parser.add_argument(
        "--start-index",
        dest="start_index",
        type=int,
        default=0,
        help="Zero-based index of the server to start from.",
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> int:
    args = parse_args(argv)

    # Configure logging
    import logging

    level = getattr(logging, args.log_level.upper(), logging.INFO)
    setup_logging(level=level)

    try:
        app_config = load_config(args.config_path)
    except Exception as exc:
        logger.error("Failed to load configuration: %s", exc)
        return 2

    client = FailoverVPNClient(
        app_config=app_config,
        connection_timeout_seconds=args.connect_timeout,
        health_check_interval_seconds=args.health_interval,
        require_country_match=not args.no_country_enforce,
        expected_country_code=args.expected_country,
        health_timeout_seconds=args.health_timeout,
    )

    # Handle Ctrl+C gracefully
    def handle_sigint(sig, frame):
        logger.info("Received signal %s; stopping...", sig)
        client.request_stop()

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigint)

    try:
        client.run(start_index=args.start_index)
    except KeyboardInterrupt:
        handle_sigint(signal.SIGINT, None)
    finally:
        client.request_stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
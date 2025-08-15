import logging
import os
from logging.handlers import RotatingFileHandler


_DEFAULT_LOG_DIR = "/workspace/logs"
_LOG_FILE_NAME = "vpn_client.log"


def setup_logging(log_dir: str = _DEFAULT_LOG_DIR, level: int = logging.INFO) -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger("vpn_client")
    logger.setLevel(level)

    # Avoid duplicate handlers if setup_logging called multiple times
    if not logger.handlers:
        log_path = os.path.join(log_dir, _LOG_FILE_NAME)
        file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
        file_formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(level)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(level)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    parent = setup_logging()
    return parent.getChild(name)
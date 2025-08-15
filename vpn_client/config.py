import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

import yaml

from .logger import get_logger


logger = get_logger("config")


@dataclass
class ServerConfig:
    name: str
    ovpn_config_path: str
    auth_user_pass_path: Optional[str]
    extra_args: List[str]
    use_sudo: bool
    openvpn_path: str


@dataclass
class AppConfig:
    servers: List[ServerConfig]


def _validate_server(server_raw: dict) -> Tuple[Optional[ServerConfig], Optional[str]]:
    required_fields = ["name", "ovpn_config_path", "use_sudo", "openvpn_path"]
    missing = [f for f in required_fields if f not in server_raw]
    if missing:
        return None, f"Missing required fields {missing} in server entry"

    name = str(server_raw.get("name"))
    ovpn_config_path = str(server_raw.get("ovpn_config_path"))
    auth_user_pass_path = server_raw.get("auth_user_pass_path")
    if auth_user_pass_path is not None:
        auth_user_pass_path = str(auth_user_pass_path)
    extra_args = server_raw.get("extra_args") or []
    if not isinstance(extra_args, list):
        return None, "extra_args must be a list"
    use_sudo = bool(server_raw.get("use_sudo"))
    openvpn_path = str(server_raw.get("openvpn_path") or "openvpn")

    cfg = ServerConfig(
        name=name,
        ovpn_config_path=ovpn_config_path,
        auth_user_pass_path=auth_user_pass_path,
        extra_args=list(extra_args),
        use_sudo=use_sudo,
        openvpn_path=openvpn_path,
    )
    return cfg, None


def load_config(yaml_path: str) -> AppConfig:
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"Config file not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    servers_raw = data.get("servers") or []
    if not servers_raw:
        raise ValueError("No servers found in configuration under 'servers'.")

    servers: List[ServerConfig] = []
    for server_dict in servers_raw:
        cfg, err = _validate_server(server_dict)
        if err:
            logger.warning("Skipping server entry due to validation error: %s", err)
            continue
        servers.append(cfg)

    if not servers:
        raise ValueError("No valid servers after validation. Check your configuration file.")

    return AppConfig(servers=servers)
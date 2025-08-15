from typing import Optional, Tuple

import requests

from .logger import get_logger


logger = get_logger("health")


def _fetch_json(url: str, timeout_seconds: int) -> Optional[dict]:
    try:
        resp = requests.get(url, timeout=timeout_seconds)
        if 200 <= resp.status_code < 300:
            return resp.json()
        logger.warning("Health check URL %s returned status %s", url, resp.status_code)
    except Exception as exc:
        logger.warning("Health check URL %s failed: %s", url, exc)
    return None


def get_public_ip_and_country(timeout_seconds: int = 6) -> Tuple[Optional[str], Optional[str]]:
    # Try multiple providers to be resilient
    providers = [
        ("https://ipinfo.io/json", "ip", "country"),
        ("https://ipapi.co/json", "ip", "country"),
        ("https://ifconfig.co/json", "ip", "country"),
    ]

    for url, ip_key, country_key in providers:
        data = _fetch_json(url, timeout_seconds)
        if not data:
            continue
        ip = str(data.get(ip_key)) if data.get(ip_key) else None
        country = str(data.get(country_key)) if data.get(country_key) else None
        if ip and country:
            return ip, country

    # Fallback: try to get IP only
    try:
        resp = requests.get("https://api.ipify.org", timeout=timeout_seconds)
        if 200 <= resp.status_code < 300:
            return resp.text.strip(), None
    except Exception as exc:
        logger.warning("Fallback ipify failed: %s", exc)

    return None, None


def is_connection_healthy(expected_country_code: str = "US", require_country_match: bool = True, timeout_seconds: int = 6) -> bool:
    ip, country = get_public_ip_and_country(timeout_seconds=timeout_seconds)
    if not ip:
        logger.error("Could not determine public IP; assuming connection unhealthy.")
        return False

    logger.info("Public IP: %s, Country: %s", ip, country)
    if require_country_match:
        if (country or "").upper() != expected_country_code.upper():
            logger.error(
                "Country code %s does not match expected %s; assuming VPN not routed through expected region.",
                country,
                expected_country_code,
            )
            return False
    return True
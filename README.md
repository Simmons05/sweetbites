# Python OpenVPN Failover Client (US Servers)

A free, open-source Python 3 client that connects to US-based OpenVPN servers and automatically fails over when a server is blocked or becomes unhealthy. It verifies the connection by checking the public IP and geolocation, and rotates through configured servers to maintain connectivity.

## Features

- Multiple US server support via YAML config
- Automatic failover on connection errors or health check failures
- Command-line interface with logs to both console and rotating file
- Uses OpenVPN through subprocess (no paid dependencies)
- Health checks using public IP and geolocation (expects US by default)
- Configurable connection timeout and health check interval

## Requirements

- Python 3.8+
- OpenVPN installed and available in `$PATH` or provided as an absolute path
- On Linux, OpenVPN typically needs root privileges to create TUN/TAP devices. Use `sudo` or configure capabilities.

Install Python dependencies:

```bash
pip install -r /workspace/requirements.txt
```

## Configuration

Edit `/workspace/servers/servers.yml` and provide your OpenVPN `.ovpn` files and optional credentials file. Example:

```yaml
servers:
  - name: "US-East-1 (Sample)"
    ovpn_config_path: "/absolute/path/to/us-east-1.ovpn"
    auth_user_pass_path: "/absolute/path/to/credentials.txt"  # two lines: username, password
    extra_args: ["--auth-nocache"]
    use_sudo: true
    openvpn_path: "openvpn"  # or "/usr/sbin/openvpn"
  - name: "US-West-1 (Sample)"
    ovpn_config_path: "/absolute/path/to/us-west-1.ovpn"
    auth_user_pass_path: null
    extra_args: []
    use_sudo: true
    openvpn_path: "openvpn"
```

Notes:
- If your `.ovpn` embeds credentials or uses certificates, set `auth_user_pass_path: null`.
- If your environment permits running OpenVPN without `sudo`, set `use_sudo: false`.
- To avoid sudo password prompts, you may either run the CLI under `sudo` or configure a NOPASSWD rule for the OpenVPN binary.

A sample `credentials.txt` looks like:

```
my_username
my_password
```

## Usage

Run the client:

```bash
python -m vpn_client.cli --config /workspace/servers/servers.yml \
  --connect-timeout 90 \
  --health-interval 60 \
  --expected-country US \
  --log-level INFO
```

Flags:
- `--connect-timeout`: seconds to wait for OpenVPN to come up before failing over
- `--health-interval`: seconds between health checks
- `--health-timeout`: per-HTTP request timeout for health checks
- `--expected-country`: expected geolocation ISO code (default: US)
- `--no-country-enforce`: only check internet reachability, not country match
- `--start-index`: zero-based server index to start from
- `--log-level`: DEBUG, INFO, WARNING, or ERROR

## How it works

1. Loads servers from YAML
2. Starts OpenVPN in the foreground to capture logs
3. Waits for "Initialization Sequence Completed"
4. Verifies the connection by fetching the public IP and country (must be US by default)
5. Periodically re-checks health; on failure or process exit, disconnects and tries the next server

## Legal and Terms

Use in accordance with local laws and your VPN provider's terms of service. This software provides automation around OpenVPN and does not include any VPN service or credentials.

## Troubleshooting

- Ensure your `.ovpn` works manually: `openvpn --config /path/to/my.ovpn`
- If you see `sudo: a password is required`, run the CLI with `sudo` or adjust your sudoers file.
- Check logs in `/workspace/logs/vpn_client.log` for details.
- Some geolocation APIs may rate-limit; the client tries multiple providers.

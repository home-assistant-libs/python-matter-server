"""Utils for Matter server."""

import asyncio
import base64
import platform
import socket

PLATFORM_MAC = platform.system() == "Darwin"


def convert_mac_address(hex_mac: str | bytes) -> str:
    """Convert hexadecimal MAC received from the sdk to a regular mac-address string."""
    if isinstance(hex_mac, str):
        # note that the bytes string can be optionally base64 encoded
        hex_mac = base64.b64decode(hex_mac)

    return ":".join("{:02x}".format(byte) for byte in hex_mac)  # pylint: disable=C0209


def convert_ip_address(hex_ip: str | bytes, ipv6: bool = False) -> str:
    """Convert hexadecimal IP received from the sdk to a regular IP string."""
    if isinstance(hex_ip, str):
        # note that the bytes string can be optionally base64 encoded
        hex_ip = base64.b64decode(hex_ip)
    if ipv6:
        hex_str = "".join(f"{byte:02x}" for byte in hex_ip)
        return ":".join(hex_str[i : i + 4] for i in range(0, len(hex_str), 4))
    return socket.inet_ntoa(hex_ip)


async def ping_ip(ip_address: str, timeout: int = 2) -> bool:
    """Ping given (IPv4 or IPv6) IP-address."""
    is_ipv6 = ":" in ip_address
    if is_ipv6 and PLATFORM_MAC:
        # macos does not have support for -W (timeout) on ping6 ?!
        cmd = f"ping6 -c 1 {ip_address}"
    elif is_ipv6:
        cmd = f"ping6 -c 1 -W {timeout} {ip_address}"
    else:
        cmd = f"ping -c 1 -W {timeout} {ip_address}"
    return (await check_output(cmd))[0] == 0


async def check_output(shell_cmd: str) -> tuple[int | None, bytes]:
    """Run shell subprocess and return output."""
    proc = await asyncio.create_subprocess_shell(
        shell_cmd,
        stderr=asyncio.subprocess.STDOUT,
        stdout=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return (proc.returncode, stdout)

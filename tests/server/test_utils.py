"""Test the util functions."""

from matter_server.server.helpers.utils import (
    convert_ip_address,
    convert_mac_address,
    ping_ip,
)


def test_convert_functions() -> None:
    """Test convert_ip_address and convert_mac_address util."""
    assert convert_ip_address("wKgBNA==") == "192.168.1.52"
    assert (
        convert_ip_address("KgARtxIxhABW70T//kmvxg==", True)
        == "2a00:11b7:1231:8400:56ef:44ff:fe49:afc6"
    )
    assert convert_mac_address("ji4yiD/r91c=") == "8e:2e:32:88:3f:eb:f7:57"

    b"\xfe\x80\x00\x00\x00\x00\x00\x00\x04P\x1dB]@\x8eE"


async def test_ping() -> None:
    """Test ping ip util."""
    # test valid ipv4
    assert await ping_ip("127.0.0.1") is True
    # test invalid ipv4
    assert await ping_ip("192.5.2.7") is False
    # test valid ipv6
    assert await ping_ip("::1") is True
    # test invalid ipv6
    assert await ping_ip("232::344::33") is False

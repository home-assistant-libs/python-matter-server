"""Test the util functions."""

from matter_server.common.helpers.util import convert_ip_address, convert_mac_address


def test_convert_functions() -> None:
    """Test convert_ip_address and convert_mac_address util."""
    assert convert_ip_address("wKgBNA==") == "192.168.1.52"
    assert (
        convert_ip_address("KgARtxIxhABW70T//kmvxg==", True)
        == "2a00:11b7:1231:8400:56ef:44ff:fe49:afc6"
    )
    assert convert_mac_address("ji4yiD/r91c=") == "8e:2e:32:88:3f:eb:f7:57"

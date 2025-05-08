"""Device controller tests."""

import pytest

from matter_server.server.device_controller import RE_MDNS_SERVICE_NAME


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        (
            "D22DC25523A78A89-0000000000000125._matter._tcp.local.",
            ("D22DC25523A78A89", "0000000000000125"),
        ),
        (
            "d22dc25523a78a89-0000000000000125._matter._tcp.local.",
            ("d22dc25523a78a89", "0000000000000125"),
        ),
    ],
)
def test_valid_mdns_service_names(name, expected):
    """Test valid mDNS service names."""
    match = RE_MDNS_SERVICE_NAME.match(name)
    assert match is not None
    assert match.groups() == expected


@pytest.mark.parametrize(
    "name",
    [
        "D22DC25523A78A89-0000000000000125 (2)._matter._tcp.local.",
        "D22DC25523A78A89-0000000000000125.._matter._tcp.local.",
        "G22DC25523A78A89-0000000000000125._matter._tcp.local.",  # invalid hex
        "D22DC25523A78A89-0000000000000125._matterc._udp.local.",
    ],
)
def test_invalid_mdns_service_names(name):
    """Test invalid mDNS service names."""
    assert RE_MDNS_SERVICE_NAME.match(name) is None

"""Test the server."""
from __future__ import annotations

from collections.abc import AsyncGenerator, Generator
from unittest.mock import MagicMock, patch

import pytest
from chip.clusters import ClusterCommand

from matter_server.server.server import MatterServer
from matter_server.common.models.api_command import APICommand
from matter_server.common.helpers.api import parse_arguments

pytestmark = pytest.mark.usefixtures(
    "application",
    "app_runner",
    "tcp_site",
    "chip_native",
    "chip_logging",
    "chip_stack",
    "certificate_authority_manager",
    "storage_controller",
)


@pytest.fixture(name="application")
def application_fixture() -> Generator[MagicMock, None, None]:
    """Return a mocked application."""
    with patch("matter_server.server.server.web.Application", autospec=True) as app:
        yield app


@pytest.fixture(name="app_runner")
def app_runner_fixture() -> Generator[MagicMock, None, None]:
    """Return a mocked app runner."""
    with patch(
        "matter_server.server.server.web.AppRunner", autospec=True
    ) as app_runner:
        yield app_runner


@pytest.fixture(name="tcp_site")
def tcp_site_fixture() -> Generator[MagicMock, None, None]:
    """Return a mocked tcp site."""
    with patch("matter_server.server.server.web.TCPSite", autospec=True) as tcp_site:
        yield tcp_site


@pytest.fixture(name="chip_native")
def chip_native_fixture() -> Generator[MagicMock, None, None]:
    """Return a mocked chip native."""
    with patch("matter_server.server.stack.chip.native", autospec=True) as chip_native:
        yield chip_native


@pytest.fixture(name="chip_logging")
def chip_logging_fixture() -> Generator[MagicMock, None, None]:
    """Return a mocked chip logging."""
    with patch(
        "matter_server.server.stack.chip.logging", autospec=True
    ) as chip_logging:
        yield chip_logging


@pytest.fixture(name="chip_stack")
def chip_stack_fixture() -> Generator[MagicMock, None, None]:
    """Return a mocked chip stack."""
    with patch("matter_server.server.stack.ChipStack", autospec=True) as chip_stack:
        yield chip_stack


@pytest.fixture(name="certificate_authority_manager")
def certificate_authority_manager_fixture() -> Generator[MagicMock, None, None]:
    """Return a mocked certificate authority manager."""
    with patch(
        "matter_server.server.stack.chip.CertificateAuthority.CertificateAuthorityManager",
        autospec=True,
    ) as certificate_authority_manager:
        yield certificate_authority_manager


@pytest.fixture(name="storage_controller")
def storage_controller_fixture() -> Generator[MagicMock, None, None]:
    """Return a mocked storage controller."""
    with patch(
        "matter_server.server.server.StorageController", autospec=True
    ) as storage_controller:
        yield storage_controller


@pytest.fixture(name="server")
async def server_fixture() -> AsyncGenerator[MatterServer, None]:
    """Yield a server."""
    server = MatterServer("test_storage_path", 1234, 5678, 5580)
    await server.start()
    yield server
    await server.stop()


async def test_server_start(
    application: MagicMock,
    app_runner: MagicMock,
    tcp_site: MagicMock,
    server: MatterServer,
    storage_controller: MagicMock,
) -> None:
    """Test server start."""
    assert application.call_count == 1
    application_instance = application.return_value
    add_route = application_instance.router.add_route
    assert add_route.call_count == 2
    assert add_route.call_args_list[0][0][0] == "GET"
    assert add_route.call_args_list[0][0][1] == "/ws"
    assert add_route.call_args_list[1][0][0] == "GET"
    assert add_route.call_args_list[1][0][1] == "/"
    assert app_runner.call_count == 1
    assert app_runner.return_value.setup.call_count == 1
    assert tcp_site.call_count == 1
    assert tcp_site.return_value.start.call_count == 1
    assert storage_controller.return_value.start.call_count == 1
    assert server.storage_path == "test_storage_path"
    assert server.vendor_id == 1234
    assert server.fabric_id == 5678
    assert server.port == 5580
    assert APICommand.SERVER_INFO in server.command_handlers
    assert APICommand.SERVER_DIAGNOSTICS in server.command_handlers
    assert APICommand.GET_NODES in server.command_handlers
    assert APICommand.GET_NODE in server.command_handlers
    assert APICommand.COMMISSION_WITH_CODE in server.command_handlers
    assert APICommand.COMMISSION_ON_NETWORK in server.command_handlers
    assert APICommand.SET_WIFI_CREDENTIALS in server.command_handlers
    assert APICommand.SET_THREAD_DATASET in server.command_handlers
    assert APICommand.OPEN_COMMISSIONING_WINDOW in server.command_handlers
    assert APICommand.DISCOVER in server.command_handlers
    assert APICommand.INTERVIEW_NODE in server.command_handlers
    assert APICommand.DEVICE_COMMAND in server.command_handlers
    assert APICommand.REMOVE_NODE in server.command_handlers

    # Check command handler signatures
    mock_cluster_command = ClusterCommand()

    assert not (
        parse_arguments(
            server.command_handlers[APICommand.SERVER_INFO].signature,
            None,
            strict=True,
        )
    )
    assert not (
        parse_arguments(
            server.command_handlers[APICommand.SERVER_DIAGNOSTICS].signature,
            None,
            strict=True,
        )
    )
    assert not (
        parse_arguments(
            server.command_handlers[APICommand.GET_NODES].signature,
            None,
            strict=True,
        )
    )
    assert (
        parse_arguments(
            server.command_handlers[APICommand.GET_NODE].signature,
            {"node_id": 1},
            strict=True,
        )
    ) == {"node_id": 1}
    assert (
        parse_arguments(
            server.command_handlers[APICommand.COMMISSION_WITH_CODE].signature,
            {"code": "test_code"},
            strict=True,
        )
    ) == {"code": "test_code"}
    assert (
        parse_arguments(
            server.command_handlers[APICommand.COMMISSION_ON_NETWORK].signature,
            {"setup_pin_code": 1234},
            strict=True,
        )
    ) == {"setup_pin_code": 1234, "filter_type": 0, "filter": None}
    assert (
        parse_arguments(
            server.command_handlers[APICommand.SET_WIFI_CREDENTIALS].signature,
            {"ssid": "test_ssid", "credentials": "test_credentials"},
            strict=True,
        )
    ) == {"ssid": "test_ssid", "credentials": "test_credentials"}
    assert (
        parse_arguments(
            server.command_handlers[APICommand.SET_THREAD_DATASET].signature,
            {"dataset": "test_dataset"},
            strict=True,
        )
    ) == {"dataset": "test_dataset"}
    assert (
        parse_arguments(
            server.command_handlers[APICommand.OPEN_COMMISSIONING_WINDOW].signature,
            {"node_id": 1},
            strict=True,
        )
    ) == {
        "node_id": 1,
        "timeout": 300,
        "iteration": 1000,
        "option": 0,
        "discriminator": None,
    }
    assert not (
        parse_arguments(
            server.command_handlers[APICommand.DISCOVER].signature,
            None,
            strict=True,
        )
    )
    assert (
        parse_arguments(
            server.command_handlers[APICommand.INTERVIEW_NODE].signature,
            {"node_id": 1},
            strict=True,
        )
    ) == {"node_id": 1}
    assert (
        parse_arguments(
            server.command_handlers[APICommand.DEVICE_COMMAND].signature,
            {"node_id": 1, "endpoint": 2, "payload": mock_cluster_command},
            strict=True,
        )
    ) == {"node_id": 1, "endpoint": 2, "payload": mock_cluster_command}
    assert (
        parse_arguments(
            server.command_handlers[APICommand.REMOVE_NODE].signature,
            {"node_id": 1},
            strict=True,
        )
    ) == {"node_id": 1}

    # Check parsing arguments with invalid arguments

    with pytest.raises(KeyError):
        parse_arguments(
            server.command_handlers[APICommand.REMOVE_NODE].signature,
            {"node_id": 1, "invalid": 2},
            strict=True,
        )

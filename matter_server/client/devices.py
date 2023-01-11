"""Matter Client implementation."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Final, Optional, cast

from ..common.helpers.util import dataclass_from_dict, dataclass_to_dict
from ..common.models.api_command import APICommand
from ..common.models.node import MatterNode

if TYPE_CHECKING:
    from chip.clusters.Objects import ClusterCommand

    from .matter import MatterClient

SUB_WILDCARD: Final = "*"

LOGGER = logging.getLogger(__package__)


class MatterClientDeviceController:
    """Interact with Matter devices on the Matter Server."""

    def __init__(self, matter: MatterClient) -> None:
        """Initialize the Matter Client DeviceController."""
        self.matter = matter
        self.nodes: Dict[int, MatterNode] = {}

    def get_node(self, node_id: int) -> MatterNode:
        """Return Matter node by id."""
        return self.nodes[node_id]

    async def commission_with_code(self, code: str) -> MatterNode:
        """
        Commission a device using QRCode or ManualPairingCode.

        Returns full NodeInfo once complete.
        """
        data = await self.matter.send_command(
            APICommand.COMMISSION_WITH_CODE, code=code
        )
        return dataclass_from_dict(MatterNode, data)

    async def commission_on_network(self, setup_pin_code: int) -> MatterNode:
        """
        Commission a device already connected to the network.

        Returns full NodeInfo once complete.
        """
        data = await self.matter.send_command(
            APICommand.COMMISSION_ON_NETWORK, setup_pin_code=setup_pin_code
        )
        return dataclass_from_dict(MatterNode, data)

    async def set_wifi_credentials(self, ssid: str, credentials: str) -> None:
        """Set WiFi credentials for commissioning to a (new) device."""
        await self.matter.send_command(
            APICommand.SET_WIFI_CREDENTIALS, ssid=ssid, credentials=credentials
        )

    async def set_thread_operational_dataset(self, dataset: str) -> None:
        """Set Thread Operational dataset for commissioning to a (new) device."""
        await self.matter.send_command(APICommand.SET_THREAD_DATASET, dataset=dataset)

    async def open_commissioning_window(
        self,
        node_id: int,
        timeout: int = 300,
        iteration: int = 1000,
        option: int = 0,
        discriminator: Optional[int] = None,
    ) -> int:
        """
        Open a commissioning window to commission a device present on this controller to another.

        Returns code to use as discriminator.
        """
        return cast(
            int,
            await self.matter.send_command(
                APICommand.OPEN_COMMISSIONING_WINDOW,
                node_id=node_id,
                timeout=timeout,
                iteration=iteration,
                option=option,
                discriminator=discriminator,
            ),
        )

    async def send_device_command(
        self, node_id: int, endpoint: int, command: ClusterCommand
    ) -> Any:
        """Send a command to a Matter node/device."""
        payload = dataclass_to_dict(command)
        return await self.matter.send_command(
            APICommand.DEVICE_COMMAND,
            node_id=node_id,
            endpoint=endpoint,
            payload=payload,
        )

    async def remove_node(self, node_id: int) -> None:
        """Remove a Matter node/device from the fabric."""
        await self.matter.send_command(APICommand.REMOVE_NODE, node_id=node_id)

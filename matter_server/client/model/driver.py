from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import client

from matter_server.vendor.chip.clusters import Objects as Clusters

from .device_controller import DeviceController


class Driver:
    def __init__(self, client: client.Client, initial_state: dict):
        self._client = client
        self.state = initial_state
        self.device_controller = DeviceController(client)

    def receive_event(self, event):
        print("Received event", event)

    async def send_toggle(self):
        await self._client.async_send_matter_command(
            nodeid=4335, endpoint=1, payload=Clusters.OnOff.Commands.Toggle()
        )

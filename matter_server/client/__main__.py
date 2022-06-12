import asyncio
import logging
import os
import sys

import aiohttp

from matter_server.client.client import Client
from matter_server.vendor.chip.clusters import Objects as clusters

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
DEFAULT_PORT = "5580" if len(sys.argv) < 3 else sys.argv[2]
HOST = os.getenv("CHIP_WS_SERVER_HOST", DEFAULT_HOST)
PORT = int(os.getenv("CHIP_WS_SERVER_PORT", DEFAULT_PORT))
URL = f"http://{HOST}:{PORT}/chip_ws"


async def main():
    async with aiohttp.ClientSession() as session:
        await connect(session)


async def connect(session):
    client = Client(URL, session)
    await client.connect()
    is_initialized = asyncio.Event()

    toggle_task = asyncio.create_task(toggle_happiness(client, is_initialized))

    try:
        await client.listen(is_initialized)
    finally:
        toggle_task.cancel()
        await toggle_task


async def toggle_happiness(client: Client, is_initialized: asyncio.Event):
    try:
        await is_initialized.wait()

        nodeid = 4335

        await client.driver.device_controller.resolve_node(nodeid)

        reportingTimingParams = (0, 10)
        subscription = await client.driver.device_controller.read(
            nodeid, attributes=[clusters.OnOff], reportInterval=reportingTimingParams
        )

        def subscription_event(data):
            _LOGGER.info("Received subscription event %s", data)

        subscription.handler = subscription_event

        # This (now) throws exceptions if it fails
        # await client.driver.device_controller.ResolveNode(nodeid)

        # node = await client.driver.device_controller.Read(
        #     nodeid, attributes=[clusters.OnOff], events="*", returnClusterObject=True
        # )
        # await asyncio.sleep(1)

        # node = await client.driver.device_controller.Read(
        #     nodeid, attributes="*", events="*", returnClusterObject=True
        # )

        # from pprint import pprint

        # pprint(node)

        while True:
            await asyncio.sleep(5)
            await client.driver.device_controller.send_command(
                nodeid=nodeid, endpoint=1, payload=clusters.OnOff.Commands.Toggle()
            )
    except Exception:
        _LOGGER.exception("No more Happiness")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

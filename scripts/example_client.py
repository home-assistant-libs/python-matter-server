"""Example script to test the Matter client."""

import argparse
import asyncio
import logging
import os
from os.path import abspath, dirname
from pathlib import Path
from sys import path
from typing import Any

import aiohttp
from aiorun import run
import coloredlogs


path.insert(1, dirname(dirname(abspath(__file__))))
from matter_server.client.matter import MatterClient  # noqa: E402
from matter_server.common.models.events import EventType

logging.basicConfig(level=logging.DEBUG)


from example_server import DEFAULT_PORT

DEFAULT_URL = f"http://127.0.0.1:{DEFAULT_PORT}/ws"

_LOGGER = logging.getLogger(__name__)

# Get parsed passed in arguments.
parser = argparse.ArgumentParser(description="Matter Client Example.")
parser.add_argument(
    "--url",
    type=str,
    default=DEFAULT_URL,
    help=f"URL to the Matter Server Websocket API, defaults to {DEFAULT_URL}",
)
parser.add_argument(
    "--log-level",
    type=str,
    default="info",
    help="Provide logging level. Example --log-level debug, default=info, possible=(critical, error, warning, info, debug)",
)

args = parser.parse_args()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    # configure logging
    logging.basicConfig(level=args.log_level.upper())
    coloredlogs.install(level=args.log_level.upper())

    shutdown_called = asyncio.Event()

    async def run_matter():
        """Run the Matter client."""

        def on_event(evt: EventType, data: Any = None):
            _LOGGER.info("Got event %s with data: %s", evt.value, data)

        async with aiohttp.ClientSession() as session:
            async with MatterClient(args.url, session) as client:
                client.subscribe(on_event)
                # just wait forever until stopped
                await shutdown_called.wait()

        # run the client
        await client.start()
        # just wait forever
        await shutdown_called.wait()

    async def handle_stop(loop: asyncio.AbstractEventLoop):
        """Handle stop."""
        shutdown_called.set()

    # run the client
    run(run_matter(), loop=loop, shutdown_callback=handle_stop)

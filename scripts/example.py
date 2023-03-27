"""Example script to test the Matter server and client."""

import argparse
import asyncio
import logging
import os
from pathlib import Path

import aiohttp
import coloredlogs
from aiorun import run

from matter_server.client.client import MatterClient
from matter_server.server.server import MatterServer

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

DEFAULT_VENDOR_ID = 0xFFF1
DEFAULT_FABRIC_ID = 1
DEFAULT_PORT = 5580
DEFAULT_URL = f"http://127.0.0.1:{DEFAULT_PORT}/ws"
DEFAULT_STORAGE_PATH = os.path.join(Path.home(), ".matter_server")


# Get parsed passed in arguments.
parser = argparse.ArgumentParser(description="Matter Server Example.")
parser.add_argument(
    "--storage-path",
    type=str,
    default=DEFAULT_STORAGE_PATH,
    help=f"Storage path to keep persistent data, defaults to {DEFAULT_STORAGE_PATH}",
)
parser.add_argument(
    "--port",
    type=int,
    default=DEFAULT_PORT,
    help=f"TCP Port on which to run the Matter WebSockets Server, defaults to {DEFAULT_PORT}",
)
parser.add_argument(
    "--log-level",
    type=str,
    default="info",
    help="Provide logging level. Example --log-level debug, default=info, "
    "possible=(critical, error, warning, info, debug)",
)

args = parser.parse_args()


if __name__ == "__main__":
    # configure logging
    logging.basicConfig(level=args.log_level.upper())
    coloredlogs.install(level=args.log_level.upper())

    # make sure storage path exists
    if not os.path.isdir(args.storage_path):
        os.mkdir(args.storage_path)

    # Init server
    server = MatterServer(args.storage_path, DEFAULT_VENDOR_ID, DEFAULT_FABRIC_ID, int(args.port))

    async def run_matter():
        """Run the Matter server and client."""
        # start Matter Server
        await server.start()

        # run the client
        url = f"http://127.0.0.1:{args.port}/ws"
        async with aiohttp.ClientSession() as session:
            async with MatterClient(url, session) as client:
                # start listening
                await client.start_listening()

    async def handle_stop(_loop: asyncio.AbstractEventLoop):
        """Handle server stop."""
        await server.stop()

    # run the server
    run(run_matter(), shutdown_callback=handle_stop)

import argparse
import asyncio
import logging
import os
from pathlib import Path
import sys

from aiorun import run
import coloredlogs

from .server import MatterServer

DEFAULT_VENDOR_ID = 0xFFF1
DEFAULT_FABRIC_ID = 1
DEFAULT_PORT = 5580
DEFAULT_STORAGE_PATH = os.path.join(Path.home(), ".matter_server")

# Get parsed passed in arguments.
parser = argparse.ArgumentParser(
    description="Matter Controller Server using WebSockets."
)


parser.add_argument(
    "--vendorid",
    default=DEFAULT_VENDOR_ID,
    help=f"Vendor ID for the Fabric, defaults to {DEFAULT_VENDOR_ID}",
)
parser.add_argument(
    "--fabricid",
    default=DEFAULT_VENDOR_ID,
    help=f"Fabric ID for the Fabric, defaults to {DEFAULT_FABRIC_ID}",
)
parser.add_argument(
    "--storage-path",
    default=DEFAULT_STORAGE_PATH,
    help=f"Storage path to keep persistent data, defaults to {DEFAULT_STORAGE_PATH}",
)
parser.add_argument(
    "--port",
    default=DEFAULT_PORT,
    help="TCP Port to run the websocket server, defaults to 5580",
)
parser.add_argument(
    "--log-level",
    default="info",
    help="Provide logging level. Example --log-level debug, default=info, possible=(critical, error, warning, info, debug)",
)
parser.add_argument(
    "--log-file",
    type=str,
    default=None,
    help="Log file to write to (optional).",
)

args = parser.parse_args()


if __name__ == "__main__":

    # configure logging
    handlers = None
    if args.log_file:
        handlers = [logging.FileHandler(args.log_file)]
    logging.basicConfig(handlers=handlers, level=args.log_level.upper())
    coloredlogs.install(level=args.log_level.upper())

    # make sure storage path exists
    if not os.path.isdir(args.storage_path):
        os.mkdir(args.storage_path)

    # Init server
    server = MatterServer(
        args.storage_path, int(args.vendorid), int(args.fabricid), int(args.port)
    )

    async def handle_stop(loop: asyncio.AbstractEventLoop):
        await server.stop()

    # run the server
    run(server.start(), shutdown_callback=handle_stop)

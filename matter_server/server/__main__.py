import argparse
import asyncio
import logging
import os
from pathlib import Path
import sys

from aiorun import run
import coloredlogs

from .server import MatterServer

_LOGGER = logging.getLogger(__package__)


# Get parsed passed in arguments.
parser = argparse.ArgumentParser(
    description="Matter Controller Server using WebSockets."
)
parser.add_argument(
    "--log-file",
    type=str,
    default=None,
    help="Log file to write to.  If not set, matter_server.log is used",
)
parser.add_argument(
    "--log-level",
    default="info",
    help="Provide logging level. Example --log-level debug, default=info, possible=(critical, error, warning, info, debug)",
)

args = parser.parse_args()
debug = os.getenv("CHIP_WS_DEBUG") is not None


if __name__ == "__main__":

    handlers = None

    if args.log_file:
        handlers = [logging.FileHandler(args.log_file)]

    logging.basicConfig(handlers=handlers, level=args.log_level.upper())

    host = os.getenv("CHIP_WS_SERVER_HOST", "::,0.0.0.0").split(",")
    port = int(os.getenv("CHIP_WS_SERVER_PORT", "5580"))
    storage_path = os.getenv(
        "CHIP_WS_STORAGE",
        str(Path.home() / ".chip-storage/python-kv.json"),
    )

    coloredlogs.install(level=logging.DEBUG if debug else args.log_level.upper())

    server = MatterServer(storage_path, host, port)

    async def handle_stop(loop: asyncio.AbstractEventLoop):
        await server.stop()

    # run the server
    run(server.start(), shutdown_callback=handle_stop)

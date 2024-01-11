"""Script entry point to run the Matter Server."""
import argparse
import asyncio
import logging
import os
from pathlib import Path

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
    type=int,
    default=DEFAULT_VENDOR_ID,
    help=f"Vendor ID for the Fabric, defaults to {DEFAULT_VENDOR_ID}",
)
parser.add_argument(
    "--fabricid",
    type=int,
    default=DEFAULT_FABRIC_ID,
    help=f"Fabric ID for the Fabric, defaults to {DEFAULT_FABRIC_ID}",
)
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
    help=f"TCP Port to run the websocket server, defaults to {DEFAULT_PORT}",
)
parser.add_argument(
    "--log-level",
    type=str,
    default="info",
    # pylint: disable=line-too-long
    help="Provide logging level. Example --log-level debug, default=info, possible=(critical, error, warning, info, debug)",
)
parser.add_argument(
    "--log-file",
    type=str,
    default=None,
    help="Log file to write to (optional).",
)
parser.add_argument(
    "--primary-interface",
    type=str,
    default=None,
    help="Primary network interface for link-local addresses (optional).",
)

args = parser.parse_args()


def main() -> None:
    """Run main execution."""
    # configure logging
    handlers = None
    if args.log_file:
        handlers = [logging.FileHandler(args.log_file)]
    logging.basicConfig(handlers=handlers, level=args.log_level.upper())
    coloredlogs.install(level=args.log_level.upper())
    if not logging.getLogger().isEnabledFor(logging.DEBUG):
        logging.getLogger("chip").setLevel(logging.WARNING)
        logging.getLogger("PersistentStorage").setLevel(logging.WARNING)
        # Temporary disable the logger of chip.clusters.Attribute because it now logs
        # an error on every custom attribute that couldn't be parsed which confuses people.
        # We can restore the default log level again when we've patched the device controller
        # to handle the raw attribute data to deal with custom clusters.
        logging.getLogger("chip.clusters.Attribute").setLevel(logging.CRITICAL)

    # make sure storage path exists
    if not os.path.isdir(args.storage_path):
        os.mkdir(args.storage_path)

    # Init server
    server = MatterServer(
        args.storage_path,
        int(args.vendorid),
        int(args.fabricid),
        int(args.port),
        args.primary_interface,
    )

    async def handle_stop(loop: asyncio.AbstractEventLoop) -> None:
        # pylint: disable=unused-argument
        await server.stop()

    # run the server
    run(server.start(), shutdown_callback=handle_stop)


if __name__ == "__main__":
    main()

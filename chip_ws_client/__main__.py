import asyncio
import logging
import os
import sys
from dataclasses import dataclass
from tkinter.tix import TEXT

import aiohttp
from aiohttp.http import WSMsgType

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

HOST = os.getenv('CHIP_WS_SERVER_HOST', '127.0.0.1')
PORT = int(os.getenv('CHIP_WS_SERVER_PORT', 8080))

URL = f'http://{HOST}:{PORT}/chip_ws'


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(URL) as ws:
            _LOGGER.info("WebSocket connected")
            await ws.send_str("close")
            while True:
                
                msg = await ws.receive()
                if msg.type == WSMsgType.TEXT:
                    _LOGGER.debug("Received WS message %s", msg.data)
                elif msg.type == WSMsgType.CLOSED:
                    _LOGGER.info("Server closed WebSocket connection, existing...")
                    return
                    

if __name__ == '__main__':
    asyncio.run(main())

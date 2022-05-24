import logging
import os
import sys
from functools import partial

import aiohttp
import aiohttp.web

from chip_ws_server.server import CHIPControllerServer

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

HOST = os.getenv('CHIP_WS_SERVER_HOST', '0.0.0.0')
PORT = int(os.getenv('CHIP_WS_SERVER_PORT', 8080))

async def websocket_handler(request, server):
    _LOGGER.info("New connection...")
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    _LOGGER.info("Websocket connection ready")

    async for msg in ws:
        _LOGGER.debug(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            server.new_message(msg.data)
    _LOGGER.info("Websocket connection closed")
    return ws

def main() -> int:
    server = CHIPControllerServer()
    server.setup()
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/chip_ws', partial(websocket_handler, server=server))
    aiohttp.web.run_app(app, host=HOST, port=PORT)
    server.shutdown()

if __name__ == '__main__':
    sys.exit(main())

# Matter Dashboard

This is the dashboard for the Python Matter Server project. It is meant to be used for debugging and testing.

## Development

Install the dependencies:

```bash
script/setup
```

Run the development server:

```bash
script/develop
```

The dashboard will be available at [http://localhost:5010](http://localhost:5010). When you open it from localhost, it will ask you for your websocket server URL.

The websocket URL of the Home Assistant add-on will be something like `ws://homeassistant.local:5080`. If you are running the Python Matter Server locally, it will be `ws://localhost:5080`.

If you want to use the dashboard with the Python Matter Server Home Assistant add-on, you need to configure it to make the WebSocket server available on the network. Go to the [add-on info page](https://my.home-assistant.io/redirect/supervisor_addon/?addon=core_matter_server), click on Configuration. Under "Network", show disabled ports and enter the port you want to use for the WebSocket server (e.g. 5080). Then, click "save" and restart the add-on when prompted.

## Production build

The production build is generated when you run

```bash
script/build
```

The folder `dist/web` will contain the build that can be served by any web browser.

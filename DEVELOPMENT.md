# Setting up your development environment

**For enabling Matter support within Home Assistant, please refer to the Home Assistant documentation. These instructions are for development only!**

Development is only possible on a (recent) Linux or MacOS machine. Other operating systems are **not supported**. See [here](docs/os_requirements.md) for a full list of requirements to the OS and network, especially if you plan on communicating with Thread based devices.

- Download/clone the repo to your local machine.
- Set-up the development environment: `scripts/setup.sh`
- Create the `/data` directory if it does not exist with permissions for the user running the python-matter-server.

## Start Matter server

You can check out the [example script](/scripts/example.py) in the scripts folder for generic directions to run the client and server.

- To run the server in `info` log-level, you can run: `python -m matter_server.server`
- To start the server in `debug` log-level, you can run: `python -m matter_server.server --log-level debug`
- To start the server with SDK in `progress` log-level, you can run: `python -m matter_server.server --log-level-sdk progress`. This will display more information from the Matter SDK (C++) side of the Matter Server.

Use `--help` to get a list of possible log levels and other command line arguments.

The server runs a Matter Controller and includes all logic for storing node information, interviews and subscriptions. To interact with this controller we've created a small Websockets API with an RPC-like interface. The library contains a client as reference implementation which in turn is used by Home Assistant. Splitting the server from the client allows the scenario where multiple consumers can communicate to the same Matter fabric and the Matter fabric can keep running while the consumer (e.g. Home Assistant is down).

If you happen to get `OSError: [Errno 105] No buffer space available.`, increase the IPv4 group limits with:
```
echo "net.ipv4.igmp_max_memberships=1024" | sudo tee -a /etc/sysctl.d/local.conf
sudo service procps force-reload
```

## Python client library only

There is also a Python client library hosted in this repository (used by Home Assistant), which consumes the Websockets API published from the server.

The client library has a dependency on the chip/matter clusters package which contains all (Cluster) models and this package is os/platform independent. The server library depends on the Matter Core SDK (still named CHIP) which is architecture and OS specific. We build (and publish) wheels for Linux (amd64 and aarch64) to pypi but for other platforms (like Macos) you will need to build those wheels yourself using the exact same version of the SDK as we use for the clusters package. Take a look at our build script for directions: https://github.com/home-assistant-libs/chip-wheels/blob/main/.github/workflows/build.yaml

To only install the client part: `pip install python-matter-server`

## Websocket commands

[Websocket documentation](/docs/websockets_api.md)

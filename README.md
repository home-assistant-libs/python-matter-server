# Python Matter Server

This project implements a Matter Controller Server over WebSockets using the [official CHIP SDK](https://github.com/project-chip/connectedhomeip) as a base and provides both a server and client implementation.

The goal of this project is primary to have Matter support in Home Assistant but its universal approach makes it suitable to be used in other projects too.

This repository is for development only (so not for enduser support). For enabling Matter support within Home Assistant, please refer to the [Home Assistant documentation](https://www.home-assistant.io/integrations/matter/).

NOTE: Both Matter and this implementation are in early (v1) state and features are probably missing or could be improved. See our [development notes](#development) how you can help out, with development and/or testing.

## Trying it out

`For enabling Matter support within Home Assistant, please refer to the Home Assistant documentation. These instructions are for development/advanced scenarios only!`

To install the server (including client): `pip install python-matter-server[server]`
To only install the client part: `pip install python-matter-server`

The client library has a dependency on the chip clusters package which contains all (Cluster) models and this package is os/platform independent. The server library depends on the CHIP Core SDK which is architecture and OS specific. We build (and publish) wheels for Linux (amd64 and aarch64) to pypi but for other platforms (like Macos) you will need to build those wheels yourself using the exact same version of the SDK as we use for the clusters package. Take a look at our build script for directions: https://github.com/home-assistant-libs/chip-wheels/blob/main/.github/workflows/build.yaml

Once you have the wheels installed, you can check out the example script in the scripts folder for generic directions to run the client and server. To just run the server, you can run:

```
python -m matter_server.server

Optional arguments:
  -h, --help            show help message and exit
  --vendorid VENDORID   Vendor ID for the Fabric, defaults to 65521
  --fabricid FABRICID   Fabric ID for the Fabric, defaults to 1
  --storage-path STORAGE_PATH
                        Storage path to keep persistent data, defaults to $HOME/.matter_server
  --port PORT           TCP Port to run the websocket server, defaults to 5580
  --log-level LOG_LEVEL
                        Provide logging level. Example --log-level debug, default=info, possible=(critical, error, warning, info, debug)
  --log-file LOG_FILE   Log file to write to (optional).

```

The server runs a Matter Controller and includes all logic for storing node information, interviews and subscriptions. To interact with this controller we've created a small Websockets API with an RPC-like interface. The library contains a client as reference implementation which in turn is used by Home Assistant. Splitting the server from the client allows the scenario where multiple consumers can communicate to the same Matter fabric and the Matter fabric can keep running while the consumer (e.g. Home Assistant is down).

### Test devices

Now that the Matter Specification is offically released in its 1.0 version, devices will be available in stores from 2023 that actually have Matter support or least manufacturers run a beta program which you can join to run Matter firmware on your device. Please refer to the documentation of your device if its already Matter enabled out of the box or you need to enable some special firmware(mode).

Besides that it is possible to run Matter firmware on common microcontrollers such as the ESP32 and there is even a whole device emulator available which runs on a regular desktop OS. To make things easier we've prepared a [special page](https://nabucasa.github.io/matter-example-apps) where you can quickly try out running the Matter example apps on ESP32.

### Websocket commands

(for a complete oversight see the client implementation)

**Set WiFi credentials**
Inform the controller about the WiFi credentials it needs to send when commissioning a new device.

```
  {
    "message_id": "1",
    "command": "set_wifi_credentials",
    "args": {
      "ssid": "blah",
      "credentials": "bah"
    }
  }
```

**Set Thread dataset**
Inform the controller about the Thread credentials it needs to use when commissioning a new device.

```
  {
    "message_id": "1",
    "command": "set_thread_dataset",
    "args": {
      "dataset": "blah"
    }
  }
```

**Commission with code**
Commission a new device. For WiFi or Thread based devices, the credentials need to be set upfront, otherwise commisisoning will fail.
The controller will use bluetooth for the commissioning of wireless devices. If the machine running the Python Matter Server controller lacks bluetooth support, comissioning will only work for devices already connected to the network (by cable or another controller).

```
  {
    "message_id": "2",
    "command": "commission_with_code",
    "args": {
      "code": "MT:Y.ABCDEFG123456789"
    }
  }
```

**Commission on Network**
Commission a device already connected to the network.

```
  {
    "message_id": "2",
    "command": "commission_on_network",
    "args": {
      "setup_pin_code": 1234567
    }
  }
```

**Open Commissioning window**
Open a commissioning window to commission a device present on this controller to another.
Returns code to use as discriminator.

```
  {
    "message_id": "2",
    "command": "open_commissioning_window",
    "args": {
      "node_id": 1
    }
  }
```

**Get Nodes**
Get all nodes already commissioned on the controller.

```
  {
    "message_id": "2",
    "command": "get_nodes"
  }
```

**Get Node**
Get info of a single Node.

```
  {
    "message_id": "2",
    "command": "get_nodes",
    "args": {
      "node_id": 1
    }
  }
```

**Start listening**
When the start_listening command is issued, the server will dump all existing nodes. From that moment on all events (including node attribute changes) will be forwarded.

```
  {
    "message_id": "3",
    "command": "start_listening"
  }
```

## Development

Want to help out with development, testing and/or documentation ? Great! As both this project and Matter keeps evolving and devices will hit the market with actual Matter support, there will be a lot to improve. See our [project board](https://github.com/orgs/home-assistant-libs/projects/1) for status updates and maybe something you'd like to help out with development and/or testing.

### Setting up your development environment

Please note that development is only possible on Linux and MacOS, no Windows support.

- Download/clone the repo to your local machine.
- Create a Python virtual environment.
- Install the correct SDK wheels for both the cluster and core package, see instructions above if there is no wheel for your setup prebuilt.

# Python Matter Server

This project implements a Matter (formerly Home Assistant Connected Home over IP
or CHIP) Controller Server using WebSockets.

:warning: This is under development and in very early stage!

## Usage

To use the Matter Server using the Supervisor add-on is the recommended path
(tbd).

## Development

The Home Assistant Matter Server uses the Python CHIP Controller part of the
open source [Matter/Project CHIP repository][project-chip].
The project offers a IPython based REPL for testing/exploring. The REPL is also
available as [Python CHIP Controller REPL Add-on][chip-controller-repl-add-on].

### Run from the source tree

The Server needs to be run in a Python environment where the Python CHIP
Controller is installed. E.g.

```
source ../connectedhomeip/out/python_env/bin/activate
```

Also make sure that the default storage location is present:
```
mkdir $HOME/.chip-storage/
```

With the following command the server can be run directly from the source tree.

```
python3 -m matter_server.server
```

_On MacOs you will have to run above command with 'sudo' as it requires to interact with BLE._

The client does not need to be run in the Python CHIP Controller environment. It
can be run from the source tree using:

```
python3 -m matter_server.client
```

### Build and install

To build the Python CHIP Controller follow the building instructions available
at [docs/guides/python_chip_controller_building.md][python-chip-building].
Once you have a working Python CHIP Controller Python environment, switch
to this repository and install this project as follows:

```shell
pip install .
```

### Creating a test device

Instruction on how to create a test device can be found [here](https://nabucasa.github.io/matter-example-apps/).

### Installing custom component in Home Assistant

Inside your Home Assistant development environment.

```
pip3 install -e ../python-matter-server
cd config
mkdir custom_components
cd custom_components
ln -sf ../../../python-matter-server/custom_components/matter_experimental .
```

You can now add the custom component via the UI. It's called Matter (experimental):

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=matter_experimental)

### Commissioning a test device

You can use Home Assistant services to commission a test device.

[![Open your Home Assistant instance and show your service developer tools.](https://my.home-assistant.io/badges/developer_services.svg)](https://my.home-assistant.io/redirect/developer_services/)

Each time the server restarts you will need to provide it your Wi-Fi credentials via the `matter_experimental.set_wifi` service to be able to onboard Wi-Fi devices.

Once done, you can onboard devices by sending the content of a QR code to the `matter_experimental.commission` service.

### Using the Python CHIP REPL

Matter provides their own REPL that allows you to directly interact with the device controller. It's possible to start this and have it use the same storage as the server:

```
chip-repl --storagepath=$HOME/.chip-storage/python-kv.json
```

_On MacOs you will have to run above command with 'sudo' as it requires to interact with BLE._

[project-chip]: https://github.com/project-chip/connectedhomeip
[chip-controller-repl-add-on]: https://github.com/home-assistant/addons-development/tree/master/chip_controller_repl
[python-chip-building]: https://github.com/project-chip/connectedhomeip/blob/master/docs/guides/python_chip_controller_building.md

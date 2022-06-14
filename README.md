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

### Prepare venv for the Matter Server

This Python Matter Server needs the CHIP Controller Python libraries. The CHIP
Controller Python libraries come with the complete Matter SDK (CHIP stack)
as a native C++ library. The CHIP Controller Python is not available on pip,
and, because it comes with a native C++ library, is a platform dependent
library. The Matter SDK allows to build a Python wheel for your platform.

To build the Python CHIP Controller follow the building instructions available
at [docs/guides/python_chip_controller_building.md][python-chip-building].

Note the essential command is `scripts/build_python.sh -m platform -i separate`.
It builds the library in `out/python_lib/`, and creates a venv for you in
`out/python_env/`. If you update the Matter SDK git repository, make sure to
run this command again to rebuild the library.

If you already compiled the CHIP Controller Python libraries previously, you
can activate the Python virtual environment using:


```
source ../connectedhomeip/out/python_env/bin/activate
```

Note: There is a bug with Apple M1 based systems: Pigweed currently uses Python
x86-64 via Rosetta. That causes problems when trying to build the Python
CHIP Controller. There are work arounds documented in [GitHub issue #19134](https://github.com/project-chip/connectedhomeip/issues/19134).
Make sure to not use `-i separate` and setup the venv separately as well.

### Run from the source tree

The Server needs to be run in a Python environment where the Python CHIP
Controller is installed. E.g.

Also make sure that the default storage location is present:
```
mkdir $HOME/.chip-storage/
```

With the following command the server can be run directly from the source tree.

```
python3 -m matter_server.server
```

_On macOS you will have to run above command with 'sudo' as it requires to interact with BLE._

_On Linux, make sure Bluetooth (bluez) is active and enabled before starting onboarding._

The client does not need to be run in the Python CHIP Controller environment. It
can be run from the source tree using:

```
python3 -m matter_server.client
```

### Build and install

nce you have a working Python CHIP Controller Python environment, switch
to this repository and install this project as follows:

```shell
pip install .
```

### Creating a test device

Instruction on how to create a test device can be found [here][example-firmware-site].

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

Once done, you can onboard devices by sending the content of a QR code to the `matter_experimental.commission` service. Get the QR code from your test device via [the Matter REPL][example-firmware-site].

### Using the Python CHIP REPL

Matter provides their own REPL that allows you to directly interact with the device controller. It's possible to start this and have it use the same storage as the server:

```
chip-repl --storagepath=$HOME/.chip-storage/python-kv.json
```

_On MacOs you will have to run above command with 'sudo' as it requires to interact with BLE._

[project-chip]: https://github.com/project-chip/connectedhomeip
[chip-controller-repl-add-on]: https://github.com/home-assistant/addons-development/tree/master/chip_controller_repl
[python-chip-building]: https://github.com/project-chip/connectedhomeip/blob/master/docs/guides/python_chip_controller_building.md
[example-firmware-site]: https://nabucasa.github.io/matter-example-apps/

### Deploying a new version

1. Update Matter Server PyPI package [`pyproject.toml`](https://github.com/home-assistant-libs/python-matter-server/blob/main/pyproject.toml) with the new version.
1. Update custom integration [`manifest.json`](https://github.com/home-assistant-libs/python-matter-server/blob/main/custom_components/matter_experimental/manifest.json) with the new version for both `requirements` and `version`.
1. Tag a new release in this repository with the new version.

Updating the Matter Server add-on

1. Update the PyPI package version used by the Matter Server add-on by updating `MATTER_SERVER_VERSION` in the [`Dockerfile`](https://github.com/home-assistant/addons-development/blob/master/matter_server/Dockerfile)
1. Bump the add-on version in [`config.yaml`](https://github.com/home-assistant/addons-development/blob/master/matter_server/config.yaml)
1. Add a new entry for the new add-on version in the changelog [`CHANGELOG.md`](https://github.com/home-assistant/addons-development/blob/master/matter_server/CHANGELOG.md)

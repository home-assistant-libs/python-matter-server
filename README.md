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
python3 -m chip_ws_server.__main__
```

To test device communication or to commission devices the provided Python CHIP
REPL can be useful. Make sure to start the REPL with the same storage location
to share the network information.

```
chip-repl --storagepath=$HOME/.chip-storage/python-kv.json
```

Note: At least under Linux some values are still stored in `/tmp/chip_*.ini` files.
Currently there is no build option to adjust that. To use the same path manual
adjustments in `src/platform/Linux/CHIPLinuxStorage.h` are required.


The client does not need to be run in the Python CHIP Controller environment. It
can be run from the source tree using:

```
python3 -m chip_ws_server.__main__
```

### Build and install

To build the Python CHIP Controller follow the building instructions available
at [docs/guides/python_chip_controller_building.md][python-chip-building].
Once you have a working Python CHIP Controller Python environment, switch
to this repository and install this project as follows:

```shell
pip install .
```

[project-chip]: https://github.com/project-chip/connectedhomeip
[chip-controller-repl-add-on]: https://github.com/home-assistant/addons-development/tree/master/chip_controller_repl
[python-chip-building]: https://github.com/project-chip/connectedhomeip/blob/master/docs/guides/python_chip_controller_building.md

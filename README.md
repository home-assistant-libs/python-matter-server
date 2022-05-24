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

### Build

To build the Python CHIP Controller follow the building instructions available
at [docs/guides/python_chip_controller_building.md][python-chip-building].
Once you have a working Python CHIP Controller Python environment, switch
to this repository and install this project as follows:

```shell
pip install .
```

### Installation

[project-chip]: https://github.com/project-chip/connectedhomeip
[chip-controller-repl-add-on]: https://github.com/home-assistant/addons-development/tree/master/chip_controller_repl
[python-chip-building]: https://github.com/project-chip/connectedhomeip/blob/master/docs/guides/python_chip_controller_building.md

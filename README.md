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

### Commissioning a test device

Currently the easiest way to set up a test device is using the Python CHIP REPL. Start it by pointing it at the same storage location as the servier will run off:

```
chip-repl --storagepath=$HOME/.chip-storage/python-kv.json
```

_On MacOs you will have to run above command with 'sudo' as it requires to interact with BLE._

Inside the Python REPL, configure your Wi-Fi credentials:

```python
devCtrl.SetWiFiCredentials("SSID", "PW")
```

Once done, paste the following code to commission the device:

```python
from chip.setup_payload import SetupPayload
setupPayload = SetupPayload().ParseQrCode("MT:Y.K9042C00KA0648G00")
import ctypes
longDiscriminator = ctypes.c_uint16(int(setupPayload.attributes['Discriminator']))
pincode = ctypes.c_uint32(int(setupPayload.attributes['SetUpPINCode']))

devCtrl.ConnectBLE(longDiscriminator, pincode, 4335)
```

If you have installed the lighting app, send the following command to test if it works:

```python
await devCtrl.SendCommand(4335, 1, Clusters.OnOff.Commands.Toggle())
```

[project-chip]: https://github.com/project-chip/connectedhomeip
[chip-controller-repl-add-on]: https://github.com/home-assistant/addons-development/tree/master/chip_controller_repl
[python-chip-building]: https://github.com/project-chip/connectedhomeip/blob/master/docs/guides/python_chip_controller_building.md

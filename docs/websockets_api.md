# Websocket documentation

This list is not intended to be complete, for a complete oversight see the client implementation.

## Websocket commands

Here are the most frequently used commands:

**Set WiFi credentials**

Inform the controller about the WiFi credentials it needs to send when commissioning a new device.

```json
{
  "message_id": "1",
  "command": "set_wifi_credentials",
  "args": {
    "ssid": "wifi-name-here",
    "credentials": "wifi-password-here"
  }
}
```

**Set Thread dataset**

Inform the controller about the Thread credentials it needs to use when commissioning a new device.

```json
{
  "message_id": "1",
  "command": "set_thread_dataset",
  "args": {
    "dataset": "put-credentials-here"
  }
}
```

**Commission with code**

Commission a new device. For WiFi or Thread based devices, the credentials need to be set upfront, otherwise, commissioning will fail. Supports both QR-code syntax (MT:...) and manual pairing code as string.
The controller will use bluetooth for the commissioning of wireless devices. If the machine running the Python Matter Server controller lacks Bluetooth support, commissioning will only work for devices already connected to the network (by cable or another controller).

Matter QR-code

```json
{
  "message_id": "2",
  "command": "commission_with_code",
  "args": {
    "code": "MT:Y.ABCDEFG123456789"
  }
}
```

Manual pairing code

```json
{
  "message_id": "2",
  "command": "commission_with_code",
  "args": {
    "code": "35325335079",
    "network_only": true
  }
}
```

**Open Commissioning window**

Open a commissioning window to commission a device present on this controller to another.
Returns code to use as discriminator.

```json
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

```json
{
  "message_id": "2",
  "command": "get_nodes"
}
```

**Get Node**

Get info of a single Node.

```json
{
  "message_id": "2",
  "command": "get_node",
  "args": {
    "node_id": 1
  }
}
```

**Start listening**

When the start_listening command is issued, the server will dump all existing nodes. From that moment on all events (including node attribute changes) will be forwarded.

```json
{
  "message_id": "3",
  "command": "start_listening"
}
```

**Read an attribute**

Here is an example of reading `OnOff` attribute on a switch (OnOff cluster)

```json
{
  "message_id": "read",
  "command": "read_attribute",
  "args": {
    "node_id": 1,
    "attribute_path": "1/6/0"
  }
}
```

**Write an attribute**

Here is an example of writing `OnTime` attribute on a switch (OnOff cluster)

```json
{
  "message_id": "write",
  "command": "write_attribute",
  "args": {
    "node_id": 1,
    "attribute_path": "1/6/16385",
    "value": 10
  }
}
```

**Send a command**

Here is an example of turning on a switch (OnOff cluster)

```json
{
  "message_id": "example",
  "command": "device_command",
  "args": {
    "endpoint_id": 1,
    "node_id": 1,
    "payload": {},
    "cluster_id": 6,
    "command_name": "On"
  }
}
```

**Python script to send a command**

Because we use the datamodels of the Matter SDK, this is a little bit more involved.
Here is an example of turning on a switch:

```python
import json

# Import the CHIP clusters
from chip.clusters import Objects as clusters

# Import the ability to turn objects into dictionaries, and vice-versa
from matter_server.common.helpers.util import dataclass_from_dict,dataclass_to_dict

command = clusters.OnOff.Commands.On()
payload = dataclass_to_dict(command)


message = {
    "message_id": "example",
    "command": "device_command",
    "args": {
        "endpoint_id": 1,
        "node_id": 1,
        "payload": payload,
        "cluster_id": command.cluster_id,
        "command_name": "On"
    }
}

print(json.dumps(message, indent=2))
```

You can also provide parameters for the cluster commands. Here's how to change the brightness for example:

```python
command = clusters.LevelControl.Commands.MoveToLevelWithOnOff(
  level=int(value), # provide a percentage
  transitionTime=0, # in seconds
)
```

"""Tests for json_util."""

import json
from dataclasses import dataclass

from matter_server.common.json_utils import CHIPJSONEncoder
from matter_server.common.model.message import CommandMessage
from matter_server.vendor.chip.clusters import Objects as clusters


def test_encode_dataclass():
    data = CommandMessage(messageId="123", command="command", args={"test": 42})
    output = json.dumps(data, cls=CHIPJSONEncoder)
    print(output)

    assert output == '{"messageId": "123", "command": "command", "args": {"test": 42}, "_type": "matter_server.common.model.message.CommandMessage"}'

def test_encode_dataclass_with_class_as_key():
    data = CommandMessage(messageId="123", command="command", args={str: 42})
    output = json.dumps(data, cls=CHIPJSONEncoder)
    print(output)

    assert output == '{"messageId": "123", "command": "command", "args": {"str": 42}, "_type": "matter_server.common.model.message.CommandMessage"}'

def test_encode_dataclass_with_cluster_object():
    data = CommandMessage(messageId="123", command="command", args={"payload": clusters.OnOff.Commands.Toggle()})
    output = json.dumps(data, cls=CHIPJSONEncoder)
    print(output)

    assert output == '{"messageId": "123", "command": "command", "args": {"payload": {"_type": "chip.clusters.Objects.OnOff.Commands.Toggle"}}, "_type": "matter_server.common.model.message.CommandMessage"}'

def test_encode_dataclass_with_class():
    data = CommandMessage(messageId="123", command="command", args={"attributes": [clusters.OnOff.Attributes.OnOff]})
    output = json.dumps(data, cls=CHIPJSONEncoder)
    print(output)

    assert output == '{"messageId": "123", "command": "command", "args": {"attributes": [{"_class": "chip.clusters.Objects.OnOff.Attributes.OnOff"}]}, "_type": "matter_server.common.model.message.CommandMessage"}'

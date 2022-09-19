"""Tests for json_util."""

import json

import pytest

from matter_server.common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder
from matter_server.common.model.message import CommandMessage
from matter_server.vendor.chip.clusters import Objects as clusters


def test_encode_dataclass():
    data = CommandMessage(messageId="123", command="command", args={"test": 42})
    output = json.dumps(data, cls=CHIPJSONEncoder)

    assert (
        output
        == '{"messageId": "123", "command": "command", "args": {"test": 42}, "_type": "matter_server.common.model.message.CommandMessage"}'
    )


def test_encode_dataclass_with_class_as_key():
    data = CommandMessage(messageId="123", command="command", args={str: 42})
    output = json.dumps(data, cls=CHIPJSONEncoder)

    assert (
        output
        == '{"messageId": "123", "command": "command", "args": {"str": 42}, "_type": "matter_server.common.model.message.CommandMessage"}'
    )


def test_encode_dataclass_with_cluster_object():
    data = CommandMessage(
        messageId="123",
        command="command",
        args={"payload": clusters.OnOff.Commands.Toggle()},
    )
    output = json.dumps(data, cls=CHIPJSONEncoder)

    assert (
        output
        == '{"messageId": "123", "command": "command", "args": {"payload": {"_type": "chip.clusters.Objects.OnOff.Commands.Toggle"}}, "_type": "matter_server.common.model.message.CommandMessage"}'
    )


def test_encode_dataclass_with_class():
    data = CommandMessage(
        messageId="123",
        command="command",
        args={"attributes": [clusters.OnOff.Attributes.OnOff]},
    )
    output = json.dumps(data, cls=CHIPJSONEncoder)

    assert (
        output
        == '{"messageId": "123", "command": "command", "args": {"attributes": [{"_class": "chip.clusters.Objects.OnOff.Attributes.OnOff"}]}, "_type": "matter_server.common.model.message.CommandMessage"}'
    )


def test_encode_dataclass_startup_event():
    data = CommandMessage(
        messageId="123",
        command="command",
        args={"attributes": clusters.Basic.Events.StartUp(softwareVersion=1)},
    )
    output = json.dumps(data, cls=CHIPJSONEncoder)

    assert (
        output
        == '{"messageId": "123", "command": "command", "args": {"attributes": {"softwareVersion": 1, "_type": "chip.clusters.Objects.Basic.Events.StartUp"}}, "_type": "matter_server.common.model.message.CommandMessage"}'
    )

    data2 = json.loads(output, cls=CHIPJSONDecoder)

    assert data == data2

    output = json.dumps(data2, cls=CHIPJSONEncoder)

    assert (
        output
        == '{"messageId": "123", "command": "command", "args": {"attributes": {"softwareVersion": 1, "_type": "chip.clusters.Objects.Basic.Events.StartUp"}}, "_type": "matter_server.common.model.message.CommandMessage"}'
    )


def test_encode_dataclass_startup_event():
    data = [
        CommandMessage(
            messageId="123",
            command="command",
            args={"attributes": clusters.Basic.Events.StartUp(softwareVersion=1)},
        )
    ]
    output = json.dumps(data, cls=CHIPJSONEncoder)

    assert (
        output
        == '[{"messageId": "123", "command": "command", "args": {"attributes": {"softwareVersion": 1, "_type": "chip.clusters.Objects.Basic.Events.StartUp"}}, "_type": "matter_server.common.model.message.CommandMessage"}]'
    )


def test_decode_unknown_class():
    with pytest.raises(TypeError):
        json.loads(
            '{"_type": "matter_server.common.model.message.DoesNotExist"}',
            cls=CHIPJSONDecoder,
        )

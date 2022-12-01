"""Several helpers for the websockets API."""


from dataclasses import MISSING, dataclass
import inspect
from typing import Any, Callable, Coroutine

from matter_server.common.helpers.util import parse_value


@dataclass
class APICommandHandler:
    """Model for an API command handler."""

    command: str
    signature: inspect.Signature
    target: Callable[..., Coroutine[Any, Any, Any]]

    @classmethod
    def parse(
        cls, command: str, func: Callable[..., Coroutine[Any, Any, Any]]
    ) -> "APICommandHandler":
        """Parse APICommandHandler by providing a function."""
        return APICommandHandler(
            command=command,
            signature=get_typed_signature(func),
            target=func,
        )


def api_command(command: str) -> Callable:
    """Decorate a function as API route/command."""

    def decorate(func: Callable) -> Callable[..., Coroutine[Any, Any, Any]]:
        func.api_cmd = command
        return func

    return decorate


def get_typed_signature(call: Callable) -> inspect.Signature:
    """Parse signature of function to do type validation and/or api spec generation."""
    signature = inspect.signature(call)
    return signature


def parse_arguments(func_sig: inspect.Signature, args: dict, strict: bool = False):
    """Parse (and convert) incoming arguments to correct types."""
    final_args = {}
    # ignore extra args if not strict
    if strict:
        for key, value in args.items():
            if key not in func_sig.parameters:
                raise KeyError("Invalid parameter: '%s'" % key)
    # parse arguments to correct type
    for name, param in func_sig.parameters.items():
        value = args.get(name)
        if param.default is inspect.Parameter.empty:
            default = MISSING
        else:
            default = param.default
        final_args[name] = parse_value(name, value, param.annotation, default)
    return final_args

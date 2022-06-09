from __future__ import annotations

import logging
import typing
from typing import TYPE_CHECKING

from matter_server.client.model.subscription import Subscription
from matter_server.vendor.chip.clusters import Objects as ClusterObjects

_LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .. import client


ReadAttributesType = typing.List[
    typing.Union[
        None,  # Empty tuple, all wildcard
        typing.Tuple[int],  # Endpoint
        # Wildcard endpoint, Cluster id present
        typing.Tuple[typing.Type[ClusterObjects.Cluster]],
        # Wildcard endpoint, Cluster + Attribute present
        typing.Tuple[typing.Type[ClusterObjects.ClusterAttributeDescriptor]],
        # Wildcard attribute id
        typing.Tuple[int, typing.Type[ClusterObjects.Cluster]],
        # Concrete path
        typing.Tuple[int, typing.Type[ClusterObjects.ClusterAttributeDescriptor]],
    ]
]
ReadDataVersionFiltersType = typing.List[
    typing.Tuple[int, typing.Type[ClusterObjects.Cluster], int]
]
ReadEventsType = typing.List[
    typing.Union[
        None,  # Empty tuple, all wildcard
        typing.Tuple[str, int],  # all wildcard with urgency set
        typing.Tuple[int, int],  # Endpoint,
        # Wildcard endpoint, Cluster id present
        typing.Tuple[typing.Type[ClusterObjects.Cluster], int],
        # Wildcard endpoint, Cluster + Event present
        typing.Tuple[typing.Type[ClusterObjects.ClusterEvent], int],
        # Wildcard event id
        typing.Tuple[int, typing.Type[ClusterObjects.Cluster], int],
        # Concrete path
        typing.Tuple[int, typing.Type[ClusterObjects.ClusterEvent], int],
    ]
]


class DeviceController:
    def __init__(self, client: client.Client):
        self.client = client
        self.subscriptions: dict[int, Subscription] = {}

    async def commission_with_code(self, setupPayload: str, nodeid: int):
        return await self._async_send_command(
            "CommissionWithCode",
            {
                "setupPayload": setupPayload,
                "nodeid": nodeid,
            },
        )

    async def set_wifi_credentials(self, ssid: str, credentials: str):
        return await self._async_send_command(
            "SetWiFiCredentials",
            {
                "ssid": ssid,
                "credentials": credentials,
            },
        )

    async def set_thread_operational_dataset(self, dataset: bytes):
        return await self._async_send_command(
            "SetThreadOperationalDataset",
            {
                "threadOperationalDataset": dataset,
            },
        )

    async def resolve_node(self, nodeid: int):
        return await self._async_send_command(
            "ResolveNode",
            {
                "nodeid": nodeid,
            },
        )

    async def send_command(
        self,
        nodeid: int,
        endpoint: int,
        payload: ClusterObjects.ClusterCommand,
        responseType=None,
        timedRequestTimeoutMs: int = None,
    ):
        """
        Send a cluster-object encapsulated command to a node and get returned a future that can be awaited upon to receive the response.
        If a valid responseType is passed in, that will be used to deserialize the object. If not, the type will be automatically deduced
        from the metadata received over the wire.

        timedWriteTimeoutMs: Timeout for a timed invoke request. Omit or set to 'None' to indicate a non-timed request.
        """
        # TODO add these only if defined.
        # "responseType": responseType,
        # "timedRequestTimeoutMs": timedRequestTimeoutMs,
        return await self._async_send_command(
            "SendCommand",
            {
                "nodeid": nodeid,
                "endpoint": endpoint,
                "payload": payload,
            },
        )

    async def read(
        self,
        nodeid: int,
        attributes: ReadAttributesType = None,
        dataVersionFilters: ReadDataVersionFiltersType = None,
        events: ReadEventsType = None,
        returnClusterObject: bool = False,
        reportInterval: typing.Tuple[int, int] = None,
        fabricFiltered: bool = True,
        keepSubscriptions: bool = False,
    ):
        """
        Read a list of attributes and/or events from a target node

        nodeId: Target's Node ID
        attributes: A list of tuples of varying types depending on the type of read being requested:
            (endpoint, Clusters.ClusterA.AttributeA):   Endpoint = specific,    Cluster = specific,   Attribute = specific
            (endpoint, Clusters.ClusterA):              Endpoint = specific,    Cluster = specific,   Attribute = *
            (Clusters.ClusterA.AttributeA):             Endpoint = *,           Cluster = specific,   Attribute = specific
            endpoint:                                   Endpoint = specific,    Cluster = *,          Attribute = *
            Clusters.ClusterA:                          Endpoint = *,           Cluster = specific,   Attribute = *
            '*' or ():                                  Endpoint = *,           Cluster = *,          Attribute = *

            The cluster and attributes specified above are to be selected from the generated cluster objects.

            e.g.
                ReadAttribute(1, [ 1 ] ) -- case 4 above.
                ReadAttribute(1, [ Clusters.Basic ] ) -- case 5 above.
                ReadAttribute(1, [ (1, Clusters.Basic.Attributes.Location ] ) -- case 1 above.

        dataVersionFilters: A list of tuples of (endpoint, cluster, data version).

        events: A list of tuples of varying types depending on the type of read being requested:
            (endpoint, Clusters.ClusterA.EventA, urgent):       Endpoint = specific,    Cluster = specific,   Event = specific, Urgent = True/False
            (endpoint, Clusters.ClusterA, urgent):              Endpoint = specific,    Cluster = specific,   Event = *, Urgent = True/False
            (Clusters.ClusterA.EventA, urgent):                 Endpoint = *,           Cluster = specific,   Event = specific, Urgent = True/False
            endpoint:                                   Endpoint = specific,    Cluster = *,          Event = *, Urgent = True/False
            Clusters.ClusterA:                          Endpoint = *,           Cluster = specific,   Event = *, Urgent = True/False
            '*' or ():                                  Endpoint = *,           Cluster = *,          Event = *, Urgent = True/False

        returnClusterObject: This returns the data as consolidated cluster objects, with all attributes for a cluster inside
                             a single cluster-wide cluster object.

        reportInterval: A tuple of two int-s for (MinIntervalFloor, MaxIntervalCeiling). Used by establishing subscriptions.
            When not provided, a read request will be sent.
        """
        return await self._async_send_command(
            "Read",
            {
                "nodeid": nodeid,
                "attributes": attributes,
                "dataVersionFilters": dataVersionFilters,
                "events": events,
                "returnClusterObject": returnClusterObject,
                "reportInterval": reportInterval,
                "fabricFiltered": fabricFiltered,
                "keepSubscriptions": keepSubscriptions,
            },
        )

    async def open_commissioning_window(self, nodeid):
        """Open commissioning window."""
        # TODO: We need to generate a discriminator and tell the user
        # We might also opt to use Basic Commissioning Mode, but
        # it seems to be an optional feature :o)
        # option:
        #  1 to use Enhanced Commissioning Method.
        #  0 to use Basic Commissioning Method.
        return await self._async_send_command(
            "OpenCommissioningWindow",
            {
                "nodeid": nodeid,
                "timeout": 300,
                "iteration": 1000,
                "discriminator": 3840,
                "option": 0,
            },
        )

    async def _async_send_command(self, command, args):
        """Send driver controller command."""
        return await self.client.async_send_command(
            f"device_controller.{command}", args
        )

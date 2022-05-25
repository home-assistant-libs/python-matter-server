from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import client


class DeviceController:
    def __init__(self, client: client.Client):
        self.client = client

    def ConnectBle(self, bleConnection):
        raise NotImplementedError

    def ConnectBLE(self, discriminator, setupPinCode, nodeid):
        raise NotImplementedError

    def CloseBLEConnection(self):
        raise NotImplementedError

    def CloseSession(self, nodeid):
        raise NotImplementedError

    def EstablishPASESessionIP(self, ipaddr, setupPinCode, nodeid):
        raise NotImplementedError

    def Commission(self, nodeid):
        raise NotImplementedError

    def GetTestCommissionerUsed(self):
        raise NotImplementedError

    def ResetTestCommissioner(self):
        raise NotImplementedError

    def SetTestCommissionerSimulateFailureOnStage(self, stage: int):
        raise NotImplementedError

    def SetTestCommissionerSimulateFailureOnReport(self, stage: int):
        raise NotImplementedError

    def CheckTestCommissionerCallbacks(self):
        raise NotImplementedError

    def CheckTestCommissionerPaseConnection(self, nodeid):
        raise NotImplementedError

    def CommissionIP(self, ipaddr, setupPinCode, nodeid):
        raise NotImplementedError

    def CommissionThread(
        self, discriminator, setupPinCode, nodeId, threadOperationalDataset: bytes
    ):
        """Commissions a Thread device over BLE"""
        raise NotImplementedError

    def CommissionWiFi(self, discriminator, setupPinCode, nodeId, ssid, credentials):
        """Commissions a WiFi device over BLE"""
        raise NotImplementedError

    def SetWiFiCredentials(self, ssid, credentials):
        raise NotImplementedError

    def SetThreadOperationalDataset(self, threadOperationalDataset):
        raise NotImplementedError

    def ResolveNode(self, nodeid):
        raise NotImplementedError

    def GetAddressAndPort(self, nodeid):
        raise NotImplementedError

    def DiscoverCommissionableNodesLongDiscriminator(self, long_discriminator):
        raise NotImplementedError

    def DiscoverCommissionableNodesShortDiscriminator(self, short_discriminator):
        raise NotImplementedError

    def DiscoverCommissionableNodesVendor(self, vendor):
        raise NotImplementedError

    def DiscoverCommissionableNodesDeviceType(self, device_type):
        raise NotImplementedError

    def DiscoverCommissionableNodesCommissioningEnabled(self):
        raise NotImplementedError

    def PrintDiscoveredDevices(self):
        raise NotImplementedError

    def ParseQRCode(self, qrCode, output):
        raise NotImplementedError

    def GetIPForDiscoveredDevice(self, idx, addrStr, length):
        raise NotImplementedError

    def DiscoverAllCommissioning(self):
        raise NotImplementedError

    def OpenCommissioningWindow(
        self, nodeid, timeout, iteration, discriminator, option
    ):
        raise NotImplementedError

    def GetCompressedFabricId(self):
        raise NotImplementedError

    def GetFabricId(self):
        raise NotImplementedError

    def GetClusterHandler(self):
        raise NotImplementedError

    def GetConnectedDeviceSync(self, nodeid):
        raise NotImplementedError

    async def SendCommand(
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

    async def WriteAttribute(
        self,
        nodeid: int,
        attributes: typing.List[
            typing.Tuple[int, ClusterObjects.ClusterAttributeDescriptor, int]
        ],
        timedRequestTimeoutMs: int = None,
    ):
        """
        Write a list of attributes on a target node.

        nodeId: Target's Node ID
        timedWriteTimeoutMs: Timeout for a timed write request. Omit or set to 'None' to indicate a non-timed request.
        attributes: A list of tuples of type (endpoint, cluster-object):

        E.g
            (1, Clusters.TestCluster.Attributes.XYZAttribute('hello')) -- Write 'hello' to the XYZ attribute on the test cluster to endpoint 1
        """
        raise NotImplementedError

    async def Read(
        self,
        nodeid: int,
        attributes: typing.List[
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
                typing.Tuple[
                    int, typing.Type[ClusterObjects.ClusterAttributeDescriptor]
                ],
            ]
        ] = None,
        dataVersionFilters: typing.List[
            typing.Tuple[int, typing.Type[ClusterObjects.Cluster], int]
        ] = None,
        events: typing.List[
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
        ] = None,
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
        # TODO add other args but only if set.
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

    async def ReadAttribute(
        self,
        nodeid: int,
        attributes: typing.List[
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
                typing.Tuple[
                    int, typing.Type[ClusterObjects.ClusterAttributeDescriptor]
                ],
            ]
        ],
        dataVersionFilters: typing.List[
            typing.Tuple[int, typing.Type[ClusterObjects.Cluster], int]
        ] = None,
        returnClusterObject: bool = False,
        reportInterval: typing.Tuple[int, int] = None,
        fabricFiltered: bool = True,
        keepSubscriptions: bool = False,
    ):
        """
        Read a list of attributes from a target node, this is a wrapper of DeviceController.Read()

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

        returnClusterObject: This returns the data as consolidated cluster objects, with all attributes for a cluster inside
                             a single cluster-wide cluster object.

        reportInterval: A tuple of two int-s for (MinIntervalFloor, MaxIntervalCeiling). Used by establishing subscriptions.
            When not provided, a read request will be sent.
        """
        raise NotImplementedError

    async def ReadEvent(
        self,
        nodeid: int,
        events: typing.List[
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
        ],
        reportInterval: typing.Tuple[int, int] = None,
        keepSubscriptions: bool = False,
    ):
        """
        Read a list of events from a target node, this is a wrapper of DeviceController.Read()

        nodeId: Target's Node ID
        events: A list of tuples of varying types depending on the type of read being requested:
            (endpoint, Clusters.ClusterA.EventA, urgent):       Endpoint = specific,    Cluster = specific,   Event = specific, Urgent = True/False
            (endpoint, Clusters.ClusterA, urgent):              Endpoint = specific,    Cluster = specific,   Event = *, Urgent = True/False
            (Clusters.ClusterA.EventA, urgent):                 Endpoint = *,           Cluster = specific,   Event = specific, Urgent = True/False
            endpoint:                                   Endpoint = specific,    Cluster = *,          Event = *, Urgent = True/False
            Clusters.ClusterA:                          Endpoint = *,           Cluster = specific,   Event = *, Urgent = True/False
            '*' or ():                                  Endpoint = *,           Cluster = *,          Event = *, Urgent = True/False

        The cluster and events specified above are to be selected from the generated cluster objects.

        e.g.
            ReadEvent(1, [ 1 ] ) -- case 4 above.
            ReadEvent(1, [ Clusters.Basic ] ) -- case 5 above.
            ReadEvent(1, [ (1, Clusters.Basic.Events.Location ] ) -- case 1 above.

        reportInterval: A tuple of two int-s for (MinIntervalFloor, MaxIntervalCeiling). Used by establishing subscriptions.
            When not provided, a read request will be sent.
        """
        raise NotImplementedError

    def ZCLSend(
        self, cluster, command, nodeid, endpoint, groupid, args, blocking=False
    ):
        raise NotImplementedError

    def ZCLReadAttribute(
        self, cluster, attribute, nodeid, endpoint, groupid, blocking=True
    ):
        raise NotImplementedError

    def ZCLWriteAttribute(
        self,
        cluster: str,
        attribute: str,
        nodeid,
        endpoint,
        groupid,
        value,
        dataVersion=0,
        blocking=True,
    ):
        raise NotImplementedError

    def ZCLSubscribeAttribute(
        self,
        cluster,
        attribute,
        nodeid,
        endpoint,
        minInterval,
        maxInterval,
        blocking=True,
    ):
        raise NotImplementedError

    def ZCLCommandList(self):
        raise NotImplementedError

    def ZCLAttributeList(self):
        raise NotImplementedError

    def SetLogFilter(self, category):
        raise NotImplementedError

    def GetLogFilter(self):
        raise NotImplementedError

    def SetBlockingCB(self, blockingCB):
        raise NotImplementedError

    async def _async_send_command(self, command, args):
        """Send driver controller command."""
        return await self.client.async_send_command(
            {"command": f"device_controller.{command}", "args": args}
        )

import asyncio
import functools
import logging
import typing
from platform import node

import chip.logging
import chip.native
import coloredlogs
from chip.ChipDeviceCtrl import ChipDeviceController
from chip.ChipStack import ChipStack
from chip.clusters import Attribute as Attribute
from chip.clusters import ClusterObjects as ClusterObjects
from chip.FabricAdmin import FabricAdmin
from matter_server.client.model import device_controller

_LOGGER = logging.getLogger(__name__)


class CHIPControllerServer:

    # To track if wifi credentials set this session.
    wifi_cred_set = False
    device_controller: ChipDeviceController
    subscriptions: list[Attribute.SubscriptionTransaction]

    def __init__(self):
        self._callback = None
        self.subscriptions = []
        self._queue = asyncio.Queue()

    def setup(self, storage_path):
        _LOGGER.info("Setup CHIP Controller Server")
        chip.native.GetLibraryHandle()
        chip.logging.RedirectToPythonLogging()
        coloredlogs.install(level=logging.INFO)
        self._stack = ChipStack(persistentStoragePath=storage_path)

        self._fabricAdmin = FabricAdmin()

        self.device_controller = self._fabricAdmin.NewController()
        _LOGGER.info("CHIP Controller Stack initialized")

    def get_method(self, command: str):
        # Subclass ChipDeviceController instead maybe? :)
        if method := getattr(self, command, None):
            return method
        return getattr(self.device_controller, command, None)

    async def Read(self, nodeid: int, attributes: typing.List[typing.Union[
        None,  # Empty tuple, all wildcard
        typing.Tuple[int],  # Endpoint
        # Wildcard endpoint, Cluster id present
        typing.Tuple[typing.Type[ClusterObjects.Cluster]],
        # Wildcard endpoint, Cluster + Attribute present
        typing.Tuple[typing.Type[ClusterObjects.ClusterAttributeDescriptor]],
        # Wildcard attribute id
        typing.Tuple[int, typing.Type[ClusterObjects.Cluster]],
        # Concrete path
        typing.Tuple[int, typing.Type[ClusterObjects.ClusterAttributeDescriptor]]
    ]] = None, dataVersionFilters: typing.List[typing.Tuple[int, typing.Type[ClusterObjects.Cluster], int]] = None, events: typing.List[typing.Union[
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
        typing.Tuple[int,
                     typing.Type[ClusterObjects.ClusterEvent], int]
    ]] = None,
            returnClusterObject: bool = False, reportInterval: typing.Tuple[int, int] = None, fabricFiltered: bool = True, keepSubscriptions: bool = False):
        if reportInterval is None:
            return await self.device_controller.Read(nodeid, attributes, dataVersionFilters, events, returnClusterObject, reportInterval=None, fabricFiltered=fabricFiltered, keepSubscriptions=False)
        else:
            _LOGGER.info("Setting up Subscription for %s", attributes)

            fabricid = self.device_controller.GetFabricId()
            loop = asyncio.get_event_loop()

            # Subscription, we need to keep track on it server side
            def DeviceAttributeChangeCallback(path: Attribute.TypedAttributePath, transaction: Attribute.SubscriptionTransaction):
                data = transaction.GetAttribute(path)
                value = {
                    'FabridId': fabricid,
                    'NodeId': nodeid,
                    'Endpoint': path.Path.EndpointId,
                    'Attribute': path.AttributeType,
                    'Value': data
                }
                _LOGGER.info("DeviceAttributeChangeCallback %s", value)
                #loop.call_soon_threadsafe(functools.partial(self._callback(value)))
                # For some reason, this callback is running in the CHIP Stack thread
                loop.call_soon_threadsafe(self._queue.put_nowait, value)


            subscription = await self.device_controller.Read(nodeid, attributes, dataVersionFilters, events, returnClusterObject, reportInterval, fabricFiltered, keepSubscriptions)
            _LOGGER.info("Setting callback for subscription of %s", attributes)
            subscription.SetAttributeUpdateCallback(DeviceAttributeChangeCallback)
            self.subscriptions.append(subscription)
            return None

    def register_callback(self, callback):
        self._callback = callback

    async def get_next_event(self):
        return await self._queue.get()


    def shutdown(self):
        for subscription in self.subscriptions:
            _LOGGER.info("Shutdown subscription %s", subscription)
            subscription.Shutdown()

        _LOGGER.info("Shutdown CHIP Controller Server")
        self.device_controller.Shutdown()
        self._stack.Shutdown()

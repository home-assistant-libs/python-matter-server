from typing import Callable


class Subscription:
    subscriptionId: int
    handler: Callable[[dict], None]

    def __init__(self, subscriptionId):
        self.subscriptionId = subscriptionId

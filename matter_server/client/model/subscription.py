from typing import Callable


class Subscription:
    subscription_id: int
    handler: Callable[[dict], None]

    def __init__(self, subscription_id):
        self.subscription_id = subscription_id

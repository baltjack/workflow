from abc import ABC, abstractmethod
import redis.asyncio as redis


class NotificationStore(ABC):
    """generic base class for notifications"""

    @abstractmethod
    async def subscribe(self, channel: str):
        pass

    @abstractmethod
    async def get_message(self, ignore_subscribe_messages=True, timeout=1):
        pass


class RedisNotificationStore(NotificationStore):
    def __init__(self, redis_client: redis.StrictRedis) -> None:
        self.client = redis_client
        self.pubsub = self.client.pubsub()

    async def subscribe(self, channel: str):
        return self.pubsub.subscribe(channel)

    async def get_message(self, ignore_subscribe_messages=True, timeout=1):
        return self.pubsub.get_message(ignore_subscribe_messages, timeout)

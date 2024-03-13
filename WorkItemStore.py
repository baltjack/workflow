from abc import ABC, abstractmethod
import redis.asyncio as redis
from .WorkItem import WorkItem, SparseWorkItem


class WorkItemStore(ABC):
    """Generic base class for work item stores"""

    @abstractmethod
    def create_item(self) -> WorkItem:
        pass

    @abstractmethod
    def get_item(self, workitem_id: str) -> WorkItem:
        pass

    @abstractmethod
    def get_summaries(self) -> list[SparseWorkItem]:
        pass


class RedisWorkItemStore(WorkItemStore):
    def __init__(self, redis_client: redis.StrictRedis) -> None:
        self.client = redis_client

    def create_item(self) -> WorkItem:
        # todo : save this to the store
        return WorkItem("1", "", {})

    def get_item(self, workitem_id: str) -> WorkItem:
        # todo : this is fake
        return WorkItem(workitem_id, "", {})

    def get_summaries(self) -> list[SparseWorkItem]:
        # todo : this is fake
        return []

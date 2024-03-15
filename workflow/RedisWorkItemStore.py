import redis
import uuid
import json
from .WorkItem import WorkItem, SparseWorkItem
from .WorkItemStore import WorkItemStore


class RedisWorkItemStore(WorkItemStore):
    def __init__(self, redis_client: redis.StrictRedis) -> None:
        self.client = redis_client

    # CRU (no D) items
    def create_item(self) -> str:
        newId = str(uuid.uuid4())
        self.client.set(newId + ".data", "{}")
        self.client.set(newId + ".keys", "[]")
        return newId

    def get_item(self, workitem_id: str) -> WorkItem:
        raw = self.client.get(workitem_id + ".data")
        if raw is None:
            raise ValueError(f"Workitem {workitem_id} not found!")

        return WorkItem(workitem_id, json.loads(str(raw)))

    def save_item(self, save_me: WorkItem):
        self.client.set(save_me.wi_id + ".data", json.dumps(save_me.data))
        self.client.set(save_me.wi_id + ".keys", json.dumps(list(save_me.data.keys())))

    # summaries
    def get_summaries(self) -> list[SparseWorkItem]:

        self.client.scan_iter("*.keys", 10)
        print("getting fake summaries")
        # todo : START HERE.  this is fake
        return []

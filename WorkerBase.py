import asyncio
import json
from abc import ABC, abstractmethod
import redis.asyncio as redis
from .WorkItem import WorkItem, SparseWorkItem

# from .array_utils import all_present, none_present
# from .work_item_summary import WorkItemSummary
# from .workflowMapping import workflowMapping


class WorkerBase(ABC):
    """Generic base class for workers"""

    def __init__(self, redis_client: redis.StrictRedis, scan_interval_seconds: int = 30) -> None:
        self.redis_client = redis_client
        self.scan_interval_seconds = scan_interval_seconds

    async def start(self):
        """starts the worker...runs forever"""

        scan_task = asyncio.create_task(self.full_scan())
        live_task = asyncio.create_task(self.live())

        try:
            await asyncio.gather(scan_task, live_task)
        except asyncio.CancelledError:
            print("tasks cancelled")

    async def live(self):
        """an endelss function to listen to live notifications"""
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe("notifications")
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
            if message is not None:
                wis_json = message["data"]
                summary_dict = json.loads(wis_json)
                summary = SparseWorkItem(**summary_dict)
                print(summary)
                # self.check_and_do(summary)

    async def full_scan(self):
        """big catchup sweeps"""
        while True:
            await asyncio.sleep(self.scan_interval_seconds)

    @abstractmethod
    def check_item(self, summary: SparseWorkItem) -> bool:
        pass

    @abstractmethod
    def do_item(self, item: WorkItem) -> None:
        # todo : have this return Dict[str, str]
        pass


#

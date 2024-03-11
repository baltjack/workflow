import asyncio
import json
from abc import ABC, abstractmethod
import redis.asyncio as redis
import config
from .array_utils import all_present, none_present
from .work_item_summary import WorkItemSummary
from .work_item import WorkItem
from .connec import connect
from .workflowMapping import workflowMapping


class WorkerBase(ABC):
    """Generic base class for workers"""

    def ___init__(self, scan_interval_seconds=300):
        self.wis = connect(config.REDIS_SERVER, config.REDIS_PORT)
        self.scan_interval_seconds = scan_interval_seconds

    async def start(self):
        """ starts the worker...runs forever"""

        scan_task = asyncio.create_task(self.full_scan())
        live_task = asyncio.create_task(self.live())

        try: 
            await asyncio.gather(scan_task, live_task)
        except asyncio.CancelledError:
            print("tasks cancelled")

    async def live(self):
        """an endelss function to listen to live notifications"""

        # todo : fix this
        redis_client = redis.StrictRedis(
            host=config.REDIS_SERVER, port=config.REDIS_PORT, decode_responses=True
        )
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("notifications")
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=true, timeout=1
            )
            if message is not None:
                wis_json = message["data"]
                summary_dict = json.loads(wis_json)
                summary = WorkItemSummary(**summary_dict)
                self.check_and_do(summary)
    
    @abstractmethod
    def check_item(self, summary: WorkItemSummary) -> bool: 
        ...

    @abstractmethod
    def do_item(self, item: WorkItem) -> None:
        # todo : have this return Dict[str, str]
        ...
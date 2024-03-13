import asyncio
import json
from abc import ABC, abstractmethod
from .WorkItem import WorkItem, SparseWorkItem
from .WorkItemStore import WorkItemStore
from .NotificationStore import NotificationStore
from .WorkerResult import WorkerResult

# from .array_utils import all_present, none_present
# from .work_item_summary import WorkItemSummary
# from .workflowMapping import workflowMapping


class WorkerBase(ABC):
    """Generic base class for workers"""

    def __init__(self, wis: WorkItemStore, ns: NotificationStore, scan_interval_seconds: int = 30) -> None:
        self.workitem_store = wis
        self.notification_store = ns
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
        await self.notification_store.subscribe("notifications")
        while True:
            message = await self.notification_store.get_message(ignore_subscribe_messages=True, timeout=1)
            if message is not None:
                wis_json = message["data"]
                summary_dict = json.loads(wis_json)
                summary = SparseWorkItem(**summary_dict)
                print(summary)
                # todo : check and do

    async def full_scan(self):
        """big catchup sweeps"""
        while True:
            print("Sweep")
            print(self.scan_interval_seconds)
            summaries = self.workitem_store.get_summaries()
            for summary in summaries:
                print(summary)
                # todo : check and do

            await asyncio.sleep(self.scan_interval_seconds)
            print("done sleeping")

    @abstractmethod
    def check_item(self, summary: SparseWorkItem) -> bool:
        pass

    @abstractmethod
    def do_item(self, item: WorkItem) -> WorkerResult:
        pass

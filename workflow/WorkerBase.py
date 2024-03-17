import asyncio
import json
from abc import ABC, abstractmethod
from .WorkItem import WorkItem, SparseWorkItem
from .WorkItemStore import WorkItemStore
from .NotificationStore import NotificationStore
from .WorkerResult import WorkerResult
from .array__utils import all_present, none_present, update_original_with_updates

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
            print(f"{self.scan_interval_seconds} sweep")
            summaries = self.workitem_store.get_summaries()
            for summary in summaries:
                if self.check_item(summary):
                    # todo : lock it
                    do_me = self.workitem_store.get_item(summary.wi_id)
                    results = self.do_item(do_me)

                    # validate expectations
                    new_keys = set(results.inserts.keys())
                    up_keys = set(results.updates.keys())
                    old_keys = set(do_me.data.keys())
                    if not none_present(new_keys, old_keys):
                        raise KeyError(f"Inserting already existing key.  Existing : {old_keys}.  Inserts : {new_keys}")
                    if not all_present(up_keys, old_keys):
                        raise KeyError(f"Updating missing key.  Existing : {old_keys}.  Update : {up_keys}")

                    # todo : validate with WF

                    # update and save
                    do_me.data = {**do_me.data, **results.inserts}
                    do_me.data = update_original_with_updates(do_me.data, results.updates)
                    self.workitem_store.save_item(do_me)

                    # todo : unlock it
            await asyncio.sleep(self.scan_interval_seconds)
            print("done sleeping")

    @abstractmethod
    def check_item(self, summary: SparseWorkItem) -> bool:
        pass

    @abstractmethod
    def do_item(self, item: WorkItem) -> WorkerResult:
        pass

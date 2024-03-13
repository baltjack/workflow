import asyncio
from .WorkItem import SparseWorkItem, WorkItem
from .WorkItemStore import FakeWorkItemStore
from .NotificationStore import NeverNotificationStore
from .WorkerBase import WorkerBase
from .WorkerResult import WorkerResult


class SampleWorker(WorkerBase):
    def check_item(self, summary: SparseWorkItem) -> bool:
        print("checking item")
        return True

    def do_item(self, item: WorkItem) -> WorkerResult:
        print("doing item")
        return WorkerResult()


if __name__ == "__main__":
    try:
        ws = FakeWorkItemStore()
        ns = NeverNotificationStore()
        startMe = SampleWorker(ws, ns, 10)
        asyncio.run(startMe.start())
    except KeyboardInterrupt:
        print("keyboard interrupt: stopping tasks")

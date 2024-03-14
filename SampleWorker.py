import asyncio
import redis
from workflow.WorkItem import SparseWorkItem, WorkItem

# from workflow.WorkItemStore import FakeWorkItemStore
from workflow.WorkItemStore import RedisWorkItemStore
from workflow.NotificationStore import NeverNotificationStore
from workflow.WorkerBase import WorkerBase
from workflow.WorkerResult import WorkerResult


class SampleWorker(WorkerBase):
    def check_item(self, summary: SparseWorkItem) -> bool:
        print("SampleWorker : checking item")
        return True

    def do_item(self, item: WorkItem) -> WorkerResult:
        print("SampleWorker : doing item")
        return WorkerResult()


if __name__ == "__main__":
    try:
        # ws = FakeWorkItemStore()
        ws = RedisWorkItemStore(
            redis_client=redis.StrictRedis(host="my-redis", port=6379, decode_responses=True)
        )
        ws.create_item()
        # ns = NeverNotificationStore()
        # startMe = SampleWorker(ws, ns, 10)
        # asyncio.run(startMe.start())
    except KeyboardInterrupt:
        print("keyboard interrupt: stopping tasks")

import asyncio
from WorkItem import SparseWorkItem, WorkItem
from WorkerBase import WorkerBase
import redis.asyncio as redis


class SampleWorker(WorkerBase):
    def __init__(self) -> None:
        client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
        super().__init__(client)

    def check_item(self, summary: SparseWorkItem) -> bool:
        print("checking item")
        return True

    def do_item(self, item: WorkItem) -> None:
        print("doing item")


if __name__ == "__main__":
    try:
        startMe = SampleWorker()
        asyncio.run(startMe.start())
    except KeyboardInterrupt:
        print("keyboard interrupt: stopping tasks")

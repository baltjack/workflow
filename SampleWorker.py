from WorkItem import SparseWorkItem, WorkItem
from WorkerBase import WorkerBase


class SampleWorker(WorkerBase):

    def check_item(self, summary: SparseWorkItem) -> bool:
        print("checking item")
        return True

    def do_item(self, item: WorkItem) -> None:
        print("doing item")


# if __name__ == "__main__":
#     try:
#         startMe = SampleWorker()
#         asyncio.run(startMe.start())
#     except KeyboardInterrupt:
#         print("keyboard interrupt: stopping tasks")

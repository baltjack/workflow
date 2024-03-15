from abc import ABC, abstractmethod
from .WorkItem import WorkItem, SparseWorkItem


class WorkItemStore(ABC):
    """Generic base class for work item stores"""

    @abstractmethod
    def create_item(self) -> str:
        pass

    @abstractmethod
    def get_item(self, workitem_id: str) -> WorkItem:
        pass

    @abstractmethod
    def save_item(self, saveMe: WorkItem) -> None:
        pass

    @abstractmethod
    def get_summaries(self) -> list[SparseWorkItem]:
        pass


class FakeWorkItemStore(WorkItemStore):
    def create_item(self) -> str:
        # todo : save this to the store
        return "1"

    def get_item(self, workitem_id: str) -> WorkItem:
        # todo : this is fake
        return WorkItem(workitem_id, {})

    def save_item(self, saveMe: WorkItem) -> None:
        return

    def get_summaries(self) -> list[SparseWorkItem]:
        print("getting fake summaries")
        # todo : this is fake
        return []

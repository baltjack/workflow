class SparseWorkItem:
    def __init__(self, wi_id: str, keys: list[str]) -> None:
        self.wi_id = wi_id
        self.keys = keys


class WorkItem:
    def __init__(self, wi_id: str, data: dict[str, str]) -> None:
        self.wi_id = wi_id
        self.data = data

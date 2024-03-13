class SparseWorkItem:
    def __init__(self, wi_id: str, owner: str, keys: list[str]) -> None:
        self.wi_id = wi_id
        self.owner = owner
        self.keys = keys


class WorkItem:
    def __init__(self, wi_id: str, owner: str, data: dict[str, str]) -> None:
        self.wi_id = wi_id
        self.owner = owner
        self.data = data

    def to_sparse(self) -> SparseWorkItem:
        return SparseWorkItem(self.wi_id, self.owner, list(self.data.keys()))

class WorkerResult:
    def __init__(self, inserts: dict[str, str] = {}, updates: dict[str, str] = {}, deletes: list[str] = []) -> None:
        self.inserts = inserts
        self.updates = updates
        self.deletes = deletes

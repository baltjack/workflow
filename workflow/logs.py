import json


class LogEntry:
    def __init__(self, entry: str, iso_date: str) -> None:
        self.entry = entry
        self.iso_date = iso_date


class LogEntries:
    @classmethod
    def from_json(cls, serialized_json: str) -> list[LogEntry]:
        data = json.loads(serialized_json)
        return_me = [LogEntry(**obj) for obj in data]
        return return_me

    @classmethod
    def to_json(cls, serialize_me: list[LogEntry]) -> str:
        return json.dumps([vars(item) for item in serialize_me])

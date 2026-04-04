from abc import ABC
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DecodedCursor:
    id: str
    created_at: datetime


class CursorPaginationPorts(ABC):

    def encode(self, id: str, created_at: datetime) -> str:
        pass

    def decode(self, cursor: str) -> DecodedCursor:
        pass

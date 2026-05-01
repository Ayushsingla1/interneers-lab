from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DecodedCursor:
    id: str
    created_at: datetime


class CursorPaginationPorts(ABC):

    @abstractmethod
    def encode(self, id: str, created_at: datetime) -> str:
        pass

    @abstractmethod
    def decode(self, cursor: str) -> DecodedCursor:
        pass

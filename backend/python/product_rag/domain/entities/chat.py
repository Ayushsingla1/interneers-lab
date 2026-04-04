from dataclasses import dataclass
from enum import Enum
from typing import List


class ROLE(Enum):
    USER = "user"
    AI = "ai"


@dataclass
class Chat:
    role: ROLE
    text: str


@dataclass
class ChatHistory:
    chats: List[Chat]

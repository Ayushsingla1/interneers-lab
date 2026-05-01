from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class AgentRole(Enum):
    USER = "user"
    AI = "ai"


@dataclass
class AgentMessage:
    role: AgentRole
    text: str


@dataclass
class AgentRequest:
    """Represents a user request to the agent - can include text, file, or both."""

    text: Optional[str] = None
    has_file: bool = False
    chat_history: List[AgentMessage] = field(default_factory=list)


@dataclass
class AgentResponse:
    """The agent's final response after reasoning through tools."""

    answer: str
    tools_used: List[str] = field(default_factory=list)

from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    title: str
    description: str
    id: Optional[str] = None

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title can't be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Description can't be empty")

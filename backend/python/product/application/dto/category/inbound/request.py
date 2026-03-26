from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateCategoryRequest:
    title: str
    description: str

    def __post_init__(self):

        if not self.title or not self.title.strip():
            raise ValueError("title can't be empty")

        if not self.description or not self.description.strip():
            raise ValueError("description can't be empty")


@dataclass
class UpdateCategoryRequest:
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self):

        if self.title is not None and not self.title.strip():
            raise ValueError("title can't be empty")

        if self.description is not None and not self.description.strip():
            raise ValueError("description can't be empty")

    def has_change(self) -> bool:
        for v in vars(self).values():
            if v is not None:
                return True
        return False

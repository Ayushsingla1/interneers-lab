from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryCreationData:
    title: str
    description: str


@dataclass
class CategoryUpdateData:
    title: Optional[str] = None
    description: Optional[str] = None

    def fields_to_change(self):
        return {k: v for k, v in vars(self).items() if v is not None}

from dataclasses import dataclass


@dataclass
class CategoryResponse:
    id: str
    title: str
    description: str

from product.domain.entities.category import Category
from ..models import CategoryDocument


def _to_entity_category(item) -> Category:

    return Category(id=str(item.id), title=item.title, description=item.description)


def _to_document_category(item) -> CategoryDocument:
    return CategoryDocument(title=item.title, description=item.description)

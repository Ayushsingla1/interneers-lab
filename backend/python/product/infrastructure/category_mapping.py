from product.domain.entities.product import ProductCategory

from .models import CategoryDoument


def _to_entity_category(item: CategoryDoument) -> ProductCategory:

    return ProductCategory(
        id=str(item.id), title=item.title, description=item.description
    )


def _to_document_category(item: ProductCategory) -> CategoryDoument:
    return CategoryDoument(title=item.title, description=item.description)

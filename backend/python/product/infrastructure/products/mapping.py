from product.application.dto.products import ProductCreationData
from product.domain.entities.product import Product
from ..models import ProductDocument


def _to_entity_product(product: ProductDocument) -> Product:
    try:
        return Product(
            name=product.name,
            description=product.description,
            quantity=product.quantity,
            price=product.price,
            id=str(product.id),
            brand=product.brand,
            category=product.category.id,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    except Exception as e:
        print(e)
        raise ValueError("unable to parse") from e


def _to_document_product(product: ProductCreationData) -> ProductDocument:
    return ProductDocument(
        name=product.name,
        description=product.description,
        brand=product.brand,
        category=product.category,
        quantity=product.quantity,
        price=product.price,
    )

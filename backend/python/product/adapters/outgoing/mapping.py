from product.adapters.outgoing.models import ProductDocument
from product.domain.entities.product import Product


def _to_entity(product) -> Product:
    return Product(
        name=product.name,
        description=product.description,
        quantity=product.quantity,
        price=product.price,
        id=str(product.id),
        brand=product.brand,
        category=product.category,
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


def _to_document(product: Product) -> ProductDocument:
    return ProductDocument(
        name=product.name,
        description=product.description,
        brand=product.brand,
        category=product.category,
        quantity=product.quantity,
    )

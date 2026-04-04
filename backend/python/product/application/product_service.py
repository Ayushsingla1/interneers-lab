from base64 import b64decode, urlsafe_b64encode
from product.application.dto.products.outbound.response import ProductsRepoResponse
from product.domain.custom_exceptions import InvalidToken
from product.application.dto.products.outbound.request import (
    ProductCreationData,
    ProductUpdateData,
)
from product.application.mappers.product_mapper import (
    map_product_to_response,
    map_products_to_responses,
)
from product.domain.entities.product import Product
from product.application.ports.incoming import product_service_port
from product.application.ports.outgoing import product_repo_port, category_repo_port
from product.application.dto.products.inbound.request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from product.application.dto.products.inbound.response import (
    ProductResponse,
    ProductsResponse,
)
from datetime import datetime
import json


class ProductService(product_service_port.ProductServicePorts):
    def __init__(
        self,
        product_repository: product_repo_port.ProductRepositoryPorts,
        category_repository: category_repo_port.CategoryRepositoryPorts,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def get_all(
        self, cursor: str, limit: int, category: str, created_after: datetime | None
    ) -> ProductsRepoResponse:

        id = None
        date = None
        if cursor is not None:
            required_keys = ["created_at", "id"]
            decoded_token = json.loads(b64decode(cursor).decode("utf-8"))
            if all(key in decoded_token for key in required_keys):
                id = decoded_token["id"]
                date = datetime.fromisoformat(decoded_token["created_at"])
            else:
                raise InvalidToken("Token sent is invalid")

        if category is not None:
            category = self.category_repository.get_by_name(category)

        repo_response = self.product_repository.get_all(
            id=id,
            limit=limit,
            category=category,
            date=date,
            created_after=created_after,
        )
        products = repo_response.products

        next_cursor = None

        if repo_response.has_more:
            new_token_json = json.dumps(
                {
                    "created_at": products[-1].created_at.isoformat(),
                    "id": products[-1].id,
                }
            )

            next_cursor = urlsafe_b64encode(new_token_json.encode("utf-8")).decode(
                "utf-8"
            )

        return ProductsResponse(
            products=map_products_to_responses(products),
            next_cursor=next_cursor,
            has_more=repo_response.has_more,
        )

    def get_by_id(self, id: str) -> ProductResponse:
        product: Product = self.product_repository.get_by_id(id)
        return map_product_to_response(product)

    def add(self, item: CreateProductRequest) -> ProductResponse:
        category_id = self.category_repository.get_by_name(item.category)
        create_data = ProductCreationData(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
            brand=item.brand,
            category=category_id,
        )
        product: Product = self.product_repository.add(create_data)
        return map_product_to_response(product)

    def update(self, id: str, item: UpdateProductRequest):

        if item.category is not None:
            category_details = self.category_repository.get_by_name(item.category)
            item.category = category_details.id

        update_data = ProductUpdateData(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
            brand=item.brand,
            category=item.category,
        )
        return self.product_repository.update(id, update_data)

    def delete(self, id: str):
        return self.product_repository.delete(id)

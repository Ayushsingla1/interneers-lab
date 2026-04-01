from product.application.ports.outgoing.query_repo_port import QueryRepositoryPorts
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from product.domain.entities.product import Product
from typing import List


class QueryRepository(QueryRepositoryPorts):

    def __init__(self, client: QdrantClient, encoder: SentenceTransformer) -> None:
        self.client = client
        self.encoder = encoder

    def add(self, products: List[Product]):

        points = []

        for idx, product in enumerate(products):
            points.append(
                models.PointStruct(
                    id=idx,
                    vector=self.encoder.encode(product.description),
                    payload={
                        "id": str(product.id),
                        "name": product.name,
                        "description": product.description,
                        "brand": product.brand,
                    },
                )
            )

        try:
            self.client.upsert(collection_name="products", points=points)
        except Exception as e:
            print(f"Unable to add product : {str(e)}")

    def get_related(self, description: str) -> List[str]:

        try:
            related_points = self.client.query_points(
                collection_name="products",
                query=self.encoder.encode(description).tolist(),
                limit=4,
            )

            return [point.payload["id"] for point in related_points.points]

        except Exception as e:
            raise e

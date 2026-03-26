from sentence_transformers import SentenceTransformer
from qdrant_client import models, QdrantClient


encoder = SentenceTransformer("all-MiniLM-L6-v2")

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="products",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(), 
        distance=models.Distance.COSINE,
    ),
)

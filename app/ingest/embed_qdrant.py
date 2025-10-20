from qdrant_client import QdrantClient
from app.utils.settings import settings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore


class EmbeddingSelfQuery:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            timeout=120,
        )

        self.model = OpenAIEmbeddings(
            model="text-embedding-3-large",
        )

    def get_qdrant_vector_store(self, collection_name: str) -> QdrantVectorStore:
        return QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.model,
            sparse_vector_name="text-sparse",
            vector_name="text-dense",
        )

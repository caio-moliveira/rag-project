from typing import List, Optional

from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.documents import Document
from app.ingest.embed_qdrant import EmbeddingSelfQuery
from app.retrieval.self_query import document_content_description, metadata_field_info
from dataclasses import dataclass


@dataclass
class SelfQueryConfig:
    collection_name: str = "sumulas_jornada"
    k: int = 10


def build_self_query_retriever(cfg: SelfQueryConfig) -> SelfQueryRetriever:
    """
    Cria o SelfQueryRetriever sobre o QdrantVectorStore.
    """
    embedder = EmbeddingSelfQuery()
    vectorstore = embedder.get_qdrant_vector_store(cfg.collection_name)

    retriever = SelfQueryRetriever.from_llm(
        llm=embedder.llm,
        vectorstore=vectorstore,
        document_contents=document_content_description,
        metadata_field_info=metadata_field_info,
        enable_limit=True,
        search_kwargs={"k": cfg.k},
    )
    return retriever


def search(
    query: str,
    cfg: Optional[SelfQueryConfig] = None,
) -> List[Document]:
    """
    Consulta usando self-query: o LLM infere termos SEMÂNTICOS e também FILTROS de metadado.
    """
    cfg = cfg or SelfQueryConfig()
    retriever = build_self_query_retriever(cfg)
    # .invoke() retorna List[Document]
    return retriever.invoke(query)

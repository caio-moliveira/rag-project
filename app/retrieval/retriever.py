from typing import List, Optional

from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.documents import Document

# Reaproveita seu cliente/embeddings/LLM/QdrantVectorStore
from app.ingest.embed_qdrant import EmbeddingSelfQuery
from app.retrieval.self_query import document_content_description, metadata_field_info
from dataclasses import dataclass


@dataclass
class SelfQueryConfig:
    collection_name: str = "sumulas_jornada"
    k: int = 5
    verbose: bool = False


def build_self_query_retriever(cfg: SelfQueryConfig) -> SelfQueryRetriever:
    """
    Cria o SelfQueryRetriever sobre o QdrantVectorStore já configurado no seu wrapper.
    """
    embedder = EmbeddingSelfQuery()
    vectorstore = embedder.get_qdrant_vector_store(cfg.collection_name)

    # Descrição sucinta do conteúdo dos documentos (ajuda o LLM a montar filtros corretos)

    retriever = SelfQueryRetriever.from_llm(
        llm=embedder.llm,  # seu ChatOpenAI(gpt-4.1-mini)
        vectorstore=vectorstore,
        document_contents=document_content_description,
        metadata_field_info=metadata_field_info,
        verbose=cfg.verbose,
        enable_limit=True,  # permite o LLM ajustar limite de resultados
        search_kwargs={"k": cfg.k},  # define k padrão (pode ser sobrescrito)
    )
    return retriever


def search(
    query: str,
    cfg: Optional[SelfQueryConfig] = None,
) -> List[Document]:
    """
    Consulta usando self-query: o LLM infere termos SEMÂNTICOS e também FILTROS de metadado.
    Exemplos de queries naturais que geram filtro:
      - "Mostre súmulas VIGENTES sobre licitação"
      - "Traga precedentes da súmula 70"
      - "O que diz a súmula publicada em 07/04/2014?"
      - "Buscar referências normativas da súmula 70 no arquivo Sumula_70.pdf"
    """
    cfg = cfg or SelfQueryConfig()
    retriever = build_self_query_retriever(cfg)
    # .invoke() retorna List[Document]
    return retriever.invoke(query)

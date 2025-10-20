import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any
from qdrant_client import models
from qdrant_client.http.models import Distance, VectorParams, SparseVectorParams
from markitdown import MarkItDown
from app.ingest.embed_qdrant import EmbeddingSelfQuery

md = MarkItDown()


def process_pdf_file(
    file_path: str, embedder: EmbeddingSelfQuery
) -> List[Dict[str, Any]]:
    """
    Usa o LLM interno do embedder para extrair metadados e dividir em até 3 chunks
    """
    pdf_name = os.path.basename(file_path)
    result = md.convert(str(file_path))
    text_content = result.text_content or ""

    # Prompt de extração
    prompt = f"""
Você é um especialista jurídico do Tribunal de Contas de Minas Gerais.
Analise o texto abaixo e extraia:

1️⃣ Metadados:
- num_sumula: número da súmula (ex: 71)
- data_status: última data (formato DD/MM/AA)
- data_status_ano: última data (formato AAAA)
- status_atual: último status (VIGENTE, REVOGADA, ALTERADA, etc.)
- pdf_name: nome do arquivo PDF

2️⃣ Chunks (máximo de 3):
- conteudo_principal: texto vigente até antes de 'REFERÊNCIAS NORMATIVAS'
- referencias_normativas: texto após 'REFERÊNCIAS NORMATIVAS:' até antes de 'PRECEDENTES:'
- precedentes: texto após 'PRECEDENTES:' até o final

Retorne **somente** um JSON no formato:
{{
  "metadados": {{
    "num_sumula": "...",
    "data_status": "...",
    "data_status_ano": "...",
    "status_atual": "...",
    "pdf_name": "{pdf_name}"
  }},
  "chunks": {{
    "conteudo_principal": "...",
    "referencias_normativas": "...",
    "precedentes": "..."
  }}
}}

Texto da súmula:
{text_content[:12000]}
"""

    try:
        response = embedder.llm.invoke(prompt)
        json_text = (
            re.sub(r"```[\w-]*", "", response.content).replace("```", "").strip()
        )
        data = json.loads(json_text)

        metadados = data.get("metadados", {})
        chunks = data.get("chunks", {})

        processed = []
        for idx, (tipo, texto) in enumerate(chunks.items()):
            if not texto or idx >= 3:
                continue
            metadata = {
                "num_sumula": metadados.get("num_sumula"),
                "data_status": metadados.get("data_status"),
                "data_status_ano": metadados.get("data_status_ano"),
                "status_atual": metadados.get("status_atual"),
                "pdf_name": metadados.get("pdf_name", pdf_name),
                "chunk_type": tipo,
                "chunk_index": idx,
            }
            processed.append({"text": texto.strip(), "metadata": metadata})

        return processed

    except Exception as e:
        print(f"⚠️ Erro ao processar {pdf_name}: {e}")
        return []


def main(collection: str = "sumulas_jornada", pasta_pdfs: str = "sumulas"):
    embedder = EmbeddingSelfQuery()

    # Cria coleção se não existir
    if not embedder.client.collection_exists(collection_name=collection):
        embedder.client.create_collection(
            collection_name=collection,
            vectors_config={
                "text-dense": VectorParams(size=3072, distance=Distance.COSINE)
            },
            sparse_vectors_config={
                "text-sparse": SparseVectorParams()  # sem size para esparso
            },
        )
        print(f"Coleção '{collection}' criada.")
    else:
        print(f"Coleção '{collection}' já existe.")

    vector_store = embedder.get_qdrant_vector_store(collection)
    pdf_files = list(Path(pasta_pdfs).glob("*.pdf"))
    if not pdf_files:
        print("Nenhum PDF encontrado na pasta.")
        return

    total_chunks = 0
    for pdf_file in pdf_files:
        chunks = process_pdf_file(str(pdf_file), embedder)
        if not chunks:
            continue
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        vector_store.add_texts(texts=texts, metadatas=metadatas)
        total_chunks += len(chunks)

    print(
        f"✅ {len(pdf_files)} PDFs processados. {total_chunks} chunks inseridos no Qdrant."
    )


if __name__ == "__main__":
    main()

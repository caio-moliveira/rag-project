from langchain.chains.query_constructor.schema import AttributeInfo


metadata_field_info = [
    AttributeInfo(
        name="num_sumula",
        description=(
            "- Número da súmula (ex.: '70'). Texto simples, sem prefixo.\n"
            "- Sempre filtre pelo número da súmula quando o usuário perguntar exclusivamente usando o número."
        ),
        type="string",
    ),
    AttributeInfo(
        name="status_atual",
        description="Status atual da súmula (ex.: 'VIGENTE', 'REVOGADA', 'ALTERADA', etc.).",
        type="string",
    ),
    AttributeInfo(
        name="data_status",
        description="Data do último status no formato DD/MM/AA ou DD/MM/AAAA (ex.: '07/04/2014').",
        type="string",
    ),
    AttributeInfo(
        name="pdf_name",
        description="Nome do arquivo PDF de origem (ex.: 'Sumula_70.pdf').",
        type="string",
    ),
    AttributeInfo(
        name="chunk_type",
        description="Tipo do chunk: 'conteudo_principal', 'referencias_normativas' ou 'precedentes'.",
        type="string",
    ),
    AttributeInfo(
        name="chunk_index",
        description="Índice do chunk no documento.",
        type="integer",
    ),
]
document_content_description = (
    "Trechos (chunks) de súmulas do TCEMG. Cada chunk possui tipo "
    "('conteudo_principal', 'referencias_normativas', 'precedentes')."
)

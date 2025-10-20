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
        description=("Data textual no formato 'DD/MM/AA' (string). Ex.: '07/04/14'.\n"),
        type="string",
    ),
    AttributeInfo(
        name="data_status_ano",
        description=(
            "Ano da publicação no formato 'AAAA' (integer). Ex.: '2014'.\n"
            "- Você PODE usar operadores de comparação (lt, gt, lte, gte) e igualdade (eq).\n"
            "- Para anos (ex.: 'antes de 2010'), interprete como comparações sobre datas, mesmo que o campo seja string.\n"
            "- Se o usuário disser 'antes de AAAA', use 'lt' e considere o começo do ano AAAA como limite.\n"
            "- Se o usuário disser 'depois de AAAA', use 'gt' e considere o fim do ano AAAA como limite.\n"
        ),
        type="integer",
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
document_content_description = """
    Coleção de trechos (chunks) de súmulas do Tribunal de Contas de Minas Gerais, 
    cada uma com metadados como número (num_sumula), status (status_atual), 
    data textual (data_status, formato 'DD/MM/AA'), nome do arquivo (pdf_name) e tipo de trecho (chunk_type).\n\n
"""

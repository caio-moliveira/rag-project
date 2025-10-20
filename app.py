import streamlit as st

from app.graph.rag_graph import run_streaming_rag

# Configuração da Página e Título
st.set_page_config(
    page_title="Jornada de Dados",
)
st.title("Assistente do Jornada de Dados (RAG com Self-Query)")
st.write(
    "Faça uma pergunta em linguagem natural sobre as súmulas. O sistema irá inferir filtros e realizar a busca semântica."
)

# Gerenciamento do Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura da Pergunta e Execução do Fluxo
if prompt := st.chat_input("Ex: Quais os precedentes da súmula 70 vigente?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Inicia a UI de resposta do assistente
    with st.chat_message("assistant"):
        # Placeholders que serão preenchidos em tempo real
        details_expander = st.expander("🔎 **Detalhes da Busca (Self-Query)**")
        query_placeholder = details_expander.empty()
        filter_placeholder = details_expander.empty()
        answer_placeholder = st.empty()

        full_answer = ""

        # Chama a função do backend e processa os eventos
        # Esta é a única interação entre o frontend e o backend!
        for event in run_streaming_rag(prompt):
            if event["type"] == "details":
                data = event["data"]
                query_placeholder.markdown(f"**Busca Semântica:** `{data['query']}`")
                filter_placeholder.markdown(
                    f"**Filtro de Metadados:** `{data['filter']}`"
                )

            elif event["type"] == "token":
                token = event["data"]
                full_answer += token
                answer_placeholder.markdown(full_answer + "▌")  # O ▌ simula um cursor

            elif event["type"] == "sources":
                answer_placeholder.markdown(full_answer)  # Resposta final sem o cursor
                sources = event["data"]
                if sources:
                    with st.expander("📚 **Fontes Utilizadas**"):
                        for source in sources:
                            st.markdown(
                                f"- **Arquivo:** `{source['pdf_name']}`\n"
                                f"- **Súmula:** `{source['num_sumula']}`\n"
                                f"- **Tipo:** `{source['chunk_type']}`"
                            )

    # Adiciona a resposta completa ao histórico de chat
    st.session_state.messages.append({"role": "assistant", "content": full_answer})

import streamlit as st
from roteador import responder_roteado
from indexar import colecao, indexar

# Máquina nova (deploy) = banco vazio. Indexa uma vez ao subir.
if colecao.count() == 0:
    indexar()

# Configuração da página
st.set_page_config(page_title="Assistente de Banda", page_icon="🎸")

st.title("🎸 Assistente de Produção de Banda")
st.caption("Pergunte sobre repertório, equipamentos e montagem de setlist.")

# Caixa onde o usuário digita a pergunta
pergunta = st.text_input(
    "O que você precisa?",
    placeholder="Ex: monta um set pra público sertanejo",
)

# Botão
if st.button("Perguntar"):
    if pergunta:
        with st.spinner("Consultando a base..."):
            resposta = responder_roteado(pergunta)
        st.markdown(resposta)
    else:
        st.warning("Digita uma pergunta primeiro 🙂")
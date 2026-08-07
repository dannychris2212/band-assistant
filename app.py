import streamlit as st
from responder import responder

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
            resposta = responder(pergunta)
        st.markdown(resposta)
    else:
        st.warning("Digita uma pergunta primeiro 🙂")
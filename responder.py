import os
from dotenv import load_dotenv
from anthropic import Anthropic
from buscar import buscar

# Carrega a chave do .env (nunca fica escrita no código)
load_dotenv()
cliente = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def responder(pergunta):
    """Fluxo completo do RAG: busca os chunks e pede ao Claude pra responder."""
    # 1. Recupera os chunks mais relevantes
    resultado = buscar(pergunta, n=5)
    chunks = resultado["documents"][0]

    # 2. Monta o contexto juntando os chunks recuperados
    contexto = "\n\n".join(chunks)

    # 3. Monta a instrução pro Claude
    prompt = f"""Você é o assistente de produção técnica de uma banda.
Responda a pergunta usando SOMENTE as informações do contexto abaixo.
Se a informação não estiver no contexto, diga que não tem esse dado registrado.

CONTEXTO:
{contexto}

PERGUNTA: {pergunta}"""

    # 4. Chama o Claude
    resposta = cliente.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    return resposta.content[0].text


if __name__ == "__main__":
    pergunta = "monta um set curto pra um público que curte sertanejo e valley"
    print(f"PERGUNTA: {pergunta}\n")
    print(responder(pergunta))
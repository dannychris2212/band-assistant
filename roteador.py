import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
cliente = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def classificar(pergunta):
    """Classifica a pergunta como CONSULTA (factual) ou ANALITICA (julgamento)."""
    prompt = f"""Classifique a pergunta do usuário em UMA das duas categorias:

CONSULTA: pergunta factual sobre o que existe na base. Ex: "qual amplificador eu tenho?", "tem música da Pitty?", "quais guitarras tenho?", "temos violão de nylon?". A resposta é achar itens exatos que existem ou não.

ANALITICA: pergunta que pede julgamento, recomendação ou montagem. Ex: "o que serve pra público sertanejo?", "monta um set pra abrir o show", "qual música combina com clima romântico?".

Responda utilizando SOMENTE uma única palavra: CONSULTA ou ANALITICA.
Não explique. Não adicione pontuação. Apenas a palavra.

PERGUNTA: {pergunta}"""

    resposta = cliente.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    return resposta.content[0].text.strip().upper()

from ingest import carregar_chunks
from responder import responder as responder_analitico

# Carrega os chunks uma vez pra busca exata
_chunks = carregar_chunks()


import re

def _limpar(texto):
    """Deixa o texto cru: minúsculo e sem pontuação, só palavras e espaços."""
    return re.sub(r"[^\w\s]", " ", texto.lower())


def busca_exata(pergunta):
    """Busca literal em texto limpo dos dois lados. Vazio se nada bate."""
    tokens = [t for t in _limpar(pergunta).split() if len(t) > 3]
    encontrados = []
    for c in _chunks:
        texto_low = _limpar(c["texto"])
        if any(token in texto_low for token in tokens):
            encontrados.append(c["texto"])
    return encontrados


def responder_consulta(pergunta):
    """Responde uma consulta factual usando só o que a busca exata achou."""
    achados = busca_exata(pergunta)
    if not achados:
        return "Não tenho esse item registrado na base."

    contexto = "\n".join(achados)
    prompt = f"""Responda a pergunta usando SOMENTE o contexto abaixo.
Liste os itens que existem. Se não houver nada relevante, diga que não tem registro.

CONTEXTO:
{contexto}

PERGUNTA: {pergunta}"""

    resposta = cliente.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return resposta.content[0].text


def responder_roteado(pergunta):
    """Classifica e roteia pro caminho certo."""
    tipo = classificar(pergunta)
    if tipo == "CONSULTA":
        return responder_consulta(pergunta)
    else:
        return responder_analitico(pergunta)

if __name__ == "__main__":
    for p in ["qual amplificador eu tenho?", "tem música da Pitty?", "o que serve pra público sertanejo?"]:
        print(f"=== {p} ===")
        print(responder_roteado(p))
        print()
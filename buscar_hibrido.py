import chromadb
from rank_bm25 import BM25Okapi
from ingest import carregar_chunks

# --- Preparação: carrega os chunks uma vez ---
chunks = carregar_chunks()
textos = [c["texto"] for c in chunks]

# BM25 (palavra-chave)
corpus_tokenizado = [t.lower().split() for t in textos]
bm25 = BM25Okapi(corpus_tokenizado)

# ChromaDB (semântica) — mesmo banco de sempre
cliente = chromadb.PersistentClient(path="./chroma_db")
colecao = cliente.get_or_create_collection(name="banda")


def ranking_semantico(pergunta, n=20):
    """Retorna os textos ordenados por similaridade semântica."""
    resultado = colecao.query(query_texts=[pergunta], n_results=n)
    return resultado["documents"][0]


def ranking_palavra_chave(pergunta, n=20):
    """Retorna os textos ordenados por BM25."""
    tokens = pergunta.lower().split()
    scores = bm25.get_scores(tokens)
    melhores = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n]
    return [textos[i] for i in melhores]


def buscar_hibrido(pergunta, n=5, k=60):
    """Funde os dois rankings usando RRF (Reciprocal Rank Fusion)."""
    sem = ranking_semantico(pergunta)
    kw = ranking_palavra_chave(pergunta)

    # RRF: cada documento ganha pontos por sua POSIÇÃO em cada ranking
    pontos = {}
    for ranking in [sem, kw]:
        for posicao, texto in enumerate(ranking):
            pontos[texto] = pontos.get(texto, 0) + 1 / (k + posicao + 1)

    # Ordena pelos pontos totais e pega os n melhores
    ordenados = sorted(pontos.items(), key=lambda x: x[1], reverse=True)
    return [texto for texto, _ in ordenados[:n]]


if __name__ == "__main__":
    for pergunta in ["tem música da Pitty?", "o que serve pra público sertanejo?"]:
        print(f"=== Pergunta: {pergunta} ===\n")
        for i, texto in enumerate(buscar_hibrido(pergunta)):
            print(f"--- {i+1} ---")
            print(texto[:120])
            print()
        print()
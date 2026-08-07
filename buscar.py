import chromadb
from ingest import carregar_chunks

# Cria o banco de vetores (guarda em disco, na pasta ./chroma_db)
cliente = chromadb.PersistentClient(path="./chroma_db")

# Uma "coleção" é como uma tabela dentro do banco
colecao = cliente.get_or_create_collection(name="banda")


def indexar():
    """Pega os chunks e guarda no ChromaDB (ele calcula os embeddings sozinho)."""
    chunks = carregar_chunks()

    colecao.add(
        documents=[c["texto"] for c in chunks],
        metadatas=[{"fonte": c["fonte"]} for c in chunks],
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    print(f"Indexados {len(chunks)} chunks no banco.\n")


def buscar(pergunta, n=3):
    """Busca os n chunks mais próximos em significado da pergunta."""
    resultado = colecao.query(
        query_texts=[pergunta],
        n_results=n,
    )
    return resultado


if __name__ == "__main__":
    # Indexa uma vez
    indexar()

    # Testa uma busca
    pergunta = "o que serve pra público sertanejo?"
    print(f"Pergunta: {pergunta}\n")

    resultado = buscar(pergunta)
    for i, doc in enumerate(resultado["documents"][0]):
        print(f"--- Resultado {i+1} ---")
        print(doc[:250])
        print()
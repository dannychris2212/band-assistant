import chromadb
from ingest import carregar_chunks

# Conecta no banco de vetores (guarda em disco, na pasta ./chroma_db)
cliente = chromadb.PersistentClient(path="./chroma_db")
colecao = cliente.get_or_create_collection(name="banda")


def indexar():
    """Lê os chunks e guarda no ChromaDB (ele calcula os embeddings sozinho)."""
    chunks = carregar_chunks()

    colecao.add(
        documents=[c["texto"] for c in chunks],
        metadatas=[{"fonte": c["fonte"]} for c in chunks],
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    print(f"Indexados {len(chunks)} chunks no banco.")


if __name__ == "__main__":
    indexar()
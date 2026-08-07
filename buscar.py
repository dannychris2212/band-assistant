import chromadb

# Conecta no MESMO banco que o indexar.py encheu
cliente = chromadb.PersistentClient(path="./chroma_db")
colecao = cliente.get_or_create_collection(name="banda")


def buscar(pergunta, n=3):
    """Busca os n chunks mais próximos em significado da pergunta."""
    resultado = colecao.query(
        query_texts=[pergunta],
        n_results=n,
    )
    return resultado


if __name__ == "__main__":
    pergunta = "o que serve pra público sertanejo?"
    print(f"Pergunta: {pergunta}\n")

    resultado = buscar(pergunta)
    for i, doc in enumerate(resultado["documents"][0]):
        print(f"--- Resultado {i+1} ---")
        print(doc[:250])
        print()
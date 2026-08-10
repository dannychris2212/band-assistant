from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge_base")

# Arquivos que são LISTAS (chunk por linha, não por ##)
ARQUIVOS_LISTA = {"repertorio_completo.md"}


def chunkar_por_bloco(texto):
    """Quebra por '## ' — pra documentos ricos (equipamentos, núcleo)."""
    chunks = []
    for bloco in texto.split("\n## "):
        bloco = bloco.strip()
        if not bloco or bloco.startswith("#") or bloco.startswith(">"):
            continue
        chunks.append("## " + bloco)
    return chunks


def chunkar_por_linha(texto):
    """Quebra por linha — pra listas (cada música vira um chunk)."""
    chunks = []
    for linha in texto.split("\n"):
        linha = linha.strip()
        # Só linhas que são item de música (começam com '-')
        if linha.startswith("- "):
            chunks.append(linha)
    return chunks


def carregar_chunks():
    """Lê todos os .md e chunka cada um pela estratégia certa."""
    chunks = []

    for arquivo in KNOWLEDGE_DIR.glob("*.md"):
        texto = arquivo.read_text(encoding="utf-8")

        # Escolhe a estratégia de chunking conforme o arquivo
        if arquivo.name in ARQUIVOS_LISTA:
            textos = chunkar_por_linha(texto)
        else:
            textos = chunkar_por_bloco(texto)

        for t in textos:
            chunks.append({"fonte": arquivo.name, "texto": t})

    return chunks


if __name__ == "__main__":
    chunks = carregar_chunks()
    print(f"Total de chunks: {len(chunks)}\n")
    # Mostra os 3 primeiros de cada arquivo pra conferir
    vistos = {}
    for c in chunks:
        fonte = c["fonte"]
        if vistos.get(fonte, 0) < 2:
            print(f"[{fonte}] {c['texto'][:80]}")
            vistos[fonte] = vistos.get(fonte, 0) + 1
from pathlib import Path

# Onde estão os arquivos de conhecimento
KNOWLEDGE_DIR = Path("knowledge_base")


def carregar_chunks():
    """Lê todos os .md e quebra cada um em blocos (chunks) por '## '."""
    chunks = []

    for arquivo in KNOWLEDGE_DIR.glob("*.md"):
        texto = arquivo.read_text(encoding="utf-8")

        # Cada bloco começa com "## " — foi assim que estruturamos a base
        blocos = texto.split("\n## ")

        for bloco in blocos:
            bloco = bloco.strip()
            if not bloco or bloco.startswith("#") or bloco.startswith(">"):
                continue  # pula cabeçalho do arquivo e notas

            chunks.append({
                "fonte": arquivo.name,
                "texto": "## " + bloco,
            })

    return chunks


# Teste: roda e mostra os chunks
if __name__ == "__main__":
    chunks = carregar_chunks()
    print(f"Total de chunks: {len(chunks)}\n")
    for i, c in enumerate(chunks[:3]):  # mostra os 3 primeiros
        print(f"--- Chunk {i+1} (de {c['fonte']}) ---")
        print(c["texto"][:200])  # primeiros 200 caracteres
        print()
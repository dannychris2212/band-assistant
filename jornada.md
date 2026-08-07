## Dia 1
- Criei o repo com README, .gitignore (Python) e licença MIT.
- Aprendi o ciclo: add (staging) → commit (salva local) → push (publica).
- Clique da sessão: commit e push são coisas diferentes. Commit é salvar
  na minha máquina, push é mandar pro GitHub. Posso commitar várias vezes
  e dar push só quando tá pronto — isso é o "altera, testa, launch" que eu
  já queria fazer no Braavos e não sabia como.
- origin = repo no GitHub, main = branch principal.
## Dia 1 (continuação)
- Documentei equipamentos e repertório (completo + núcleo detalhado).
- Descoberta: o valor da minha base não tá nas specs, tá no conhecimento
  condicional — "O Sol funciona pra sertanejo mas não pra rock", phantom
  power, o que funciona com cada público. Isso nenhum modelo genérico sabe.
- Aprendi BRANCH: checkout -b cria e entra, checkout troca, merge junta.
  É o "altera→testa→launch" isolado que eu queria pro Braavos.
- Não decorei os comandos e tá tudo bem — peguei a lógica, o resto vem na prática.
## Dia 2
- Montei o ambiente: venv, instalei chromadb e anthropic, requirements.txt.
- Escrevi ingest.py (lê os .md e quebra em chunks) e buscar.py (embeddings + busca).
- MARCO: busca semântica funcionando. Perguntei "público sertanejo" e o
  sistema trouxe O Sol no topo SEM a palavra bater — achou por significado.
  Foi exatamente a resposta pra pergunta que eu fiz: é isso que os LLMs
  mudaram, a máquina entende sentido, não só palavra igual.
- Aprendi: metade do RAG é a preparação dos dados. A estrutura em blocos ##
  que fiz no dia 1 é o que fez o chunking funcionar fácil.
- Ficou pra próxima: entender melhor indexar vs buscar, separar em dois
  arquivos, e plugar o Claude pra gerar resposta.
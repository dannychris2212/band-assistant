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
  ## Dia 2 (parte 2)
- Refatorei: separei indexar.py (roda 1x) de buscar.py (roda sempre). Entendi
  sozinha que só reindexo quando os dados mudam (analogia da biblioteca).
- Pluguei o Claude (responder.py). O RAG está COMPLETO ponta a ponta.
- Guardei a chave no .env, confirmei que o .gitignore protege (invisível no git).
- MOMENTO: pedi um set pra público sertanejo e o assistente montou E explicou
  o que deixou de fora (tirou Aiaiai com justificativa). O "SOMENTE" no prompt
  é o que impede ele de inventar música que eu não toco.
  ## Dia 2 (parte 4)
- Testei "tem música da Pitty?" na interface e ele disse que não tinha — mas
  EU TENHO Pitty no repertório. Não aceitei a resposta.
- Debuguei: busquei "música da Pitty" isolado e o chunk dela não aparece nos
  resultados. Então o Claude nunca recebeu a Pitty — o problema é a RECUPERAÇÃO,
  não o prompt.
- Causa raiz: os chunks rasos da lista completa têm pouco texto, então perdem
  pros chunks ricos na busca por significado. Busca semântica é boa pra pergunta
  conceitual ("sertanejo") e fraca pra fato pontual ("tem Pitty?").
- Solução escolhida: busca híbrida (semântica + palavra-chave). Próxima sessão.
## Dia 3
- Construí a busca híbrida: BM25 (palavra-chave) + semântica, fundidos com RRF.
- Entendi por que RRF soma posição e não score: as escalas são diferentes, e
  somar bruto faz uma busca atropelar a outra. Posição põe as duas na mesma régua.
- A híbrida não resolveu a Pitty ainda — mas o debug revelou que a raiz é mais
  funda: o problema é o CHUNKING. Na lista completa a Pitty é um bullet, não tem
  ## próprio, então virou parte de um chunk gigante de 40 músicas.
- Descobri camada por camada: consertei a busca e apareceu o problema do chunking.
  É assim que debug funciona de verdade.
  ## Dia 3 (parte 2)
- Consertei o chunking: o ingest agora usa estratégia diferente por tipo de
  arquivo (lista quebra por linha, resto por ##). 45 → 127 chunks.
- Mas apareceu coisa nova: busca de "sertanejo" trouxe a Pitty, que não tem
  nada a ver. Percebi que o problema real é mais fundo: tem pergunta de
  CONSULTA ("tenho tal amp?") e pergunta de ANÁLISE ("o que serve pra tal
  público?"), e são coisas diferentes. Consulta tem que ser busca exata, não
  similaridade. Estávamos usando a ferramenta errada.
- Solução pra próxima: roteador que classifica a pergunta (via LLM) e manda
  pra busca exata ou pra semântica conforme o tipo.
  ## Dia 4
- Construí o roteador: o Claude classifica a pergunta em CONSULTA ou ANALITICA
  antes de buscar, e manda pro caminho certo (busca exata ou semântica/híbrida).
- Classificador acertou 6/6. Fechei o caso da Pitty de vez: "tem Pitty?" agora
  acha ela pela busca exata, sem trazer lixo.
- Debuguei dois detalhes de texto: o "?" grudado em "pitty?" quebrava o match,
  e precisei limpar a pontuação dos dois lados (pergunta e chunk).
- Lição: o conserto certo não era refinar a busca — era reconhecer que consulta
  e análise pedem ferramentas diferentes. Rotear resolveu na raiz.
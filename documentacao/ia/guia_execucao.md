# GS de IA — guia de execução

- Lucas Lino Marques da Silva — RM 572863
- Gabriel Martins Cordeiro Rodrigues — RM 570497
- Gustavo Martins da Silva — RM 570584

FIAP — Ciência da Computação, 1CCPX — Citizen Assist AI, GS 2026.2.

## Instalação

Na pasta do repositório:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Versões instaladas: Python 3.14.3, LangChain 1.5.0, langchain-groq 1.1.3 e python-dotenv 1.2.4. PCP continua usando somente a biblioteca padrão; suas regras e seus dados não participam das respostas de IA.

## Chave e modelos

Crie uma chave em [Groq API Keys](https://console.groq.com/keys). Em uma instalação nova, copie `.env.example` para `.env` sem sobrescrever uma configuração existente. Preencha somente no computador:

```text
GROQ_API_KEY=SUA_CHAVE_LOCAL
IA_MODELO=openai/gpt-oss-20b
IA_MODELO_JUIZ=openai/gpt-oss-120b
```

Não publique o `.env` nem cole a chave em relatórios, capturas ou chats. O Git ignora o arquivo. As variáveis do ambiente têm preferência sobre ele. A API usa os modelos hospedados pela Groq; não é necessária uma chave da API da OpenAI.

O serviço tem limites por conta e modelo. Uma mensagem de limite de uso é falha de infraestrutura, não erro de conteúdo. Aguarde e retome a avaliação preservada. Confira no painel da conta os limites aplicáveis antes de executar muitas rodadas.

## Usar o assistente

```bash
python main.py --dados data/demonstracao_pcp
```

Escolha a opção **2 — Documentação pessoal (IA)**. Há perguntas livres, menu de sete assuntos e exemplos. Use `0` para voltar em cada nível. Toda resposta informa que Aurora é fictícia e que o programa não representa um canal oficial.

Exemplos: `Quanto custa a segunda via do RG?`, `Que documentos preciso para a segunda via do RG?`, `Quanto demora a carteira de trabalho digital?` e `Preciso de intérprete de Libras. Como faço?`.

Apenas as sete fichas são fonte. O programa não consulta cadastros, agenda atendimento, abre documentos nem pede identificação. As fichas não fornecem uma URL real do portal de Aurora; o assistente não deve inventá-la. Perguntas de IA não são inseridas no histórico ou nos indicadores de PCP.

O filtro evita enviar padrões comuns de dados pessoais à API, mas não reconhece toda identificação possível. Não envie nomes, documentos, contato, endereço, dados sensíveis ou histórias identificáveis. Mensagens liberadas pelo filtro são processadas pela Groq; o programa não garante políticas de retenção de terceiros.

## Avaliação automática

A base em `golden_dataset.json` mantém as 26 mensagens e os conteúdos esperados do enunciado. O número de CPF fictício obrigatório do caso 22 existe apenas no fixture; o agente recebe o caso exato, bloqueia-o localmente e os relatórios/juiz recebem a mensagem sem o identificador.

```bash
python -B -m modulos.documentos_ia.avaliador --versao v1 --saida evidencias/ia/antes.json --pausa 40
```

Se uma saída já existir, o comando não a sobrescreve. Para continuar casos pendentes, use o mesmo comando com `--retomar`. O programa valida os hashes de prompt, código, fichas e dataset e os modelos configurados. Uma versão alterada precisa de uma nova rodada/arquivo. `--limite 1` permite testar conexão, mas uma rodada parcial não produz percentual final das 26 mensagens.

A melhoria v2 separou texto e códigos de fichas. A versão final v3 reforça a completude e acrescenta, em perguntas de custo, o trecho literal do campo Custo da ficha escolhida. O programa não inventa valores. A opção 2 do menu usa v3. A segunda rodada usa:

```bash
python -B -m modulos.documentos_ia.avaliador --versao v3 --saida evidencias/ia/depois.json --pausa 25
```

Para repetir uma rodada completa, escolha outro arquivo de saída; `--retomar` serve apenas para continuar uma execução com a mesma configuração. A versão inicial está preservada em `evidencias/ia/codigo_v1.zip`, sem chave ou arquivo .env. A rodada estruturada intermediária foi preservada em `intermediaria_v2.json` e seu código em `codigo_v2.zip`. O teste parcial anterior à complementação de custo está identificado como `exploratoria_v3_parcial.json`; ele não conta como uma rodada completa. Para gerar a comparação sem chamar a API novamente:

```bash
python -B -m modulos.documentos_ia.relatorio
```

O comando exige duas rodadas completas com as mesmas fichas, dataset, modelos e régua; produz `comparacao.json` e `comparacao.csv`. Não modifica os resultados originais.

Não confundir valores do LLM as a Judge com resultados de pessoas.

## Verificações técnicas sem chamadas à API

```bash
python -B -m unittest discover -s testes -v
```

Os testes de IA substituem as chamadas externas por modelos/controladores de teste. Exercitam privacidade, referências, menus, framework e avaliação sem consumir a chave. As evidências reais da API ficam separadas em `evidencias/ia/`. O notebook `notebooks/avaliacao_ia.ipynb` lê esses JSONs e apresenta tabelas sem novas chamadas à API.

Os testes humanos exigidos ainda precisam de cinco pessoas externas, três tarefas por pessoa e questionário de cinco itens. Veja [plano de usuários](testes_usuarios.md). Os resultados de PCP não substituem essa avaliação.

# RECOMEÇO — Citizen Assist AI

- **Lucas Lino Marques da Silva — RM 572863**
- **Gabriel Martins Cordeiro Rodrigues — RM 570497**
- **Gustavo Martins da Silva — RM 570584**

FIAP · Ciência da Computação · 1CCPX · Global Solution 2026.2.

Criamos o RECOMEÇO para reunir orientações sobre desastres em um programa de terminal. O projeto junta os trabalhos de PCP, IA e SERS, com uma parte para cada matéria. Ele foi feito para a GS e não substitui os canais oficiais ou de emergência. ODS relacionados: **7** — energia limpa e acessível; **10** — redução das desigualdades; **11** — cidades e comunidades sustentáveis; **13** — ação contra a mudança global do clima.

## As três matérias

| Disciplina | Comece por aqui | Código e opção no programa | Evidências |
|---|---|---|---|
| Pensamento Computacional e Automação com Python — **PCP** | **[Documentação de PCP](documentacao/pcp/README.md)** | `main.py`, `orientacao.py`, `base_conhecimento.py`, `assistente.py` e `data/`; opções **1 e 4** | [Avaliação e testes de PCP](evidencias/pcp/README.md) |
| Prompt and Artificial Intelligence — **IA** | **[Documentação de IA](documentacao/ia/README.md)** | [Agente e juiz](modulos/documentos_ia/); opção **2** | [Avaliação automática e humana](evidencias/ia/README.md) e [notebook executado](notebooks/avaliacao_ia.ipynb) |
| Soluções em Energias Renováveis e Sustentáveis — **SERS** | **[Documentação de SERS](documentacao/sers/README.md)** | [Cálculo de energia](modulos/energia/); opção **3** | [Avaliação e testes de SERS](evidencias/sers/README.md) |

**[Entregas e pendências por disciplina](entregas/README.md)** · [Documentação compartilhada](documentacao/README.md) · [Checklist completo](documentacao/checklist.md).

## Executar o projeto

Python testado: **3.14.3**. PCP e SERS usam somente a biblioteca padrão. Na pasta do repositório:

```bash
python3 main.py
```

Para experimentar sem acrescentar atendimentos aos dados de PCP já registrados:

```bash
python3 main.py --dados data/demonstracao_pcp
```

O menu apresenta orientações sobre desastres, documentação pessoal com IA, energia/sustentabilidade e indicadores. Use `0` para voltar ou encerrar. Não informe dados pessoais.

**Para usar a opção de IA**, instale as dependências e configure a chave Groq no `.env` local:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Siga o [guia de configuração de IA](documentacao/ia/guia_execucao.md). O `.env` é ignorado pelo Git; `.env.example` é somente um modelo sem chave. PCP e SERS continuam acessíveis sem configurar a API.

## O que cada disciplina entrega

**PCP:** três classes por composição, base JSON com 34 orientações em três categorias, busca por regras, navegação, histórico, indicadores e CSV. Fontes reais e limitações em [fontes de PCP](documentacao/pcp/fontes.md). A busca normaliza acentos/pontuação, soma **+3 por expressão-chave completa** e **+1 por palavra distinta da pergunta, com quatro ou mais letras, presente no título**. Confiança ALTA a partir de 6; MÉDIA de 3 a 5; abaixo de 3, oferece reformulação/categorias. Retorna tuplas ordenadas e apresenta até duas alternativas. Detalhes em [funcionamento de PCP](documentacao/pcp/funcionamento.md).

**IA:** um agente LangChain/Groq responde exclusivamente pelas sete fichas **fictícias** de Aurora. As fichas não são usadas como informação real em PCP. Inclui as 26 mensagens do golden dataset, juiz LLM, comparação antes/depois, diagrama e relatório de usuários. A versão atual é v4; as medições automáticas e humanas publicadas pertencem à v3.

**SERS:** compara a mesma iluminação de abrigo pela rede e por solar isolado com bateria, no mesmo período. Mostra consumo, custo de aquisição/operação, autonomia, sequência de dias, fontes, hipóteses e impactos ambientais qualitativos. O caso público de São Paulo é identificado; a orientação permanece geral para o Brasil. A versão atual é v3, com ajuste de HSP motivado pela avaliação de uma participante.

## Resultados das avaliações

Organizamos os resultados abaixo por matéria. Os relatórios têm os detalhes dos testes e os arquivos usados nos cálculos.

| Disciplina e rodada | Resultados | Observações |
|---|---|---|
| **PCP — 14/11** | 3 pessoas de fora do grupo, 10 atendimentos; 80% de orientações encontradas/selecionadas, 70% indicaram que ajudou, tempo médio 43,24 s, facilidade 3,0/5 | Facilidade por sessão; não há distribuição dos atendimentos por pessoa nem nova medida humana após a correção. |
| **IA — 15/11** | Juiz: 20/26 → 25/26, de 76,92% para 96,15%; 5 pessoas de fora do grupo, 15 tarefas, tempo humano médio 23,04 s e facilidade 4,04/5 | Juiz sujeito a erros; v4 recebeu correções posteriores sem novo benchmark ou rodada humana. |
| **SERS — 17/11** | Uma pessoa de fora do grupo testou cinco situações, achou a ideia útil e confundiu HSP com o tempo de sol na casa | Lucas anotou os comentários. Não registramos tempo ou nota nessa rodada, e a participante ainda não testou a v3. |

Em **PCP**, as dúvidas sem solução foram enchente na rua do serviço, tempestade forte e número da Enel. A revisão acrescentou expressões de busca, conteúdos de tempestade/falta de energia/contatos e melhorou sugestões e encaminhamento urgente. Conservou os pesos +3/+1 e os registros da avaliação. Veja o [relatório de PCP](documentacao/pcp/avaliacao_usuarios.md).

Em **IA**, as melhorias do agente/juiz e suas ressalvas estão na [avaliação automática](documentacao/ia/avaliacao.md) e no [relatório humano](documentacao/ia/usuarios_2026-11-15.md). Em **SERS**, a observação de HSP levou a uma explicação concreta e confirmação de hipóteses altas; veja o [registro S01](evidencias/sers/usuarios/rodada_2026-11-17/README.md).

## Organização das pastas

```text
main.py + orientacao.py + base_conhecimento.py + assistente.py
    PCP na estrutura solicitada pelo enunciado

data/                       base e registros exigidos por PCP
modulos/documentos_ia/       agente, juiz, fichas fictícias e prompts de IA
modulos/energia/             cálculo, dados e referências de SERS
documentacao/pcp/            guia, funcionamento, fontes e avaliação de PCP
documentacao/ia/             arquitetura, avaliação e relatório de IA
documentacao/sers/           análise, execução e avaliação de SERS
evidencias/pcp/              usuários, testes técnicos e histórico de PCP
evidencias/ia/               antes/depois, usuários e histórico de IA
evidencias/sers/             versões técnicas e usuários de SERS
notebooks/                  notebook executado de IA
testes/                     testes automatizados e análises reproduzíveis
entregas/                   arquivos e instruções para o Portal
```

Os arquivos que mudaram de pasta estão no [mapa da organização](documentacao/organizacao.md). Os registros antigos continuam com seus resultados originais.

## Testes e limites

Com o ambiente de dependências ativado:

```bash
python -B -m unittest discover -s testes -v
python -B testes/analisar_validacao_pcp.py
python -B testes/analisar_usuarios_ia.py
python -B testes/analisar_sers.py
```

Os testes usam arquivos temporários e modelos de IA simulados, sem novas chamadas pagas. O projeto passou em **171 testes automatizados**, sendo 36 de SERS. Também [conferimos os arquivos e links](evidencias/organizacao/README.md) depois de organizar as pastas.

A busca de PCP não compreende toda linguagem natural; a confiança mede coincidência textual. IA não consulta cadastros ou informações além das fichas fictícias e depende da API para perguntas encaminhadas ao modelo. SERS usa aproximações e orçamento estimado, sem certificar instalação, fornecer previsão meteorológica ou garantir economia/autonomia. Consulte os guias de cada disciplina para os demais limites.

## Vídeo e entrega

**Vídeo técnico PCP + SERS: link pendente de gravação/publicação.** Vamos apresentar PCP e SERS em um único vídeo técnico de **5 a 8 minutos**. Todos os integrantes vão explicar uma parte do código e demonstrar as funções de PCP e SERS. [Planejamento do vídeo integrado](documentacao/roteiro_video_tecnico.md).

Os [TXT de PCP e SERS](entregas/README.md) deverão receber o mesmo link desse vídeo. A contribuição de IA tem seu conjunto de entregáveis identificado separadamente. Vamos conferir as orientações gerais da GS antes de preparar o pitch, pois ele não aparece nesses três enunciados.

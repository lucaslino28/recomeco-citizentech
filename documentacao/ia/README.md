# IA — documentação

Lucas Lino Marques da Silva — RM 572863; Gabriel Martins Cordeiro Rodrigues — RM 570497; Gustavo Martins da Silva — RM 570584.

**Prompt and Artificial Intelligence.** Usamos LangChain e Groq para responder perguntas com base nas sete fichas de Aurora fornecidas pelo professor. A opção 2 abre essa parte do programa. Aurora é fictícia; essas regras não valem como orientação real sobre documentos brasileiros.

## Arquivos da disciplina

| Etapa | Material |
|---|---|
| 1. Executar | [Guia de configuração e execução](guia_execucao.md); opção 2 de `main.py`. Chave Groq somente no `.env` local. |
| 2. Conferir a implementação | [Agente](../../modulos/documentos_ia/agente.py), [juiz](../../modulos/documentos_ia/avaliador.py), [fichas](../../modulos/documentos_ia/fichas/) e [golden dataset](../../modulos/documentos_ia/golden_dataset.json). |
| 3. Entender a arquitetura | [Decisões e limitações](decisoes.md); diagrama [PNG](arquitetura.png) / [SVG](arquitetura.svg), incluído porque o protótipo é um script. |
| 4. Avaliar antes/depois | [Notebook executado](../../notebooks/avaliacao_ia.ipynb), [análise do juiz](avaliacao.md) e [evidências automáticas](../../evidencias/ia/README.md). |
| 5. Conferir os três indicadores | [Relatório de usuários](usuarios_2026-11-15.md): acerto do juiz, tempo humano e facilidade, com limites separados. [Arquivos da coleta](../../evidencias/ia/usuarios/rodada_2026-11-15/README.md). |
| 6. Conferir revisão e correções | [Amostra confirmada](revisao_amostra.md), [fechamento v4](fechamento.md) e [conferência dos requisitos](requisitos_ia.md). |
| 7. Localizar a entrega | [Mapa dos materiais de IA](../../entregas/ia.md), sem presumir TXT ou vídeo próprio não especificados no enunciado. |

## Resultados e versões

- Juiz sobre 26 mensagens: v1 com **20/26 — 76,92%**; v3 com **25/26 — 96,15%**, diferença de 19,23 pontos percentuais. As respostas e as avaliações do juiz estão nos arquivos das rodadas.
- Nos testes com usuários: **5 pessoas externas**, **15 tarefas**, tempo humano médio **23,04 s** e facilidade **4,04/5**. Esses resultados são da v3, a mesma versão da avaliação automática.
- Atendimento atual: **v4**, com correções posteriores de banco, lista documental do RG e recuperação de CPF. A v4 passou pelos testes de código, mas ainda não repetimos a avaliação com o juiz ou com usuários. Lucas conferiu seis casos da v3 com as fichas; as observações estão na revisão da amostra.

## Organização e fontes

O [plano de usuários](testes_usuarios.md) e os formulários vazios continuam disponíveis para novas coletas. [proveniencia.json](proveniencia.json) registra os hashes das sete fichas e do dataset extraído dos documentos fornecidos. Mantivemos as fichas como fonte do agente e tratamos tentativas de mudar suas instruções como entradas do usuário.

Os resultados principais ficam em `evidencias/ia/`, a coleta em `usuarios/` e as versões antigas em `historico/`, conforme o [índice de evidências](../../evidencias/ia/README.md). O notebook continua com os resultados das rodadas já realizadas. A chave fica no `.env` local, fora do Git.

[Voltar ao projeto](../../README.md) · [Entregas](../../entregas/README.md) · [Documentação das três disciplinas](../README.md).

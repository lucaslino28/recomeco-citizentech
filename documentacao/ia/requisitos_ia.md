# Prompt & IA — conferência dos requisitos

- Lucas Lino Marques da Silva — RM 572863
- Gabriel Martins Cordeiro Rodrigues — RM 570497
- Gustavo Martins da Silva — RM 570584

Usamos esta lista para conferir os itens do enunciado depois dos testes de 15/11/2026. Os links indicam onde está cada parte do trabalho.

| Requisito | Situação verificada | Evidência |
|---|---|---|
| Integrantes no início do trabalho | Atendido nos documentos, README e notebook | Cabeçalhos e RMs fornecidos pela equipe |
| Sete fichas de Aurora como fonte | Sete arquivos iguais byte a byte ao ZIP original | `fichas/`, `proveniencia.json` e auditoria local |
| Organização/carregamento das fichas | Carregamento completo das sete fichas, sem banco vetorial; justificativa documentada | `agente.py`, `decisoes.md` |
| Framework, agente e modelo | LangChain; um agente Groq GPT-OSS 20B; juiz GPT-OSS 120B; escolhas justificadas | Código, dependências e decisões |
| Menu e pergunta livre | Implementados; teste por terminal e conjunto de testes locais | `main.py`, `menu_documentos_ia()`, testes |
| Respostas com referência, data e limitação | Implementado; v4 corrige os casos de encaminhamento identificados, com limites documentados | Terminal da coleta, caso bancário P04/T03 |
| Fora do escopo e entradas inválidas | Recusas e entrada vazia testadas; o encaminhamento bancário da coleta v3 foi corrigido na v4 | P03/T03, P04/T03, P05/T03 e terminal |
| Privacidade | Filtros antes da API, sem histórico de perguntas de uso; limites documentados; caso 22 bloqueado no benchmark | Código, testes e JSONs; nenhuma identidade de participante adicionada |
| Golden dataset | As 26 mensagens e conteúdos esperados conferem com a tabela original | `golden_dataset.json` e auditoria local |
| Prompt injection | Casos 24 e 25 preservados e julgados; instrução de prefixo do documento tratada como conteúdo externo | Dataset, prompts e decisões |
| LLM as a Judge e régua | Implementados; três rodadas completas de 26; falhas de infraestrutura não viram acerto | `avaliador.py`, JSONs e comparação |
| Melhoria e antes/depois | V1 20/26, V3 25/26; intermediária e teste parcial preservados | `avaliacao.md`, snapshots e notebook |
| Conferência manual da amostra | Seis casos conferidos com conferência manual de Lucas; divergência do caso 20 preservada | `revisao_amostra.md` e `revisao_amostra.json` |
| Cinco pessoas externas, três tarefas | Cinco pessoas segundo as anotações de Lucas; 15 registros e 15 perguntas principais extraídas | CSV e terminal organizado; tarefas variaram |
| Tempo humano | 15 tempos informados e validados, média 23,04 s | `tarefas.csv`, `indicadores.json` |
| Questionário de cinco itens | Cinco questionários e 25 notas, média 4,04/5 | `questionario.csv`, `indicadores.json` |
| Relatório com três indicadores | Preparado, separando acerto do juiz, tempo humano e facilidade; conclusão informada é medida adicional | `usuarios_2026-11-15.md` |
| Imagem da arquitetura para script | PNG e SVG presentes | `arquitetura.png`, `arquitetura.svg` |
| Protótipo testável e notebook | Código, instruções e notebook automático executado presentes | Guia e `notebooks/avaliacao_ia.ipynb` |
| Testes técnicos | 135 testes locais aprovados na v4; sem chamadas reais à API na suíte | `fechamento/testes_v4_2026-11-15.txt`; logs de 121 e 125 preservados |
| Publicação/revisão final | Código e evidências enviados ao GitHub; referência remota e acesso HTTP conferidos | Commit de conteúdo e30872d e `fechamento/publicacao.json` |

## Fechamento da revisão

1. A conferência da amostra foi confirmada por Lucas; casos e ressalvas estão em [revisão da amostra](revisao_amostra.md).
2. A v4 aplica correções pontuais e passou em 135 testes locais. Veja [fechamento](fechamento.md). O benchmark de 96,15% e os dados humanos de 23,04 s/4,04 pertencem à v3; não foram remensurados na v4.
3. O conteúdo foi publicado em `e30872d`, com referência remota e acesso HTTP conferidos. A chave e os dados originais permanecem preservados.

A auditoria anterior em [JSON](../../evidencias/ia/usuarios/rodada_2026-11-15/verificacao_requisitos.json) retrata o estado antes da v4. A validação atual está em [validação da v4](../../evidencias/ia/fechamento/validacao_v4.json). Os registros anteriores não foram reescritos.

A parte de IA já está publicada. As pendências atuais das três matérias estão na [página de entregas](../../entregas/README.md). Se repetirmos os testes, vamos guardar os novos resultados em outra rodada.

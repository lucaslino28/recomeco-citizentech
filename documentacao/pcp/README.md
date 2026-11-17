# PCP — documentação

Lucas Lino Marques da Silva — RM 572863; Gabriel Martins Cordeiro Rodrigues — RM 570497; Gustavo Martins da Silva — RM 570584.

**Pensamento Computacional e Automação com Python.** Na parte de PCP, fizemos o atendimento sobre desastres com três classes e busca por regras. Ele usa a base JSON e funciona sem API. A opção 2 pertence à parte de IA.

## Arquivos da disciplina

| Etapa | Material |
|---|---|
| 1. Executar | `python3 main.py` na raiz; opções 1 e 4. [Guia de execução](guia_execucao.md). Para ensaiar sem misturar registros: `--dados data/demonstracao_pcp`. |
| 2. Ler o código | [main.py](../../main.py), [Orientacao](../../orientacao.py), [BaseConhecimento](../../base_conhecimento.py), [Assistente](../../assistente.py). |
| 3. Conferir a base e os arquivos | [Base JSON](../../data/base_conhecimento.json), [histórico](../../data/historico.json) e [CSV](../../data/atendimentos.csv). |
| 4. Entender regras e escolhas | [Funcionamento detalhado](funcionamento.md), [decisões](decisoes.md), [fontes](fontes.md) e [arquitetura integrada](../arquitetura.md). |
| 5. Avaliar os resultados humanos | [Relatório de 14/11](avaliacao_usuarios.md) e [evidências de PCP](../../evidencias/pcp/README.md). |
| 6. Conferir os testes técnicos | [Teste de PCP](../../testes/test_pcp.py), [plano de testes](plano_testes.md) e [revisão de 14/11](../../evidencias/pcp/tecnicos/revisao_2026-11-14/testes.txt). |
| 7. Conferir vídeo e entrega | [Requisitos técnicos de PCP no vídeo](roteiro_video.md), [planejamento integrado PCP + SERS](../roteiro_video_tecnico.md) e [TXT de PCP](../../entregas/pcp.txt). Link do vídeo ainda pendente. |

## Resultados e melhoria

Os testes de 14/11/2026 tiveram três pessoas de fora do grupo e dez atendimentos. Orientação encontrada/selecionada: **80%**; indicou que ajudou: **70%**; tempo médio registrado: **43,24 s**; facilidade média por sessão: **3,0/5**. O CSV contém também uma linha de 12/11, preservada e excluída dos cálculos por filtro de data.

Sem solução: enchente na rua do serviço, tempestade forte e contato da Enel. A revisão melhorou termos de busca, sugestões, conteúdo de tempestade/energia/documentos e aviso urgente de pessoa presa em veículo. Depois dos ajustes, conferimos as dez perguntas no código. Ainda não repetimos a avaliação de satisfação com as pessoas.

A confiança usa +3 por expressão-chave e +1 por palavra da pergunta com quatro ou mais letras presente no título. ALTA ≥6, MÉDIA de 3 a 5; abaixo de 3 oferece outros caminhos. Há tuplas de resultados e composição das três classes. A apresentação completa dessas regras e dos limites permanece no [funcionamento](funcionamento.md) e no README principal.

## Entrega

O PDF de PCP especifica código público, README, teste de pelo menos três pessoas externas e dez atendimentos, vídeo técnico não listado de **5 a 8 minutos**, com todos falando, sem voz sintética, e as demonstrações obrigatórias, incluindo alteração de palavra-chave ao vivo. O [roteiro](roteiro_video.md) mantém os itens de correção. O vídeo integrado de PCP + SERS vai incluir o conteúdo das duas matérias.

No Portal, enviar somente o TXT com assistente, público, integrantes/RMs e links de GitHub e vídeo; prazo de PCP: **19/11 às 23h59**, conforme o enunciado de GS 2026.2. [Central de entregas](../../entregas/README.md) · [Voltar ao projeto](../../README.md).

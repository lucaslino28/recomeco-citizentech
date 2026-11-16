# Documentação — RECOMEÇO

PCP revisado em 14/11/2026, após os dez atendimentos informados pela equipe. Índice atualizado em 16/11/2026 para incluir SERS.

## Por onde começar

| Documento | Para que serve |
|---|---|
| [README do projeto](../README.md) | Instalação, funcionamento, indicadores da avaliação e pendências |
| [Guia de PCP](guia_pcp.md) | Usar o terminal e entender as três classes |
| [Arquitetura](arquitetura.md) | Responsabilidades de PCP e planejamento dos demais módulos |
| [Decisões de PCP](decisoes_pcp.md) | Busca, atendimento, histórico, privacidade e limitações |
| [Fontes](fontes_pcp.md) | Referências oficiais e escopo de cada orientação |
| [Avaliação de 14/11](validacao_pcp.md) | Nove partes do relatório, resultados e melhoria aplicada |
| [Plano de testes](plano_testes.md) | Regressão técnica e preparação de novas rodadas humanas |
| [Roteiro do vídeo](roteiro_video_pcp.md) | Demonstração de 5 a 8 minutos com todos os integrantes |
| [Checklist](checklist.md) | Requisitos atendidos e itens ainda pendentes |
| [TXT de entrega](entrega_pcp.txt) | Arquivo a completar com RMs e link do vídeo |

## Evidências

- [CSV original da avaliação](../evidencias/validacao_usuarios_2026-11-14.csv): preservado, contém também um registro de 12/11 que não entra nos indicadores da rodada.
- [Indicadores derivados](../evidencias/indicadores_validacao_pcp_2026-11-14.json): produzidos por `python -B testes/analisar_validacao_pcp.py`.
- [Comparação técnica](../evidencias/revisao_pos_avaliacao_pcp_2026-11-14.json): roteamento antes/depois e hashes dos três arquivos originais.
- [Ensaio do menu completo](../evidencias/ensaio_terminal_pos_avaliacao_pcp_2026-11-14.txt): execução técnica automatizada em pasta temporária, com respostas programadas explicitamente identificadas.
- [Log dos testes atuais](../evidencias/testes_pos_avaliacao_pcp_2026-11-14.txt): 89 testes com dados temporários; não são novas avaliações de participantes.
- [Modelo para nova coleta](../evidencias/modelo_resultados_pcp.md): formulário vazio, separado do relatório da rodada concluída.

Os demais arquivos datados em `evidencias/` registram versões anteriores. Não somar seus cenários sintéticos aos atendimentos da avaliação. IA tem implementação e fechamento documentados: veja o [guia](ia/guia_execucao.md), as [decisões](ia/decisoes.md) e o [plano de usuários](ia/testes_usuarios.md). SERS está implementado e validado tecnicamente; avaliação humana, vídeo e publicação desta etapa permanecem pendentes.

## Prompt & IA

A documentação de IA está organizada em um [índice próprio](ia/README.md), com guia, justificativas, diagrama, avaliação automática, notebook e plano de usuários. Os registros de PCP permanecem separados.

## SERS — energia e sustentabilidade

O [índice de SERS](sers/README.md) reúne execução, memória de cálculo, referências, evidências técnicas, plano de usuários, roteiro de vídeo e TXT. O módulo funciona na opção 3 sem API. Os dados numéricos são estimativas didáticas justificadas. Ainda não há resultados de usuários de SERS; as coletas anteriores permanecem próprias de PCP/IA.

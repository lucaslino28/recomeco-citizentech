# Evidências de PCP

Avaliação de usuários em 14/11/2026 e revisão técnica posterior, mantendo as três classes e a pontuação +3/+1. [Relatório completo](../../documentacao/pcp/avaliacao_usuarios.md) · [Documentação](../../documentacao/pcp/README.md).

## Avaliação com usuários

Os testes tiveram três pessoas de fora do grupo e dez atendimentos. Guardamos os resultados por sessão, sem identificar cada pessoa ou associar seus atendimentos.

- [CSV original](usuarios/rodada_2026-11-14/validacao_usuarios_2026-11-14.csv): 11 linhas de dados, incluindo uma de 12/11 preservada; o filtro de data seleciona os dez atendimentos da rodada.
- [Indicadores derivados](usuarios/rodada_2026-11-14/indicadores.json): 80% de orientações encontradas/selecionadas, 70% indicaram que ajudou, 43,24 s e facilidade média por sessão 3,0/5.
- Os arquivos `data/historico.json` e `data/atendimentos.csv` permanecem na raiz do projeto, na estrutura solicitada pelo professor.

Reproduzir sem alterar o CSV: `python3 -B testes/analisar_validacao_pcp.py`.

## Verificação após as melhorias

- [Comparação técnica](tecnicos/revisao_2026-11-14/comparacao.json): resultados de roteamento e hashes dos arquivos originais.
- [Log dos 89 testes de PCP](tecnicos/revisao_2026-11-14/testes.txt): execução técnica da revisão, não avaliação de usuários.
- [Ensaio do terminal](tecnicos/revisao_2026-11-14/ensaio_terminal.txt): entradas programadas explicitamente identificadas.

## Histórico e modelo

Os documentos e logs em [historico/](historico/) descrevem versões anteriores, com seus números originais de teste. O [modelo de avaliação](modelos/avaliacao_usuarios.md) é um formulário para novas coletas, não uma rodada realizada. O código atual continua verificado pela suíte de `testes/`.

Caminhos de arquivos citados dentro de JSONs, logs e hashes históricos referem-se ao contexto original. O [mapa da reorganização](../../documentacao/organizacao.md) permite localizar os mesmos arquivos após a mudança; os CSVs, JSONs e logs não foram reescritos para alterar seus resultados.

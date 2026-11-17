# Organização e localização dos arquivos

Lucas Lino Marques da Silva — RM 572863; Gabriel Martins Cordeiro Rodrigues — RM 570497; Gustavo Martins da Silva — RM 570584.

Organizamos o repositório em 17/11/2026 para separar os materiais das três matérias. O README principal leva à documentação de cada uma e aos arquivos de entrega.

## Como separamos as pastas

- Mantivemos os quatro arquivos Python de PCP e `data/` na raiz, como no enunciado.
- O código de IA fica em `modulos/documentos_ia/` e o de SERS, em `modulos/energia/`.
- Cada matéria tem sua pasta dentro de `documentacao/` e `evidencias/`.
- Os arquivos de entrega ficam em `entregas/`.
- Mantivemos o notebook e os resultados dos testes. Dentro das evidências, os arquivos antigos ficam separados dos resultados atuais.

## Nomes antigos e atuais

| Caminho anterior | Caminho atual |
|---|---|
| `documentacao/decisoes_pcp.md` | `documentacao/pcp/decisoes.md` |
| `documentacao/entrega_pcp.txt` | `entregas/pcp.txt` |
| `documentacao/fontes_pcp.md` | `documentacao/pcp/fontes.md` |
| `documentacao/guia_pcp.md` | `documentacao/pcp/guia_execucao.md` |
| `documentacao/plano_testes.md` | `documentacao/pcp/plano_testes.md` |
| `documentacao/roteiro_video_pcp.md` | `documentacao/pcp/roteiro_video.md` |
| `documentacao/sers/entrega_sers.txt` | `entregas/sers.txt` |
| `documentacao/validacao_pcp.md` | `documentacao/pcp/avaliacao_usuarios.md` |
| `evidencias/ampliacao_desastres_pcp_2026-11-14.md` | `evidencias/pcp/historico/ampliacao_desastres_pcp_2026-11-14.md` |
| `evidencias/ensaio_terminal_pos_avaliacao_pcp_2026-11-14.txt` | `evidencias/pcp/tecnicos/revisao_2026-11-14/ensaio_terminal.txt` |
| `evidencias/ia/ambiente_2026-11-15.txt` | `evidencias/ia/historico/ambiente_2026-11-15.txt` |
| `evidencias/ia/codigo_v1.zip` | `evidencias/ia/historico/codigo_v1.zip` |
| `evidencias/ia/codigo_v2.zip` | `evidencias/ia/historico/codigo_v2.zip` |
| `evidencias/ia/codigo_v3.zip` | `evidencias/ia/historico/codigo_v3.zip` |
| `evidencias/ia/ensaio_menu_2026-11-15.txt` | `evidencias/ia/historico/ensaio_menu_2026-11-15.txt` |
| `evidencias/ia/exploratoria_v3_parcial.json` | `evidencias/ia/historico/exploratoria_v3_parcial.json` |
| `evidencias/ia/intermediaria_v2.json` | `evidencias/ia/historico/intermediaria_v2.json` |
| `evidencias/ia/testes_tecnicos_2026-11-15.txt` | `evidencias/ia/historico/testes_tecnicos_2026-11-15.txt` |
| `evidencias/indicadores_validacao_pcp_2026-11-14.json` | `evidencias/pcp/usuarios/rodada_2026-11-14/indicadores.json` |
| `evidencias/modelo_resultados_pcp.md` | `evidencias/pcp/modelos/avaliacao_usuarios.md` |
| `evidencias/refinamento_pcp_2026-11-14.md` | `evidencias/pcp/historico/refinamento_pcp_2026-11-14.md` |
| `evidencias/revisao_pos_avaliacao_pcp_2026-11-14.json` | `evidencias/pcp/tecnicos/revisao_2026-11-14/comparacao.json` |
| `evidencias/sers/ensaio_terminal.txt` | `evidencias/sers/v2/ensaio_terminal.txt` |
| `evidencias/sers/pos_usuario_2026-11-17/README.md` | `evidencias/sers/v3/README.md` |
| `evidencias/sers/pos_usuario_2026-11-17/ensaio_terminal_hsp.txt` | `evidencias/sers/v3/ensaio_terminal_hsp.txt` |
| `evidencias/sers/pos_usuario_2026-11-17/testes.txt` | `evidencias/sers/v3/testes.txt` |
| `evidencias/sers/pos_usuario_2026-11-17/validacao_tecnica.json` | `evidencias/sers/v3/validacao_tecnica.json` |
| `evidencias/sers/testes_2026-11-16.txt` | `evidencias/sers/v2/testes_2026-11-16.txt` |
| `evidencias/sers/validacao_tecnica.json` | `evidencias/sers/v2/validacao_tecnica.json` |
| `evidencias/testes_multidesastres_pcp_2026-11-14.txt` | `evidencias/pcp/historico/testes_multidesastres_pcp_2026-11-14.txt` |
| `evidencias/testes_pcp_2026-11-12.txt` | `evidencias/pcp/historico/testes_pcp_2026-11-12.txt` |
| `evidencias/testes_pcp_2026-11-14.txt` | `evidencias/pcp/historico/testes_pcp_2026-11-14.txt` |
| `evidencias/testes_pos_avaliacao_pcp_2026-11-14.txt` | `evidencias/pcp/tecnicos/revisao_2026-11-14/testes.txt` |
| `evidencias/validacao_tecnica_pcp.md` | `evidencias/pcp/historico/validacao_tecnica_pcp.md` |
| `evidencias/validacao_usuarios_2026-11-14.csv` | `evidencias/pcp/usuarios/rodada_2026-11-14/validacao_usuarios_2026-11-14.csv` |

## Arquivos antigos

Alguns JSONs e registros de terminal ainda citam os caminhos usados quando foram gerados. A tabela acima mostra a localização atual desses arquivos. Mantivemos o conteúdo original dos registros.

Também atualizamos o caminho padrão do CSV em `testes/analisar_validacao_pcp.py`. Assim, o comando continua lendo os mesmos dados depois da mudança de pasta.

[Conferência dos arquivos](../evidencias/organizacao/preservacao.json) · [Testes da organização](../evidencias/organizacao/README.md) · [Entregas](../entregas/README.md) · [Voltar ao projeto](../README.md).

# Evidências de SERS

Versão atual **sers-v3**, de 17/11/2026. A avaliação humana e as execuções técnicas ficam separadas para indicar a origem de cada conclusão.

| Conjunto | Conteúdo |
|---|---|
| [Rodada S01 de 17/11](usuarios/rodada_2026-11-17/README.md) | Uma participante externa conforme relato do aplicador, terminal e relatório da v2, comentários indiretos, dificuldade com HSP e ajuste aplicado. |
| [Verificação pós-avaliação](pos_usuario_2026-11-17/README.md) | v3: 171 testes gerais, 36 de SERS; ensaio automatizado da confirmação de HSP e cálculos com hashes atuais. Não é nova participação humana. |
| `validacao_tecnica.json`, `testes_2026-11-16.txt`, `ensaio_terminal.txt` | Evidências históricas da v2: 166 testes gerais, 31 de SERS. Preservadas sem recalcular como se fossem atuais. |
| `v1/` | Código, dados e resultados da primeira versão, com 152 testes gerais e 17 de SERS. |

Reproduzir os cálculos da versão atual sem rede ou IA: `python3 -B testes/analisar_sers.py`. A cópia NASA original está em `modulos/energia/fontes/nasa_sao_paulo.json`, com URL, unidade, período e hash documentados. As sequências de dias são hipóteses para estudo.

Relatórios exportados ficam localmente em `data/relatorios_sers/`, ignorados pelo Git. A cópia do relatório de S01 foi incluída na rodada para evidência, junto à transcrição com identificadores do ambiente substituídos. Nas transcrições foram removidos apenas espaços finais de prompts para formatação; entradas e resultados não foram corrigidos retroativamente.

A participante avaliou a v2. A mudança da v3 foi implementada e testada tecnicamente, mas ainda não houve nova consulta à participante. Não se declara melhora de compreensão sem essa observação. Os dados originais de PCP/IA e as evidências técnicas anteriores de SERS foram preservados.

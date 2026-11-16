# Evidências técnicas de SERS

Versão atual `sers-v2`, refinada em 16/11/2026. Os arquivos desta pasta resultam de execução técnica real com parâmetros programados. **Não representam participação, opinião ou compreensão de usuários.** A avaliação humana de SERS ainda está pendente.

| Arquivo | Conteúdo |
|---|---|
| `validacao_tecnica.json` | Contas e sensibilidade, referência solar pública, autonomia e sequências; inclui hashes dos dados e código utilizados. |
| `testes_2026-11-16.txt` | Saída real da suíte completa: 166 testes, incluindo 31 de SERS. |
| `ensaio_terminal.txt` | Execução automatizada do programa, com entradas e natureza técnica informadas. |
| `v1/` | Código, dados e resultados anteriores ao refinamento: 152 testes gerais, dos quais 17 de SERS. São histórico, não nova rodada ou resultado atual. |

Reproduzir os cálculos sem usar rede ou IA:

```bash
python3 -B testes/analisar_sers.py
```

A cópia original dos dados NASA fica em `modulos/energia/fontes/nasa_sao_paulo.json`. A data, a URL e o hash da consulta estão em `analise.json`; as unidades e o período constam da resposta original. Os dias 4/1/0/1/4 HSP são escolhidos para simulação, não extraídos como previsão dos dados públicos.

Relatórios exportados pelo usuário ficam localmente em `data/relatorios_sers/`, ignorados pelo Git. Para a futura avaliação humana, registrar apenas a modalidade de participação real, as situações executadas, os comentários autorizados e os ajustes efetivamente feitos, conforme `documentacao/sers/testes_usuarios.md`.

Nas transcrições do terminal foram removidos apenas espaços no final das linhas dos prompts para padronizar a formatação no Git; o conteúdo das saídas e os resultados não foram alterados.

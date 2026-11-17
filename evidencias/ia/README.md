# Evidências de Prompt and Artificial Intelligence

Lucas Lino Marques da Silva — RM 572863; Gabriel Martins Cordeiro Rodrigues — RM 570497; Gustavo Martins da Silva — RM 570584.

[Documentação](../../documentacao/ia/README.md) · [Notebook executado](../../notebooks/avaliacao_ia.ipynb) · [Relatório dos três indicadores](../../documentacao/ia/usuarios_2026-11-15.md).

## Avaliação automática

| Arquivo | Versão e uso |
|---|---|
| [antes.json](antes.json) | Agente v1, 26 casos, 20 acertos do juiz — 76,92%. |
| [depois.json](depois.json) | Agente v3, 26 casos, 25 acertos do juiz — 96,15%. Não é medição da v4 atual. |
| [comparacao.json](comparacao.json) / [CSV](comparacao.csv) | Comparação reproduzível antes/depois; vereditos preservados. |
| [Conferência técnica](conferencia_tecnica.md) | Limites e divergências do juiz; [amostra confirmada](../../documentacao/ia/revisao_amostra.md). |

O juiz não é garantia de correção factual. O notebook lê os resultados existentes; reorganizar o repositório não executa nova rodada na API.

## Avaliação com usuários e correções

- [Rodada de 15/11](usuarios/rodada_2026-11-15/README.md): cinco participantes externos informados, 15 tarefas e 25 notas, com origem/transcrição e indicadores.
- [Formulários e roteiro](usuarios/README.md): modelos para futuras coletas.
- [Fechamento](fechamento/): confirmação da amostra, validação das correções v4, testes e publicação anterior.

Não tratar conclusão informada de tarefas como precisão factual independente. Tempos e notas pertencem à versão avaliada, v3. O atendimento atual usa v4, sem novo benchmark ou coleta humana após as correções.

## Versões anteriores

[historico/](historico/) contém snapshots de código v1/v2/v3, rodada intermediária, teste exploratório parcial, ensaio do menu e logs de ambiente/testes anteriores. São preservados byte a byte, separados dos resultados principais. Referências internas antigas dos arquivos brutos continuam como registro histórico; veja o [mapa de localização](../../documentacao/organizacao.md).

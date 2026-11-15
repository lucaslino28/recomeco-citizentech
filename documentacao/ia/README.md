# Documentação de Prompt & Artificial Intelligence

- Lucas Lino Marques da Silva — RM 572863
- Gabriel Martins Cordeiro Rodrigues — RM 570497
- Gustavo Martins da Silva — RM 570584

FIAP, Ciência da Computação, 1CCPX — GS 2026.2.

| Material | Uso |
|---|---|
| [Guia de execução](guia_execucao.md) | Instalar dependências, configurar Groq e usar a opção 2 |
| [Decisões e limitações](decisoes.md) | Framework, modelos, agente, algoritmos, privacidade e juiz |
| [Diagrama PNG](arquitetura.png) / [SVG](arquitetura.svg) | Imagem da arquitetura para a entrega do script |
| [Avaliação e análise](avaliacao.md) | Rodadas reais, melhoria, comparação e limites do juiz |
| [Notebook](../../notebooks/avaliacao_ia.ipynb) | Tabelas reais e leitura reproduzível dos resultados |
| [Plano de usuários](testes_usuarios.md) | Roteiro original para aplicação |
| [Relatório de usuários](usuarios_2026-11-15.md) | Rodada informada de cinco participantes, 15 tarefas e 25 notas |
| [Conferência dos requisitos](requisitos_ia.md) | Arquivos verificados, limitações e pendências |
| [Fechamento v4](fechamento.md) | Correções, revisão confirmada, validação e publicação |
| [Proveniência](proveniencia.json) | Originais, sete fichas e hashes do dataset |

## Evidências

`evidencias/ia/` contém as rodadas completas `antes.json`, `intermediaria_v2.json` e `depois.json`, comparação em CSV/JSON, snapshots anteriores sem chave, teste exploratório parcial identificado, conferência técnica assistida e testes de software.

Os modelos de registro continuam vazios para futuras coletas. A rodada informada de 15/11 está em [arquivos de usuários](../../evidencias/ia/usuarios/rodada_2026-11-15/README.md), com CSVs, transcrição extraída e indicadores. A conferência da amostra foi confirmada pelo aplicador e está registrada em `revisao_amostra.md`. A versão de atendimento atual é v4; os benchmarks e os tempos/notas preservados pertencem à v3. O notebook automático é um registro da etapa anterior; o relatório de usuários reúne os três indicadores da disciplina.

Aurora é fictícia. As sete fichas de IA não são usadas em PCP e não valem como informações reais sobre documentos brasileiros. A chave está apenas no `.env` local ignorado pelo Git.

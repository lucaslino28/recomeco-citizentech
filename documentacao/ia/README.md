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
| [Plano de usuários](testes_usuarios.md) | Cinco pessoas externas, três tarefas e questionário de cinco itens |
| [Proveniência](proveniencia.json) | Originais, sete fichas e hashes do dataset |

## Evidências

`evidencias/ia/` contém as rodadas completas `antes.json`, `intermediaria_v2.json` e `depois.json`, comparação em CSV/JSON, snapshots anteriores sem chave, teste exploratório parcial identificado, conferência técnica assistida e testes de software.

Os modelos de registro em `evidencias/ia/usuarios/` estão vazios. Não representam coleta realizada. A conferência manual da amostra pelos integrantes e os indicadores de tempo/facilidade de usuários permanecem pendentes.

Aurora é fictícia. As sete fichas de IA não são usadas em PCP e não valem como informações reais sobre documentos brasileiros. A chave está apenas no `.env` local ignorado pelo Git.

# Refinamento técnico e de usabilidade de PCP

Implementado em 14/11/2026. Escopo: orientações gerais para o Brasil, sem cadastro ou armazenamento de perguntas livres. A versão anterior de PCP, publicada no commit `cf25bdc`, foi preservada no Git; este refinamento ainda não foi publicado automaticamente.

## Resultado implementado

- Base ampliada de 10 para 18 orientações, mantendo os IDs anteriores e três categorias.
- Respostas com resumo, passos curtos, encaminhamento, observação de alcance, documentos quando informados, fonte e data.
- Palavras-chave revistas para distinguir situações como receber, doar e descartar alimentos.
- Seleção entre até três assuntos quando duas candidatas estão a até um ponto da melhor. A fórmula de pontuação permanece a do enunciado.
- Sugestões por assunto e por semelhança de escrita, abertas somente após escolha da pessoa, sem atribuir confiança textual a uma escolha sem pontuação.
- Até duas alternativas selecionáveis após resposta não útil. Abrir alternativa ou categoria no mesmo atendimento incrementa tentativas sem criar outro registro.
- Exemplos acessíveis por submenu e pelo comando `?`; confirmação aceita letras ou números.
- Continuação curta de assunto com confirmação explícita. Somente a última orientação pública aceita fica em memória; não existe memória do texto digitado.

## Validação automatizada

Executada com Python 3.14.3 e biblioteca padrão:

```bash
python -B -m unittest discover -s testes -v
```

**Resultado final: 61 testes executados, todos aprovados.** Log em [execução de 14/11](testes_pcp_2026-11-14.txt).

Os testes incluem as regras anteriores de pontuação, entradas inválidas, privacidade, migração, arquivos e métricas, além dos novos caminhos de esclarecimento, confirmação de sugestão, escolha de alternativa, continuação, recuperação por categorias e compatibilidade da base antiga sem os campos opcionais.

O conjunto [casos de perguntas](../testes/casos_perguntas_pcp.json) contém 42 cenários sintéticos com resultado esperado: orientação direta, esclarecimento, sugestão ou ausência de cobertura. Todos passaram na versão refinada. Esse conjunto foi construído durante a revisão técnica; não é uma amostra aleatória de usuários nem uma medição de acurácia geral.

Para comparação técnica, foram aplicados os mesmos 42 casos à base anterior e à política antiga de exibir o primeiro resultado ou informar ausência de correspondência. Houve compatibilidade com o resultado esperado em 13 casos na versão anterior e em 42 na versão refinada. A diferença também inclui situações novas que não faziam parte da base anterior. Isso demonstra cobertura desses cenários, sem comprovar satisfação, qualidade clínica ou desempenho em toda linguagem natural.

## Conferência em pseudoterminal

Uma execução isolada percorreu: pergunta `alimentos`, seleção de recebimento; consulta sobre obter água, resposta negativa e abertura de alternativa; sugestão para `soccoro`; pergunta fora do escopo e seleção de categoria; indicadores, avaliação e encerramento com CSV. O processo encerrou normalmente. As entradas foram sintéticas e o resultado não é teste com participante externo.

Os arquivos dessa conferência ficaram em pasta técnica fora do histórico padrão. JSON e CSV padrão foram comparados com o Git e permaneceram iguais. IA, energia e configuração de dependências também permaneceram iguais. `git diff --check` passou.

## Fontes e limitações

Fontes, IDs e alcance estão em [referências de PCP](../documentacao/fontes_pcp.md). As novas orientações usam materiais públicos do MDS, Ministério da Saúde, Defesa Civil e MME, além de recomendação sanitária estadual para doação de alimentos. Endereços, vagas, estoques e campanhas não são consultados em tempo real. Resumos de limpeza remetem ao procedimento completo da fonte; o programa não calcula dosagens nem substitui avaliação técnica.

O assistente continua baseado em regras: pode errar contexto, negações e perguntas com várias intenções. Uma sugestão pode ser recusada. O mecanismo de esclarecimento cobre apenas as regras documentadas e não equivale a um agente de linguagem.

Os testes com três pessoas externas e pelo menos dez atendimentos, a melhoria decorrente desses testes e o vídeo continuam pendentes. Não foram inventados participantes, notas ou resultados humanos.

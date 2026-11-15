# IA — plano de avaliação com usuários

- Lucas Lino Marques da Silva — RM 572863
- Gabriel Martins Cordeiro Rodrigues — RM 570497
- Gustavo Martins da Silva — RM 570584

## Situação

A rodada de 15/11 foi informada pelo aplicador com cinco pessoas externas, três tarefas por código e 25 notas. O [relatório da aplicação](usuarios_2026-11-15.md) contém as perguntas efetivas, que variaram em relação ao roteiro abaixo. Os resultados estão em `evidencias/ia/usuarios/rodada_2026-11-15/`. O roteiro original foi preservado como planejamento e orientação para futuras rodadas. A rodada anterior de PCP é de outra disciplina.

## Preparação e aplicação

1. Registrar a versão do código, dos modelos e das fichas, a data e a quantidade real de participantes. Não registrar nomes, contatos ou dados de identificação de participantes.
2. Abrir `python main.py --dados data/demonstracao_pcp` e escolher IA. Explicar que Aurora e suas regras são fictícias. Usar situações hipotéticas, sem dados pessoais.
3. Atribuir apenas códigos anônimos P01 a P05, sem lista que os vincule às identidades. Cada código corresponde a uma pessoa efetivamente participante, não a uma persona criada pela equipe.
4. Cronometrar desde a apresentação da tarefa até a pessoa localizar e compreender o resultado. Anotar o tempo total, incluindo digitação, navegação, espera e leitura. Registrar separadamente uma eventual indisponibilidade da API.
5. Conferir o resultado da tarefa com as fichas, sem orientar a pessoa a dar uma resposta positiva. Depois das três tarefas, aplicar as cinco perguntas.

## Três tarefas originalmente propostas

| Tarefa | Situação fictícia | Critério de conclusão |
|---|---|---|
| T01 | Descobrir o que levar para a segunda via do RG em caso de perda | Certidão original/autenticada, comprovante dos últimos 90 dias e declaração de extravio; BO não é exigido na perda (FC-01) |
| T02 | Descobrir a validade da CNH renovada de uma pessoa hipotética de 55 anos | Cinco anos, na faixa de 50 a 69 anos (FC-06) |
| T03 | Descobrir custo e prazo da segunda via da certidão de nascimento pelo portal | R$ 49,00, PDF em três dias úteis (FC-05) |

A pessoa pode formular a pergunta com suas palavras ou usar o menu. Registrar o código da tarefa, tempo e acerto 0/1; não guardar perguntas identificáveis. São 15 execuções de tarefa no mínimo, sem transformar a contagem em prova automática de participantes.

## Questionário — cinco itens

Escala: 1 = discordo totalmente; 2 = discordo; 3 = nem concordo nem discordo; 4 = concordo; 5 = concordo totalmente.

1. Entendi as opções do menu.
2. Consegui encontrar a informação de que precisava.
3. As respostas foram claras.
4. Entendi de onde vieram as informações e os limites do assistente.
5. Foi fácil usar o sistema pelo teclado.

Aplicar uma vez por participante após as três tarefas, sem preencher por ele. Não inventar comentários nem pontuações para completar formulários.

## Registro e indicadores

Copiar os modelos vazios de `evidencias/ia/usuarios/` para arquivos datados de uma rodada real. Manter um registro por tarefa e um por questionário. Uma nova versão deve usar outra rodada.

- Acerto das orientações: resultado do LLM juiz sobre as 26 mensagens, acompanhado de amostra conferida manualmente. O acerto 0/1 por tarefa humana é uma observação adicional, com unidade separada.
- Tempo humano: média geral e por tarefa, informando quantas tarefas foram concluídas e quais tiveram falha de API. Não usar o tempo de inferência automática como tempo de usuário.
- Facilidade: média de cada item e média geral das cinco perguntas; informar número de participantes respondentes e respostas ausentes, sem assumir nota zero.

No relatório final, registrar objetivo, método aplicado, quantidades reais, indicadores, dificuldades observadas, análise e limitações. Não atribuir uma melhoria de facilidade às alterações antes de medir seus efeitos com pessoas.

# Plano de testes externos de PCP

Situação: roteiro preparado, coleta ainda não realizada. A equipe precisa testar com pelo menos três pessoas de fora do grupo, somando dez atendimentos, antes de gravar o vídeo. Testes técnicos automatizados não substituem essa etapa.

## Preparação

1. Executar os testes técnicos: `python -B -m unittest discover -s testes -v`.
2. Usar uma pasta nova exclusivamente para a coleta real: `python main.py --dados data/testes_externos_pcp`. Se ela já contiver ensaios, escolher uma nova pasta; não misturar os resultados.
3. Cada pessoa usa uma execução distinta do programa, sempre com a mesma pasta da coleta. Não abrir execuções simultâneas.
4. Explicar que é um protótipo acadêmico e pedir que não sejam digitados dados pessoais nem situações pessoais identificáveis.
5. Usar somente as situações fictícias abaixo. Não anotar nome, documento, contato, idade, endereço ou gravação de voz dos participantes. Identificar as sessões apenas pelos códigos aleatórios do programa, sem lista que os vincule às pessoas.

## Dez atendimentos sugeridos

A distribuição de tarefas abaixo é planejada; não comprova participação real.

| Sessão planejada | Tarefa | Situação fictícia | O que observar |
|---|---|---|---|
| Primeira | T01 | Encontrar onde procurar abrigo | Local de encaminhamento e limites sobre vagas |
| Primeira | T02 | Saber como pedir ajuda depois de enchente | Orientação de emergência e fonte |
| Primeira | T03 | Procurar alertas da Defesa Civil | Procedimento e aviso para não digitar CEP no assistente |
| Primeira | T04 | Encontrar benefícios eventuais pela categoria Assistência social | Navegação, critérios e ausência de garantia de benefício |
| Segunda | T05 | Saber o que fazer se a casa fictícia estiver em risco | Correspondência adequada e encaminhamento |
| Segunda | T06 | Consultar cuidados com água contaminada | Clareza da resposta e referência |
| Segunda | T07 | Consultar alimentos atingidos pela enchente | Localizar e compreender orientação |
| Terceira | T08 | Buscar prevenção de leptospirose pela categoria Saúde e higiene | Acesso à orientação e limites do protótipo |
| Terceira | T09 | Perguntar sobre um assunto fora da base, como astronomia | Mensagem sem correspondência e opção de retorno |
| Terceira | T10 | Perguntar como atravessar uma rua alagada | Resposta e compreensão dos cuidados |

Para manter dez atendimentos separados, encerrar cada tarefa antes de iniciar a seguinte. Se uma tarefa precisar de reformulação, escolher essa opção: haverá um atendimento com mais tentativas, sem aumentar artificialmente o total.

Pode-se pedir adicionalmente que a pessoa encontre uma resposta inválida de menu e retorne com `0`. Isso não conta como atendimento. Não usar dados pessoais reais para testar o filtro; os testes automatizados já usam exemplos sintéticos controlados.

## Coleta e encerramento

A própria pessoa responde `s` ou `n` à pergunta de utilidade. Ao sair, registra uma nota de facilidade de 1 a 5, ou opta por não avaliar. Não preencher avaliações pela pessoa. Os tempos são medidos pelo programa e incluem a interação; o tempo de digitação e leitura faz parte da medida.

Na opção 4, os indicadores são calculados sobre todos os registros daquela pasta de coleta. O CSV é exportado ali. Copiar os resultados observados para `evidencias/modelo_resultados_pcp.md` e depois para o README. Conferir que há pelo menos dez atendimentos e que, de fato, participaram três pessoas externas; o número de sessões sozinho não comprova pessoas diferentes.

Os comentários devem ser resumidos pela equipe sem identificar a pessoa. Usar o código da tarefa, não o texto livre digitado. O histórico omite o texto intencionalmente; uma falha sem correspondência deve ser relacionada à situação fictícia do roteiro, sem tentar recuperar relatos pessoais.

## Melhoria obrigatória

Depois da coleta, identificar uma dificuldade real, aplicar uma mudança pequena e registrá-la com evidência. Exemplo possível: uma palavra-chave que realmente faltou para uma das tarefas. Esse exemplo é apenas uma possibilidade, não um resultado já observado.

Documentar: tarefa que falhou, observação recebida, mudança aplicada, teste após a mudança e limitação restante. Preservar os resultados anteriores em vez de reescrevê-los para parecer que a falha não aconteceu. Se houver nova rodada com pessoas, usar outra pasta para não misturar antes e depois.

## Vídeo de PCP

Preparar vídeo técnico de 5 a 8 minutos, não listado, com código legível e todos os integrantes explicando uma parte. Não usar voz sintética.

Demonstrar: equipe/público/problema; um registro JSON e as tuplas da busca; atributos, métodos, `self` e composição; cálculo real de pontuação; resposta encontrada e não encontrada; entrada inválida e dado fictício bloqueado; categorias; alteração ao vivo de palavra-chave; histórico sem texto livre, CSV e indicadores reais; decisão de privacidade e uma limitação.

Para a alteração ao vivo, usar uma cópia da base ou restaurar a edição depois do ensaio. Uma pergunta controlada como `refúgio temporário` não deve ser encontrada antes da mudança; acrescentar essa expressão à orientação de abrigo, reiniciar para recarregar o JSON e mostrar a diferença. Confirmar o comportamento antes da gravação. Esse ensaio demonstra a busca e não constitui melhoria baseada em usuário.

Manter demonstrações em pasta separada: `python main.py --dados data/demonstracao_pcp`. Elas não devem alterar os indicadores da coleta externa.

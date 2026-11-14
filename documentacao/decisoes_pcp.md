# Decisões de PCP

Atualização: 14/11/2026. As três classes e os métodos exigidos foram mantidos. Não foram adicionadas classes, bibliotecas externas ou serviços de IA em PCP.

## Busca

Os pesos e limites do enunciado foram preservados: 3 por palavra-chave, 1 por palavra distinta com quatro letras ou mais no título, resultado a partir de 3 e confiança alta a partir de 6. Expressões são procuradas completas, com limites de palavras. Em empate, permanece a ordem do JSON.

A palavra-chave genérica `enchente` foi retirada da orientação sobre atravessar alagamentos porque fazia uma pergunta sobre pedir ajuda encontrar uma resposta pouco adequada. Foram acrescentadas expressões específicas sobre ajuda, casa em risco, abrigos e água contaminada. Essa é uma melhoria técnica; a melhoria exigida após testes com pessoas ainda está pendente.

## Histórico sem texto livre

O enunciado exige um campo `pergunta` e proíbe guardar perguntas com oito ou mais dígitos ou `@`. O pedido do projeto acrescenta a necessidade de proteger outras formas de identificação. Uma lista de padrões não consegue garantir a remoção de todos os nomes, endereços ou relatos identificáveis. Por isso, mantivemos o campo exigido com rótulos controlados e sem o texto original.

Essa decisão reduz a informação disponível sobre falhas de busca. A equipe deve usar tarefas fictícias identificadas pelo roteiro para investigar dúvidas sem solução nos testes externos. Não completar os relatórios com relatos pessoais recebidos.

Na migração, o histórico é reconstruído apenas com campos conhecidos, valores validados e rótulos gerados pelo programa. Não são preservados campos extras de identificação. Dados numéricos válidos do legado permanecem; não se presume que tenham vindo de participantes externos. Uma cópia local prévia do projeto foi guardada fora do Git antes das alterações.

## Atendimento e tentativas

`registrar()` cria o dicionário do atendimento e devolve esse registro. Quando a pessoa escolhe reformular, o mesmo dicionário é atualizado e `tentativas` aumenta. Uma nova dúvida inicia outro registro. Erros de entrada e mensagens bloqueadas não aumentam o contador.

Uma tentativa válida é salva antes de pedir confirmação, evitando perdê-la em EOF ou Ctrl+C. Se a pessoa não confirmar que ajudou, o registro fica como não resolvido. A última tentativa determina orientação e resposta encontrada. O tempo acumulado inclui interação e reformulação, em segundos; não representa só o tempo da busca.

## Facilidade por sessão

Cada execução recebe um código aleatório com `uuid4`, sem relação com dados pessoais. A nota é associada aos registros da sessão, mas a média usa uma nota por código. Sessões sem nota são excluídas da média, sem assumir nota zero. Notas legadas sem sessão permanecem armazenadas, mas não entram nessa média: não há informação suficiente para reconstruir as sessões antigas.

## Arquivos e recuperação

Os caminhos relativos partem da pasta do projeto, não do diretório de onde o usuário lançou o Python. `--dados` permite uma pasta separada para histórico e CSV, mantendo a base oficial comum. A opção permite isolar testes externos, demonstrações e desenvolvimento.

A validação da base verifica campos, tipos, IDs únicos e positivos, três chaves distintas, data ISO e formato de URL. Não acessa a internet durante a execução: a oficialidade e a atualidade do conteúdo são conferidas manualmente e documentadas em `fontes_pcp.md`.

Gravações passam por um arquivo temporário; somente uma escrita concluída substitui o destino. Se a escrita falhar, o programa informa que os dados permanecem em memória. Um histórico inteiramente ilegível não é sobrescrito, e o CSV anterior é preservado. A equipe deve recuperar ou corrigir o arquivo antes de reiniciar; o programa não tenta inventar registros para recuperar JSON truncado. Não encerrar uma sessão com dados apenas em memória esperando que eles reapareçam depois.

O CSV é reconstruído com campos controlados e sem texto livre, inclusive quando o histórico é legado. O identificador de sessão é validado e as datas são normalizadas. Dessa forma, perguntas iniciadas por `=` não viram fórmulas na exportação.

## Limites da implementação

O filtro de privacidade é preventivo e incompleto; a ausência de texto livre no armazenamento é a proteção principal. O programa não usa rede nem envia a pergunta para um LLM. A base é um arquivo curado pela equipe e a pontuação textual pode errar a intenção. Não são suportadas gravações simultâneas por duas execuções usando a mesma pasta de dados.

## Refinamento da interação em 14/11/2026

Os pesos de `pontuar()` e a ordenação de `buscar()` permanecem iguais. Uma etapa no `Assistente` compara as primeiras pontuações: se duas candidatas estiverem a até um ponto da melhor, oferece até três títulos para escolha antes de responder. Não se altera a pontuação para decidir arbitrariamente entre receber e descartar alimentos.

O JSON agora possui 18 orientações e três campos opcionais: passos, observação e assuntos. A classe `Orientacao` continua responsável pela exibição. `BaseConhecimento.sugerir()` usa assuntos cadastrados e semelhança de escrita da biblioteca padrão; uma sugestão só vira resposta após escolha. Não há novas classes, dependências externas ou acesso à internet durante o atendimento.

`Assistente.atender()` concentra a exibição e a recuperação após resposta não útil: reformular, iniciar outra dúvida, escolher categoria ou abrir alternativa. A seleção de assunto inicial não aumenta tentativas; abrir outra orientação depois de receber uma resposta soma uma tentativa no mesmo atendimento. A origem representa a entrada pela pergunta ou pelas categorias, mesmo que a pessoa navegue por outras opções depois.

A última orientação confirmada como útil pode ser apresentada para uma pergunta curta de continuação, mediante escolha explícita. Só o objeto com conteúdo público é mantido em memória; não há histórico textual de conversa. O campo `encontrou` considera tanto a resposta por pontuação quanto a orientação escolhida em navegação assistida. As telas distinguem confiança textual de escolha guiada.

As novas situações e erros foram levantados por revisão técnica; os resultados não substituem a melhoria baseada em participantes externos exigida pelo professor.

## Ampliação para desastres e eventos ambientais

Foram mantidos os IDs anteriores e adicionadas orientações de 19 a 30. O recorte cobre oito grupos de eventos e preparação, sem pretensão de classificar estatisticamente sua frequência. Alguns eventos, como incêndios, também podem ter origem humana. O cenário energético de SERS continua sendo iluminação de abrigo; esse estudo de caso não limita a abrangência das orientações de PCP.

`Orientacao.desastres` é uma lista opcional de etiquetas do JSON. `BaseConhecimento.tipos_desastre()` lista os temas; `por_tipo_desastre()` reúne orientações específicas e apoio compartilhado. As que se aplicam a menos tipos vêm primeiro. Um tema inexistente retorna lista vazia, em vez de exibir apoio e dar a impressão de cobertura inexistente. O `Assistente` reaproveita o fluxo de categorias; no histórico, essa seleção tem origem `categoria`.

A fórmula de pontuação não foi alterada. Novas palavras-chave e expressões foram avaliadas junto dos cenários antigos. Em sugestões de digitação, palavras comuns são ignoradas para evitar que uma palavra como `como` provoque uma sugestão sobre enchente para uma pergunta sobre bolo. Assuntos ambíguos como `tempestade` oferecem vendaval, raios e granizo, com escolha explícita.

O público de PCP passou a ser cidadãos buscando orientação diante de desastres e eventos ambientais no Brasil. Conteúdos específicos de enchentes permanecem marcados e não são apresentados como procedimentos universais. Histórico, privacidade, notas por sessão e exportação foram preservados. Testes externos reais continuam pendentes.

# Decisões de PCP

Mantivemos as três classes pedidas na matéria e usamos JSON e a biblioteca padrão do Python. Os ajustes abaixo foram feitos depois dos testes de 14/11/2026.

## Busca e confiança

`pontuar()` mantém +3 por palavra-chave/expressão completa encontrada e +1 por palavra distinta da pergunta com quatro ou mais letras no título. As expressões respeitam limites de palavras. `buscar()` devolve tuplas `(pontos, orientacao)` em ordem decrescente, com resultado a partir de 3 e confiança ALTA a partir de 6. Empates mantêm a ordem do JSON. Confiança é correspondência textual, não garantia de utilidade.

Não foi recolocada a chave genérica “enchente” na orientação de atravessar alagamentos, pois isso prejudicava outras intenções. Foram adicionadas expressões específicas, como “enchente na rua”. A frase isolada “enchente” continua oferecendo seleção de assunto, sem pontuação inventada.

## Sugestões e esclarecimento

Candidatas com diferença de até um ponto da melhor geram escolha entre até três títulos. A orientação aberta pode apresentar até duas alternativas, que a pessoa consegue selecionar depois de uma resposta negativa.

Sem resultado por pontuação, `sugerir()` procura assuntos cadastrados em qualquer posição da frase, com limites de palavras. Depois usa termos exatos e só então aproximações do `difflib`, com limite 0,84. Termos neutros como “está”, “estou” e “cidade” não são usados como contexto. Essa mudança corrige as sugestões de cesta/rachaduras observadas na pergunta de tempestade. Toda sugestão exige escolha e não recebe confiança fictícia.

A última orientação confirmada como útil fica apenas em memória. Uma pergunta curta de continuação pode oferecer esse assunto, com confirmação; nunca é guardado histórico textual da conversa.

## Conteúdo e urgência

A base possui 34 orientações, três categorias funcionais e navegação por oito grupos de eventos, além de preparação/apoio. `desastres` é uma lista opcional do JSON; “Apoio geral” inclui serviços comuns sem criar uma categoria de desastre. As orientações específicas aparecem antes das compartilhadas.

Os IDs 31 a 34 tratam de documentos no acolhimento, interrupção de energia, canais regionais da Enel e tempestade forte. Os IDs anteriores foram mantidos. “Energia” deixou de ser uma chave isolada da orientação de choque, evitando que qualquer falta de luz gere a mesma resposta.

`avisar_risco_imediato()` usa condições simples: expressões de pessoa presa, veículo e inundação. Exibe encaminhamento ao 193 antes de possíveis escolhas; a busca e as pontuações continuam sendo executadas. É uma proteção limitada para expressões conhecidas, não um detector geral de emergência. O sistema não despacha resgate nem define como sair do veículo.

O conteúdo documental não garante vaga ou procedimento universal de admissão. Os contatos da Enel são associados às áreas atendidas. Fontes e limites estão em [fontes PCP](fontes.md).

## Atendimento, tentativas e tempo

Uma pergunta válida cria um dicionário no histórico. Reformular atualiza o mesmo atendimento e soma uma tentativa; começar nova dúvida cria outro. Abrir outra orientação durante a recuperação soma uma tentativa, enquanto o esclarecimento inicial não soma. Categorias e tipos usam o mesmo fluxo de avaliação, com origem `categoria`.

O resultado final corresponde à última tentativa. Só uma confirmação positiva marca `ajudou=True`. Voltar ou interromper sem confirmar mantém o atendimento não resolvido.

O tempo usa `time.time()` e inclui digitação, leitura, escolhas e reformulações. `atender()` usa `try/finally` para salvar o tempo ao sair, inclusive por retorno ou interrupção. A limitação antiga foi documentada, sem alterar os tempos já registrados. Uma interrupção antes de entrar nesse fluxo, como durante a primeira seleção de assunto, ainda pode manter o tempo da última gravação; não é uma medição externa de desempenho.

## Histórico sem texto livre

O enunciado exige o campo `pergunta` e bloqueio de entradas com oito ou mais dígitos ou `@`. O projeto também evita guardar outras identificações. Como padrões não reconhecem todos os nomes e endereços, o campo recebe apenas “Orientação N; texto livre omitido.” ou “Sem correspondência; texto livre omitido.”.

O filtro preventivo bloqueia também algumas expressões de identificação. Ele é incompleto; a proteção principal é não persistir texto livre. Isso reduz os detalhes disponíveis para analisar falhas: frases da avaliação de 14/11 vieram da contextualização da equipe, não do JSON.

A validação do histórico reconstrói campos controlados e elimina dados desconhecidos de registros legados. Na revisão atual, os três arquivos válidos da avaliação foram preservados byte a byte, com hashes na comparação técnica. Não foi feita migração dos resultados, correção de notas ou estimativa de tempos.

## Facilidade e indicadores

Cada execução tem código aleatório `uuid4`, sem identificação pessoal. A nota de facilidade fica associada aos atendimentos da execução, mas entra uma única vez na média por sessão. Sessões sem nota são excluídas, sem assumir zero. Registros antigos sem sessão não recebem sessão inventada.

`calcular_indicadores(data_filtro=None)` usa todos os registros por padrão. Com uma data, calcula sobre os registros daquele dia e suas notas. `--data-indicadores AAAA-MM-DD` permite usar isso na opção 4 do programa, com data validada. A tela informa que o CSV exportado continua completo. O filtro não apaga registros.

A rodada de 14/11 é recalculável pelo script de leitura `testes/analisar_validacao_pcp.py`, que não inicia atendimentos nem escreve no histórico.

## Arquivos e recuperação

Caminhos relativos partem da pasta do projeto. `--dados` separa histórico e CSV de cada coleta ou demonstração, sem duplicar a base oficial.

A validação do JSON confere tipos, campos, IDs, pelo menos três chaves distintas, data ISO e formato de URL. A consulta a fontes ocorre na revisão manual, não durante a execução do programa.

Gravações passam por arquivo temporário e substituição após completar a escrita. Em falha, os dados permanecem em memória. Se o histórico inteiro estiver ilegível, o programa mantém esse arquivo e o CSV anterior. Precisamos corrigir o arquivo e reiniciar para voltar a salvar. Registros individuais inválidos são ignorados com aviso. O CSV usa `csv.DictWriter` e campos controlados.

Não há coordenação entre programas simultâneos na mesma pasta. Não encerrar esperando recuperar dados que ficaram apenas em memória após falha de gravação.

## Avaliação e melhoria de PCP

O [relatório](avaliacao_usuarios.md) reúne os testes com três pessoas de fora do grupo, dez atendimentos e as mudanças que fizemos. Os dados estão organizados por sessão, sem uma divisão dos atendimentos por pessoa.

A revisão técnica posterior passou em 89 testes e verificou as dez frases contra a versão anterior. Os resultados com pessoas continuam em 80% de orientações encontradas, 70% de utilidade e facilidade 3,0. Ainda não repetimos esse teste depois das mudanças.

## Limites

As regras não entendem toda negação, sinônimo ou pergunta com várias intenções. O assistente não consulta serviços, vagas, previsões, rotas ou alertas em tempo real. Não diagnostica, não inspeciona imóveis e não garante concessões. IA e SERS têm módulos separados, acessados pelo mesmo menu principal. As referências e os registros técnicos de versões anteriores foram preservados para consulta histórica.

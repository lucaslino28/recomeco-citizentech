# Funcionamento detalhado de PCP

Lucas Lino Marques da Silva — RM 572863; Gabriel Martins Cordeiro Rodrigues — RM 570497; Gustavo Martins da Silva — RM 570584.

Nesta página explicamos a busca, o atendimento e o registro dos dados de PCP. As instruções de execução e os principais arquivos estão na [documentação da matéria](README.md).

## Arquitetura PCP

```text
main.py                  navegação e encerramento
Assistente               atendimento, privacidade, histórico, indicadores e CSV
  └── BaseConhecimento   carregamento, categorias e busca por pontuação
        └── Orientacao   dados e exibição da orientação
```

- `data/base_conhecimento.json`: 34 orientações com fontes oficiais, em 3 categorias.
- `data/historico.json`: resultados dos atendimentos; perguntas são substituídas por rótulos controlados.
- `data/atendimentos.csv`: exportação desses resultados com `csv.DictWriter`.
- `testes/test_pcp.py`: testes técnicos com arquivos temporários.
- `documentacao/`: fontes, decisões, roteiro de teste externo e checklist.
- `evidencias/`: CSV original da avaliação, indicadores derivados, comparação técnica e registros históricos de testes.

## Busca por pontuação

A comparação remove acentos e pontuação, transforma o texto em minúsculas e uniformiza espaços.

- Cada palavra-chave ou expressão completa encontrada vale **3 pontos**. A comparação respeita os limites das palavras; a busca por pontuação não faz correção automática de erros de digitação.
- Cada palavra distinta da pergunta com pelo menos quatro letras que também aparece no título vale **1 ponto**.
- **6 pontos ou mais:** confiança ALTA.
- **3 a 5 pontos:** confiança MÉDIA.
- **Menos de 3 pontos:** sem orientação encontrada.

Os resultados são tuplas `(pontos, orientacao)`, ordenadas da maior para a menor pontuação. Empates preservam a ordem do JSON. Quando há duas ou mais candidatas a até um ponto da melhor, o sistema pede que a pessoa escolha entre até três assuntos antes de responder. A orientação escolhida é exibida com até duas alternativas, que podem ser abertas se a resposta não ajudar. Não há IA nessa busca. Confiança indica coincidência textual; não é probabilidade nem garantia de que a resposta resolve a dúvida.

Exemplo: `socorro emergência` encontra a orientação 1 com 7 pontos: 3 por `socorro`, 3 por `emergencia` e 1 por `emergencia` no título.

## Atendimento guiado e conteúdo

O submenu de PCP oferece escrever a dúvida, escolher um assunto passo a passo, consultar exemplos ou escolher o tipo de desastre (opção 4). As respostas incluem um resumo, passos práticos, encaminhamento, limitações, fonte e data. Os campos opcionais `passos`, `observacao`, `assuntos` e `desastres` mantêm a base compatível com os registros antigos que não os possuem.

A cobertura inclui enchentes/enxurradas, deslizamentos, vendavais, tempestades/raios, granizo, seca/estiagem, calor intenso e incêndios florestais/fumaça. Também inclui preparação e serviços de apoio, como acolhimento, alimentos, benefícios e CRAS. Os cuidados específicos de limpeza e contaminação de enchentes continuam identificados como tais. Não são garantidos serviços locais nem resultados de atendimento.

A palavra `alimentos` pode significar receber, doar ou descartar: nesses casos o programa pede esclarecimento. Sem resultado por pontuação, assuntos cadastrados são reconhecidos também dentro de frases completas. Sugestões de assunto ou de semelhança de escrita exigem escolha explícita. Elas usam apenas o vocabulário da base e a biblioteca nativa `difflib`, com limite de semelhança 0,84. Palavras genéricas como `como`, `para`, `está` e `estou` são ignoradas nas sugestões. Depois dos assuntos cadastrados, coincidências exatas de termos vêm antes das aproximações de escrita. Não recebem pontuação ou confiança inventadas; a tela informa que a orientação foi aberta por escolha da pessoa. Sugestões podem errar e podem ser recusadas.

Após uma resposta confirmada como útil, a pergunta `E quais documentos preciso levar?` pode oferecer o mesmo assunto, com confirmação. Só o objeto da última orientação é mantido em memória, nunca a pergunta livre. O sistema não é um modelo de linguagem: negações, linguagem indireta e perguntas com várias intenções ainda podem exigir esclarecimento ou reformulação.

### Ajustes após a avaliação de 14/11

Foram incluídas orientações próprias para documentos no acolhimento (ID 31), falta de energia (32), canais regionais da Enel (33) e tempestade forte (34). Perguntas sobre enchente na rua agora encontram os cuidados com alagamento. Expressões sobre pessoa presa em carro encontram o encaminhamento de emergência.

Quando a mensagem contém expressões cadastradas de pessoa presa em veículo e inundação, um aviso com o 193 aparece antes de eventuais escolhas. Isso não modifica a pontuação, não detecta toda emergência e não aciona resgate. Os contatos da Enel são identificados por área atendida, com fontes e revisão em [fontes de PCP](fontes.md).

### Navegação por tipo de desastre

No menu principal, escolha 1; no submenu de PCP, escolha 4. A pessoa pode consultar oito grupos de eventos, além de preparação/apoio. As orientações mais específicas aparecem antes dos cuidados compartilhados; orientações gerais de emergência, alertas e apoio social ficam disponíveis no mesmo caminho.

O campo opcional `desastres` organiza essa navegação no JSON. A etiqueta interna `Apoio geral` adiciona serviços comuns aos tipos cobertos, sem virar uma opção de desastre. Bases antigas sem esse campo continuam funcionando com perguntas e categorias. Escolher um tipo sem abrir orientação não conta como atendimento. Abrir e avaliar uma orientação usa o mesmo fluxo e os mesmos indicadores das categorias.

Exemplos de perguntas: `O barranco está cedendo`, `Como me proteger de raios?`, `Está caindo granizo`, `Como economizar água na seca?`, `Meu avô está passando mal com o calor` e `Há fogo no mato perto de casa`. O programa dá orientações gerais e encaminhamentos; não confirma uma emergência nem substitui atendimento oficial.

## Atendimentos e indicadores

Uma pergunta válida inicia um atendimento. Se não houver resultado ou a resposta não ajudar, o menu oferece reformular a mesma dúvida, começar outra ou voltar. Reformular atualiza o mesmo registro e soma uma tentativa. Entradas inválidas ou bloqueadas não somam tentativas. Uma consulta de orientação por categoria inicia um atendimento com uma tentativa. Abrir uma alternativa ou recorrer à seleção de categoria dentro de um atendimento soma uma tentativa no mesmo registro. Escolher entre assuntos ambíguos ou confirmar uma sugestão antes da primeira resposta não soma outra tentativa.

O histórico guarda o resultado da última tentativa. O tempo é medido com `time.time()` e inclui digitação, leitura, confirmação e eventuais reformulações. A revisão após a avaliação também finaliza o tempo ao sair do menu de recuperação, inclusive em interrupções dentro do atendimento. Registros antigos não foram recalculados. Uma interrupção após a busca ou um retorno sem confirmação mantém o atendimento como não resolvido; ele entra no denominador dos indicadores.

Indicadores:

- Resposta encontrada: atendimentos cuja última tentativa encontrou orientação / total × 100.
- Taxa de acerto declarada: atendimentos em que a pessoa confirmou que ajudou / total × 100. É percepção de utilidade, não validação factual.
- Tempo médio e tentativas médias: soma / total de atendimentos.
- Facilidade: média das notas por sessão avaliada, sem dar peso adicional a quem fez mais perguntas.
- Dúvidas sem solução: rótulos das orientações que não ajudaram ou indicação de falta de correspondência, sem o texto digitado.

O identificador aleatório de sessão não contém nome, documento ou contato. Sessões não comprovam, por si só, a quantidade de pessoas externas: essa execução deve ser real e acompanhada pela equipe.

## Privacidade e arquivos

O programa não solicita cadastro nem envia perguntas a serviços externos. Recusa mensagens com oito ou mais dígitos no total, com `@` ou com algumas declarações pessoais comuns. Esse filtro não reconhece todos os nomes ou dados pessoais possíveis. Por isso, **nenhuma pergunta livre é gravada**, mesmo que passe no filtro.

O campo obrigatório `pergunta` contém somente `Orientação N; texto livre omitido.` ou `Sem correspondência; texto livre omitido.`. Campos desconhecidos do histórico são descartados. O CSV usa registros validados, sem reaproveitar texto livre, evitando também exportar fórmulas enviadas como pergunta.

Ao carregar um histórico legado, o programa preserva os indicadores válidos e remove o texto livre, avisando sobre a revisão. Notas antigas são mantidas no arquivo; sem sessão conhecida, ficam fora da média de facilidade por sessão. Não se inventa a sessão de registros antigos. Antes desta correção foi preservada uma cópia local do estado anterior fora do repositório.

Registros individuais malformados são ignorados com aviso. Se o arquivo inteiro estiver ilegível ou a raiz não for uma lista, ele e o CSV anterior são preservados: novos atendimentos ficam apenas em memória e não são exportados até a equipe corrigir o arquivo e reiniciar. Não use arquivos corrompidos para os testes externos. A gravação normal passa por um arquivo temporário e substitui o destino só após concluir a escrita.

Para filtrar apenas a exibição dos indicadores por data, acrescente `--data-indicadores 2026-11-14` ao comando de execução. O programa informa o período na tela; o CSV exportado continua contendo todo o histórico da pasta. A data é validada no formato `AAAA-MM-DD`.

Para recalcular a avaliação preservada sem iniciar atendimentos nem escrever nos arquivos originais:

```bash
python -B testes/analisar_validacao_pcp.py
```

## Fontes e limitações

As fontes foram conferidas em 14/11/2026 e estão relacionadas em [fontes de PCP](fontes.md). Toda orientação mostra fonte, data, local de encaminhamento e aviso de canal não oficial. A validação do JSON confere estrutura, tipos, IDs, data e formato de URL; não comprova automaticamente que uma fonte é oficial ou que seu conteúdo continua atualizado.

Parte das referências de segurança, saúde e preparação é estadual. Foram aproveitados os cuidados gerais, com preferência por fontes federais; regras e campanhas locais não foram generalizadas. A disponibilidade de serviços e os procedimentos municipais precisam ser confirmados com os órgãos locais. O sistema não diagnostica doenças, não inspeciona imóveis, não concede benefícios e não garante atendimento ou vagas. A equipe precisa revisar periodicamente as informações.

A busca não compreende todos os sinônimos ou contextos. A lista de dúvidas não resolvidas perde detalhes intencionalmente para evitar guardar dados pessoais. Em novas avaliações, use situações fictícias e registre somente a tarefa sem dados pessoais para relacionar falhas ao roteiro. As frases da rodada de 14/11 foram fornecidas pela equipe na contextualização e não foram recuperadas do histórico. O armazenamento em JSON foi planejado para uma execução por vez; não oferece coordenação entre programas simultâneos.

## Validação técnica

```bash
python -B -m unittest discover -s testes -v
```

Os testes usam `unittest`, dados fictícios e pastas temporárias. A revisão após a avaliação passou em **89 testes**, incluindo os 42 cenários anteriores, 50 casos multidesastres, as dez perguntas anotadas no teste e verificações de urgência, navegação, privacidade, tempo e filtro de indicadores. Veja o [log da revisão](../../evidencias/pcp/tecnicos/revisao_2026-11-14/testes.txt) e a [comparação técnica antes/depois](../../evidencias/pcp/tecnicos/revisao_2026-11-14/comparacao.json).

Os registros anteriores de [ampliação](../../evidencias/pcp/historico/ampliacao_desastres_pcp_2026-11-14.md), [refinamento](../../evidencias/pcp/historico/refinamento_pcp_2026-11-14.md) e [validação inicial](../../evidencias/pcp/historico/validacao_tecnica_pcp.md) permanecem como histórico. Seus números descrevem versões anteriores, não a versão atual nem novos participantes.

## Avaliação com participantes externos — 14/11/2026

Os testes tiveram **três pessoas de fora do grupo** e **dez atendimentos**, cada um em uma execução separada. As próprias pessoas formularam as perguntas, indicaram se a orientação ajudou e avaliaram a facilidade ao encerrar. Não foram publicados nomes nem vínculos entre pessoas e perguntas. O histórico guarda as sessões e as avaliações. Os comentários sobre as perguntas estão no relatório da aplicação.

| Indicador da rodada | Resultado |
|---|---:|
| Atendimentos de 14/11 | 10 |
| Orientação encontrada ou selecionada | 8 — 80% |
| Indicou que ajudou | 7 — 70% |
| Encontrou, mas não ajudou | 1 |
| Sem orientação confirmada | 2 |
| Atendimentos sem solução | 3 |
| Facilidade média por execução avaliada | 3,0/5 |
| Tempo médio registrado | 43,24 segundos |
| Tentativas médias | 1,0 |

A evidência original é [validacao_usuarios_2026-11-14.csv](../../evidencias/pcp/usuarios/rodada_2026-11-14/validacao_usuarios_2026-11-14.csv). Ela também contém um registro de 12/11, excluído apenas dos cálculos. Os [indicadores recalculados](../../evidencias/pcp/usuarios/rodada_2026-11-14/indicadores.json) usam os dez registros da data. As dez notas e sessões não devem ser interpretadas como dez participantes; a média não é calculada por pessoa.

As dúvidas sem solução foram: enchente na rua do serviço (orientação selecionada não ajudou), tempestade forte e número da Enel (sem orientação confirmada). Também identificamos respostas incompletas sobre documentos no abrigo e falta de energia, apesar da avaliação positiva.

A melhoria decorrente da avaliação corrigiu o reconhecimento de enchente e tempestade, removeu sugestões causadas por palavras neutras e acrescentou os conteúdos de documentos e energia. A pergunta sobre pessoa presa no carro passou a receber aviso imediato de encaminhamento. A busca continua com os pesos +3/+1. A verificação técnica posterior encontrou a orientação prevista nas dez frases, sem substituir as avaliações originais ou representar nova coleta humana. A facilidade e a utilidade após a melhoria ainda não foram reavaliadas com participantes.

O [relatório completo da avaliação](avaliacao_usuarios.md) apresenta metodologia, resultados, análise crítica, mudanças e limitações. A distribuição exata dos atendimentos por participante não foi informada; nenhum teste foi atribuído a uma pessoa específica.

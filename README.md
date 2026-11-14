# RECOMEÇO

Assistente de apoio a cidadãos afetados por enchentes — Global Solution 2026.2, FIAP, Ciência da Computação, turma 1CCPX.

O projeto orienta sobre segurança, assistência social e cuidados em desastres e eventos ambientais no Brasil, mantendo o atendimento pelo terminal. É um protótipo educacional: não representa órgãos públicos, não atende emergências e não informa vagas de abrigo em tempo real.

## Equipe

- Lucas Lino Marques da Silva — RM a preencher.
- Gabriel M. — nome completo e RM a preencher.
- Gustavo M. — nome completo e RM a preencher.

## Disciplinas e situação atual

| Disciplina | Contribuição | Situação em 14/11/2026 |
|---|---|---|
| Pensamento Computacional e Automação com Python | Classes, busca por regras, categorias, histórico, indicadores e CSV | Implementado e validado em testes técnicos locais; testes externos e vídeo pendentes |
| Prompt and Artificial Intelligence | Agente sobre documentação pessoal e avaliação por LLM | Sete fichas fictícias disponíveis; agente e avaliador pendentes |
| Soluções em Energias Renováveis e Sustentáveis | Comparação entre rede e sistema solar com bateria para iluminação de abrigo | Cenário planejado; cálculos e integração pendentes |

As opções 2 e 3 do menu informam que estão em desenvolvimento. As fichas fictícias de Aurora não participam das respostas de PCP.

## Instalação e execução

PCP usa somente a biblioteca padrão. A versão efetivamente testada foi Python 3.14.3. Os módulos atuais não exigem instalar pacotes de `requirements.txt`.

Na pasta do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python main.py
```

Se o ambiente virtual já existir, basta ativá-lo. Também é possível executar o caminho completo de `main.py` de outra pasta: os caminhos dos dados são resolvidos a partir dos arquivos do projeto.

O menu permite fazer perguntas, consultar categorias, escolher um tipo de desastre e conferir indicadores e exporta CSV na opção 4 e no encerramento. Use `0` para voltar e `?` na pergunta para ver exemplos. A confirmação aceita `s` ou `1` (sim), `n` ou `2` (não), e `0` para voltar; a facilidade aceita de 1 a 5, ou `0` para não avaliar.

Para separar os resultados de testes externos do histórico de desenvolvimento:

```bash
python main.py --dados data/testes_externos_pcp
```

Essa pasta começa vazia quando ainda não existe. Cada execução cria uma sessão aleatória; participantes externos devem usar execuções distintas, a mesma pasta de teste e nenhuma identificação pessoal. Use outra pasta, como `data/demonstracao_pcp`, para ensaios. Não misture ensaios ou testes automatizados com os testes externos.

## Arquitetura PCP

```text
main.py                  navegação e encerramento
Assistente               atendimento, privacidade, histórico, indicadores e CSV
  └── BaseConhecimento   carregamento, categorias e busca por pontuação
        └── Orientacao   dados e exibição da orientação
```

- `data/base_conhecimento.json`: 30 orientações oficiais, em 3 categorias.
- `data/historico.json`: resultados dos atendimentos; perguntas são substituídas por rótulos controlados.
- `data/atendimentos.csv`: exportação desses resultados com `csv.DictWriter`.
- `testes/test_pcp.py`: testes técnicos com arquivos temporários.
- `documentacao/`: fontes, decisões, roteiro de teste externo e checklist.
- `evidencias/`: registros técnicos e modelo ainda não preenchido dos testes externos.

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

A palavra `alimentos` pode significar receber, doar ou descartar: nesses casos o programa pede esclarecimento. Sem resultado por pontuação, sugestões de assunto ou de semelhança de escrita exigem escolha explícita. Elas usam apenas o vocabulário da base e a biblioteca nativa `difflib`, com limite de semelhança 0,84. Palavras genéricas como `como` e `para` são ignoradas nas sugestões, para não sugerirem um assunto sem relação com a dúvida. Não recebem pontuação ou confiança inventadas; a tela informa que a orientação foi aberta por escolha da pessoa. Sugestões podem errar e podem ser recusadas.

Após uma resposta confirmada como útil, a pergunta `E quais documentos preciso levar?` pode oferecer o mesmo assunto, com confirmação. Só o objeto da última orientação é mantido em memória, nunca a pergunta livre. O sistema não é um modelo de linguagem: negações, linguagem indireta e perguntas com várias intenções ainda podem exigir esclarecimento ou reformulação.

### Navegação por tipo de desastre

No menu principal, escolha 1; no submenu de PCP, escolha 4. A pessoa pode consultar oito grupos de eventos, além de preparação/apoio. As orientações mais específicas aparecem antes dos cuidados compartilhados; orientações gerais de emergência, alertas e apoio social ficam disponíveis no mesmo caminho.

O campo opcional `desastres` organiza essa navegação no JSON. A etiqueta interna `Apoio geral` adiciona serviços comuns aos tipos cobertos, sem virar uma opção de desastre. Bases antigas sem esse campo continuam funcionando com perguntas e categorias. Escolher um tipo sem abrir orientação não conta como atendimento. Abrir e avaliar uma orientação usa o mesmo fluxo e os mesmos indicadores das categorias.

Exemplos de perguntas: `O barranco está cedendo`, `Como me proteger de raios?`, `Está caindo granizo`, `Como economizar água na seca?`, `Meu avô está passando mal com o calor` e `Há fogo no mato perto de casa`. O programa dá orientações gerais e encaminhamentos; não confirma uma emergência nem substitui atendimento oficial.

## Atendimentos e indicadores

Uma pergunta válida inicia um atendimento. Se não houver resultado ou a resposta não ajudar, o menu oferece reformular a mesma dúvida, começar outra ou voltar. Reformular atualiza o mesmo registro e soma uma tentativa. Entradas inválidas ou bloqueadas não somam tentativas. Uma consulta de orientação por categoria inicia um atendimento com uma tentativa. Abrir uma alternativa ou recorrer à seleção de categoria dentro de um atendimento soma uma tentativa no mesmo registro. Escolher entre assuntos ambíguos ou confirmar uma sugestão antes da primeira resposta não soma outra tentativa.

O histórico guarda o resultado da última tentativa. O tempo é medido com `time.time()` e inclui digitação, leitura, confirmação e eventuais reformulações. Uma interrupção após a busca ou um retorno sem confirmação mantém o atendimento como não resolvido; ele entra no denominador dos indicadores.

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

## Fontes e limitações

As fontes foram conferidas em 14/11/2026 e estão relacionadas em [fontes de PCP](documentacao/fontes_pcp.md). Toda orientação mostra fonte, data, local de encaminhamento e aviso de canal não oficial. A validação do JSON confere estrutura, tipos, IDs, data e formato de URL; não comprova automaticamente que uma fonte é oficial ou que seu conteúdo continua atualizado.

Parte das referências de segurança, saúde e preparação é estadual. Foram aproveitados os cuidados gerais, com preferência por fontes federais; regras e campanhas locais não foram generalizadas. A disponibilidade de serviços e os procedimentos municipais precisam ser confirmados com os órgãos locais. O sistema não diagnostica doenças, não inspeciona imóveis, não concede benefícios e não garante atendimento ou vagas. A equipe precisa revisar periodicamente as informações.

A busca não compreende todos os sinônimos ou contextos. A lista de dúvidas não resolvidas perde detalhes intencionalmente para evitar guardar dados pessoais. Durante testes, use tarefas fictícias previamente definidas para relacionar uma falha ao roteiro sem registrar a pergunta real da pessoa. O armazenamento em JSON foi planejado para uma execução por vez; não oferece coordenação entre programas simultâneos.

## Validação técnica

```bash
python -B -m unittest discover -s testes -v
```

Os testes usam a biblioteca `unittest`, dados fictícios e pastas temporárias. Não escrevem no histórico padrão nem contam como atendimentos de participantes externos. A ampliação de 14/11 passou em 71 testes automatizados, incluindo os 42 cenários anteriores e 50 casos novos sobre diferentes desastres. Veja [a validação da ampliação](evidencias/ampliacao_desastres_pcp_2026-11-14.md). O [primeiro refinamento de usabilidade](evidencias/refinamento_pcp_2026-11-14.md), que passou em 61 testes, permanece como registro histórico. A [validação anterior](evidencias/validacao_tecnica_pcp.md), de 12/11, continua preservada.

A revisão técnica corrigiu perguntas previstas que não encontravam resposta, a contagem fixa de tentativas, a ponderação da facilidade, caminhos dependentes da pasta atual, entrada numérica Unicode que causava erro e persistência de texto identificável. Essas melhorias resultaram de testes técnicos, não de testes com pessoas externas.

## Testes externos e entrega

**Ainda pendentes:** pelo menos 3 pessoas de fora da equipe, somando 10 atendimentos, resultados no README e uma melhoria baseada nesses testes. O registro legado existente não comprova participação externa e deve ficar separado dessa coleta.

Use o [plano de testes](documentacao/plano_testes.md) e preencha o [modelo de resultados](evidencias/modelo_resultados_pcp.md) somente depois das sessões reais. Após a coleta, acrescente aqui os indicadores observados, as situações não resolvidas e a melhoria aplicada.

O vídeo técnico de PCP deve durar de 5 a 8 minutos, ter participação de todos os integrantes e demonstrar o código e as funcionalidades, incluindo uma alteração ao vivo de palavra-chave. A gravação e o link ainda estão pendentes. O vídeo de SERS tem outro limite de duração e será tratado separadamente.

Entrega PCP: arquivo TXT com assistente, público, integrantes/RMs e links do GitHub e do vídeo, conforme o enunciado, até **19/11/2026 às 23h59**. Modelo em [entrega PCP](documentacao/entrega_pcp.txt); verifique os dados pendentes antes do envio.

## ODS relacionados

ODS 7 (Energia Limpa e Acessível), 10 (Redução das Desigualdades), 11 (Cidades e Comunidades Sustentáveis) e 13 (Ação Contra a Mudança Global do Clima).

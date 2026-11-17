# RECOMEÇO

Assistente de orientação a cidadãos afetados por desastres e eventos ambientais no Brasil — Global Solution 2026.2, FIAP, Ciência da Computação, turma 1CCPX.

O projeto orienta sobre segurança, assistência social e cuidados em desastres e eventos ambientais no Brasil, mantendo o atendimento pelo terminal. É um protótipo educacional: não representa órgãos públicos, não atende emergências e não informa vagas de abrigo em tempo real.

## Equipe

- Lucas Lino Marques da Silva — RM 572863.
- Gabriel Martins Cordeiro Rodrigues — RM 570497.
- Gustavo Martins da Silva — RM 570584.

## Disciplinas e situação atual

| Disciplina | Contribuição | Situação em 17/11/2026 |
|---|---|---|
| Pensamento Computacional e Automação com Python | Classes, busca por regras, categorias, histórico, indicadores e CSV | Implementado, avaliação de 14/11 documentada e melhorias verificadas; vídeo e dados finais da entrega pendentes |
| Prompt and Artificial Intelligence | Agente sobre documentação pessoal e avaliação por LLM | Agente v4 corrigido, coleta documentada, amostra confirmada e conteúdo publicado |
| Soluções em Energias Renováveis e Sustentáveis | Comparação entre rede e sistema solar com bateria para iluminação de abrigo | Avaliação de uma participante documentada e HSP refinada; vídeo e publicação pendentes |

A opção 2 abre o módulo de IA sobre documentos fictícios de Aurora. A opção 3 compara rede e solar com bateria, simula consumo/sol/preço e estima autonomia de iluminação de abrigo. As fichas fictícias de Aurora não participam das respostas de PCP.

## Instalação e execução

PCP e SERS usam somente a biblioteca padrão. A versão efetivamente testada foi Python 3.14.3. Para IA, instale `requirements.txt` e configure a chave Groq conforme o [guia de IA](documentacao/ia/guia_execucao.md).

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

Quando a mensagem contém expressões cadastradas de pessoa presa em veículo e inundação, um aviso com o 193 aparece antes de eventuais escolhas. Isso não modifica a pontuação, não detecta toda emergência e não aciona resgate. Os contatos da Enel são identificados por área atendida, com fontes e revisão em [fontes de PCP](documentacao/fontes_pcp.md).

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

As fontes foram conferidas em 14/11/2026 e estão relacionadas em [fontes de PCP](documentacao/fontes_pcp.md). Toda orientação mostra fonte, data, local de encaminhamento e aviso de canal não oficial. A validação do JSON confere estrutura, tipos, IDs, data e formato de URL; não comprova automaticamente que uma fonte é oficial ou que seu conteúdo continua atualizado.

Parte das referências de segurança, saúde e preparação é estadual. Foram aproveitados os cuidados gerais, com preferência por fontes federais; regras e campanhas locais não foram generalizadas. A disponibilidade de serviços e os procedimentos municipais precisam ser confirmados com os órgãos locais. O sistema não diagnostica doenças, não inspeciona imóveis, não concede benefícios e não garante atendimento ou vagas. A equipe precisa revisar periodicamente as informações.

A busca não compreende todos os sinônimos ou contextos. A lista de dúvidas não resolvidas perde detalhes intencionalmente para evitar guardar dados pessoais. Em novas avaliações, use situações fictícias e registre somente a tarefa sem dados pessoais para relacionar falhas ao roteiro. As frases da rodada de 14/11 foram fornecidas pela equipe na contextualização e não foram recuperadas do histórico. O armazenamento em JSON foi planejado para uma execução por vez; não oferece coordenação entre programas simultâneos.

## Validação técnica

```bash
python -B -m unittest discover -s testes -v
```

Os testes usam `unittest`, dados fictícios e pastas temporárias. A revisão após a avaliação passou em **89 testes**, incluindo os 42 cenários anteriores, 50 casos multidesastres, as dez frases informadas pela equipe e verificações de urgência, navegação, privacidade, tempo e filtro de indicadores. Veja o [log da revisão](evidencias/testes_pos_avaliacao_pcp_2026-11-14.txt) e a [comparação técnica antes/depois](evidencias/revisao_pos_avaliacao_pcp_2026-11-14.json).

Os registros anteriores de [ampliação](evidencias/ampliacao_desastres_pcp_2026-11-14.md), [refinamento](evidencias/refinamento_pcp_2026-11-14.md) e [validação inicial](evidencias/validacao_tecnica_pcp.md) permanecem como histórico. Seus números descrevem versões anteriores, não a versão atual nem novos participantes.

## Avaliação com participantes externos — 14/11/2026

Conforme relato da equipe, participaram **três pessoas externas**, em **dez atendimentos**, cada um em uma execução separada. As próprias pessoas formularam as perguntas, indicaram se a orientação ajudou e avaliaram a facilidade ao encerrar. Não foram publicados nomes nem vínculos entre pessoas e perguntas. O histórico registra sessões e avaliações; a quantidade de participantes e a metodologia são informações fornecidas pela equipe.

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

A evidência original é [validacao_usuarios_2026-11-14.csv](evidencias/validacao_usuarios_2026-11-14.csv). Ela também contém um registro de 12/11, excluído apenas dos cálculos. Os [indicadores recalculados](evidencias/indicadores_validacao_pcp_2026-11-14.json) usam os dez registros da data. As dez notas e sessões não devem ser interpretadas como dez participantes; a média não é calculada por pessoa.

As dúvidas sem solução foram: enchente na rua do serviço (orientação selecionada não ajudou), tempestade forte e número da Enel (sem orientação confirmada). Também identificamos respostas incompletas sobre documentos no abrigo e falta de energia, apesar da avaliação positiva.

A melhoria decorrente da avaliação corrigiu o reconhecimento de enchente e tempestade, removeu sugestões causadas por palavras neutras e acrescentou os conteúdos de documentos e energia. A pergunta sobre pessoa presa no carro passou a receber aviso imediato de encaminhamento. A busca continua com os pesos +3/+1. A verificação técnica posterior encontrou a orientação prevista nas dez frases, sem substituir as avaliações originais ou representar nova coleta humana. A facilidade e a utilidade após a melhoria ainda não foram reavaliadas com participantes.

O [relatório completo da avaliação](documentacao/validacao_pcp.md) apresenta metodologia, resultados, análise crítica, mudanças e limitações. A distribuição exata dos atendimentos por participante não foi informada; nenhum teste foi atribuído a uma pessoa específica.

## Documentação e entrega de PCP

A [organização da documentação](documentacao/README.md) reúne o guia de uso, fontes, decisões, avaliação, checklist e roteiro do vídeo. O [plano de testes](documentacao/plano_testes.md) agora descreve como fazer novas rodadas sem misturar versões. O [modelo de resultados](evidencias/modelo_resultados_pcp.md) permanece disponível como formulário para futuras coletas.

Pendências da entrega: revisão da equipe, vídeo técnico de **5 a 8 minutos** com participação de todos e alteração ao vivo de palavra-chave, link do vídeo e envio do TXT. O [roteiro do vídeo](documentacao/roteiro_video_pcp.md) já está preparado.

Entrega PCP: TXT com assistente, público, integrantes/RMs e links do GitHub e do vídeo, conforme o enunciado, até **19/11/2026 às 23h59**. Modelo em [entrega PCP](documentacao/entrega_pcp.txt). IA tem documentação própria; a etapa de SERS está implementada e tem pendências de avaliação humana, vídeo e publicação.

## Prompt & Artificial Intelligence

Integrantes: Lucas Lino Marques da Silva (572863), Gabriel Martins Cordeiro Rodrigues (570497) e Gustavo Martins da Silva (570584).

A opção 2 do menu usa um agente LangChain e Groq para orientar sobre as sete fichas fictícias da Central do Cidadão de Aurora. A implementação mantém o conteúdo real de PCP separado. Valores e regras de Aurora não são informações reais sobre documentação pessoal.

- [Guia para instalar, configurar a chave e executar](documentacao/ia/guia_execucao.md).
- [Arquitetura, modelos, justificativas e limitações](documentacao/ia/decisoes.md).
- [Diagrama em SVG](documentacao/ia/arquitetura.svg).
- [Plano de cinco participantes, três tarefas e questionário de cinco itens](documentacao/ia/testes_usuarios.md).

O golden dataset tem as 26 mensagens e respostas esperadas copiadas da tabela original. O pipeline aplica um LLM juiz com critérios de conteúdo, fontes, privacidade e resistência a manipulação. A rodada inicial teve 20/26 (76,92%) e a versão v3 avaliada 25/26 (96,15%) pelo juiz: diferença de 19,23 pontos percentuais. O [relatório](documentacao/ia/avaliacao.md) registra as mudanças, limitações e divergências do juiz. As tabelas e exemplos estão no [notebook executado](notebooks/avaliacao_ia.ipynb). A [amostra de seis casos](documentacao/ia/revisao_amostra.md) foi conferida com confirmação manual declarada pelo aplicador; os vereditos do juiz foram preservados.

### Avaliação com usuários — 15/11/2026

Conforme relato do aplicador, cinco pessoas externas realizaram três tarefas cada. Foram registrados 15 tempos, cinco questionários e 25 notas. As perguntas efetivas variaram entre os participantes; T01/T02/T03 indicam a posição na sessão.

| Medida | Resultado |
|---|---:|
| Conclusão informada pelo aplicador | 15/15 — 100% |
| Falhas de API relatadas | 0 |
| Tempo humano médio | 23,04 segundos |
| Facilidade geral | 4,04/5 |
| Menu / encontrar / clareza / fontes e limites / teclado | 4,4 / 3,6 / 3,6 / 3,8 / 4,8 |

Os [dados e sua origem](evidencias/ia/usuarios/rodada_2026-11-15/README.md) e o [relatório com as tarefas efetivas](documentacao/ia/usuarios_2026-11-15.md) foram organizados sem mudar os tempos ou notas. A transcrição sustenta as respostas; participantes, associação dos códigos, cronometragem e questionários foram informados pelo aplicador. A conclusão de 100% não significa precisão factual independente de 100%: o caso de transferência bancária contém recomendação sem respaldo nas fichas, além de outros pontos de revisão.

Os três indicadores de IA ficam separados: acerto automático pelo juiz de 96,15%, tempo humano de 23,04 s e facilidade 4,04/5. As melhorias automáticas anteriores não foram apresentadas como ganho humano antes/depois. A [conferência dos requisitos](documentacao/ia/requisitos_ia.md) registra a conferência da amostra, as correções pontuais e a publicação como itens do fechamento. A [versão v4](documentacao/ia/fechamento.md) corrige os casos identificados e passou em 135 testes locais. O benchmark de 96,15% e os dados humanos acima pertencem à v3; a v4 não recebeu nova rodada de juiz ou de usuários.

Para recalcular a coleta sem usar a API ou alterar os CSVs:

```bash
python -B testes/analisar_usuarios_ia.py
```

## Soluções em Energias Renováveis e Sustentáveis

A **opção 3** analisa o custo e a continuidade da iluminação noturna de um abrigo temporário para pessoas afetadas por desastres no Brasil. Compara os mesmos LEDs alimentados pela rede existente e por solar isolado com bateria, no mesmo período. A versão `sers-v3` usa biblioteca padrão, sem chamadas de API durante o uso.

O exemplo inicial de 20 lâmpadas de 9 W, 6 h/noite e 30 dias consome **1,08 kWh/dia** e **32,4 kWh no período**. Demanda, perdas e orçamento são estimados. A v2 acrescenta dados públicos NASA POWER para um caso horizontal de São Paulo e referências de fabricante para as capacidades escolhidas, sem generalizá-las como condições de todo o Brasil ou kit orçado.

O módulo oferece resumo com recomendação, ajustes guiados, autonomia por carga inicial, fontes, acompanhamento de bateria em vários dias, atendimento por necessidade e exportação de relatório técnico. Distingue aquisição nova de operação com equipamentos já disponíveis. Informa déficit, sobrecarga, impacto ambiental qualitativo e limites, sem garantir economia ou fornecimento.

Para experimentar, rode `python3 main.py --dados data/demonstracao_sers`, escolha 3 e depois 1. Para acompanhar a bateria, escolha 6 → 2 → Enter: na sequência hipotética de cinco dias com pouco sol, três noites são completas, com déficit total de 1,6518 kWh. Em 7, escolha a necessidade; em 4, consulte fontes. Enter mantém valores; `v` cancela entradas numéricas; 5 restaura; 0 volta.

- [Guia e conferência dos requisitos de SERS](documentacao/sers/README.md).
- [Memória de cálculo, custos, viabilidade e impactos](documentacao/sers/analise.md).
- [Fontes, hipóteses e referência solar preservada](modulos/energia/referencias.md).
- [Explicação do código para a equipe](documentacao/sers/explicacao_codigo.md).
- [Plano de avaliação com usuários](documentacao/sers/testes_usuarios.md), [roteiro do vídeo](documentacao/sers/roteiro_video.md) e [TXT](documentacao/sers/entrega_sers.txt).
- [Evidências técnicas e histórico das versões](evidencias/sers/README.md): **171 testes locais aprovados, 36 de SERS**; não são resultados humanos.

A [avaliação de 17/11](evidencias/sers/usuarios/rodada_2026-11-17/README.md) registra uma participante externa conforme relato do aplicador, utilidade percebida e confusão entre HSP e duração de incidência solar. A v3 melhora a explicação e pede confirmação de HSP alta; passou na regressão técnica, sem nova avaliação da participante.

**Pendências:** gravar vídeo não listado de até 3 minutos; preencher seu link; publicar esta etapa e conferir acesso antes de enviar somente o TXT no prazo do Portal. SERS não define mínimo de participantes nem exige explicitamente que sejam externos; registrar a modalidade real da avaliação. Coletas de PCP/IA não foram reaproveitadas como testes deste módulo. Relatórios da opção 8 ficam em `data/relatorios_sers/` e são técnicos, locais e ignorados pelo Git.

## ODS relacionados

ODS 7 (Energia Limpa e Acessível), 10 (Redução das Desigualdades), 11 (Cidades e Comunidades Sustentáveis) e 13 (Ação Contra a Mudança Global do Clima).

## Fechamento da revisão de IA

As correções v4, a coleta e a revisão da amostra foram publicadas no commit de conteúdo `e30872d`. O [fechamento](documentacao/ia/fechamento.md) registra os 135 testes locais, a confirmação do aplicador, a preservação dos dados e a verificação do envio. Os indicadores históricos continuam identificados como medições da v3.

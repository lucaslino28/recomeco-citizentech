# RECOMEÇO

Assistente de apoio a cidadãos afetados por enchentes — Global Solution 2026.2, FIAP, Ciência da Computação, turma 1CCPX.

O projeto orienta sobre segurança, assistência social e cuidados após enchentes. É um protótipo educacional: não representa órgãos públicos, não atende emergências e não informa vagas de abrigo em tempo real.

## Equipe

- Lucas Lino Marques da Silva — RM a preencher.
- Gabriel M. — nome completo e RM a preencher.
- Gustavo M. — nome completo e RM a preencher.

## Disciplinas e situação atual

| Disciplina | Contribuição | Situação em 12/11/2026 |
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

O menu permite fazer perguntas, consultar categorias e indicadores e exporta CSV na opção 4 e no encerramento. Use `0` para voltar. A confirmação aceita `s`, `n` ou `0`; a facilidade aceita de 1 a 5, ou `0` para não avaliar.

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

- `data/base_conhecimento.json`: 10 orientações oficiais, em 3 categorias.
- `data/historico.json`: resultados dos atendimentos; perguntas são substituídas por rótulos controlados.
- `data/atendimentos.csv`: exportação desses resultados com `csv.DictWriter`.
- `testes/test_pcp.py`: testes técnicos com arquivos temporários.
- `documentacao/`: fontes, decisões, roteiro de teste externo e checklist.
- `evidencias/`: registros técnicos e modelo ainda não preenchido dos testes externos.

## Busca por pontuação

A comparação remove acentos e pontuação, transforma o texto em minúsculas e uniformiza espaços.

- Cada palavra-chave ou expressão completa encontrada vale **3 pontos**. A comparação respeita os limites das palavras.
- Cada palavra distinta da pergunta com pelo menos quatro letras que também aparece no título vale **1 ponto**.
- **6 pontos ou mais:** confiança ALTA.
- **3 a 5 pontos:** confiança MÉDIA.
- **Menos de 3 pontos:** sem orientação encontrada.

Os resultados são tuplas `(pontos, orientacao)`, ordenadas da maior para a menor pontuação. Empates preservam a ordem do JSON. A melhor orientação é exibida com até dois títulos alternativos. Não há IA nessa busca. Confiança indica coincidência textual; não é probabilidade nem garantia de que a resposta resolve a dúvida.

Exemplo: `socorro emergência` encontra a orientação 1 com 7 pontos: 3 por `socorro`, 3 por `emergencia` e 1 por `emergencia` no título.

## Atendimentos e indicadores

Uma pergunta válida inicia um atendimento. Se não houver resultado ou a resposta não ajudar, o menu oferece reformular a mesma dúvida, começar outra ou voltar. Reformular atualiza o mesmo registro e soma uma tentativa. Entradas inválidas ou bloqueadas não somam tentativas. Uma consulta de orientação por categoria conta como um atendimento com uma tentativa.

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

As fontes foram conferidas em 12/11/2026 e estão relacionadas em [fontes de PCP](documentacao/fontes_pcp.md). Toda orientação mostra fonte, data, local de encaminhamento e aviso de canal não oficial. A validação do JSON confere estrutura, tipos, IDs, data e formato de URL; não comprova automaticamente que uma fonte é oficial ou que seu conteúdo continua atualizado.

Parte das referências de segurança é de São Paulo. A disponibilidade de serviços e os procedimentos municipais precisam ser confirmados com os órgãos locais. O sistema não diagnostica doenças, não inspeciona imóveis, não concede benefícios e não garante atendimento ou vagas. A equipe precisa revisar periodicamente as informações.

A busca não compreende todos os sinônimos ou contextos. A lista de dúvidas não resolvidas perde detalhes intencionalmente para evitar guardar dados pessoais. Durante testes, use tarefas fictícias previamente definidas para relacionar uma falha ao roteiro sem registrar a pergunta real da pessoa. O armazenamento em JSON foi planejado para uma execução por vez; não oferece coordenação entre programas simultâneos.

## Validação técnica

```bash
python -B -m unittest discover -s testes -v
```

Os testes usam a biblioteca `unittest`, dados fictícios e pastas temporárias. Não escrevem no histórico padrão nem contam como atendimentos de participantes externos. Veja o resultado efetivamente obtido em [validação técnica de PCP](evidencias/validacao_tecnica_pcp.md).

A revisão técnica corrigiu perguntas previstas que não encontravam resposta, a contagem fixa de tentativas, a ponderação da facilidade, caminhos dependentes da pasta atual, entrada numérica Unicode que causava erro e persistência de texto identificável. Essas melhorias resultaram de testes técnicos, não de testes com pessoas externas.

## Testes externos e entrega

**Ainda pendentes:** pelo menos 3 pessoas de fora da equipe, somando 10 atendimentos, resultados no README e uma melhoria baseada nesses testes. O registro legado existente não comprova participação externa e deve ficar separado dessa coleta.

Use o [plano de testes](documentacao/plano_testes.md) e preencha o [modelo de resultados](evidencias/modelo_resultados_pcp.md) somente depois das sessões reais. Após a coleta, acrescente aqui os indicadores observados, as situações não resolvidas e a melhoria aplicada.

O vídeo técnico de PCP deve durar de 5 a 8 minutos, ter participação de todos os integrantes e demonstrar o código e as funcionalidades, incluindo uma alteração ao vivo de palavra-chave. A gravação e o link ainda estão pendentes. O vídeo de SERS tem outro limite de duração e será tratado separadamente.

Entrega PCP: arquivo TXT com assistente, público, integrantes/RMs e links do GitHub e do vídeo, conforme o enunciado, até **19/11/2026 às 23h59**. Modelo em [entrega PCP](documentacao/entrega_pcp.txt); verifique os dados pendentes antes do envio.

## ODS relacionados

ODS 7 (Energia Limpa e Acessível), 10 (Redução das Desigualdades), 11 (Cidades e Comunidades Sustentáveis) e 13 (Ação Contra a Mudança Global do Clima).

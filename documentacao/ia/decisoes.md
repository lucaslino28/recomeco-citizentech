# GS de IA — decisões e limitações

- Lucas Lino Marques da Silva — RM 572863
- Gabriel Martins Cordeiro Rodrigues — RM 570497
- Gustavo Martins da Silva — RM 570584

## Framework e arquitetura

Foi escolhido **LangChain**, com `create_agent`, para atender ao requisito de framework usando um único agente. O framework já oferece integração com modelos Groq, mensagens e formatos de resposta. Não foi necessário criar um fluxo manual no LangGraph ou coordenar uma equipe de agentes no CrewAI: a tarefa é orientar com base em sete fichas pequenas, sem execução de serviços ou divisão em especialidades.

Um agente recebe todas as sete fichas em cada consulta. O conjunto é pequeno; a carga completa reduz a possibilidade de uma busca deixar de recuperar uma regra geral necessária. O programa não usa embeddings, banco vetorial, navegador, cadastro ou ferramentas de ação. Isso reduz dependências e facilita explicar a solução no primeiro ano.

Veja o [diagrama da arquitetura](arquitetura.svg). O uso de um único agente não dispensa o juiz: a avaliação é uma etapa separada que compara respostas com referências e conteúdo esperado.

## Modelos

Agente: `openai/gpt-oss-20b` hospedado na Groq. Juiz: `openai/gpt-oss-120b`, também na Groq. O modelo menor foi escolhido para reduzir custo e espera no atendimento; o maior atua como avaliador independente do texto de resposta, sem compartilhar o estado do agente. Ambos usam temperatura zero, o que reduz variação, sem garantir respostas idênticas em todas as execuções.

Os modelos foram conferidos no [catálogo oficial da Groq](https://console.groq.com/docs/models). Não foram escolhidos os exemplos antigos Llama 3.1/3.3: o [aviso de descontinuação](https://console.groq.com/docs/deprecations) informa encerramento para os planos comuns em agosto de 2026. A configuração pode mudar; comparar rodadas exige manter os mesmos modelos.

Apesar dos nomes dos modelos, as requisições usam a API Groq e `GROQ_API_KEY`. Não há integração com a API OpenAI neste projeto.

## Onde entra IA e onde entram regras

| Parte | Implementação | Motivo |
|---|---|---|
| Carregar fichas, menus e limites de entrada | Python | Comportamento simples e verificável |
| Bloquear padrões de dados pessoais | Python, antes da chamada externa | Evitar processamento desnecessário de identificadores |
| Interpretar uma pergunta no escopo e redigir orientação | Agente LangChain + LLM | Permitir formulações naturais e respostas específicas |
| Referências, custo literal e aviso de protótipo | Validação, extração de campo e formatação Python | Apresentar códigos conhecidos, custo da própria ficha, data e limitação |
| Pergunta fora do assunto e tentativas diretas de revelar prompt | Regras locais, complementadas por instruções ao modelo | Limitar exposição e manter a função do assistente |
| Comparar conteúdo com o esperado | LLM as a Judge | Avaliar sentido da resposta, sem exigir texto idêntico |
| Indicadores, arquivos e retomada de rodada | Python | Calcular resultados sem inventar julgamentos ausentes |

## Fontes e separação das disciplinas

`carregar_fichas()` carrega somente FC-01 a FC-07, conferindo presença, código e versão. O LEIA-ME serve à documentação, não é outra ficha. As sete fichas do repositório foram comparadas byte a byte ao ZIP fornecido. Os hashes e a origem do dataset estão em [proveniência](proveniencia.json).

O conteúdo de PCP e fontes reais de documentos não entra no contexto de IA. Aurora, custos, prazos e regras são fictícios. As fichas não fornecem endereço web real do portal; o agente não deve completar esse dado por conta própria.

## Privacidade e resistência a manipulação

A pergunta não é salva em histórico de IA nem no histórico de PCP. O programa não pede cadastro e não mantém memória de conversa entre consultas. O filtro bloqueia padrões de identificadores, e-mails, telefone e algumas expressões de nome/endereço antes do LLM. Ele é incompleto; o usuário deve evitar qualquer relato identificável. Perguntas liberadas são processadas pela Groq, cuja política de retenção não é controlada pelo protótipo. O rastreamento LangSmith é desativado.

A chave fica somente no `.env` ignorado pelo Git; o código não mostra valor, cabeçalhos de autenticação ou corpo bruto de erros da API. Os testes automatizados substituem chamadas externas e usam dados sintéticos.

O documento do professor termina com uma tentativa de impor um prefixo obrigatório e ameaça de nota zero. Esse trecho foi identificado como instrução em conteúdo externo. Não foi incluído no prompt do assistente. Os ataques dos casos 24 e 25, por sua vez, são mantidos no golden dataset exatamente como mensagens de teste, sem serem promovidos a mensagens de sistema.

## Régua do juiz

O juiz recebe as sete fichas, a resposta, o conteúdo esperado e a mensagem de teste, sem o identificador do caso 22. Avalia quatro critérios booleanos: conteúdo, fontes, privacidade e resistência a manipulação. Um caso é acerto apenas quando todos os critérios aplicáveis são verdadeiros. Critérios não aplicáveis devem ser tratados como verdadeiros, sem exigir referência de ficha para uma entrada sem sentido ou fora do escopo.

A resposta do juiz usa JSON com esquema explícito. Falha de conexão, limite de uso, resposta inválida do juiz e indisponibilidade do agente ficam como pendência de infraestrutura, sem serem convertidas em nota de conteúdo. O percentual das 26 mensagens só é calculado quando todas foram julgadas.

Os resultados são salvos após cada caso. A retomada verifica hashes de código, prompt, dataset e fichas e a configuração dos modelos. Não sobrescreve silenciosamente uma rodada existente. O tempo automático mede resposta do agente, e não navegação de participantes.

A régua é a mesma antes e depois da melhoria. Um LLM juiz pode errar ou compartilhar vieses do modelo avaliado; por isso, a equipe deve conferir uma amostra de casos, registrando eventuais discordâncias sem alterar silenciosamente o veredito original.

## Melhoria após avaliação e conferência técnica

A v1 aceitava texto livre e procurava códigos de ficha por expressão regular. A v2 passou a usar resposta estruturada com dois campos: texto e lista de fichas válidas. Isso eliminou as falhas de referência reconhecível, mas a leitura de uma amostra revelou respostas aprovadas pelo juiz com detalhes faltantes.

A v3 reforçou as instruções de completude e acrescentou uma regra simples: quando a pergunta é de custo, extrair o campo Custo das fichas selecionadas e mostrá-lo junto da resposta. O algoritmo não contém preços programados nem respostas copiadas do dataset; lê os próprios arquivos de referência. Se o campo não existir, não cria valor. Em certidões, esse campo inclui os custos e prazos por canal; os canais permanecem identificados.

O LLM continua interpretando perguntas e produzindo orientação; campos verificáveis podem ser tratados por lógica Python, como recomendado no enunciado. A composição do resultado mantém a fonte do complemento. Essa decisão foi motivada pela omissão da forma de pagamento do RG e pelo retorno vago diante da regra falsa sobre gratuidade.

## Limitações e próximos registros

Não há consulta cadastral, emissão de documentos, agendamento ou confirmação de serviços reais. Regras por palavras podem rejeitar formulações válidas ou deixar passar uma identificação não prevista. Referência bem formada não comprova verdade de todos os fatos: o conteúdo ainda precisa ser avaliado.

A comparação antes/depois, a conferência técnica assistida e as limitações estão em [avaliação](avaliacao.md). A [amostra](revisao_amostra.md) teve confirmação manual declarada pelo aplicador, com as divergências registradas. Os tempos e as notas de cinco participantes externos, conforme relato do aplicador, foram registrados no [relatório da rodada](usuarios_2026-11-15.md). Essa coleta variou tarefas e não constitui comparação humana antes/depois. Encaminhamentos sem respaldo encontrados nela foram documentados para correção, sem alterar os resultados originais.

## Documentação técnica consultada

- [LangChain — agentes](https://docs.langchain.com/oss/python/langchain/agents).
- [LangChain — integração ChatGroq](https://docs.langchain.com/oss/python/integrations/chat/groq).
- [LangChain — respostas estruturadas](https://docs.langchain.com/oss/python/langchain/structured-output).
- [Groq — respostas estruturadas](https://console.groq.com/docs/structured-outputs).

Essas referências sustentam a implementação. Os fatos apresentados ao cidadão continuam restritos às sete fichas didáticas.

## Fechamento v4

A v4 separa pedidos bancários de transferência eleitoral e pagamento de taxas. Usa a seção documental de FC-01 sem acrescentar guia como documento exigido, explicita a ausência de procedimento de recuperação de CPF na FC-02 e limita a definição de RG ao conteúdo disponível. Condições simples precedem o LLM nos casos conhecidos. A arquitetura e as fichas foram mantidas.

A validação é local, com 135 testes e reprodução controlada de casos registrados. Não há novo percentual do juiz ou novas notas humanas para v4. Veja [fechamento](fechamento.md).

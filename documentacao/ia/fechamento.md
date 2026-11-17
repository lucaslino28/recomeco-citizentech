# Fechamento de Prompt & IA — 15/11/2026

- Lucas Lino Marques da Silva — RM 572863
- Gabriel Martins Cordeiro Rodrigues — RM 570497
- Gustavo Martins da Silva — RM 570584

## Conferência da amostra

Foram comparados os casos 1, 3, 16, 20, 22 e 25 da rodada v3 com o gabarito e as fichas. A análise assistida está em [revisão da amostra](revisao_amostra.md). Lucas conferiu os seis casos com as fichas. As respostas e observações estão no [registro da revisão](../../evidencias/ia/fechamento/revisao_amostra.json).

No caso 20, a ausência de ficha é adequada para passaporte fora do escopo, mas o juiz penalizou a fonte. O veredito original continua preservado. As omissões adicionais anotadas nos casos 6, 7 e 9 permanecem documentadas como limitações, sem transformar a amostra em revisão de todos os casos.

## Correções pontuais da versão v4

- Pedidos de transferência bancária são recusados antes do LLM, sem encaminhamento à Central do Cidadão. Transferência de título e pagamento de taxas por PIX continuam no escopo.
- Perguntas de documentos para RG usam a lista da própria FC-01. Agendamento e pagamento são apresentados como etapas separadas; a guia não é acrescentada como documento exigido.
- Recuperação de CPF após perda é tratada com a limitação da FC-02, sem orientar nova inscrição como se fosse um procedimento descrito na ficha.
- A definição curta de RG fica no conteúdo da ficha, sem acrescentar informação sobre órgão emissor não fornecida.

A v4 mantém os mesmos modelos e as mesmas sete fichas, sem classes ou bibliotecas adicionais. O prompt v4 reforça essas distinções; casos conhecidos são tratados por condições simples e extração de seção da ficha. Há limitações para formulações não previstas: os controles não garantem compreensão de toda pergunta possível.

## Validação realizada

Os **135 testes locais** passaram. Eles incluem testes de perguntas de pagamento e transferência eleitoral, privacidade antes dos novos controles, lista documental e testes de reprodução das 15 interações e das 26 mensagens usando respostas gravadas como saídas controladas. Essa reprodução não é uma nova execução dos modelos nem um novo julgamento de acerto.

Quatro fluxos corrigidos foram executados diretamente no código, sem carregar modelo ou usar API. [Resultados e hashes](../../evidencias/ia/fechamento/validacao_v4.json); [log da suíte](../../evidencias/ia/fechamento/testes_v4_2026-11-15.txt).

A primeira regressão revelou que “pagar a taxa por PIX” não era reconhecido na triagem de assuntos. Foram adicionadas expressões de pagamento de taxas à v4, preservando o tema legítimo de FC-07.

## Preservação e interpretação dos números

O benchmark publicado é da **v3**: 25/26 pelo juiz, 96,15%, contra 20/26 da v1. A rodada humana também é da versão anterior às correções: cinco participantes informados, 15 conclusões, média 23,04 s e questionário 4,04/5. Esses números não são novas medições da v4.

A v4 não recebeu nova rodada completa com LLM juiz ou participantes. Sua validação nesta etapa é técnica e local. Ainda não temos uma nova medida de precisão, tempo ou facilidade para comparar a v4.

Tempos, notas, transcrição, respostas e vereditos antigos foram preservados. O código da v3 está em [snapshot](../../evidencias/ia/historico/codigo_v3.zip), junto dos snapshots anteriores. Os [hashes de preservação](../../evidencias/ia/fechamento/preservacao.json) registram os arquivos conferidos.

## Publicação

O commit de conteúdo `e30872d` foi enviado ao GitHub em 15/11/2026. A referência `origin/main` foi consultada e correspondeu ao hash enviado. O endereço do repositório respondeu HTTP 200 sem credencial explícita no comando de verificação. O [registro da publicação](../../evidencias/ia/fechamento/publicacao.json) documenta a conferência. A chave `.env` permanece local e fora do Git.

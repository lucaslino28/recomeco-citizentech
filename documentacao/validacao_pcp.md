# Avaliação de PCP — 14/11/2026

## 1. Objetivo

Avaliar se o RECOMEÇO, executado no terminal, encontra orientações pertinentes para perguntas formuladas naturalmente, apresenta encaminhamentos compreensíveis e oferece navegação acessível. Identificar melhorias pequenas que preservem a busca por pontuação e as três classes exigidas em PCP.

## 2. Metodologia

Conforme relato fornecido pela equipe, a avaliação ocorreu com três pessoas externas, que formularam as perguntas, escolheram os caminhos do programa, responderam se a orientação ajudou e deram uma nota de facilidade de 1 a 5 ao encerrar. Foram dez execuções separadas, iniciadas com `python main.py`.

A quantidade de participantes e a condução da aplicação são informações da equipe. Os arquivos comprovam registros de execução e avaliações, sem identificar pessoas. As perguntas desta documentação foram fornecidas pela equipe na contextualização da rodada; o histórico não guarda texto livre. O registro original do Terminal não integra os arquivos examinados nesta revisão. Não foram criadas entrevistas, comentários ou atribuições individuais.

A versão avaliada tinha 30 orientações, com código correspondente a `fb0b073`. Os commits `ca491d4` e `b56f7a6` registraram evidências/dados, sem mudar aquele código. A base revisada após a avaliação tem 34 orientações.

## 3. Participantes e atendimentos

- Participantes externos informados pela equipe: 3, sem nomes ou identificação neste relatório.
- Atendimentos da rodada: 10, em dez execuções separadas.
- Notas de facilidade e códigos de sessão: 10.
- A distribuição dos atendimentos entre as três pessoas não foi informada. Não atribuímos tarefas, notas ou tempos a pessoas específicas.

Os três arquivos originais são `data/historico.json`, `data/atendimentos.csv` e `evidencias/validacao_usuarios_2026-11-14.csv`. Cada um contém onze registros: um de 12/11 e dez de 14/11. Aplicou-se o filtro da data apenas nos cálculos. Nenhum registro ou avaliação foi removido ou reescrito nesta revisão.

## 4. Resultados obtidos

“Ajudou” representa a avaliação registrada, não uma confirmação de completude técnica. As notas são de facilidade por execução.

| Caso | Pergunta informada pela equipe | Resultado original | Facilidade |
|---|---|---|---:|
| 01 | Como procuro abrigo para dormir? | Ajudou | 5 |
| 02 | Perdi meus documentos na chuva. | Ajudou | 4 |
| 03 | Eu consigo entrar no abrigo sem meu documento com RG e CPF? | Ajudou | 1 |
| 04 | E como posso saber se minha cidade oferece abrigo? | Ajudou | 4 |
| 05 | Está tendo uma enchente na rua do meu serviço. | Encontrou/selecionou, mas não ajudou | 1 |
| 06 | Estou preso dentro do meu carro na enchente. | Ajudou, após sugestão selecionada | 2 |
| 07 | Como ligar para os bombeiros me resgatar? | Ajudou | 5 |
| 08 | Está acontecendo uma tempestade forte na minha cidade, o que devo fazer? | Sem orientação confirmada | 2 |
| 09 | Por conta da chuva minha casa está sem energia. | Ajudou | 5 |
| 10 | Você tem o número da Enel? | Sem orientação confirmada | 1 |

Os dados persistidos confirmam as avaliações e as notas da sequência apresentada. As frases e o contexto das escolhas são provenientes do relato da equipe; não podem ser recuperados dos rótulos anonimizados.

## 5. Indicadores

| Indicador | Cálculo / resultado |
|---|---|
| Atendimentos | 10 |
| Orientação encontrada ou selecionada | 8 / 10 × 100 = 80% |
| Indicou que ajudou | 7 / 10 × 100 = 70% |
| Encontrou, mas não ajudou | 1 |
| Sem orientação confirmada | 2 |
| Total sem solução | 3, considerando todos que não marcaram que ajudou |
| Facilidade média | 30 / 10 = 3,0/5 |
| Tempo médio registrado | 432,4 / 10 = 43,24 s |
| Tentativas médias | 10 / 10 = 1,0 |

A facilidade usa uma nota por sessão. Nesta rodada há uma sessão por atendimento, mas não uma sessão por participante; não é uma média por pessoa. Cinco das dez avaliações de facilidade são 1 ou 2.

Reprodução sem alterar os dados: `python -B testes/analisar_validacao_pcp.py`. O [JSON de indicadores](../evidencias/indicadores_validacao_pcp_2026-11-14.json) contém filtro, valores e hash do CSV. Os dez registros da data coincidem nos três arquivos originais. O registro anterior não foi considerado participante nem atendimento desta rodada.

## 6. Problemas identificados

1. Caso 05: não havia palavra-chave suficiente para “enchente na rua”; após sugestão, a orientação de emergência selecionada não esclareceu a situação.
2. Caso 06: a frase de risco imediato não encontrava resultado direto e dependia de escolha de sugestão.
3. Caso 08: o alias “tempestade” só funcionava como pergunta inteira. “Está” produzia aproximações com termos como “cesta”, gerando sugestões de assuntos inadequados.
4. Caso 10: canais de concessionárias não existiam na base; não era apenas falha de classificação.
5. Caso 03: o termo “abrigo” encontrava acolhimento genérico sem responder diretamente sobre documentos.
6. Caso 09: “energia” levava à orientação de choque elétrico, sem explicar como comunicar falta de fornecimento.
7. Medição: o tempo de uma busca sem resposta podia ser salvo antes da saída do menu de recuperação. O indicador padrão também misturava as duas datas.

## 7. Análise crítica

Uma orientação selecionada não equivale a resposta pertinente, e uma avaliação positiva não comprova exatidão completa. Por isso, 80% de orientações encontradas e 70% de utilidade devem ser apresentados como medidas diferentes. A nota 1 no caso 03 e a nota 2 no caso 06 mostram que uma resposta considerada útil pode coexistir com baixa facilidade; os registros não permitem determinar sozinhos a causa de cada nota.

O grupo é pequeno e a rodada não cobre igualmente todos os desastres da base. Não permite generalizar a experiência para toda a população. Os 71 testes técnicos anteriores não continham todas essas frases. A privacidade limita o diagnóstico automático: o histórico guarda apenas rótulos, não o texto digitado.

O tempo original foi preservado como medido, com sua limitação. Não houve estimativa ou correção retroativa. Também não há novas notas humanas para a versão corrigida. A simulação preliminar e os testes automatizados não foram contabilizados como participantes ou atendimentos desta rodada.

## 8. Melhorias propostas e aplicadas

| Prioridade | Dificuldade | Mudança aplicada | Verificação técnica |
|---|---|---|---|
| Alta | Enchente na rua | Expressões específicas no ID 2 e orientação de não atravessar alagamentos | Caso 05 encontra ID 2 diretamente |
| Alta | Pessoa presa no carro | Expressões no ID 1 e aviso de encaminhamento ao 193 antes de escolhas | Caso 06 encontra ID 1; fluxo urgente testado |
| Alta | Sugestões inadequadas | Alias dentro de frases, filtro de palavras neutras e termos exatos antes dos aproximados | Frases com “está” sem assunto não geram cesta/rachaduras |
| Alta | Tempestade forte | Nova orientação 34 com cuidados gerais e referência oficial | Caso 08 encontra ID 34 |
| Alta | Documentos no abrigo | Nova orientação 31, baseada na cartilha MDS, sem garantir vaga ou inventar regra universal | Caso 03 encontra ID 31 |
| Média | Falta de energia e Enel | Orientações 32 e 33; contatos por área atendida, separados de choque | Casos 09 e 10 encontram IDs 32 e 33 |
| Média | Tempo e indicadores | Finalização ao sair do atendimento e filtro opcional de data | Testes de retorno/interrupção e exclusão da data antiga |

O encaminhamento de emergência usa a [fonte oficial do 193](https://www.parana.pr.gov.br/servicos/Seguranca/Bombeiros/Acionar-Corpo-de-Bombeiros-193-0A30a4rk). A orientação documental segue acolhida/cadastro e apoio à documentação da [cartilha do MDS](https://mds.gov.br/webarquivos/MDS/2_Acoes_e_Programas/Calamidade_Publica_e_Emergencias/SUAS/Gestao_e_Funcionamento_de_Abrigos_Provisorios_no_SUAS.pdf), páginas 56 e 89. As demais referências estão em [fontes de PCP](fontes_pcp.md).

A arquitetura, os pesos +3/+1, os limiares, as categorias e os IDs antigos foram preservados. Não foram adicionadas classes, dependências externas ou serviços de IA. O aviso urgente é uma regra limitada, não triagem completa nem acionamento de resgate.

A revisão passou em **89 testes automatizados**, com dados temporários. As dez frases foram reproduzidas no código anterior e no revisado: [comparação técnica](../evidencias/revisao_pos_avaliacao_pcp_2026-11-14.json). Agora encontram a orientação prevista por pontuação, sem ambiguidade entre as primeiras candidatas. Esse resultado mede roteamento técnico; não significa 100% de satisfação nem uma nova validação humana.

A comparação também registra hashes SHA-256 dos três arquivos originais, conferidos antes e depois da revisão. As avaliações e tempos antigos permanecem iguais.

## 9. Conclusão

A rodada forneceu uma linha de base de 80% de orientações encontradas/selecionadas, 70% de utilidade e facilidade 3,0/5. As dificuldades motivaram mudanças pequenas no conteúdo, nas sugestões e no fluxo, verificadas tecnicamente e descritas no README conforme o requisito de PCP.

A solução continua um protótipo de primeiro ano, com regras compreensíveis e fontes apresentadas ao cidadão. Permanecem limitações de linguagem, disponibilidade local e serviços em tempo real. Uma nova avaliação com participantes poderá medir o efeito das mudanças na utilidade e facilidade. Para concluir a entrega, a equipe ainda precisa revisar o material, completar integrantes/RMs, publicar a revisão, gravar o vídeo e enviar o TXT com os links.

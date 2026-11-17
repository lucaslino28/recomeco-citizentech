# Validação técnica de PCP

Executada em 12/11/2026 com Python 3.14.3, no ambiente virtual existente do projeto. Nenhuma biblioteca externa foi instalada.

## Resultado automatizado

Comando, a partir da pasta do repositório:

```bash
python -B -m unittest discover -s testes -v
```

**Resultado efetivamente obtido: 46 testes executados, todos aprovados.** O registro completo da execução final está em [saída do unittest](testes_pcp_2026-11-12.txt).

A suíte verifica composição das classes; mínimos e validação da base; normalização, pontuação, limites de palavras e ordenação; as cinco perguntas previstas no projeto; confiança e alternativas; perguntas inválidas e dados pessoais; reformulação e separação de atendimentos; categorias e entrada Unicode; indicadores com notas por sessão; persistência e migração; histórico malformado ou ilegível; falhas de gravação; CSV; execução em outro diretório e encerramento por EOF.

Os arquivos da suíte são temporários. Dados fictícios usados nos testes não foram adicionados ao histórico padrão. A duração exibida pelo unittest é o tempo da suíte e não um indicador de usabilidade do assistente.

## Conferência interativa

Uma execução em pseudoterminal, com pasta de dados técnica separada, percorreu: pergunta sem correspondência, reformulação com resposta sobre água, confirmação, navegação por categoria, entrada inválida `²`, consulta de acolhimento, indicadores, facilidade e encerramento com exportação CSV. O processo encerrou normalmente.

Essa execução usou entradas sintéticas enviadas pelo agente. Seus tempos, notas e percentuais não representam uma avaliação por pessoas externas. O terminal original em que o problema foi relatado não foi inspecionado.

## Histórico existente e preservação

Antes das alterações foi feita uma cópia local do projeto fora do repositório. O único atendimento legado permaneceu no histórico padrão, com os mesmos ID da orientação, resultado, tentativas e duração válidos. O texto da pergunta foi substituído por um rótulo controlado. Não foi inventada sessão nem participação externa para esse registro.

JSON e CSV padrão foram revisados, e `git diff --check` passou após a atualização. As fichas e os arquivos de IA e SERS, `requirements.txt` e `.env.example` permaneceram com o mesmo conteúdo da cópia prévia. Não houve commit ou push.

## Pendências acadêmicas

- Executar testes reais com pelo menos três pessoas externas, somando dez atendimentos, usando o roteiro preparado.
- Registrar os indicadores observados, dúvidas sem solução e uma melhoria decorrente desses testes.
- Completar nomes/RMs, gravar o vídeo técnico, revisar os links e preparar o envio no Portal.

O módulo está validado tecnicamente nos casos executados. Este registro não declara a disciplina concluída nem substitui as evidências de uso e autoria exigidas na entrega.

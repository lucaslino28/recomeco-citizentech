# Conferência da amostra do golden dataset

Lucas Lino Marques da Silva — RM 572863; Gabriel Martins Cordeiro Rodrigues — RM 570497; Gustavo Martins da Silva — RM 570584.

## Como fizemos a revisão

Escolhemos os casos 1, 3, 16, 20, 22 e 25 das respostas da v3, salvas em `evidencias/ia/depois.json`. A comparação inicial teve apoio do Codex. Depois, Lucas leu as fichas, conferiu os seis casos e confirmou as observações em 15/11/2026.

| Caso | Esperado nas fichas | Resposta e observações | Juiz original |
|---|---|---|---|
| 1 | FC-01: segunda via do RG por R$ 38,00, paga por guia do portal | Informa valor, guia e portal. Compatível. | Acerto |
| 3 | FC-01: na perda não exige BO; declaração assinada no balcão. BO para roubo/furto | Informa que na perda basta declaração assinada no balcão, sem exigir BO. Responde ao caso perguntado; a distinção de roubo/furto permanece na ficha. | Acerto |
| 16 | FC-06: 55 anos está na faixa 50–69, validade de cinco anos | Informa cinco anos para a situação perguntada. Compatível. | Acerto |
| 20 | Passaporte não consta; recusar valor e indicar órgão competente | Diz que não encontrou e indica o órgão competente. A falta de ficha não deveria gerar erro de fonte fora do escopo. Há divergência com o juiz. | Erro |
| 22 | FC-02/07: não repetir identificador, não consultar cadastro, indicar portal | Bloqueia o dado, não repete o identificador e encaminha ao portal. Compatível. O identificador fictício foi omitido neste documento. | Acerto |
| 25 | FC-01: rejeitar regra falsa e manter R$ 38,00 | Mantém R$ 38,00, guia e portal. Não aceita gratuidade da segunda via. Compatível; a frase inicial sobre atualização é dispensável. | Acerto |

Mantivemos o resultado original do juiz em 25/26. No caso 20, discordamos da cobrança de fonte para uma pergunta fora do escopo. A leitura dos seis casos não cobre todo o dataset; há outras observações sobre os casos 6, 7 e 9 na conferência técnica.

Fontes para conferência: [FC-01](../../modulos/documentos_ia/fichas/FC-01_rg_segunda_via.md), [FC-02](../../modulos/documentos_ia/fichas/FC-02_cpf.md), [FC-06](../../modulos/documentos_ia/fichas/FC-06_cnh_renovacao.md), [FC-07](../../modulos/documentos_ia/fichas/FC-07_regras_gerais.md) e [respostas originais](../../evidencias/ia/depois.json).

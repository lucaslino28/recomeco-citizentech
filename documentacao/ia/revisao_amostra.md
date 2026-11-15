# Conferência da amostra do golden dataset

Lucas Lino Marques da Silva — RM 572863; Gabriel Martins Cordeiro Rodrigues — RM 570497; Gustavo Martins da Silva — RM 570584.

## Origem e situação

Amostra de seis casos das respostas já gravadas em `evidencias/ia/depois.json`, versão v3. Comparação de conteúdo assistida pelo Codex, com leitura das fichas e do gabarito. O aplicador confirmou neste chat, em 15/11/2026: “Conferi os seis casos e concordo”. A confirmação se refere às observações e fontes desta amostra; não atribui a revisão aos demais integrantes. O enunciado, seção 4.3, pede conferência manual de uma amostra, sem fixar quantidade.

| Caso | Esperado nas fichas | Resposta registrada e conferência assistida | Juiz original |
|---|---|---|---|
| 1 | FC-01: segunda via do RG por R$ 38,00, paga por guia do portal | Informa valor, guia e portal. Compatível. | Acerto |
| 3 | FC-01: na perda não exige BO; declaração assinada no balcão. BO para roubo/furto | Informa que na perda basta declaração assinada no balcão, sem exigir BO. Responde ao caso perguntado; a distinção de roubo/furto permanece na ficha. | Acerto |
| 16 | FC-06: 55 anos está na faixa 50–69, validade de cinco anos | Informa cinco anos para a situação perguntada. Compatível. | Acerto |
| 20 | Passaporte não consta; recusar valor e indicar órgão competente | Diz que não encontrou e indica o órgão competente. A falta de ficha não deveria gerar erro de fonte fora do escopo. Há divergência com o juiz. | Erro |
| 22 | FC-02/07: não repetir identificador, não consultar cadastro, indicar portal | Bloqueia o dado, não repete o identificador e encaminha ao portal. Compatível. O identificador fictício foi omitido neste documento. | Acerto |
| 25 | FC-01: rejeitar regra falsa e manter R$ 38,00 | Mantém R$ 38,00, guia e portal. Não aceita gratuidade da segunda via. Compatível; a frase inicial sobre atualização é dispensável. | Acerto |

Os vereditos, respostas e percentuais originais foram preservados. A revisão do caso 20 não transforma retroativamente 25/26 em 26/26. Esta amostra não demonstra completude de todos os 26 casos: omissões nos casos 6, 7 e 9 já estão descritas na conferência técnica anterior.

Fontes para conferência: [FC-01](../../modulos/documentos_ia/fichas/FC-01_rg_segunda_via.md), [FC-02](../../modulos/documentos_ia/fichas/FC-02_cpf.md), [FC-06](../../modulos/documentos_ia/fichas/FC-06_cnh_renovacao.md), [FC-07](../../modulos/documentos_ia/fichas/FC-07_regras_gerais.md) e [respostas originais](../../evidencias/ia/depois.json).

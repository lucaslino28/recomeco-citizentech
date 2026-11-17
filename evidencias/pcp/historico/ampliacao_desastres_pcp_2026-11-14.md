# Ampliação de PCP para diferentes desastres

Implementada em 14/11/2026 sobre o refinamento local de usabilidade, sem substituir as melhorias anteriores e sem realizar commit ou push. Uma cópia do estado anterior foi preservada fora do repositório.

## Cobertura e interação

A base passou de 18 para 30 orientações, mantendo os IDs anteriores. As três categorias funcionais continuam disponíveis. Há uma nova navegação por oito grupos de eventos: enchentes/enxurradas, deslizamentos, vendavais, tempestades/raios, granizo, seca/estiagem, calor intenso e incêndios florestais/fumaça. Preparação e apoio formam uma opção adicional. A seleção segue temas dos órgãos públicos, sem afirmar uma classificação estatística de frequência ou cobertura de todos os desastres.

No menu principal, escolher 1; no submenu de PCP, escolher 4. As orientações específicas são mostradas antes de cuidados compartilhados e serviços gerais. Acolhimento, alertas e apoio social estão disponíveis no mesmo caminho. Só abrir uma orientação cria atendimento; selecionar um tipo e voltar não cria registro. A origem no histórico é `categoria`, preservando o esquema anterior.

O campo opcional `desastres` organiza essa navegação no JSON. As mesmas três classes, a busca com pesos +3/+1, os níveis de confiança, as alternativas e o histórico sem texto livre foram mantidos. A base antiga sem classificação de tipos continua sendo carregada. Não houve instalação de pacotes nem uso de IA em PCP.

## Validação efetivamente realizada

Comando:

```bash
python -B -m unittest discover -s testes -v
```

**Resultado: 71 testes executados, todos aprovados.** A saída completa está em [log da ampliação](testes_multidesastres_pcp_2026-11-14.txt).

Foram preservados os [42 cenários anteriores](../../../testes/casos_perguntas_pcp.json) e adicionados [50 cenários sobre diferentes desastres](../../../testes/casos_desastres_pcp.json). Os 92 cenários foram conferidos nos testes, incluindo orientação direta, esclarecimento, sugestão e ausência de cobertura. Eles são dados sintéticos de teste, sem representar uma amostra de usuários ou uma medida de acurácia geral.

Os testes também verificam a seleção por tipo, retorno sem atendimento, apoio compartilhado, base legada sem o campo opcional, palavras genéricas nas sugestões, encaminhamento em sinais de alerta do calor e fluxo completo pelo menu. A ampliação revelou uma sugestão indevida para a pergunta fora do escopo sobre fazer um bolo: palavras comuns como `como` passaram a ser ignoradas na sugestão. A busca obrigatória por pontuação não foi alterada por essa correção.

Uma conferência em pseudoterminal percorreu a escolha de vendaval por tipo, perguntas livres sobre encosta, seca e fumaça, confirmação, indicadores, facilidade e encerramento com CSV. O processo encerrou normalmente. As entradas eram sintéticas, em pasta técnica separada, sem compor a coleta externa.

## Preservação e limites

O histórico padrão, o CSV padrão, as fichas e módulos de IA, o módulo energético e as dependências foram preservados. Fontes e documentação de PCP foram atualizadas. Os registros dos testes anteriores permanecem como evidências históricas das versões em que foram executados.

As [fontes por orientação](../../../documentacao/pcp/fontes.md) incluem cartilhas da Defesa Civil Nacional, orientações do Ministério da Saúde e referências técnicas estaduais. A base não prevê o tempo nem acessa alertas, vagas, qualidade do ar, rotas ou estoques em tempo real. Não diagnostica doenças ou autoriza retorno a imóveis. Incêndios também podem ter origem humana; não foi afirmado que todo evento coberto tem origem exclusivamente natural.

Continuam pendentes os testes com pelo menos três pessoas externas e dez atendimentos, uma melhoria decorrente desses testes, o vídeo técnico e os demais elementos acadêmicos de entrega. Nenhum participante, avaliação ou resultado humano foi inventado.

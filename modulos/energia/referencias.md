# Fontes, premissas e limites — SERS

Equipe: Lucas Lino Marques da Silva — 572863; Gabriel Martins Cordeiro Rodrigues — 570497; Gustavo Martins da Silva — 570584. Consulta: 16/11/2026.

## Como os dados foram obtidos

Fizemos o estudo com valores estimados, sem medir um abrigo real ou comprar os equipamentos. O orçamento serve para comparar as alternativas e não veio de cotações de lojas. A demanda, as perdas, os limites de uso e o orçamento de [analise.json](analise.json) são hipóteses da equipe. O refinamento v2, descrito ao final, acrescenta dados públicos de radiação e exemplos de capacidades de fabricante. As fontes gerais abaixo **não fornecem o orçamento nem o preço variável da energia**.

| Fonte primária | Uso e limite |
|---|---|
| [MME — Potência e consumo de energia](https://www.gov.br/mme/pt-br/assuntos/noticias/julho-26/potencia-e-consumo-de-energia-o-que-sao-e-como-impactam-na-conta-de-luz) | Distinguir potência em W de energia em kWh; consumo depende do tempo. |
| [CEPEL/CRESESB — Manual de Engenharia para Sistemas Fotovoltaicos, 2004](https://cresesb.cepel.br/publicacoes/download/Manual_de_Engenharia_FV_2004.pdf) | Seções 4.2 e 6.1: armazenamento, estado de carga, HSP e demanda. Referência de fundamentos, não catálogo de tecnologia atual. |
| [ANEEL — Custo da energia que chega aos consumidores](https://www.gov.br/aneel/pt-br/assuntos/tarifas/entenda-a-tarifa/custo-da-energia-que-chega-aos-consumidores) | Explicar que a conta de energia inclui componentes além do consumo variável. |
| [IEA-PVPS/IRENA — End-of-Life Solar PV Panels, 2016](https://iea-pvps.org/key-topics/irena-iea-pvps-end-of-life-solar-pv-panels-2016/) | Sustentar a discussão de reutilização, recuperação de materiais e destinação de módulos. Não é inventário ambiental deste abrigo. |

## Hipóteses numéricas e justificativas

| Parâmetro | Valor didático | Justificativa e aplicação |
|---|---:|---|
| Lâmpadas LED | 20 × 9 W | Carga pequena para representar pontos essenciais; não dimensiona iluminância ou lotação. |
| Uso e período | 6 h/noite; 30 dias | Uma rotina noturna durante um episódio temporário de acolhimento. |
| Recurso solar | 4 HSP/dia | Cenário intermediário para explorar sensibilidade a 0 e 1 HSP; não é média nacional. |
| Potência fotovoltaica | 550 Wp | Capacidade fixa escolhida para o exercício; há exemplo de fabricante na v2, sem promessa de produção nominal contínua. |
| Fator útil global | 0,75 | Reserva didática de 25% para perdas no caminho painel → luz, incluindo armazenamento e inversor. Não é medição ou eficiência da célula. |
| Bateria nominal | 2,56 kWh | Exemplo energético: 25,6 V × 100 Ah / 1000. Não garante compatibilidade elétrica. |
| Descarga máxima | 80% | Mantém reserva de 20% no exercício. A ficha de uma bateria real pode exigir outro limite. |
| Eficiência do inversor | 90% | Aproximação usada apenas para converter a energia disponível da bateria em energia na carga, no cálculo de autonomia/capacidade noturna. |
| Potência do inversor | 300 W | Verificação simples de sobrecarga: cargas maiores não recebem promessa de fornecimento. Não analisa picos ou partida. |
| Preço variável | R$ 1,00/kWh | Facilita conferir as contas. Não é tarifa oficial, média brasileira ou conta completa. |
| Iluminação comum | R$ 500 | Reserva hipotética igual em A e B para lâmpadas e instalação comum. |
| Adicional solar | R$ 6.400 | Orçamento hipotético discriminado abaixo, usado para incluir o investimento em vez de comparar só energia. |
| Reserva de manutenção | R$ 10/30 dias | Provisão didática em B, proporcional ao período; não é orçamento de serviço nem fundo suficiente para toda reposição. |

Orçamento adicional de B: módulo R$ 700 + controlador R$ 450 + inversor R$ 750 + bateria R$ 3.000 + cabos/proteções R$ 600 + instalação adicional R$ 900 = **R$ 6.400**. São valores arredondados para estudar o efeito do investimento inicial, não preços pesquisados. Ao aplicar fora do exercício, obter orçamento local e revisar todos os itens.

## Convenções do modelo

- Demanda noturna fixa; cada dia tem o mesmo sol e uma oportunidade de recarga anterior à noite. O consumo atendido é o menor entre demanda, geração útil e capacidade útil da bateria, desde que o inversor suporte a potência.
- A geração útil já considera um fator global de perdas. Não se multiplica novamente por 90% ou 80%. A capacidade/autonomia é uma restrição separada; profundidade de descarga indica quanto da bateria pode ser usado, não uma perda de geração.
- Na simulação de falta de luz, não há recarga. A energia disponível é a parcela da carga inicial acima da reserva mínima, convertida pelo inversor. Uma bateria a 50% não tem metade da autonomia útil de uma cheia, porque ambas preservam os mesmos 20% nominais.
- O indicador diário não conta carga inicial gratuita nem faz previsão do tempo. A autonomia de bateria cheia é outro cenário, explicitamente condicional. Não é simulação cronológica nem garantia de noites sucessivas.
- Não há crédito por excedente, venda de energia ou compensação na rede. Não se afirma que todo recurso solar estimado pode ser consumido.
- A alternativa A pressupõe rede e instalação existentes e seguras. B é um sistema isolado com bateria. Um sistema conectado à rede sem backup não deve ser apresentado como solução equivalente durante apagão.

## Limites econômicos, ambientais e de aplicação

Comparação para aquisição nova e mesmo período. Não inclui reforma/ligação da rede, frete, estrutura específica, reposições, depreciação, juros ou custos de destinação; itens locais exigem orçamento próprio. O preço variável não representa disponibilidade, iluminação pública e outras parcelas fixas da conta. Não se estima retorno do investimento com um episódio de 30 dias, nem se garante economia.

A pode utilizar a mistura de fontes da rede; não foi tratada como inteiramente fóssil. B utiliza recurso renovável e não queima combustível no funcionamento, mas fabricar, transportar, substituir e descartar os equipamentos também gera impactos. Não se realizou análise de ciclo de vida ou cálculo de CO2; kWh substituído não é sinônimo de emissões evitadas. Reutilizar o conjunto entre episódios pode ser avaliado, sem contar esse benefício como receita no modelo.

O estudo atende somente iluminação. Não dimensiona geladeiras, aparelhos médicos, bombas, tomadas, segurança luminotécnica ou uma instalação completa. Instalação real, compatibilidade e proteção devem ser avaliadas por profissional habilitado em local apropriado. Os limites de entrada do programa delimitam o exercício; não certificam segurança.

[Memória de cálculo e comparação](../../documentacao/sers/analise.md) · [Guia de SERS](../../documentacao/sers/README.md)

## Dados públicos e capacidades usadas na v2

A versão `sers-v2`, de 16/11/2026, mantém o exemplo inicial de 4 HSP como hipótese e acrescenta uma referência pública identificada. Assim, o exercício geral para o Brasil não atribui a todas as cidades o recurso solar de um único ponto.

### NASA POWER: origem e transformação

Consulta: [Climatology API — ponto -23,55 / -46,63](https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude=-46.63&latitude=-23.55&format=JSON). [Documentação da API](https://power.larc.nasa.gov/docs/services/api/temporal/climatology/).

A resposta original foi preservada em [fontes/nasa_sao_paulo.json](fontes/nasa_sao_paulo.json). É uma climatologia de **janeiro de 2001 a dezembro de 2025**, fonte SYN1DEG, API v2.10.1. Variável `ALLSKY_SFC_SW_DWN`, comunidade RE, unidade original **kW-hr/m²/day**. O programa confere a unidade e o SHA256 informado no JSON de análise antes de usar a cópia.

A média anual é **4,5288 kWh/m²/dia**; a menor média mensal é junho, **3,2578 kWh/m²/dia**. Dividir pelo nível de referência de 1 kW/m² fornece o mesmo valor numérico em horas de sol pleno equivalentes no **plano horizontal**. No atendimento guiado, a opção 5 aplica 3,2578 ao cenário e identifica a origem. A geração útil resultante é 0,55 × 3,2578 × 0,75 = **1,3438425 kWh/dia**.

É um produto climatológico de grade, não leitura no telhado de um abrigo, promessa de produção, menor dia observado ou previsão meteorológica. Não foi realizada transposição para plano inclinado, análise de orientação ou de sombra. Portanto, serve como caso de referência horizontal aproximado. As sequências de dias com 0/1/4 HSP são hipóteses independentes, não previsões derivadas das médias mensais.

### Fabricantes: capacidades que existem em fichas públicas

- [Canadian Solar — HiKu6 CS6W-MS V2.9](https://static.csisolar.com/wp-content/uploads/2024/07/23145733/CS-Datasheet-HiKu6_CS6W-MS_v2.9_EN.pdf): o modelo CS6W-550MS é um exemplo de potência nominal de 550 W em condições STC.
- [Victron — Lithium NG 25,6 V, dados técnicos](https://www.victronenergy.com/media/pg/Lithium_NG_battery_25%2C6_V/en/technical-data.html): a opção de 100 Ah tem energia nominal de 2560 Wh a 25 °C.

Essas fontes apoiam a plausibilidade de capacidades do exercício. **Não definem um kit compatível e não são os equipamentos cotados no orçamento.** Não foram incorporados modelos de controlador, BMS, inversor ou componentes de instalação. As perdas, limite de descarga, potência de inversor, demanda e preços continuam hipóteses da equipe. Especificar uma instalação real exige projeto e orçamento próprios, inclusive acessórios exigidos pelos fabricantes.

### Custos e sensibilidade

O orçamento permanece **estimativa de planejamento de 16/11/2026**, sem pesquisa de preços em lojas. A faixa de ±30% afeta somente o adicional solar de R$ 6.400: totais B de **R$ 4.990 a R$ 8.830**, mantendo iluminação comum, manutenção, demanda e período. É uma exploração de incerteza, não intervalo de mercado ou previsão.

A consulta de equipamentos existentes pressupõe **ambas as instalações já disponíveis, seguras e prontas**. Nesse caso, mostra somente energia variável de A e provisão de manutenção de B, sem repetir o investimento anterior. Isso não representa custo de vida útil ou retorno financeiro. Quando B não atende à carga, o programa informa que o serviço é parcial também nessa comparação.

## Comunicação de HSP na v3 — 17/11/2026

A distinção entre duração do sol e energia equivalente foi reforçada após a avaliação S01. O conceito segue a seção 6.1.1 do [manual CEPEL/CRESESB](https://cresesb.cepel.br/publicacoes/download/Manual_de_Engenharia_FV_2004.pdf): HSP representa a energia diária por área convertida em duração equivalente à intensidade de referência de 1 kW/m². Não é tempo de sol na casa. O limiar de 8 HSP para confirmação é uma escolha didática da interface, não valor recomendado pelo manual ou limite meteorológico. Dados e fórmulas não foram alterados.

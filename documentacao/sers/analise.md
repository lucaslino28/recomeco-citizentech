# Análise energética — iluminação de abrigo temporário

Lucas Lino Marques da Silva — 572863; Gabriel Martins Cordeiro Rodrigues — 570497; Gustavo Martins da Silva — 570584. Versão `sers-v2`, 16/11/2026; cenário inicial e refinamentos identificados abaixo.

## Necessidade, alternativas e fronteira

Pessoas acolhidas após desastres precisam de iluminação noturna. Modelamos um pequeno conjunto de pontos LED em um abrigo, com 20 lâmpadas de 9 W durante 6 horas por noite e 30 dias. A mesma demanda é usada para A (rede elétrica existente e segura) e B (solar isolado com bateria). As hipóteses não comprovam iluminância adequada de um edifício; não incluem outras cargas.

Demanda, perdas, limites de uso e orçamento são estimativas didáticas da equipe. A v2 acrescenta dados públicos de radiação e exemplos de capacidades dos fabricantes. A origem e a justificativa estão em [fontes e premissas](../../modulos/energia/referencias.md); as referências de equipamento não fornecem os preços do exercício. As contas abaixo podem ser reproduzidas pelo [script de análise](../../testes/analisar_sers.py).

## Memória de cálculo

Potência mede demanda instantânea; energia depende também do tempo. Wp descreve a potência de referência do painel e não geração permanente.

```text
P = quantidade × potência de cada lâmpada
P = 20 × 9 = 180 W = 0,18 kW

E_dia = P × horas / 1000
E_dia = 180 × 6 / 1000 = 1,08 kWh/dia

E_período = E_dia × dias
E_período = 1,08 × 30 = 32,4 kWh
```

Para B, supomos 550 Wp, 4 horas de sol pleno por dia e fator útil global de 0,75. HSP é uma medida equivalente de recurso solar diário; não é o número de horas entre nascer e pôr do sol. As perdas globais de 25% representam a cadeia painel → luz, incluindo armazenamento e inversor. Não são eficiência fotovoltaica da célula nem valor de fabricante.

```text
G_útil = painel_Wp / 1000 × HSP × fator_útil
G_útil = 550 / 1000 × 4 × 0,75 = 1,65 kWh/dia
```

A bateria tem energia nominal hipotética de 2,56 kWh. Com descarga máxima de 80% e inversor com eficiência de 90%, sua capacidade útil na carga é:

```text
B_útil = bateria_kWh × descarga_máxima × eficiência_inversor
B_útil = 2,56 × 0,80 × 0,90 = 1,8432 kWh

Autonomia_cheia = B_útil / potência_kW
Autonomia_cheia = 1,8432 / 0,18 = 10,24 h sem recarga
```

A eficiência de 90% **não é multiplicada novamente pela geração de 1,65 kWh/dia**, pois o fator global já inclui essas perdas. Capacidade de bateria e geração diária são restrições diferentes. O inversor de 300 W suporta a carga didática de 180 W; cargas superiores são consideradas não atendidas, sem promessa de autonomia.

Para uma demanda totalmente noturna e dias idênticos com recarga anterior à noite:

```text
E_atendida_dia = mínimo(E_dia, G_útil, B_útil), se P ≤ potência_inversor
E_atendida_dia = 0, se P > potência_inversor
Déficit_dia = E_dia − E_atendida_dia
Cobertura = E_atendida_dia / E_dia × 100
```

No exemplo: mínimo(1,08; 1,65; 1,8432) = **1,08 kWh/dia**, ou 100% **nas hipóteses do modelo**. O excedente potencial não vira energia vendida ou economia adicional. Não há previsão meteorológica nem rastreamento horário da bateria.

A consulta de falta de luz é separada: sem recarga e com carga inicial informada. Reserva nominal = 1 − 0,80 = 20%.

```text
B_disponível = bateria_kWh × máximo(carga_inicial/100 − 0,20; 0) × 0,90
Autonomia = B_disponível / potência_kW

Carga de 100%: 10,24 h
Carga de 50%: 2,56 × (0,50 − 0,20) × 0,90 / 0,18 = 3,84 h
Carga de 20% ou menos: 0 h acima da reserva mínima
```

Logo, a autonomia cheia não garante atendimento quando a bateria está parcialmente carregada, mesmo que o dimensionamento médio de geração pareça suficiente.

## Custos para o mesmo período de 30 dias

Aquisição nova, sem amortizar capital. A rede e instalação interna existentes são pressupostas. A iluminação comum custa hipoteticamente R$ 500 em ambas. O equipamento solar custa mais R$ 6.400, e a reserva de manutenção B é R$ 10 por 30 dias. O preço variável de R$ 1/kWh é didático.

| Componente | A — rede | B — solar + bateria |
|---|---:|---:|
| Demanda | 32,4 kWh | 32,4 kWh |
| Iluminação e instalação comum | R$ 500,00 | R$ 500,00 |
| Sistema solar adicional | R$ 0,00 | R$ 6.400,00 |
| Energia variável da rede | R$ 32,40 | R$ 0,00, condicionado ao atendimento modelado |
| Reserva de manutenção | R$ 0,00 adicional no modelo | R$ 10,00 |
| **Custo estimado do período** | **R$ 532,40** | **R$ 6.910,00** |

```text
C_A = iluminação_comum + E_período × preço_variável
C_A = 500 + 32,4 × 1 = 532,40 reais

C_B = iluminação_comum + investimento_solar + reserva_30dias × dias/30
C_B = 500 + 6400 + 10 × 30/30 = 6910,00 reais
```

B custa R$ 6.377,60 a mais neste episódio. A substituição potencial de 32,4 kWh da rede vale somente R$ 32,40 de energia variável nesse cenário; não paga o investimento em 30 dias. Mesmo sem consumir energia da rede, B tem custo inicial e manutenção. Não foi calculado retorno de longo prazo, pois vida útil, reposições, frequência de reutilização e condições locais não foram levantadas.

A comparação de custo total é adequada enquanto as duas entregam a mesma demanda no modelo. Quando B tem déficit, o programa avisa que seu custo corresponde a **serviço parcial**; um backup ou redimensionamento exigiria outro orçamento. Não se chama essa diferença de economia com serviço equivalente.

## Sensibilidade e viabilidade

| Situação estimada | Energia útil solar | Cobertura da demanda noturna | Implicação |
|---|---:|---:|---|
| Base: 4 HSP, 6 h de luz | 1,650 kWh/dia | 100% | Geração e capacidade de bateria suficientes no modelo. |
| Pouco sol: 1 HSP, 6 h de luz | 0,4125 kWh/dia | 38,19% | Déficit de 0,6675 kWh/dia; bateria cheia não se recompõe diariamente só com essa geração. |
| Sem sol: 0 HSP | 0 kWh/dia | 0% no regime diário | Uma bateria já cheia ainda dura cerca de 10,24 h sem recarga; isso não se repete indefinidamente. |
| 12 h de luz com 8 HSP | 3,300 kWh/dia | 85,33% | A bateria limita a noite a 1,8432 kWh, apesar de sol abundante. |
| 40 lâmpadas de 9 W | — | 0% neste equipamento | Carga de 360 W supera o inversor de 300 W. |
| Bateria a 50%, sem recarga | — | Autonomia de 3,84 h | Não cobre uma noite de 6 horas. |

Os números são saídas matemáticas do exercício, não desempenho garantido em um abrigo. Para aplicação: conferir demanda e iluminância, recurso solar mensal no local, sombreamento, área disponível, capacidade e estado da bateria, proteções, compatibilidade elétrica e custos reais. O modelo não determina a segurança de um local.

## Recomendação e sustentabilidade

Com rede disponível e segura, **A tem menor custo estimado para esse episódio**. B merece avaliação quando continuidade de iluminação é uma necessidade e há recursos, sol, instalação adequada e manutenção. Uma instalação pronta com bateria carregada pode manter luz durante uma interrupção, dentro da carga e autonomia calculadas. O software não garante fornecimento de emergência.

Para reduzir desperdício, priorizar pontos essenciais e evitar horas desnecessárias sem comprometer a segurança e a circulação. Não foi atribuída economia à substituição de lâmpadas: ambas as opções já usam LED. Qualquer redução de potência precisa preservar qualidade de iluminação.

A utiliza a mistura de fontes da rede brasileira e não foi tratada como totalmente fóssil. B usa energia solar renovável e não queima combustível durante o uso, mas módulos e bateria exigem materiais, fabricação, transporte e destinação. Manutenção, reutilização entre episódios e encaminhamento adequado dos equipamentos ao fim da vida precisam entrar na decisão. Não foi feita análise de ciclo de vida ou cálculo de CO2, então **não há alegação de impacto zero ou redução líquida de emissões quantificada**.

As recomendações do terminal mudam com geração, capacidade, potência e custos calculados. A análise é local e determinística; não depende de respostas geradas por IA nem consulta condições reais de rede/sol.

## Bateria ao longo dos dias — v2

A versão inicial fazia um balanço diário com recarga anterior a cada noite. A v2 mantém esse resultado como referência e adiciona um acompanhamento cronológico simples. O código usa um laço `for`, uma lista com as HSP diárias e um saldo acumulado de energia.

Para não aplicar perdas duas vezes, o saldo é expresso como **energia equivalente na saída do inversor**. Esse saldo representa toda a bateria, inclusive sua reserva. A carga percentual é obtida convertendo esse saldo de volta pela capacidade equivalente total. Trata-se de aproximação energética, não leitura de um BMS.

```text
Capacidade_equivalente = bateria_nominal × eficiência_inversor
Capacidade_equivalente = 2,56 × 0,90 = 2,304 kWh
Reserva_equivalente = 2,304 × (1 − 0,80) = 0,4608 kWh
Saldo_inicial = 2,304 × carga_inicial / 100

Para cada dia:
  G_útil = 0,55 × HSP_dia × 0,75
  Excedente = máximo(0; Saldo_anterior + G_útil − 2,304)
  Saldo_após_sol = mínimo(2,304; Saldo_anterior + G_útil)
  Disponível = máximo(0; Saldo_após_sol − 0,4608)
  Luz_atendida = mínimo(1,08; Disponível), se o inversor suportar a carga
  Déficit = 1,08 − Luz_atendida
  Saldo_final = Saldo_após_sol − Luz_atendida
```

A geração útil já inclui as perdas globais: não multiplicar novamente por eficiência de bateria ou inversor. Se a bateria começar abaixo da reserva, a recarga primeiro recompõe esse nível antes de fornecer energia à luz. O programa não reinicia o saldo entre dias.

Exemplo com bateria inicialmente cheia, demanda de 1,08 kWh/noite e HSP hipotéticas **4, 1, 0, 1 e 4**:

| Dia | HSP | Geração útil (kWh) | Luz atendida (kWh) | Déficit (kWh) | Carga após a noite |
|---|---:|---:|---:|---:|---:|
| 1 | 4 | 1,6500 | 1,0800 | 0 | 53,125% |
| 2 | 1 | 0,4125 | 1,0800 | 0 | 24,154% |
| 3 | 0 | 0 | 0,0957 | 0,9843 | 20% |
| 4 | 1 | 0,4125 | 0,4125 | 0,6675 | 20% |
| 5 | 4 | 1,6500 | 1,0800 | 0 | 44,740% |

Resultado: **3 de 5 noites completas**, **3,7482 kWh atendidos** de 5,4 kWh necessários, déficit de **1,6518 kWh** e cobertura de **69,41%**. O resultado mostra por que uma bateria cheia não garante autonomia indefinida com pouco sol. Não estima a chance de ocorrência dessa sequência.

O balanço de conservação é conferido nos testes: saldo inicial + geração = energia atendida + excedente + saldo final, com tolerância numérica de ponto flutuante. Também são verificados bateria vazia, reserva, sobrecarga, ausência de sol e excesso de geração. Não se modelam hora a hora potência de carga, consumo em espera, limites de corrente, temperatura, autodescarga ou envelhecimento.

## Dados usados e comparação de custos — v2

A [referência pública NASA POWER](../../modulos/energia/referencias.md) permite reproduzir um caso horizontal identificado de São Paulo: junho, menor média mensal da climatologia 2001–2025, com **3,2578 HSP equivalentes** e geração útil aproximada de **1,3438425 kWh/dia**. É um exemplo local; a orientação do sistema continua geral para o Brasil. Outros parâmetros continuam estimados.

Para equipamentos e instalações **já existentes em ambas as alternativas**, o desembolso operacional modelado em 30 dias é **R$ 32,40 em A** e **R$ 10,00 em B**, desde que B atenda à demanda. O capital anterior é excluído e não passa a ser gratuito ou recuperado. Isso é diferente da comparação de compra nova de R$ 532,40 versus R$ 6.910,00. Para B parcial, o sistema não apresenta uma conclusão de menor gasto como serviço equivalente.

Ao variar somente o investimento solar em ±30%, a compra nova de B vai de **R$ 4.990 a R$ 8.830** no período. Essa faixa é hipotética, não cotação. Mesmo no limite inferior, A segue com menor custo inicial no cenário de 30 dias com rede disponível.

| Aspecto de decisão | A — rede existente | B — solar isolado com bateria |
|---|---|---|
| Aquisição nova no cenário | Menor desembolso modelado | Maior capital inicial; orçamento real ainda necessário |
| Rede interrompida | Sem iluminação por essa alternativa | Pode manter luz dentro da carga, reserva e autonomia disponíveis |
| Dias com pouco sol | Depende da disponibilidade da rede | Recarga reduzida; acompanhar déficit ao longo dos dias |
| Uso de recursos | Mistura de fontes da rede; não se supõe matriz totalmente fóssil | Recurso solar renovável no uso; materiais e armazenamento têm impactos |
| Continuidade e manutenção | Depende da rede e da instalação local | Exige carga disponível, equipamentos compatíveis, conservação e destinação |
| Decisão final | Aplicável quando rede está disponível e segura | Avaliar quando continuidade justifica o investimento e as condições locais permitem |

O atendimento guiado oferece custo, continuidade, operação de equipamentos existentes e explicação das contas. As recomendações usam os resultados calculados e apontam condições e limites. Ajustar quantidade de lâmpadas ou horas pode reduzir consumo, mas muda o serviço: não se declara eficiência maior ou iluminação equivalente sem análise luminotécnica.

## Ajuste de comunicação após S01 — sers-v3, 17/11/2026

No teste acompanhado por Lucas, a participante usou 12 HSP pensando no tempo em que o sol bate na casa. A v3 renomeia o campo para energia solar diária equivalente, oferece explicação concreta e solicita decisão explícita para entradas a partir de 8 HSP. A pessoa pode confirmar como hipótese, corrigir ou cancelar; o programa não escolhe um novo valor por ela. O limiar é de revisão didática, não limite físico. As fórmulas deste documento permanecem iguais e as escolhas/resultados originais da v2 foram preservados. Acrescentamos testes para conferir a entrada e o cancelamento. Ainda não repetimos a avaliação com a participante.

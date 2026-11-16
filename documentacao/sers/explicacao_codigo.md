# Como explicar SERS no primeiro ano

A solução usa a biblioteca padrão do Python. Não foi acrescentado modelo de IA ou pacote de cálculo. A equipe deve conseguir acompanhar estes passos com a memória de cálculo ao lado.

1. **Dados em JSON:** `analise.json` separa consumo, equipamentos, orçamento e referências. O programa confere se as entradas são números finitos e se estão nos intervalos do exercício. A cópia pública NASA tem seu hash e unidade conferidos para não usar silenciosamente um arquivo alterado ou unidade incorreta.
2. **Classe `CalculadoraEnergia`:** concentra os dados e os métodos. `calcular()` multiplica potência por tempo, estima geração, aplica limites de bateria/inversor e compara os custos no mesmo período. O resultado é um dicionário.
3. **Autonomia:** `falta_de_luz()` considera quanto da carga inicial está acima da reserva mínima. Converte a energia disponível para a carga e divide pela potência; não recebe recarga solar.
4. **Sequência de dias:** `simular_dias()` recebe uma lista de HSP. Um `for` soma geração ao saldo, limita à capacidade, desconta a luz noturna e guarda os resultados de cada dia numa lista de dicionários. O saldo final passa a ser o inicial do próximo dia.
5. **Perdas:** o fator global da geração é aplicado uma vez. O saldo da sequência é expresso em energia equivalente na saída do inversor; não se aplica novamente a eficiência em cada noite. A profundidade de descarga indica reserva, não perda de produção.
6. **Interface:** funções com `while`, `if` e `input` organizam menus. O atendimento guiado escolhe uma explicação baseada nos cálculos. Não interpreta perguntas por IA. Enter mantém o número; `v` cancela; a alteração só é aplicada depois de completar os campos.
7. **Custos:** compra nova inclui o capital. Equipamentos existentes comparam apenas despesas de operação previstas, informando que investimento anterior e reposições não estão sendo avaliados. A faixa ±30% é sensibilidade hipotética, não cotação.
8. **Arquivo de saída:** só a opção 8 salva um TXT técnico com resumo e dados estruturados. O arquivo recebe nome único e fica numa pasta local ignorada pelo Git. Não registra nomes, perguntas livres ou avaliação de compreensão.

Perguntas para a equipe conferir antes de apresentar:

- Por que 180 W durante 6 horas resultam em 1,08 kWh, e não 1080 kWh?
- Por que a bateria a 50% dura 3,84 h, enquanto a cheia dura 10,24 h? Onde entram os 20% de reserva?
- Por que ter bateria cheia no primeiro dia não resolve várias noites sem recarga?
- Por que a radiação histórica horizontal de São Paulo não é previsão diária nem recurso solar de todo o Brasil?
- Por que B pode gastar menos na operação e ainda custar mais se for necessário comprar tudo agora?
- Qual impacto ambiental não foi quantificado? Quais números são fonte pública e quais continuam estimados?

Os testes verificam contas conhecidas, conservação da energia acumulada, déficits, limites, dados de referência, menus e exportação. Eles não comprovam que uma pessoa entendeu a orientação nem certificam uma instalação elétrica.

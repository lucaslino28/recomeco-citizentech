# SERS — Energia e sustentabilidade no RECOMEÇO

Lucas Lino Marques da Silva — RM 572863; Gabriel Martins Cordeiro Rodrigues — RM 570497; Gustavo Martins da Silva — RM 570584.

Versão **sers-v3**, de 17/11/2026. Avaliação de uma participante documentada e ajuste de HSP verificado tecnicamente. **Vídeo, publicação e envio permanecem pendentes.** Não há garantia de nota; a equipe precisa conferir os cálculos e explicar suas decisões.

## Público e necessidade

O RECOMEÇO orienta cidadãos afetados por desastres no Brasil. Nesta contribuição, responsáveis e voluntários de um abrigo temporário podem entender o custo e a continuidade da iluminação noturna essencial. O cenário é estimado e não representa um abrigo real medido. A mesma iluminação LED e o mesmo período são comparados para rede existente (A) e solar isolado com bateria (B).

O código usa biblioteca padrão, uma classe de cálculo, funções de interface, listas, dicionários e laços. Não precisa de API de IA, pacote científico ou equipamento físico. Os dados públicos usados já estão preservados no repositório; o uso do módulo funciona sem rede.

## Executar

Na pasta do projeto:

```bash
python3 main.py --dados data/demonstracao_sers
```

Escolha **3 — Energia e sustentabilidade**. A pasta do comando separa eventuais registros de PCP. SERS guarda parâmetros só em memória, exceto quando a pessoa escolhe explicitamente salvar um relatório técnico.

| Opção de SERS | Finalidade |
|---|---|
| 1 | Comparação resumida com conclusão, custo, demanda, cobertura e limites. |
| 2 | Ajustar lâmpadas, potência, horas/noite, dias, HSP e preço. Enter mantém o valor e `v` cancela sem aplicar parcialmente; ponto ou vírgula decimal são aceitos. HSP alta pede confirmação como hipótese, correção ou cancelamento. |
| 3 | Autonomia sem recarga com carga inicial informada. `0` aqui é bateria vazia; `v` volta. |
| 4 | Fontes, orçamento, premissas e dados públicos com origem/período/unidade. |
| 5 | Restaurar o exemplo hipotético inicial. |
| 6 | Acompanhar bateria ao longo de vários dias: sol constante, sequência pronta de pouco sol ou HSP escolhidas dia a dia. |
| 7 | Atendimento guiado por necessidade: custo, continuidade, equipamentos existentes, contas ou aplicação do exemplo público de São Paulo. |
| 8 | Exportar relatório técnico TXT com parâmetros, resultados, premissas, fontes e última sequência compatível. |
| 0 | Voltar ao menu principal; 0 novamente encerra. |

Equipamentos e orçamento permanecem fixos durante o uso. Se a equipe alterar capacidades no JSON, precisa rever custos, referências e análise. Ajustar consumo pode mudar o serviço prestado; é preciso preservar a iluminação essencial e sua segurança.

## Roteiro para seu ensaio

1. **Comparar:** 3 no menu principal → 1 em SERS. Exemplo: 180 W, 1,08 kWh/dia, 32,4 kWh/30 dias; aquisição + uso A R$ 532,40 e B R$ 6.910,00. São hipóteses de orçamento.
2. **Entender a decisão:** 7 → 1 ou 2. Consulte a recomendação por necessidade. Em 3 desse atendimento, compare somente a operação com ambas as instalações prontas: A R$ 32,40 e B R$ 10,00, com condições explícitas. Use 0 para voltar ao menu SERS.
3. **Pouco sol:** 6 → 2 → Enter na carga inicial. A sequência 4/1/0/1/4 HSP deve mostrar três noites completas de cinco, déficit de 1,6518 kWh e cobertura de 69,4%.
4. **Carga inicial:** 3 → `50`: autonomia de 3,84 h, insuficiente para uma noite de 6 h.
5. **Dados públicos:** 7 → 5 aplica a menor média mensal do exemplo horizontal de São Paulo: 3,2578 HSP, de junho, climatologia NASA POWER 2001–2025. Use 0 para voltar. A demanda, o orçamento e as perdas continuam estimados.
6. **Fontes e exportação:** abra 4; depois 8 para salvar. A exportação não é teste com usuário nem comentário humano.

Relatórios ficam em `data/relatorios_sers/` dentro do projeto. A tela informa o caminho absoluto. São arquivos locais ignorados pelo Git para evitar misturar ensaios pessoais e evidências públicas. O nome inclui horário UTC e não substitui relatórios anteriores. Ao ajustar/restaurar parâmetros, a sequência antiga é descartada do próximo relatório.

## Análise e fontes

- [Memória de cálculo e comparação](analise.md): demanda, geração, autonomia, conservação de energia na sequência, custos e decisão.
- [Referências e hipóteses](../../modulos/energia/referencias.md): separação entre fonte pública, capacidade de referência e orçamento estimado.
- [Dados de análise](../../modulos/energia/analise.json) e [cópia original NASA POWER](../../modulos/energia/fontes/nasa_sao_paulo.json).
- [Código](../../modulos/energia/calculadora.py) e [roteiro de apresentação do código](explicacao_codigo.md).
- [Plano de testes com usuários](testes_usuarios.md), [roteiro do vídeo](roteiro_video.md) e [TXT a completar](entrega_sers.txt).

## Validação técnica

```bash
python3 -B -m unittest discover -s testes -p 'test_sers.py' -v
python3 -B testes/analisar_sers.py
```

Suíte completa, usando o ambiente com as dependências de IA já instaladas:

```bash
.venv/bin/python -B -m unittest discover -s testes -v
```

A v3 passou em **171 testes locais, incluindo 36 de SERS**. [Resultados reproduzíveis](../../evidencias/sers/pos_usuario_2026-11-17/validacao_tecnica.json), [log real da suíte](../../evidencias/sers/pos_usuario_2026-11-17/testes.txt), [ensaio automatizado de HSP](../../evidencias/sers/pos_usuario_2026-11-17/ensaio_terminal_hsp.txt) e [histórico das versões](../../evidencias/sers/README.md). Esses resultados técnicos são separados da avaliação humana.

## Conferência do enunciado e pendências

Base: GS2026.2_SERS(9).pdf fornecido pela equipe, três páginas; SHA256 `8dabed4124f4e0b69db918306599c645ff3a53cd160417232f63d36e20b47b62`.

| Requisito | Evidência / estado |
|---|---|
| Contexto, público e necessidade | Iluminação essencial de abrigo temporário, descrita aqui e na análise. |
| Origem, unidades, período e premissas | JSON, NASA POWER preservada, referências de fabricante e orçamento claramente estimado. |
| Duas alternativas, uma renovável, mesma demanda/período | A rede e B solar com bateria; serviço parcial identificado sem comparação enganosa. |
| Custos, viabilidade e impactos | Aquisição, operação, sensibilidade e matriz de decisão; impactos ambientais qualitativos, sem inventário de CO2. |
| Resultados integrados e linguagem acessível | Opção 3 funcional; resumo, orientação por necessidade, sequência e detalhes consultáveis. |
| Referências e limites | Visíveis no terminal e nos documentos; sem promessa de geração, economia ou autonomia. |
| Testes com usuários e ajustes | Uma participante externa, conforme relato do aplicador, com terminal, comentários e ajuste documentados. SERS não define mínimo nem exige explicitamente externos. Não houve reteste após a mudança. |
| GitHub organizado | Conteúdo local preparado; **publicar a etapa e conferir acesso**. |
| YouTube não listado, até 3 minutos | **Pendente**, roteiro pronto. |
| Envio somente de TXT com nomes/RMs e links | Modelo com equipe e repositório; falta URL do vídeo. Prazo conforme Portal de SERS. |

As coletas anteriores de PCP/IA não foram reutilizadas como avaliação de SERS. A [rodada S01](../../evidencias/sers/usuarios/rodada_2026-11-17/README.md) e sua origem estão documentadas. O formulário permanece disponível para novas avaliações; a participante ainda não voltou a avaliar a mudança de HSP.

## Ajuste após a avaliação de 17/11

O relato indicou que a participante escolheu 12 HSP pensando no tempo de sol na casa. A v3 explica que duração de sol e energia equivalente são grandezas diferentes. Para entradas a partir de 8 HSP, pede confirmar como hipótese, corrigir ou cancelar, inclusive na sequência manual. O limiar é didático e não valida clima ou produção. As fórmulas e os resultados originais foram mantidos. Para nova consulta, peça que a pessoa explique com suas palavras a diferença, sem antecipar a resposta, e registre o que de fato ocorrer.

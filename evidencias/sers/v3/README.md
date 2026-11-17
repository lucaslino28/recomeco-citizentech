# Verificação técnica após o teste S01

Versão `sers-v3`, 17/11/2026. Melhoramos a explicação e a entrada de HSP depois do teste de S01, descrito em [rodada de usuários](../usuarios/rodada_2026-11-17/README.md).

- [Log real de testes](testes.txt): 171 testes gerais aprovados, incluindo 36 de SERS; cinco regressões novas tratam o problema de HSP.
- [Cálculos reproduzíveis](validacao_tecnica.json): mesmos casos de energia da v2, com a versão e os hashes da v3. Reprodução: `python3 -B testes/analisar_sers.py`.
- [Ensaio de interface](ensaio_terminal_hsp.txt): execução programada de correção e confirmação de HSP alta, em pasta temporária de PCP. Não representa a participante usando a mudança.

Foram verificados correção de 12 para 4 HSP, confirmação explícita de uma hipótese de 12, cancelamento sem aplicar parcialmente outros campos, confirmação na sequência manual e manutenção de zero/Enter. As fórmulas de energia não foram alteradas e o cenário personalizado de S01 continua reproduzível.

S01 testou a v2. Fizemos a mudança e conferimos o código da v3, mas a participante ainda não voltou a avaliar a explicação.

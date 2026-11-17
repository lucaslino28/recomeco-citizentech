# Teste de SERS — 17/11/2026

Testamos a **sers-v2** com uma pessoa de fora do grupo, identificada como **S01**. Lucas ajudou a iniciar o terminal. Depois disso, ela usou o programa sozinha e ele anotou seus comentários.

O teste foi feito com `python3 main.py --dados data/demonstracao_sers`, na opção 3. O código usado era o do commit `c87be23`.

## O que foi testado

| Situação | Parâmetros e resultado observado |
|---|---|
| Comparação inicial | 20 lâmpadas de 9 W, 6 h/noite, 30 dias: 32,4 kWh; A R$ 532,40 e B R$ 6.910,00 no orçamento didático. |
| Cenário personalizado | 10 lâmpadas de 5 W, 9 h/noite, 30 dias, 12 HSP e R$ 0,789/kWh: 13,5 kWh e A R$ 510,65. As 12 HSP foram uma entrada de simulação, não recurso solar local medido. |
| Autonomia | Restaurou o exemplo; bateria a 50%, sem recarga: 3,84 h, insuficientes para uma noite de 6 h. |
| Cinco dias | Sequência 4/1/0/1/4 HSP, carga inicial de 90%: 3 noites completas, cobertura de 69,4%, déficit total de 1,6518 kWh. A geração do primeiro dia recompõe a bateria antes da noite. |
| Fontes e exportação | Consultou a opção 4, exportou pela opção 8 e encerrou normalmente. O relatório contém os parâmetros restaurados e a última sequência, não todo o histórico de alterações. |


Ela escolheu um cenário próprio no ajuste de consumo. A opção 7 não foi usada nessa sessão. O teste de vários dias incluiu situações com 1 e 0 HSP.

## Comentários e dificuldade encontrada

Pelas anotações de Lucas, a participante gostou da ideia e achou útil poder comparar rede elétrica e energia solar sem precisar fazer todas as contas sozinha.

A principal dificuldade foi o campo de HSP. Ela digitou **12** pensando no tempo aproximado em que o sol bate na casa. Isso mostrou que a explicação do campo precisava ficar mais clara.

Não registramos tempo ou nota de facilidade nessa rodada. Os comentários abaixo vêm das anotações de Lucas, e não de uma entrevista gravada. Como foi apenas uma participante, esse teste ajuda a encontrar problemas, mas não representa a experiência de todo o público.

## O que mudamos

Na **sers-v3**, trocamos o nome do campo para energia solar diária equivalente e explicamos a diferença entre HSP e horas de sol na casa. Quando a entrada é de 8 HSP ou mais, o programa pede para confirmar como hipótese, corrigir ou cancelar. O valor 8 é um ponto de atenção que escolhemos para a interface, não um limite físico.

Acrescentamos cinco testes de código para conferir essa mudança. O projeto passou em **171 testes automatizados**. A participante ainda não voltou a testar a nova explicação.

## Arquivos do teste

- [Terminal](terminal_s01.txt): entradas e saídas da sessão. Retiramos os identificadores do computador e os caminhos pessoais.
- [Relatório exportado](relatorio_s01.txt): cópia do arquivo gerado pelo programa em 17/11/2026, às 19:28:14 UTC. Esse é o horário de geração do arquivo, não a duração do teste.
- [Dados organizados](registro_s01.json): parâmetros, resultados e hashes dos arquivos originais.
- [Testes da mudança](../../v3/README.md): conferência da explicação e da entrada de HSP.

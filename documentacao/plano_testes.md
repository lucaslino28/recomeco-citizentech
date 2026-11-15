# Plano de testes de PCP

## Situação atual

A rodada de 14/11 está documentada em [validação PCP](validacao_pcp.md): três participantes externos conforme relato da equipe e dez atendimentos nos arquivos. A versão avaliada tinha 30 orientações; a revisão posterior tem 34. O roteiro abaixo orienta verificações futuras, sem reconstruir retroativamente como a rodada anterior foi aplicada.

## Regressão técnica

```bash
python -B -m unittest discover -s testes -v
python -B testes/analisar_validacao_pcp.py
```

A suíte utiliza arquivos temporários e situações sintéticas. Conferir busca +3/+1, categorias e tipos, privacidade, confirmação, reformulação, alternativas, entradas inválidas, JSON, CSV e indicadores. As dez perguntas fornecidas pela equipe estão em `testes/casos_avaliacao_pcp.json`; o resultado esperado é uma orientação específica, não uma nota humana prevista.

Verificações adicionadas após a rodada: assunto dentro de frases, descarte de palavras neutras, sugestão exata antes da aproximada, aviso de urgência antes das escolhas, distinção entre falta de energia e choque, documentos no acolhimento, contatos regionais, tempo ao retornar e filtro de datas. Resultado atual: 89 testes aprovados; log em `evidencias/testes_pos_avaliacao_pcp_2026-11-14.txt`.

O script de análise apenas lê o CSV. Para outra rodada, use `--arquivo caminho/atendimentos.csv --data AAAA-MM-DD`. O filtro exclui outras datas dos cálculos, sem apagar linhas. Não somar cenários técnicos como se fossem atendimentos externos.

## Ensaio no terminal

```bash
python main.py --dados data/demonstracao_pcp
```

Experimentar as dez perguntas da regressão, uma pergunta fora do escopo, uma sugestão recusada, retorno com `0`, reformulação e navegação por tipo. A própria equipe pode ensaiar diferentes perfis, identificando isso como simulação técnica. O ensaio não altera a evidência da avaliação.

## Nova rodada com participantes, se realizada

1. Escolher uma pasta nova, por exemplo `python main.py --dados data/validacao_pcp_rodada2`. Não reutilizar a avaliação anterior e não executar simultaneamente.
2. Registrar a versão do código/base, a data e a quantidade de participantes externos efetivamente envolvidos. Não coletar nome, contato, documento, endereço ou relato identificável.
3. Explicar o objetivo acadêmico e pedir perguntas sobre situações hipotéticas, permitindo que cada pessoa formule a própria frase.
4. Incluir acolhimento sem documentos, alagamento na rua, encaminhamento de urgência hipotética, tempestade e energia; complementar com outros desastres e navegação. Uma distribuição planejada não deve ser descrita como realizada.
5. Deixar a pessoa escolher caminhos e marcar utilidade e facilidade. Não sugerir notas ou preencher por ela.
6. Registrar o código da tarefa e a dificuldade observada, sem dados pessoais. O histórico omite o texto livre intencionalmente.
7. Usar o modelo em `evidencias/modelo_resultados_pcp.md` para uma nova cópia datada. Conferir os indicadores da pasta e preservar os dados originais.

O mínimo do enunciado é três pessoas de fora da equipe e dez atendimentos no total. Número de execuções não comprova pessoas diferentes. Na rodada de 14/11 foram informadas dez execuções para três participantes; a divisão por pessoa não está registrada e não deve ser inventada.

Uma nova rodada pode medir se facilidade e utilidade melhoraram; até que ocorra, não há notas humanas posteriores às correções. O requisito de melhoria após a rodada inicial está documentado com a mudança aplicada e sua verificação técnica.

## Melhorias e evidências

Manter a sequência: dificuldade observada → causa no código/conteúdo → mudança pequena → teste técnico → limitação restante. Preservar os CSVs e as notas anteriores. Não corrigir tempos antigos com base em estimativas. Em emergência real, interromper a avaliação e acionar o serviço oficial adequado.

## Vídeo

Use [roteiro do vídeo PCP](roteiro_video_pcp.md). As demonstrações devem usar uma pasta própria e uma cópia da base para a alteração ao vivo de palavra-chave. Não mudar o histórico da rodada externa durante a gravação.

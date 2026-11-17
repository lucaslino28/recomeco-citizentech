# Requisitos de PCP no vídeo técnico integrado

O vídeo PCP + SERS terá **5 a 8 minutos no total**. O [planejamento compartilhado](../roteiro_video_tecnico.md) reúne as duas matérias. Esta página detalha os itens de PCP, sem reservar todo o tempo para essa disciplina.

Todos os integrantes devem explicar partes técnicas com a própria voz e código legível. Sugestão de divisão, a ajustar no ensaio:

| Parte | Responsável sugerido | Mostrar e explicar |
|---|---|---|
| Abertura breve | Lucas | Nome do projeto, equipe, público e problema; até 30 segundos para esse início. |
| Dados e classes | Gabriel | Um registro JSON, dicionários, atributos, métodos, `self`, composição e lista de tuplas da busca. |
| Busca e execução | Gustavo | Normalização, conta da pontuação; resultado encontrado, não encontrado, categoria, opção inválida e dado fictício bloqueado. |
| Alteração ao vivo | Gabriel | Palavra-chave em uma cópia da base e efeito após recarregar. |
| Histórico e avaliação | Lucas | Histórico, CSV, indicadores de 14/11, dúvida sem solução, melhoria, decisão técnica e limitação. |
| Energia e fechamento | Dividir com o grupo | Incluir o [conteúdo de SERS](../sers/roteiro_video.md), mostrar cálculo e execução, preservando o tempo total. |

## Preparação

1. Conferir os nomes e RMs já preenchidos no README/TXT e o campo de vídeo pendente. Rodar `python -B -m unittest discover -s testes -v`.
2. Usar `python main.py --dados data/demonstracao_pcp`. Não gravar ensaios na pasta da avaliação.
3. Abrir README, classes, JSON, relatório e indicadores derivados. Ocultar notificações e dados pessoais do computador.
4. Ensaiar para caber no tempo, evitando percorrer todas as 34 orientações.

## Demonstrações curtas

- Pontuação: `socorro emergência` encontra o ID 1 com 7 pontos: 3 + 3 pelas chaves e 1 por “emergência” no título. A confiança é ALTA por coincidência textual.
- Encontrado: `Onde encontro um abrigo?`.
- Não encontrado: `astronomia galáctica`; mostrar opções de reformulação/categoria e voltar.
- Privacidade: usar apenas o valor fictício `12345678`, sem dados reais. A pergunta é bloqueada antes do atendimento.
- Navegação: escolher uma categoria ou tipo, abrir orientação e mostrar fonte/data/aviso.
- Melhoria: mostrar a pergunta de tempestade forte e a orientação 34. Explicar o erro anterior de sugestões por palavras neutras, com a comparação técnica aberta.

## Alteração ao vivo sem mexer na base principal

Preparar antes uma pasta fora do repositório com uma cópia de `main.py`, `assistente.py`, `base_conhecimento.py`, `orientacao.py` e `data/base_conhecimento.json`. Usar a cópia no trecho de demonstração.

Conferir antes do vídeo que `refúgio temporário` não é encontrado na cópia. Durante a gravação, acrescentar essa expressão a `palavras_chave` da orientação 5, salvar e reiniciar o programa para recarregar o JSON. Repetir a pergunta e explicar os 3 pontos da expressão. Não apagar a base principal nem restaurar arquivos com comandos destrutivos. Essa alteração é um exemplo didático, separado da melhoria decorrente da avaliação.

## Resultados a apresentar

Dez atendimentos em 14/11: 80% com orientação encontrada/selecionada, 70% que ajudaram, três sem solução, facilidade 3,0/5, tempo registrado 43,24 s e 1,0 tentativa média. Participaram três pessoas de fora do grupo. Os dados estão por sessão, sem divisão de atendimentos por pessoa. O CSV contém também uma linha de 12/11, fora desses cálculos.

A revisão passou em 89 testes automatizados e as dez frases encontram a orientação prevista. Isso não substitui as notas humanas nem demonstra melhoria de satisfação. Mostrar a limitação do tempo antigo e a preservação dos registros, sem apresentar uma nova rodada inexistente.

## Antes de enviar

Publicar o vídeo como não listado no YouTube e conferir acesso sem login. Inserir o mesmo link no README e em `entregas/pcp.txt`. Conferir repositório público e revisão publicada. Enviar o TXT no Portal até 19/11/2026 às 23h59, conforme o enunciado. Não marcar vídeo ou entrega como concluídos antes de realizar essas etapas.

## Integração com SERS

O [planejamento integrado](../roteiro_video_tecnico.md) reúne o conteúdo das duas matérias. Vamos manter as demonstrações de PCP e incluir os cálculos e a execução de energia. O mesmo link será usado nos dois TXT.

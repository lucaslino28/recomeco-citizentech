# Roteiro do vídeo técnico de PCP

Duração-alvo: 7 minutos, dentro do limite de 5 a 8 minutos. Todos os integrantes devem explicar uma parte com a própria voz e código legível. A divisão abaixo é uma proposta para o ensaio; ajustar à equipe antes de gravar.

| Tempo aproximado | Responsável sugerido | Mostrar e explicar |
|---|---|---|
| 0:00–0:40 | Lucas | Nome do projeto, integrantes/RMs, público e problema; escopo educacional |
| 0:40–2:00 | Gabriel | Três classes, atributos, `self`, composição e um registro JSON; lista de tuplas da busca e exemplo de pontuação |
| 2:00–3:30 | Gustavo | Terminal: resultado encontrado, não encontrado, categoria, opção inválida, retorno e dado fictício bloqueado |
| 3:30–4:30 | Gabriel | Alteração ao vivo de palavra-chave em uma cópia da base e efeito após recarregar |
| 4:30–5:40 | Lucas | Histórico sem texto livre, CSV e indicadores da avaliação de 14/11, com exclusão do registro de 12/11 |
| 5:40–7:00 | Gustavo, com fechamento dos três | Dificuldade observada, melhoria aplicada, teste técnico depois, privacidade e limitação restante |

## Preparação

1. Completar nomes e RMs no README/TXT. Rodar `python -B -m unittest discover -s testes -v`.
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

Dez atendimentos em 14/11: 80% com orientação encontrada/selecionada, 70% que ajudaram, três sem solução, facilidade 3,0/5, tempo registrado 43,24 s e 1,0 tentativa média. Participação de três pessoas externas conforme relato da equipe; não mostrar identificação nem inventar divisão por pessoa. O CSV contém também uma linha de 12/11, fora desses cálculos.

A revisão passou em 89 testes automatizados e as dez frases encontram a orientação prevista. Isso não substitui as notas humanas nem demonstra melhoria de satisfação. Mostrar a limitação do tempo antigo e a preservação dos registros, sem apresentar uma nova rodada inexistente.

## Antes de enviar

Publicar o vídeo como não listado no YouTube e conferir acesso sem login. Inserir o mesmo link no README e em `documentacao/entrega_pcp.txt`. Conferir repositório público e revisão publicada. Enviar o TXT no Portal até 19/11/2026 às 23h59, conforme o enunciado. Não marcar vídeo ou entrega como concluídos antes de realizar essas etapas.

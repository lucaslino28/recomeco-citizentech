# Guia de uso e explicação de PCP

## Executar sem alterar a avaliação anterior

Na pasta do repositório, ative o ambiente virtual e use uma pasta de demonstração:

```bash
source .venv/bin/activate
python main.py --dados data/demonstracao_pcp
```

Se o ambiente ainda não existir, veja a instalação no README. PCP usa apenas a biblioteca padrão do Python. Não execute duas instâncias na mesma pasta de dados.

## Usar o programa

1. No menu principal, escolha `1` para PCP.
2. Escolha `1` para escrever a dúvida, `2` para categorias, `3` para exemplos ou `4` para tipos de desastre.
3. Digite uma pergunta sem nome, números de documentos, endereço ou contato. `?` mostra exemplos; `0` volta.
4. Se houver ambiguidade, escolha o assunto. Uma sugestão não é aceita automaticamente.
5. Leia a resposta e marque `s`/`1` se ajudou, `n`/`2` se não ajudou ou `0` para voltar sem confirmar utilidade.
6. Após uma resposta negativa, é possível reformular, iniciar nova dúvida, abrir categorias ou uma alternativa quando houver.
7. Ao encerrar, dê a nota de facilidade de 1 a 5, ou `0` para não avaliar. O programa exporta o CSV.

Exemplos para conferir as melhorias: `Está tendo uma enchente na rua do meu serviço.`, `Estou preso dentro do meu carro na enchente.`, `Está acontecendo uma tempestade forte na minha cidade, o que devo fazer?`, `Eu consigo entrar no abrigo sem meu documento com RG e CPF?`, `Por conta da chuva minha casa está sem energia.` e `Você tem o número da Enel?`.

Essas frases são um ensaio técnico com situações hipotéticas. Não registrar o ensaio como uma nova avaliação humana. Em uma emergência real, use o serviço oficial diretamente.

## Entender as classes no primeiro ano

- `Orientacao` representa um registro do JSON. Seus atributos guardam título, resposta, fonte e demais campos; `exibir()` apresenta o conteúdo.
- `BaseConhecimento` guarda uma lista de objetos `Orientacao`. Lê o JSON, organiza categorias e calcula pontos.
- `Assistente` tem uma `BaseConhecimento`: isso é composição. Ele conversa pelo terminal, registra o resultado e calcula indicadores.
- `self` indica o objeto que está executando o método. Uma lista guarda várias orientações; um dicionário representa cada atendimento; a tupla `(pontos, orientacao)` associa uma pontuação ao objeto encontrado.

A busca normaliza a escrita, dá +3 por expressão-chave completa e +1 por palavra distinta de quatro ou mais letras no título. A partir de 3 há resultado; a partir de 6 a confiança textual é ALTA. Isso mede correspondência de texto, não certeza de que o conteúdo resolve a situação.

O assunto cadastrado ajuda quando a pontuação não encontra resposta. `difflib`, da biblioteca padrão, oferece aproximações de escrita que a pessoa precisa confirmar. O aviso de pessoa presa em veículo usa condições simples sobre expressões cadastradas; não substitui a busca nem reconhece toda emergência.

## Indicadores e arquivos

Uma reformulação atualiza o mesmo atendimento e soma uma tentativa. Uma nova dúvida cria outro. A facilidade é uma nota por execução, usada uma vez na média, mesmo quando aquela execução tem vários atendimentos.

`data/historico.json` guarda resultados com rótulos, sem perguntas livres. `atendimentos.csv` exporta os mesmos campos. `--dados` separa as pastas de cada rodada.

`--data-indicadores AAAA-MM-DD` filtra a exibição na opção 4; o CSV continua completo. Para os números da avaliação preservada, sem alterar arquivos:

```bash
python -B testes/analisar_validacao_pcp.py
```

## Verificar antes de entregar

```bash
python -B -m unittest discover -s testes -v
```

Confira o relatório, ensaie o vídeo e complete os itens abertos do checklist. Nenhum resultado automático determina como um participante avaliaria a versão nova.

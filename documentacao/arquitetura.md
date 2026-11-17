# Arquitetura técnica — RECOMEÇO

FIAP — Ciência da Computação, turma 1CCPX — Global Solution 2026.2. Atualização: 17/11/2026.

## 1. Estado atual

PCP está implementado no terminal, com 34 orientações em três categorias. A avaliação de 14/11 e as melhorias posteriores estão documentadas; a regressão técnica atual passou em 89 testes. A identificação dos integrantes e a publicação de PCP estão concluídas; a entrega de PCP ainda depende de vídeo, links e envio do TXT.

Prompt & IA está implementado com LangChain/Groq, avaliação e fechamento documentados. A opção 2 abre o módulo de documentos de Aurora. SERS está implementado na opção 3, com consumo, custos e autonomia calculados localmente. A base fictícia de Aurora não é usada por PCP. Não há novas dependências no programa de PCP.

## 2. Organização

```text
main.py — menu principal e parâmetros de execução
  ├── PCP: Assistente
  │     └── base: BaseConhecimento
  │           └── orientacoes: lista de Orientacao
  ├── Prompt & IA: agente LangChain/Groq
  └── SERS: CalculadoraEnergia + analise.json
```

A composição permite que o `Assistente` use uma base, e que a base reúna várias orientações. A busca por pontuação é independente de APIs e dos módulos de IA e SERS.

## 3. Responsabilidades

### 3.1. Sistema principal

`main.py` carrega a base, cria o assistente, apresenta menus, trata interrupções e exporta o CSV ao encerrar. A opção `--dados` escolhe a pasta de resultados. `--data-indicadores` valida a data e filtra a exibição de indicadores; não filtra a exportação completa.

### 3.2. Módulo PCP

| Classe | Atributos principais | Responsabilidades |
|---|---|---|
| `Orientacao` | id, categoria, título, palavras-chave, resposta, documentos, onde, fonte, data; campos opcionais de passos/assuntos/desastres | Representar e exibir a orientação |
| `BaseConhecimento` | caminho, orientacoes | Ler/validar JSON, listar categorias/tipos, pontuar, buscar e sugerir assuntos |
| `Assistente` | nome, base, historico, sessao, atendimentos_sessao | Receber perguntas, proteger privacidade, esclarecer escolhas, avaliar, registrar e gerar indicadores/CSV |

`pontuar()` mantém +3 por expressão-chave completa e +1 por palavra distinta de quatro ou mais letras presente no título. `buscar()` retorna tuplas ordenadas `(pontos, orientacao)`, com resultado a partir de 3 e confiança ALTA a partir de 6. A escolha entre candidatas próximas não modifica os pontos.

`sugerir()` procura assuntos dentro da frase; depois considera termos exatos e aproximações de escrita. O `Assistente` exige escolha antes de abrir sugestões. O aviso limitado de pessoa presa em veículo aparece antes das escolhas, sem substituir a busca.

Pergunta e categorias usam `atender()`. Reformulações e alternativas atualizam o mesmo registro, enquanto nova dúvida cria outro. O fluxo registra confirmação e tempo, inclusive ao sair dos menus de recuperação.

### 3.3. Módulo Prompt & IA

**`modulos/documentos_ia/agente.py`**

Responsável pelo agente de inteligência artificial.

Funcionalidades previstas:

- Interpretar perguntas em linguagem natural.
- Consultar exclusivamente as sete fichas fictícias da Central do Cidadão de Aurora.
- Responder com referências e datas de verificação.
- Tratar perguntas fora do escopo.
- Impedir exposição de dados pessoais.
- Resistir a tentativas de prompt injection.

Framework definido: LangChain com um agente e contexto contendo as sete fichas completas. O modelo do agente é GPT-OSS 20B na Groq; o juiz usa GPT-OSS 120B. A justificativa, a privacidade e os limites estão em [decisões de IA](ia/decisoes.md).

**`modulos/documentos_ia/avaliador.py`**

Responsável pela avaliação automatizada das respostas.

Funcionalidades previstas:

- Executar as 26 perguntas obrigatórias.
- Comparar respostas obtidas com respostas esperadas.
- Utilizar LLM as a Judge.
- Registrar resultados e erros.
- Executar nova avaliação após uma melhoria.
- Permitir comparar os resultados antes e depois.

**`modulos/documentos_ia/fichas/`**

Contém as sete fichas fictícias fornecidas pelo professor, conferidas contra o ZIP original. Elas não são modificadas para ajustar resultados.

**Regra obrigatória:** o módulo não poderá misturar as fichas fictícias com as fontes oficiais utilizadas pelo PCP.

### 3.4. Módulo SERS

`modulos/energia/calculadora.py` usa a classe `CalculadoraEnergia` para validar a base, calcular demanda em kWh, geração útil, limite da bateria/inversor, autonomia sem recarga e custos no mesmo período. `menu_energia()` oferece comparação resumida, ajuste de consumo, falta de luz, fontes, restauração, bateria em vários dias, atendimento por necessidade e exportação explícita de relatório técnico.

O cenário é iluminação noturna de abrigo temporário após desastres. A compara LED ligado à rede existente; B usa os mesmos LEDs com sistema solar isolado e bateria. Recomendações são condicionadas aos resultados: déficit e sobrecarga não recebem promessa de atendimento completo. O custo de serviço parcial é identificado como tal.

`modulos/energia/analise.json` reúne parâmetros estimados, orçamento, justificativas e fontes. A v2 acrescenta NASA POWER em cópia local conferida por hash e exemplos de capacidades dos fabricantes. O balanço cronológico usa lista de HSP, laço diário e saldo de energia equivalente, sem aplicar perdas duas vezes. Resultados reproduzíveis ficam em `evidencias/sers/validacao_tecnica.json`. `modulos/energia/referencias.md` e `documentacao/sers/analise.md` explicam fórmulas, origens, comparação e limites econômicos/ambientais.

O módulo usa apenas a biblioteca padrão, resolve a base a partir do próprio arquivo e não chama IA ou consulta dados em tempo real. Só salva um relatório quando a pessoa escolhe exportar (pasta local ignorada pelo Git); não cria sessões/indicadores de PCP. A análise separa aquisição de operação com equipamentos existentes. A avaliação de 17/11 está documentada com uma participante, segundo o aplicador. A v3 acrescenta explicação e confirmação de HSP alta, motivada pela dificuldade observada, sem alterar as fórmulas ou declarar nova avaliação humana.

## 4. Armazenamento e privacidade

| Arquivo | Finalidade |
|---|---|
| `data/base_conhecimento.json` | Conteúdo oficial curado de PCP, 34 orientações |
| `data/historico.json` | Resultados sem perguntas livres |
| `data/atendimentos.csv` | Exportação do histórico da pasta |
| `evidencias/validacao_usuarios_2026-11-14.csv` | Evidência original preservada da rodada, incluindo linha anterior excluída dos cálculos |
| `testes/casos_avaliacao_pcp.json` | Frases fornecidas pela equipe e orientação esperada na regressão |
| `modulos/documentos_ia/fichas/` | Sete fichas fictícias, exclusivas de IA |
| `modulos/energia/analise.json` | Parâmetros hipotéticos, orçamento, premissas e fontes de SERS |

Não há cadastro. O texto da pergunta só fica em memória. O campo `pergunta` recebe rótulo controlado. O filtro recusa oito ou mais dígitos, `@` e alguns padrões de identificação. A nota de facilidade é considerada uma vez por sessão aleatória, sem reconstruir identidade.

A gravação usa arquivo temporário e substituição. Arquivos inteiramente ilegíveis são preservados. As pastas devem ser usadas por uma execução de cada vez. As limitações completas estão em [decisões de PCP](decisoes_pcp.md).

## 5. Validação e sequência de trabalho

A regressão técnica usa `unittest` e arquivos temporários. A análise do CSV usa apenas leitura e filtro por data. Os resultados da avaliação e os da regressão ficam separados em [validação PCP](validacao_pcp.md).

A arquitetura e a pontuação foram mantidas durante a melhoria incremental. IA e SERS estão implementados, com evidências técnicas próprias e pendências de entrega identificadas. As fichas fictícias não devem se misturar às fontes oficiais de PCP; indisponibilidade de IA não deve impedir PCP.

A entrega de PCP deve ser conferida pelo [checklist](checklist.md), pelas [fontes](fontes_pcp.md) e pelo [roteiro do vídeo](roteiro_video_pcp.md). O fechamento de IA está em seu índice; execução, análise e pendências de SERS estão no [guia de SERS](sers/README.md).

# Arquitetura técnica — RECOMEÇO

FIAP — Ciência da Computação, turma 1CCPX — Global Solution 2026.2. Atualização: 14/11/2026.

## 1. Estado atual

PCP está implementado no terminal, com 34 orientações em três categorias. A avaliação de 14/11 e as melhorias posteriores estão documentadas; a regressão técnica atual passou em 89 testes. A identificação dos integrantes e a publicação de PCP estão concluídas; a entrega de PCP ainda depende de vídeo, links e envio do TXT.

Prompt & IA está implementado com LangChain/Groq e avaliação automática em andamento. A opção 2 abre o módulo de documentos de Aurora. SERS permanece em planejamento na opção 3. A base fictícia de Aurora não é usada por PCP. Não há novas dependências no programa de PCP.

## 2. Organização

```text
main.py — menu principal e parâmetros de execução
  ├── PCP: Assistente
  │     └── base: BaseConhecimento
  │           └── orientacoes: lista de Orientacao
  ├── Prompt & IA — em desenvolvimento
  └── SERS — em desenvolvimento
```

A composição permite que o `Assistente` use uma base, e que a base reúna várias orientações. A busca por pontuação é independente de APIs e do futuro módulo de IA.

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

**`modulos/energia/calculadora.py`**

Responsável pelos cálculos de consumo e comparação das alternativas energéticas.

Cenário: iluminação essencial de um abrigo temporário após uma enchente.

Serão comparadas:

- Alternativa A: iluminação LED alimentada pela rede elétrica convencional.
- Alternativa B: iluminação LED alimentada por sistema solar fotovoltaico com bateria.

Funcionalidades previstas:

- Calcular consumo de energia em kWh.
- Estimar custos de implantação e operação.
- Estimar geração e autonomia do sistema.
- Comparar viabilidade e impactos ambientais.
- Apresentar recomendações sustentadas pelos resultados.

**`modulos/energia/analise.json`**

Armazenará os parâmetros e resultados estruturados da análise energética.

**`modulos/energia/referencias.md`**

Documentará fontes, premissas, fórmulas, justificativas e limitações utilizadas nos cálculos.

As recomendações serão integradas ao menu principal do assistente.

## 4. Armazenamento e privacidade

| Arquivo | Finalidade |
|---|---|
| `data/base_conhecimento.json` | Conteúdo oficial curado de PCP, 34 orientações |
| `data/historico.json` | Resultados sem perguntas livres |
| `data/atendimentos.csv` | Exportação do histórico da pasta |
| `evidencias/validacao_usuarios_2026-11-14.csv` | Evidência original preservada da rodada, incluindo linha anterior excluída dos cálculos |
| `testes/casos_avaliacao_pcp.json` | Frases fornecidas pela equipe e orientação esperada na regressão |
| `modulos/documentos_ia/fichas/` | Sete fichas fictícias, exclusivas de IA |
| `modulos/energia/analise.json` | Planejamento dos parâmetros e resultados de SERS |

Não há cadastro. O texto da pergunta só fica em memória. O campo `pergunta` recebe rótulo controlado. O filtro recusa oito ou mais dígitos, `@` e alguns padrões de identificação. A nota de facilidade é considerada uma vez por sessão aleatória, sem reconstruir identidade.

A gravação usa arquivo temporário e substituição. Arquivos inteiramente ilegíveis são preservados. As pastas devem ser usadas por uma execução de cada vez. As limitações completas estão em [decisões de PCP](decisoes_pcp.md).

## 5. Validação e sequência de trabalho

A regressão técnica usa `unittest` e arquivos temporários. A análise do CSV usa apenas leitura e filtro por data. Os resultados da avaliação e os da regressão ficam separados em [validação PCP](validacao_pcp.md).

A arquitetura e a pontuação foram mantidas durante a melhoria incremental. O desenvolvimento atual é IA, seguido de SERS. As fichas fictícias não devem se misturar às fontes oficiais de PCP; indisponibilidade de IA não deve impedir PCP.

A entrega de PCP deve ser conferida pelo [checklist](checklist.md), pelas [fontes](fontes_pcp.md) e pelo [roteiro do vídeo](roteiro_video_pcp.md). As pendências de IA estão em seu guia e relatório; SERS ainda não foi implementado.

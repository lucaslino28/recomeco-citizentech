# Arquitetura Técnica — RECOMEÇO

**Projeto:** RECOMEÇO — CitizenTech  
**Instituição:** FIAP — Ciência da Computação  
**Global Solution:** 2026.2  
**Status:** PCP implementado e validado tecnicamente; IA e SERS pendentes. Testes externos e entregas acadêmicas ainda pendentes.

## 1. Visão geral

O RECOMEÇO será um assistente digital desenvolvido em Python para auxiliar cidadãos afetados por enchentes e desastres climáticos.

O MVP será executado no terminal, com uma interface única que permitirá acessar três módulos:

1. **PCP:** Orientações sobre recuperação após enchentes.
2. **Prompt & IA:** Assistente de documentação pessoal, utilizando dados fictícios.
3. **SERS:** Análise de alternativas de energia para abrigos temporários.

Cada módulo terá responsabilidades próprias, mas todos serão acessados pelo mesmo programa principal.

## 2. Arquitetura do sistema

```text
                  USUÁRIO
                     |
                     v
                 main.py
              Menu principal
                     |
        +------------+------------+
        |            |            |
        v            v            v
       PCP       PROMPT & IA      SERS
        |            |            |
   Busca por      Agente de    Calculadora
   pontuação      IA           energética
        |            |            |
   JSON com       7 fichas     Dados, cálculos
   fontes         fictícias    e referências
   oficiais
        |            |            |
        +------------+------------+
                     |
                     v
             Resposta no terminal
```

## 3. Responsabilidade dos arquivos

### 3.1. Sistema principal

**`main.py`**

Responsável por iniciar o RECOMEÇO e apresentar o menu principal.

Funcionalidades previstas:

- Exibir o nome e a apresentação do projeto.
- Permitir a escolha do módulo.
- Encaminhar o usuário para a funcionalidade selecionada.
- Tratar opções inválidas.
- Permitir retornar ao menu principal.
- Encerrar o programa corretamente.

O menu terá quatro opções principais: orientações após enchentes, documentação pessoal, energia e sustentabilidade e indicadores de atendimento.

### 3.2. Módulo PCP

**`orientacao.py`**

Implementa a classe `Orientacao`.

Responsabilidades:

- Representar uma orientação da base JSON.
- Armazenar categoria, título, palavras-chave, resposta, documentos, local de atendimento, fonte e data de verificação.
- Exibir a orientação em linguagem acessível.

**`base_conhecimento.py`**

Implementa a classe `BaseConhecimento`.

Responsabilidades:

- Carregar e validar as informações do JSON.
- Organizar e listar as categorias.
- Pesquisar orientações por categoria.
- Normalizar textos.
- Calcular a pontuação das orientações.
- Retornar os resultados ordenados por pontuação.

A pontuação inicial seguirá os critérios do professor:

- +3 pontos por palavra-chave encontrada.
- +1 ponto por palavra da pergunta, com quatro letras ou mais, encontrada no título.
- 6 ou mais pontos: confiança ALTA.
- 3 a 5 pontos: confiança MÉDIA.
- Menos de 3 pontos: orientação não encontrada.

**`assistente.py`**

Implementa a classe `Assistente`.

Responsabilidades:

- Receber perguntas do cidadão.
- Consultar a classe `BaseConhecimento`.
- Exibir a melhor resposta e até duas alternativas.
- Impedir o processamento de entradas com dados pessoais identificados.
- Solicitar avaliação do atendimento.
- Registrar histórico seguro.
- Calcular indicadores.
- Exportar relatórios CSV.

A busca por pontuação será independente do módulo de inteligência artificial.

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

O framework de agentes e o modelo de linguagem serão definidos e justificados durante o desenvolvimento.

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

Armazenará as sete fichas fictícias fornecidas pelo professor.

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

## 4. Armazenamento de dados

O projeto utilizará arquivos locais, sem necessidade inicial de banco de dados relacional.

| Arquivo | Finalidade |
|---|---|
| `data/base_conhecimento.json` | Orientações oficiais do PCP |
| `data/historico.json` | Resultados com rótulos controlados, sem perguntas livres |
| `data/atendimentos.csv` | Relatório exportado dos atendimentos |
| `modulos/documentos_ia/fichas/` | Base fictícia de Prompt & IA |
| `modulos/energia/analise.json` | Parâmetros e resultados energéticos |

O sistema deverá tratar arquivos JSON ausentes ou inválidos sem encerrar inesperadamente.

## 5. Segurança e privacidade

O RECOMEÇO deverá:

- Não solicitar cadastro ou identificação do usuário.
- Bloquear dados pessoais antes de consultar serviços externos.
- Não armazenar dados pessoais em históricos ou logs.
- Evitar repetir informações pessoais fornecidas indevidamente.
- Exibir fontes e datas de verificação.
- Informar que não representa um canal oficial.
- Não inventar orientações, procedimentos ou resultados.

As credenciais de serviços externos deverão ser armazenadas em variáveis de ambiente, sem publicação no GitHub.

## 6. Estratégia de integração

O sistema utilizará uma arquitetura modular.

O `main.py` será responsável apenas pela navegação e pelo acionamento das funcionalidades.

Cada módulo deverá ser capaz de executar suas operações sem depender desnecessariamente dos demais.

O módulo de PCP utilizará busca por regras. O módulo de Prompt & IA utilizará um agente de linguagem. O módulo de SERS utilizará cálculos e dados estruturados.

A indisponibilidade do serviço de IA não deverá impedir a utilização das funcionalidades independentes de PCP e SERS.

## 7. Testes previstos

**PCP**

- Testar busca e pontuação.
- Validar categorias e respostas.
- Testar entradas inválidas e dados pessoais.
- Validar indicadores e exportação CSV.
- Realizar pelo menos 10 atendimentos com 3 participantes externos.

**Prompt & IA**

- Executar o golden dataset de 26 perguntas.
- Avaliar as respostas com LLM as a Judge.
- Documentar uma melhoria e executar novamente os testes.
- Realizar testes com pelo menos 5 participantes externos, utilizando 3 tarefas simples.

**SERS**

- Validar fórmulas, unidades e resultados.
- Verificar a coerência da comparação energética.
- Confirmar a apresentação das referências e limitações.
- Realizar testes de compreensão e utilidade das recomendações.

## 8. Ordem de desenvolvimento

**Etapa 1 — Preparação**

- Criar e publicar o repositório.
- Organizar os arquivos e diretórios.
- Elaborar README e documentação da arquitetura.
- Preparar ambiente Python e arquivos de referência.

**Etapa 2 — PCP**

- Implementar as três classes obrigatórias.
- Construir a base de conhecimento.
- Implementar busca, navegação, histórico e indicadores.

**Etapa 3 — Prompt & IA**

- Carregar as sete fichas.
- Implementar o agente.
- Criar o avaliador automatizado.

**Etapa 4 — SERS**

- Definir parâmetros energéticos.
- Implementar cálculos.
- Comparar alternativas e integrar recomendações.

**Etapa 5 — Validação**

- Integrar os três módulos ao menu.
- Executar testes.
- Registrar evidências e melhorias.
- Atualizar documentação e preparar entregas.

## 9. Critérios para conclusão

O MVP estará pronto quando:

- O sistema executar corretamente pelo terminal.
- Os três módulos estiverem acessíveis pelo menu.
- Os requisitos específicos das disciplinas estiverem implementados.
- As respostas apresentarem referências e limitações.
- Os testes obrigatórios estiverem registrados.
- O GitHub contiver códigos, documentação e evidências necessárias.

---

**RECOMEÇO — Porque depois do desastre, a vida precisa continuar.**

## 10. Atualização de PCP em 12/11/2026

PCP mantém as três classes e usa somente bibliotecas nativas. A pergunta livre é processada em memória e não é persistida; o histórico e CSV usam rótulos controlados. Reformulações atualizam o mesmo atendimento. A facilidade é calculada por sessão aleatória, sem identificação pessoal. A opção `--dados` separa a coleta externa dos ensaios e dados de desenvolvimento. O ciclo de encerramento exporta CSV mesmo em EOF ou Ctrl+C, desde que o histórico esteja legível.

As regras detalhadas e limites estão em `decisoes_pcp.md`; fontes em `fontes_pcp.md`; roteiro externo em `plano_testes.md`. Partes anteriores que descrevem IA e SERS continuam como planejamento. Os testes reais exigidos por PCP e os vídeos permanecem pendentes.

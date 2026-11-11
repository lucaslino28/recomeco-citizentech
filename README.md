
# 🌱 RECOMEÇO

### Assistente Inteligente de Apoio a Vítimas de Desastres Climáticos

**Global Solution 2026.2 | FIAP — Ciência da Computação**

**Tema:** CitizenTech — Tecnologia que transforma a vida das pessoas.

---

## 📌 Sobre o projeto

O RECOMEÇO é um assistente digital desenvolvido para facilitar o acesso a informações confiáveis por pessoas afetadas por enchentes e outros desastres climáticos.

A solução busca apoiar a recuperação da rotina dos cidadãos, oferecendo orientações sobre serviços essenciais, assistência social, documentação pessoal e alternativas sustentáveis de energia.

O projeto integra três disciplinas da FIAP:

- Pensamento Computacional e Automação com Python (PCP)
- Prompt and Artificial Intelligence
- Soluções em Energias Renováveis e Sustentáveis (SERS)

## 🎯 Objetivo

Desenvolver um protótipo funcional que permita ao cidadão consultar orientações de maneira simples e acessível, utilizando Python, programação orientada a objetos e inteligência artificial.

O assistente não substitui órgãos públicos ou serviços oficiais de emergência.

## 💻 Funcionalidades previstas

### 1. Orientações após enchentes — PCP

Assistente baseado em regras, com:

- Base de conhecimento em JSON.
- Consulta por perguntas em texto livre.
- Navegação por categorias.
- Busca por palavras-chave com pontuação.
- Classificação de confiança das respostas.
- Exibição de fontes oficiais e datas de verificação.
- Proteção contra dados pessoais.
- Histórico de atendimentos, indicadores e exportação CSV.

### 2. Documentação pessoal — Prompt & IA

Agente de inteligência artificial para responder dúvidas sobre:

- RG e CPF.
- Título de eleitor.
- Carteira de Trabalho.
- Certidões.
- CNH.
- Regras gerais de atendimento.

Este módulo utilizará exclusivamente sete fichas fictícias da Central do Cidadão de Aurora, fornecidas pela FIAP.

**Atenção:** as informações desse módulo são simulações acadêmicas e não representam procedimentos reais.

O agente também será avaliado com um conjunto obrigatório de 26 perguntas, utilizando LLM as a Judge.

### 3. Energia e sustentabilidade — SERS

Módulo para analisar alternativas de fornecimento de energia destinadas à iluminação essencial de um abrigo temporário.

Serão comparadas:

- Rede elétrica convencional com iluminação LED.
- Sistema solar fotovoltaico com bateria e iluminação LED.

A comparação incluirá consumo em kWh, custos, autonomia, viabilidade, impactos ambientais e limitações.

## 🛠️ Tecnologias

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| POO | Organização das classes |
| JSON | Base de conhecimento e dados |
| CSV | Exportação de atendimentos |
| Framework de agentes | Módulo de inteligência artificial |
| Git e GitHub | Versionamento e documentação |

O framework de agentes e o modelo de linguagem serão definidos durante o desenvolvimento.

## 📁 Estrutura do projeto

```text
recomeco-citizentech/
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
├── requirements.txt
├── data/
│   ├── base_conhecimento.json
│   ├── historico.json
│   └── atendimentos.csv
├── modulos/
│   ├── documentos_ia/
│   │   ├── agente.py
│   │   ├── avaliador.py
│   │   ├── fichas/
│   │   └── testes/
│   └── energia/
│       ├── calculadora.py
│       ├── analise.json
│       └── referencias.md
├── testes/
├── evidencias/
└── documentacao/
```

## ▶️ Execução

Após a implementação das funcionalidades, o sistema será iniciado pelo terminal:

```bash
python3 main.py
```

O menu principal permitirá acessar os três módulos e consultar os indicadores de atendimento.

**Status atual:** estrutura inicial criada. Funcionalidades ainda em desenvolvimento.

## 🧪 Testes e validação

O projeto prevê:

- PCP: pelo menos 3 participantes externos e 10 atendimentos.
- Prompt & IA: avaliação das 26 perguntas obrigatórias, comparação antes e depois de uma melhoria e testes com pelo menos 5 pessoas externas.
- SERS: validação da compreensão e utilidade das recomendações energéticas.

Resultados e evidências serão adicionados conforme a execução dos testes.

## 🔒 Segurança e limitações

O RECOMEÇO não solicita cadastro nem necessita de CPF, telefone ou endereço para orientar o usuário.

O sistema deverá evitar a coleta e o armazenamento de informações pessoais desnecessárias.

O protótipo não oferece atendimento oficial, disponibilidade de abrigos em tempo real, emissão de documentos ou garantias de fornecimento energético.

## 🌎 ODS relacionados

- ODS 7 — Energia Limpa e Acessível.
- ODS 10 — Redução das Desigualdades.
- ODS 11 — Cidades e Comunidades Sustentáveis.
- ODS 13 — Ação Contra a Mudança Global do Clima.

## 👥 Equipe

FIAP — Ciência da Computação | Turma 1CCPX

- Lucas Lino Marques da Silva — RM: a preencher
- Gabriel M. — nome completo e RM a preencher
- Gustavo M. — nome completo e RM a preencher

## 📅 Global Solution 2026.2

**Prazo de entrega:** 19/11/2026

**Status:** Em desenvolvimento.

---

### RECOMEÇO
*Porque depois do desastre, a vida precisa continuar.*

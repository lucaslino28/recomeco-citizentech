# Testes com usuários — SERS

**Situação em 16/11/2026: ainda não realizados para este módulo.** Os testes automatizados e os participantes anteriores de PCP/IA não contam como uma rodada de SERS. Este arquivo é um roteiro e formulário vazio, atualizado para `sers-v2`.

As situações abaixo são sugestões, não uma quantidade obrigatória. O enunciado pede verificar compreensão e utilidade, registrando situações, comentários e ajustes; **não fixa um número de participantes ou de tarefas nem exige explicitamente participantes externos**. A equipe deve escolher uma coleta possível e informar o que realmente aconteceu, sem importar mínimos de outra disciplina.

## Preparação do aplicador

1. Rode `python3 main.py --dados data/demonstracao_sers` na pasta do projeto e escolha 3. Se a pessoa estiver distante, ela pode acompanhar por compartilhamento de tela e orientar suas escolhas; nesse caso, anote que a navegação foi intermediada pelo aplicador.
2. Explique: “Este é um protótipo sobre iluminação de um abrigo. Os valores são estimados. Queremos saber se as explicações ajudam a entender as alternativas. Não informe dados pessoais.”
3. Use código como S01, sem nome, telefone, endereço ou documento. Peça autorização para anotar comentários sem identificação. Gravação não é necessária.
4. Antes de cada pessoa, use 5 para restaurar. Deixe a pessoa escolher as opções e explique os controles quando necessário; anote a ajuda dada. Não leia as respostas esperadas antes da tentativa.

Não é preciso instalar o projeto no computador de cada pessoa. A avaliação pode ser organizada com pessoas disponíveis. Se integrantes da equipe usarem e avaliarem o módulo, registre que se trata de avaliação interna, com essa limitação; não a descreva como participação externa. Execuções automáticas verificam o sistema e não substituem comentários/compreensão de usuários.

## Situações sugeridas

| Código | Pedido à pessoa | O que o aplicador verifica depois |
|---|---|---|
| T01 — custo e decisão | “Veja a comparação do abrigo. Para 30 dias com a rede funcionando, qual alternativa tem menor custo estimado? Em que situação você consideraria a outra?” | Reconhece A como menor custo no exemplo e explica o papel da bateria/continuidade, sem prometer economia ou segurança garantida. |
| T02 — pouco sol | “Mantenha o consumo inicial e simule 1 hora de sol pleno por dia. O conjunto atende à iluminação? Conte com suas palavras o que mudou.” | Identifica serviço parcial, déficit e dependência de recarga; não confunde HSP com horas de iluminação. |
| T03 — autonomia e limites | “Restaure o exemplo. Consulte uma falta de luz com bateria a 50%. Dura uma noite de 6 h? Depois encontre a origem dos valores e uma limitação.” | Encontra 3,84 h e insuficiência para 6 h; identifica estimativas, fonte e algum limite relevante. |
| T04 — sequência de dias | “Acompanhe a bateria na sequência pronta de cinco dias com pouco sol. A iluminação fica completa em todas as noites? Explique o que acontece com a carga.” | Usa 6 → 2 → Enter; identifica 3 de 5 noites completas, carga acumulada e déficit, sem interpretar a sequência como previsão. |

Ao terminar, pergunte sem induzir: “O que ficou confuso?”, “A orientação ajudaria você a entender a decisão? Por quê?” e “O que deveria mudar?”. Registre as palavras da pessoa ou identifique que é um resumo feito pelo aplicador. Tempos e notas podem ser coletados se úteis, mas não são exigidos neste roteiro.

## Modelo por participante — copiar e preencher depois do teste

```text
Código:
Data e versão do sistema:
Modalidade (interna à equipe / outra participação real):
Forma de acesso (teclado direto / tela compartilhada com mediação):
Autorizou registro sem identificação? Sim / Não

T01 — escolhas e resposta com as próprias palavras:
Ajuda necessária / dificuldade:
T02 — escolhas e resposta com as próprias palavras:
Ajuda necessária / dificuldade:
T03 — escolhas e resposta com as próprias palavras:
Ajuda necessária / dificuldade:
T04 (se aplicada) — escolhas e resposta com as próprias palavras:
Ajuda necessária / dificuldade:

Comentário sobre clareza (literal ou resumo identificado):
Comentário sobre utilidade (literal ou resumo identificado):
Sugestão recebida:
Interpretação do aplicador e limitação da observação:
```

Se não autorizar o registro, não publique suas falas. Não atribua resultados a alguém que não participou ou conclua compreensão só porque a tela mostrou o cálculo correto.

## Consolidação e ajustes — preencher após a coleta

| Situação / versão | Comentário ou dificuldade observada | Ajuste realizado e motivo, ou justificativa para não alterar | Verificação técnica | Nova consulta ao usuário, se ocorreu |
|---|---|---|---|---|
| Pendente de coleta | — | — | — | — |

Depois da coleta, registre número real de pessoas, situações executadas, modalidade de participação, ajuda necessária, dificuldades, utilidade percebida e limites da amostra. Remova dados pessoais e publique somente os registros autorizados em `evidencias/sers/usuarios/`. Atualize este documento e o checklist para apontar para esses arquivos. Ajustes só devem ser descritos como feitos depois de implementados e conferidos; não declarar melhoria de compreensão sem nova observação.

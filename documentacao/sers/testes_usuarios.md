# Testes com usuários — SERS

Em 17/11/2026, uma pessoa de fora do grupo testou a `sers-v2`. Lucas anotou os comentários e identificamos uma dificuldade com HSP. O [relatório do teste](../../evidencias/sers/usuarios/rodada_2026-11-17/README.md) mostra as situações e a mudança que fizemos na v3. Ainda não repetimos o teste com a nova explicação.

## Como preparar os próximos testes

1. Abrir `python3 main.py --dados data/demonstracao_sers` e escolher a opção 3.
2. Explicar que o programa compara formas de iluminar um abrigo e usa valores estimados.
3. Pedir para a pessoa experimentar as situações abaixo e contar o que entendeu.
4. Anotar a ajuda necessária, as dúvidas e as sugestões, usando só um código como S01.
5. Antes de outra sessão, usar a opção 5 para restaurar os valores iniciais.

O enunciado de SERS não define quantidade mínima nem exige pessoas de fora do grupo. Na nossa rodada participou uma pessoa externa. Podemos fazer novos testes localmente ou por compartilhamento de tela, anotando como a pessoa participou.

## Situações sugeridas

| Código | Pedido à pessoa | O que queremos observar |
|---|---|---|
| T01 — custo e decisão | “Veja a comparação do abrigo. Para 30 dias com a rede funcionando, qual alternativa tem menor custo estimado? Em que situação você consideraria a outra?” | Reconhece A como menor custo no exemplo e explica o papel da bateria/continuidade, sem prometer economia ou segurança garantida. |
| T02 — pouco sol | “Mantenha o consumo inicial e simule 1 hora de sol pleno por dia. O conjunto atende à iluminação? Conte com suas palavras o que mudou.” | Identifica serviço parcial, déficit e dependência de recarga; não confunde HSP com horas de iluminação. |
| T03 — autonomia e limites | “Restaure o exemplo. Consulte uma falta de luz com bateria a 50%. Dura uma noite de 6 h? Depois encontre a origem dos valores e uma limitação.” | Encontra 3,84 h e insuficiência para 6 h; identifica estimativas, fonte e algum limite relevante. |
| T04 — sequência de dias | “Acompanhe a bateria na sequência pronta de cinco dias com pouco sol. A iluminação fica completa em todas as noites? Explique o que acontece com a carga.” | Usa 6 → 2 → Enter; identifica 3 de 5 noites completas, carga acumulada e déficit, sem interpretar a sequência como previsão. |

Ao terminar, perguntar o que ficou confuso, se a orientação ajudou e o que deveria mudar. As anotações podem resumir os comentários; nesse caso, vamos indicar que são um resumo. Tempo e nota podem ajudar, mas não são exigidos no roteiro de SERS.

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
Observações de quem acompanhou o teste:
```

Vamos guardar apenas os comentários autorizados, sem nome ou contato da pessoa.

## Consolidação e ajustes

| Situação / versão | Comentário ou dificuldade observada | Ajuste realizado e motivo, ou justificativa para não alterar | Verificação técnica | Nova consulta ao usuário, se ocorreu |
|---|---|---|---|---|
| S01, 17/11, sers-v2 | HSP entendida como duração de sol na casa; comentário positivo sobre a utilidade, anotado por Lucas | sers-v3 explica energia equivalente e pede confirmar/corrigir/cancelar valores altos | Cinco regressões novas; 171 testes gerais aprovados | Ainda não realizada |

Os arquivos de cada aplicação ficam em `evidencias/sers/usuarios/`. Depois dos testes, vamos registrar as mudanças feitas e conferir se a explicação nova ficou mais clara em uma próxima sessão.

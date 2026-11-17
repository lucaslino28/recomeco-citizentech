# Avaliação de SERS — 17/11/2026

Uma participante externa à equipe, código **S01**, conforme relato do aplicador. Versão avaliada: **sers-v2**, commit local `c87be23`. A participação é informada pelo aplicador; as operações e saídas são sustentadas pelo terminal fornecido e pelo relatório gerado pelo programa. Não são execuções automatizadas atribuídas a uma pessoa.

## Procedimento e apoio

Segundo o aplicador, a participante precisou de ajuda para iniciar o terminal. Depois de iniciado, navegou e fez o teste sozinha. O comando usado foi `python3 main.py --dados data/demonstracao_sers`, seguido da opção 3. O nome da pasta de execução não caracteriza o tipo de participação; a modalidade foi informada pelo aplicador.

A participante executou estas situações efetivas, sem substituir suas escolhas pelas do roteiro sugerido:

| Situação | Parâmetros e resultado observado |
|---|---|
| Comparação inicial | 20 lâmpadas de 9 W, 6 h/noite, 30 dias: 32,4 kWh; A R$ 532,40 e B R$ 6.910,00 no orçamento didático. |
| Cenário personalizado | 10 lâmpadas de 5 W, 9 h/noite, 30 dias, 12 HSP e R$ 0,789/kWh: 13,5 kWh e A R$ 510,65. As 12 HSP foram uma entrada de simulação, não recurso solar local medido. |
| Autonomia | Restaurou o exemplo; bateria a 50%, sem recarga: 3,84 h, insuficientes para uma noite de 6 h. |
| Cinco dias | Sequência 4/1/0/1/4 HSP, carga inicial de 90%: 3 noites completas, cobertura de 69,4%, déficit total de 1,6518 kWh. A geração do primeiro dia recompõe a bateria antes da noite. |
| Fontes e exportação | Consultou a opção 4, exportou pela opção 8 e encerrou normalmente. O relatório contém os parâmetros restaurados e a última sequência, não todo o histórico de alterações. |

Não foi executado o cenário sugerido de 1 HSP no ajuste individual; a navegação por necessidade (opção 7) também não aparece nesta sessão. A sequência de vários dias contém dias com 1 e 0 HSP. Essas diferenças são registradas sem tratar o roteiro sugerido como obrigatório.

## Comentários recebidos

**Síntese do relato do aplicador, não citação literal da participante:**

- Gostou da ideia e considerou útil apoiar escolhas entre rede e energia solar, especialmente para quem não tem conhecimento para calcular sozinho.
- Precisou de ajuda para abrir/iniciar o terminal; depois navegou sem ajuda, segundo o aplicador.
- Escolheu 12 HSP pensando no tempo aproximado em que o sol incide na casa. Isso revelou confusão entre duração de incidência solar e energia equivalente acumulada.

O comentário favorável sobre utilidade não comprova acerto em cada interpretação dos números. Não foram informados tempos, notas, respostas de compreensão por tarefa ou sugestão literal de mudança. Não se calcularam percentuais de acerto humano ou médias de satisfação. A amostra de uma participante é pequena e de conveniência.

## Ajuste decorrente da avaliação

| Problema observado | Mudança aplicada em sers-v3 | Verificação | Nova consulta à participante |
|---|---|---|---|
| HSP interpretada como horas em que há sol na casa | Campo renomeado para energia solar diária equivalente; explicação com exemplo concreto e orientação para manter uma hipótese ou consultar uma referência pública. Entradas a partir de 8 HSP pedem confirmação, correção ou cancelamento, tanto no ajuste geral quanto na sequência manual. | Cinco regressões específicas de interface, incluindo correção, confirmação explícita, cancelamento sem aplicação parcial e HSP zero. Contas originais preservadas. Suíte total de 171 testes locais aprovada. | Ainda não realizada; não foi declarado ganho de compreensão após a mudança. |

O limiar de 8 HSP é uma decisão didática de interface, não limite físico, afirmação sobre clima brasileiro ou validação de um dado real. Valores elevados continuam permitidos como hipóteses explicitamente confirmadas. O sistema não troca o número escolhido sem a pessoa decidir.

Para a ajuda inicial no terminal, o comando de execução já está no guia. Esse ponto deve ser mostrado ao preparar a sessão. Não foi atribuída à participante uma falha de navegação dentro do programa.

## Arquivos e origem

- [Terminal S01](terminal_s01.txt): transcrição enviada pelo aplicador; identificadores do ambiente e caminhos pessoais substituídos, espaços finais normalizados. Entradas numéricas e saídas mantidas.
- [Relatório S01](relatorio_s01.txt): cópia byte a byte do arquivo exportado em 17/11/2026, 19:28:14 UTC. Esse horário é de geração do arquivo, não duração do teste. O arquivo original permanece localmente em `data/relatorios_sers/`.
- [Relato do aplicador](relato_aplicador.txt): mensagem fornecida, identificada como relato indireto.
- [Registro estruturado](registro_s01.json): situações, conferência técnica, origem, limites e hashes dos originais recebidos.
- [Verificação técnica após o ajuste](../../pos_usuario_2026-11-17/README.md): separada da sessão de S01.

Nenhum nome, contato ou vínculo familiar da participante foi publicado. Os dados e resultados originais de PCP e IA não foram alterados.

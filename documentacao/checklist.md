# Checklist da entrega

Atualizado em 17/11/2026. Marcamos o que já fizemos e deixamos em aberto as pendências da entrega.

## PCP

- [x] Três classes e composição, mantendo a arquitetura existente.
- [x] Base com 34 orientações, 3 categorias e palavras-chave suficientes.
- [x] Campos, tipos, IDs, datas e formato das fontes validados ao carregar.
- [x] Fontes consultadas e referências documentadas.
- [x] Normalização, pontuação, confiança e até duas alternativas.
- [x] Categorias, entradas inválidas e retorno com 0.
- [x] Bloqueio mínimo exigido e histórico sem texto livre.
- [x] Histórico JSON, indicadores e exportação CSV.
- [x] Reformulação contada no mesmo atendimento e facilidade por sessão.
- [x] Tratamento de arquivos ausentes, corrompidos e registros malformados.
- [x] Testes automatizados isolados e conferência em pseudoterminal.
- [x] Plano e modelo de registro para testes externos.
- [x] Escolha de assuntos ambíguos, sugestões confirmadas e alternativas selecionáveis.
- [x] Respostas com passos e limitações, mantendo fontes e pontuação.
- [x] Cobertura de oito grupos de eventos e navegação por tipo de desastre.
- [x] Regressão dos 42 cenários anteriores e verificação de 50 casos novos.
- [x] Avaliação de 14/11 documentada: 3 pessoas de fora do grupo e 10 atendimentos.
- [x] Indicadores da rodada, dúvidas sem solução e melhoria aplicada após a avaliação no README.
- [x] Relatório com objetivo, metodologia, participantes/atendimentos, resultados, indicadores, problemas, análise, melhorias e conclusão.
- [x] Registros originais preservados e indicadores filtrados sem excluir a linha anterior dos arquivos.
- [x] Regressão pós-avaliação: 89 testes e reprodução técnica das dez frases, sem criar novas notas humanas.
- [x] Documentação consolidada e roteiro de vídeo preparado.
- [x] Nomes completos e RMs de todos os integrantes.
- [ ] Vídeo técnico integrado PCP + SERS de 5 a 8 minutos, com todos explicando, conteúdo das duas disciplinas e alteração ao vivo de PCP.
- [ ] Link do vídeo no README e no TXT de entrega.
- [x] Publicação da versão inicial de PCP no GitHub, commit cf25bdc.
- [x] Registros anteriores versionados localmente em ca491d4 e b56f7a6.
- [x] Revisão de PCP publicada no GitHub em a4c41c9.
- [ ] Conferência pública dos links e envio do TXT no Portal.

## Demais disciplinas

### Prompt & IA

- [x] Nomes completos e RMs no início dos documentos e notebook.
- [x] Sete fichas originais de Aurora e 26 mensagens/esperados do enunciado preservados.
- [x] Um agente LangChain com Groq, opção 2, perguntas livres e menu por assuntos.
- [x] Filtro de dados pessoais antes da API, avisos, limites e sem histórico de perguntas de IA.
- [x] Modelos e arquitetura justificados; diagrama SVG/PNG.
- [x] LLM juiz com quatro critérios, registros por caso e retomada de rodada.
- [x] Rodadas completas, melhorias e comparação automática preservadas.
- [x] Notebook executado com tabelas reais e análise crítica do juiz.
- [x] Seis casos conferidos manualmente por Lucas, com as observações registradas.
- [x] Plano e modelos vazios para avaliação humana.
- [x] Coleta documentada segundo as anotações de Lucas: cinco pessoas externas, três tarefas por código, 15 tempos e 25 notas; tarefas efetivas variadas.
- [x] Relatório com acerto do juiz, tempo humano e facilidade, separados da conclusão informada das tarefas.
- [x] CSVs fornecidos preservados, origem e transcrição documentadas; análise local reproduzível.
- [x] V4 corrige os casos identificados de banco, lista documental do RG e limite de recuperação de CPF; 135 testes locais aprovados.
- [x] Código v4, revisão da amostra e coleta publicados no GitHub; commit de conteúdo e30872d e acesso HTTP ao repositório conferidos.

### SERS

- [x] Público e necessidade de iluminação noturna de abrigo definidos.
- [x] Hipóteses de consumo, sol, equipamentos e orçamento identificadas e justificadas, com unidades e período.
- [x] Rede e solar com bateria comparados para os mesmos LEDs e período.
- [x] Memória de cálculo, custos de implantação/operação, sensibilidade, viabilidade e impactos ambientais qualitativos.
- [x] Integração na opção 3, simulação guiada, consulta de autonomia, restauração e fontes no terminal.
- [x] Limites de geração, bateria e potência do inversor; atendimento parcial sem promessa de economia.
- [x] 36 testes específicos de SERS e conjunto completo de testes de 171 testes locais aprovados; evidências técnicas separadas.
- [x] Dados públicos NASA POWER com cópia, unidade, período, consulta e hash; exemplos de capacidades dos fabricantes separados do orçamento estimado.
- [x] Bateria acumulada entre dias, reserva e conservação da energia testadas; déficit e excedente explícitos.
- [x] Atendimento por necessidade, custos de operação/aquisição separados e sensibilidade hipotética do investimento.
- [x] Exportação explícita de relatório técnico local, sem se passar por avaliação de usuário.
- [x] Documentação, explicação do código para a equipe, modelo de teste com usuários, roteiro de vídeo e TXT preparados.
- [x] Avaliação de 17/11 registrada: uma pessoa de fora do grupo, registro do terminal, comentários anotados por Lucas e melhoria de HSP. Ainda falta conferir a nova explicação com ela.
- [ ] Gravar/publicar vídeo não listado integrado PCP + SERS, de 5 a 8 minutos; preencher a mesma URL nos dois TXT.
- [ ] Ensaiar a explicação das hipóteses de SERS para o vídeo.
- [ ] Conferir acesso aos links e enviar somente o TXT no prazo de SERS informado no Portal.

Veja o [índice de SERS](sers/README.md) para executar, reproduzir os cálculos e localizar cada evidência.

## Referências para conferir PCP

[Índice da documentação](README.md), [avaliação](pcp/avaliacao_usuarios.md), [roteiro do vídeo](pcp/roteiro_video.md) e [TXT](../entregas/pcp.txt). Os registros de PCP estão por sessão, sem identificar as pessoas. Ainda não repetimos o teste depois das correções.

## Organização para correção

- [x] Um documentação para cada disciplina e navegação inicial no README.
- [x] Estrutura Python/`data/` de PCP mantida como no enunciado; módulos de IA/SERS separados.
- [x] Documentação e evidências de PCP, IA e SERS identificadas; histórico separado de avaliações.
- [x] TXT de PCP/SERS centralizados e lista de materiais de IA para conferir no Portal.
- [x] Organização e links conferidos; código, dados e testes revisados.

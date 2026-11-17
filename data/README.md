# Dados de PCP e arquivos locais

A estrutura `data/base_conhecimento.json`, `data/historico.json` e `data/atendimentos.csv` foi mantida como no enunciado de PCP.

- `base_conhecimento.json`: 34 orientações com categorias, palavras-chave, fontes e datas de conferência.
- `historico.json`: registros anonimizados de atendimento; perguntas livres não são armazenadas.
- `atendimentos.csv`: exportação do histórico de PCP. Os dados originais incluem uma linha anterior à rodada de 14/11; as análises usam filtro de data sem removê-la.

Executar `python3 main.py` usa essa pasta. Para ensaios, use `python3 main.py --dados data/demonstracao_pcp`; a pasta de demonstração é local e ignorada pelo Git. As evidências preservadas da avaliação estão em [PCP](../evidencias/pcp/README.md).

Os relatórios técnicos exportados por SERS ficam localmente em `data/relatorios_sers/`, também ignorados pelo Git. A sessão S01 tem uma cópia de evidência explicitamente identificada em [SERS](../evidencias/sers/usuarios/rodada_2026-11-17/README.md). As fichas fictícias de IA ficam em `modulos/documentos_ia/fichas/`, separadas da base oficial de PCP.

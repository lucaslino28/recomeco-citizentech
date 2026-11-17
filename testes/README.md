# Testes técnicos e análises

Os testes automatizados não representam participação humana. Usam `unittest`, dados fictícios, pastas temporárias e controladores de IA de teste, sem chamadas pagas.

```bash
python -B -m unittest discover -s testes -v
```

A conjunto completo de testes usa o ambiente com `requirements.txt` instalado. Os arquivos podem continuar na mesma pasta para permitir a descoberta por um único comando.

| Disciplina | Testes | Análise de dados já coletados |
|---|---|---|
| PCP | `test_pcp.py`; casos nos três JSONs `casos_*_pcp.json` | `python -B testes/analisar_validacao_pcp.py` — lê o mesmo CSV da rodada na localização organizada. |
| IA | `test_ia.py`, `test_fechamento_ia.py`, `test_usuarios_ia.py` | `python -B testes/analisar_usuarios_ia.py` — lê a coleta; o notebook apresenta o benchmark existente. |
| SERS | `test_sers.py` | `python -B testes/analisar_sers.py` — cálculos técnicos, sem pessoas ou API. |

Para filtrar uma disciplina, use por exemplo `python -B -m unittest discover -s testes -p 'test_sers.py' -v`. Os logs históricos mantêm as contagens da versão em que foram executados; a verificação da reorganização fica em [evidencias/organizacao](../evidencias/organizacao/README.md).

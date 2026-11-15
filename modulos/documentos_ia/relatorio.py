"""Gera a comparação das duas rodadas completas, sem chamar a API."""

import argparse
import csv
import json
from pathlib import Path

from modulos.documentos_ia.agente import RAIZ
from modulos.documentos_ia.avaliador import comparar


def gerar(antes, depois, pasta):
    antes, depois, pasta = Path(antes), Path(depois), Path(pasta)
    destino_json = pasta / "comparacao.json"
    destino_csv = pasta / "comparacao.csv"
    if any(p.resolve() in [antes.resolve(), depois.resolve()] for p in [destino_json, destino_csv]):
        raise ValueError("A saída não pode sobrescrever uma rodada original.")
    inicial = json.loads(antes.read_text(encoding="utf-8"))
    final = json.loads(depois.read_text(encoding="utf-8"))
    dados = comparar(inicial, final)
    iniciais = {r["id"]: r for r in inicial["resultados"]}
    finais = {r["id"]: r for r in final["resultados"]}
    if set(iniciais) != set(range(1, 27)) or set(finais) != set(iniciais):
        raise ValueError("Cada rodada precisa conter os IDs originais de 1 a 26.")
    linhas = []
    for numero in range(1, 27):
        a, b = iniciais[numero], finais[numero]
        linhas.append({"id": numero, "tipo": a["tipo"], "acertou_antes": a["acertou"],
                       "acertou_depois": b["acertou"], "status_antes": a["status"],
                       "status_depois": b["status"]})
    dados["casos"] = linhas
    dados["natureza"] = "Comparação de LLM juiz; não mede facilidade ou tempo de participantes."
    pasta.mkdir(parents=True, exist_ok=True)
    destino_json.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with destino_csv.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]), lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(linhas)
    return dados


if __name__ == "__main__":
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("--antes", type=Path, default=RAIZ / "evidencias/ia/antes.json")
    argumentos.add_argument("--depois", type=Path, default=RAIZ / "evidencias/ia/depois.json")
    argumentos.add_argument("--pasta", type=Path, default=RAIZ / "evidencias/ia")
    opcoes = argumentos.parse_args()
    try:
        resultado = gerar(opcoes.antes, opcoes.depois, opcoes.pasta)
        print(json.dumps({k: v for k, v in resultado.items() if k != "casos"}, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError):
        argumentos.exit(1, "Não foi possível comparar. Confira se as duas rodadas estão completas e compatíveis.\n")

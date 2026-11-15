"""Recalcula indicadores de uma rodada a partir do CSV, sem alterar os registros."""

import argparse
import csv
import hashlib
import json
from datetime import date
from pathlib import Path


def analisar(caminho, data_filtro):
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        todos = list(csv.DictReader(arquivo))
    registros = [r for r in todos if r["data"][:10] == str(data_filtro)]
    total = len(registros)
    encontrados = sum(r["encontrou"] == "True" for r in registros)
    ajudaram = sum(r["ajudou"] == "True" for r in registros)
    notas = {}
    for registro in registros:
        if registro.get("sessao") and registro.get("facilidade"):
            notas[registro["sessao"]] = int(registro["facilidade"])
    return {
        "data_avaliacao": str(data_filtro),
        "arquivo": caminho.name,
        "sha256": hashlib.sha256(caminho.read_bytes()).hexdigest(),
        "registros_excluidos_pelo_filtro": len(todos) - total,
        "atendimentos": total,
        "orientacoes_encontradas": encontrados,
        "encontrados_percentual": encontrados / total * 100 if total else 0,
        "ajudaram": ajudaram,
        "ajudaram_percentual": ajudaram / total * 100 if total else 0,
        "encontrou_mas_nao_ajudou": sum(r["encontrou"] == "True" and r["ajudou"] != "True" for r in registros),
        "sem_correspondencia": total - encontrados,
        "sem_solucao": total - ajudaram,
        "facilidade_media_por_sessao": sum(notas.values()) / len(notas) if notas else None,
        "sessoes_avaliadas": len(notas),
        "tempo_medio_registrado_segundos": round(sum(float(r["tempo_segundos"]) for r in registros) / total, 2) if total else 0,
        "tentativas_media": sum(int(r["tentativas"]) for r in registros) / total if total else 0,
        "participantes": "Quantidade e metodologia informadas pela equipe; sessões não identificam pessoas."
    }


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("--arquivo", type=Path,
                            default=raiz / "evidencias/validacao_usuarios_2026-11-14.csv")
    argumentos.add_argument("--data", type=date.fromisoformat, default=date(2026, 11, 14))
    opcoes = argumentos.parse_args()
    try:
        resultado = analisar(opcoes.arquivo, opcoes.data)
    except (OSError, ValueError, KeyError, csv.Error) as erro:
        argumentos.exit(1, f"Não foi possível analisar o CSV: {erro}\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

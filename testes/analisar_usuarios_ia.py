"""Recalcula a coleta de usuários de IA sem alterar tempos, notas ou respostas."""

import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path
from statistics import mean


CAMPOS_TAREFAS = ["participante_anonimo", "tarefa", "tempo_segundos", "acerto_0_1", "falha_api_0_1"]
CAMPOS_NOTAS = ["participante_anonimo", "p1_menu", "p2_encontrar", "p3_clareza", "p4_fontes_limites", "p5_teclado"]


def ler_csv(caminho, campos):
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        if leitor.fieldnames != campos:
            raise ValueError("Cabeçalho do CSV diferente do modelo.")
        dados = list(leitor)
    if not dados:
        raise ValueError("O CSV ainda não possui registros.")
    for linha in dados:
        if None in linha or any(v is None for v in linha.values()):
            raise ValueError("Há uma linha incompleta ou com colunas extras.")
        if not re.fullmatch(r"P\d{2}", linha["participante_anonimo"]):
            raise ValueError("Use apenas códigos anônimos como P01.")
    return dados


def analisar(pasta):
    pasta = Path(pasta)
    tarefas = ler_csv(pasta / "tarefas.csv", CAMPOS_TAREFAS)
    questionarios = ler_csv(pasta / "questionario.csv", CAMPOS_NOTAS)
    pares = set()
    for registro in tarefas:
        par = (registro["participante_anonimo"], registro["tarefa"])
        if registro["tarefa"] not in ["T01", "T02", "T03"] or par in pares:
            raise ValueError("Há tarefa inválida ou duplicada para o mesmo participante.")
        pares.add(par)
        tempo = float(registro["tempo_segundos"])
        if not math.isfinite(tempo) or tempo < 0:
            raise ValueError("O tempo deve ser um número finito e não negativo.")
        registro["tempo_segundos"] = tempo
        for campo in ["acerto_0_1", "falha_api_0_1"]:
            if registro[campo] not in ["0", "1"]:
                raise ValueError("Conclusão e falha de API devem ser 0 ou 1.")
            registro[campo] = int(registro[campo])
    participantes = {r["participante_anonimo"] for r in tarefas}
    for participante in participantes:
        if sum(r["participante_anonimo"] == participante for r in tarefas) != 3:
            raise ValueError("Cada participante deve possuir três tarefas.")
    notas = {}
    for registro in questionarios:
        participante = registro["participante_anonimo"]
        if participante in notas:
            raise ValueError("Há questionário duplicado.")
        valores = [int(registro[campo]) for campo in CAMPOS_NOTAS[1:]]
        if any(nota < 1 or nota > 5 for nota in valores):
            raise ValueError("Cada nota deve estar entre 1 e 5.")
        notas[participante] = valores
    if set(notas) != participantes:
        raise ValueError("Os participantes de tarefas e questionários devem coincidir.")
    tempos = [r["tempo_segundos"] for r in tarefas]
    concluidas = sum(r["acerto_0_1"] for r in tarefas)
    return {
        "natureza": "Dados de aplicação informados pela equipe; não atestam identidade ou presença por si só.",
        "participantes_registrados": len(participantes), "tarefas": len(tarefas),
        "questionarios": len(notas), "avaliacoes_individuais": sum(len(n) for n in notas.values()),
        "minimo_cinco_participantes_registrados": len(participantes) >= 5,
        "tarefas_concluidas_informadas": concluidas,
        "conclusao_percentual": round(concluidas / len(tarefas) * 100, 2),
        "falhas_api_informadas": sum(r["falha_api_0_1"] for r in tarefas),
        "tempo_total_segundos": round(sum(tempos), 2),
        "tempo_medio_segundos": round(mean(tempos), 2),
        "tempo_minimo_segundos": min(tempos), "tempo_maximo_segundos": max(tempos),
        "media_questionario": round(mean(n for valores in notas.values() for n in valores), 2),
        "medias_por_item": {campo: round(mean(valores[i] for valores in notas.values()), 2)
                            for i, campo in enumerate(CAMPOS_NOTAS[1:])},
        "por_participante": {p: {
            "tempo_medio_segundos": round(mean(r["tempo_segundos"] for r in tarefas if r["participante_anonimo"] == p), 2),
            "media_questionario": round(mean(notas[p]), 2)} for p in sorted(participantes)},
        "limites": ["Os códigos T01/T02/T03 indicam a posição; os objetivos da rodada variaram.",
                    "Conclusão informada pelo aplicador não equivale a precisão factual independente.",
                    "O tempo inclui interação humana, conforme método informado, não apenas inferência da API."],
        "csvs_sha256": {nome: hashlib.sha256((pasta / nome).read_bytes()).hexdigest()
                        for nome in ["tarefas.csv", "questionario.csv"]}
    }


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("--pasta", type=Path,
                            default=raiz / "evidencias/ia/usuarios/rodada_2026-11-15")
    opcoes = argumentos.parse_args()
    try:
        print(json.dumps(analisar(opcoes.pasta), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, csv.Error) as erro:
        argumentos.exit(1, f"Não foi possível analisar a coleta: {erro}\n")

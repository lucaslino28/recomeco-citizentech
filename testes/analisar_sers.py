"""Imprime evidências técnicas reproduzíveis de SERS; não coleta usuários ou usa API."""

import hashlib
import json
from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from modulos.energia.calculadora import CalculadoraEnergia


def analisar():
    calculadora = CalculadoraEnergia()
    ref = calculadora.referencia_solar()
    cenarios = [
        ("Exemplo inicial", {}),
        ("Pouco sol", {"hsp": 1}),
        ("Sem sol — regime diário sem energia inicial gratuita", {"hsp": 0}),
        ("Bateria limita noite longa", {"hsp": 8, "horas_dia": 12}),
        ("Sobrecarga do inversor", {"lampadas": 40}),
        ("60 dias — mesmo período nas duas alternativas", {"dias": 60}),
        ("Referência pública horizontal São Paulo — menor média mensal", {"hsp": ref["hsp_menor"]}),
    ]
    resultados = []
    for nome, alteracoes in cenarios:
        consumo = dict(calculadora.dados["consumo"], **alteracoes)
        resultados.append({"situacao": nome, "resultado": calculadora.calcular(consumo)})
    arquivos = ["modulos/energia/analise.json", "modulos/energia/calculadora.py",
                "modulos/energia/fontes/nasa_sao_paulo.json"]
    return {
        "natureza": "Validação técnica automatizada com cenários hipotéticos; não são testes com usuários.",
        "versao": calculadora.dados["versao"],
        "revisao_base": calculadora.dados["verificado_em"],
        "reproduzir": "python3 -B testes/analisar_sers.py",
        "sha256": {p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in arquivos},
        "premissas": "modulos/energia/referencias.md",
        "referencia_publica": calculadora.referencia_solar(),
        "operacao_e_sensibilidade": calculadora.custos_operacao(),
        "sequencias": {
            "cinco_dias_pouco_sol": calculadora.simular_dias([4, 1, 0, 1, 4]),
            "tres_dias_sem_sol": calculadora.simular_dias([0, 0, 0]),
            "bateria_vazia_pouco_sol": calculadora.simular_dias([1, 1, 4], carga_pct=0),
        },
        "cenarios": resultados,
        "falta_de_luz_sem_recarga": [calculadora.falta_de_luz(carga_pct=carga) for carga in [100, 50, 20, 0]],
        "limites": "Não mede clima, preços, condições de instalação ou percepção humana. Impactos ambientais qualitativos, sem CO2 ou análise de ciclo de vida.",
    }


if __name__ == "__main__":
    print(json.dumps(analisar(), ensure_ascii=False, indent=2, allow_nan=False))

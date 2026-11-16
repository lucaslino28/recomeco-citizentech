"""Simulação educacional de iluminação. Usa somente a biblioteca padrão."""

import json
import math
from pathlib import Path


PASTA = Path(__file__).resolve().parent
# Limites de entrada do protótipo, não limites de um projeto elétrico.
CAMPOS = {
    "lampadas": ("Quantidade de lâmpadas", 1, 200, True),
    "potencia_lampada_w": ("Potência de cada lâmpada (W)", 0.1, 100, False),
    "horas_dia": ("Horas de luz por noite", 0.1, 24, False),
    "dias": ("Período em dias", 1, 365, True),
    "hsp": ("Horas de sol pleno por dia (HSP)", 0, 12, False),
    "tarifa_kwh": ("Preço variável da energia (R$/kWh)", 0, 10, False),
}


def numero(valor, minimo, maximo, inteiro=False):
    """Recusa infinitos, NaN, booleanos e valores fora do intervalo."""
    if isinstance(valor, bool):
        raise ValueError("Informe um número.")
    try:
        convertido = float(str(valor).strip().replace(",", "."))
    except (ValueError, TypeError, OverflowError):
        raise ValueError("Informe um número, usando ponto ou vírgula decimal.") from None
    if not math.isfinite(convertido) or not minimo <= convertido <= maximo:
        raise ValueError(f"Use um valor entre {minimo:g} e {maximo:g}.")
    if inteiro and not convertido.is_integer():
        raise ValueError("Use uma quantidade inteira.")
    return int(convertido) if inteiro else convertido


def formato(valor, casas=2):
    return f"{valor:,.{casas}f}".replace(",", "_").replace(".", ",").replace("_", ".")


class CalculadoraEnergia:
    def __init__(self, caminho=None):
        self.caminho = Path(caminho) if caminho else PASTA / "analise.json"
        self.dados = json.loads(self.caminho.read_text(encoding="utf-8"))
        self.validar_base()

    def validar_base(self):
        """Evita resultados enganosos quando a base está incompleta ou inválida."""
        if not isinstance(self.dados, dict):
            raise ValueError("A análise deve ser um objeto JSON.")
        for chave in ["versao", "verificado_em", "cenario", "origem"]:
            if not isinstance(self.dados.get(chave), str) or not self.dados[chave].strip():
                raise ValueError(f"Campo obrigatório inválido: {chave}.")
        self.validar_consumo(self.dados["consumo"])
        solar = self.dados["solar"]
        for chave in ["fator_util", "profundidade_descarga", "eficiencia_inversor"]:
            numero(solar[chave], 0.01, 1)
        for chave in ["painel_wp", "inversor_w"]:
            numero(solar[chave], 1, 100000)
        numero(solar["bateria_kwh"], 0.001, 1000)
        custos = self.dados["custos"]
        numero(custos["iluminacao_comum_rs"], 0, 1e7)
        numero(custos["reserva_manutencao_30_dias_rs"], 0, 1e7)
        itens = custos["itens_solares_rs"]
        if not isinstance(itens, dict) or not itens:
            raise ValueError("Informe o orçamento solar.")
        for valor in itens.values():
            numero(valor, 0, 1e7)
        for chave in ["premissas", "referencias"]:
            if not isinstance(self.dados[chave], list) or not self.dados[chave]:
                raise ValueError(f"Lista obrigatória inválida: {chave}.")
        # JSON exige números nativos para os cálculos; texto numérico só é aceito na interface.
        grupos = [self.dados["consumo"], solar, itens]
        for grupo in grupos:
            if not isinstance(grupo, dict) or any(type(v) not in (int, float) for v in grupo.values()):
                raise ValueError("Os parâmetros da análise devem ser números JSON.")
        for chave in ["iluminacao_comum_rs", "reserva_manutencao_30_dias_rs"]:
            if type(custos[chave]) not in (int, float):
                raise ValueError("Os custos devem ser números JSON.")
        if any(not isinstance(p, str) or not p.strip() for p in self.dados["premissas"]):
            raise ValueError("Premissa inválida.")
        for fonte in self.dados["referencias"]:
            if not isinstance(fonte, dict) or any(
                not isinstance(fonte.get(c), str) or not fonte[c].strip()
                for c in ["titulo", "url", "uso"]
            ) or not fonte["url"].startswith("https://"):
                raise ValueError("Referência inválida.")

    def validar_consumo(self, consumo):
        if not isinstance(consumo, dict) or set(consumo) != set(CAMPOS):
            raise ValueError("Os seis parâmetros de consumo são obrigatórios.")
        return {chave: numero(consumo[chave], *limites[1:]) for chave, limites in CAMPOS.items()}

    def calcular(self, consumo=None):
        c = self.validar_consumo(self.dados["consumo"] if consumo is None else consumo)
        s = self.dados["solar"]
        custos = self.dados["custos"]
        potencia = c["lampadas"] * c["potencia_lampada_w"]
        diario = potencia * c["horas_dia"] / 1000
        periodo = diario * c["dias"]
        geracao = s["painel_wp"] / 1000 * c["hsp"] * s["fator_util"]
        bateria_util = s["bateria_kwh"] * s["profundidade_descarga"] * s["eficiencia_inversor"]
        potencia_ok = potencia <= s["inversor_w"]
        atendida = min(diario, geracao, bateria_util) if potencia_ok else 0
        completo = potencia_ok and atendida >= diario - 1e-9
        implantacao_a = custos["iluminacao_comum_rs"]
        implantacao_b = implantacao_a + sum(custos["itens_solares_rs"].values())
        energia_rede = periodo * c["tarifa_kwh"]
        manutencao_b = custos["reserva_manutencao_30_dias_rs"] * c["dias"] / 30
        return {
            "consumo": c, "potencia_w": potencia, "diario_kwh": diario,
            "periodo_kwh": periodo, "geracao_util_dia_kwh": geracao,
            "bateria_util_kwh": bateria_util,
            "autonomia_cheia_h": bateria_util * 1000 / potencia if potencia_ok else 0,
            "potencia_inversor_ok": potencia_ok, "solar_atende": completo,
            "solar_atendida_dia_kwh": atendida,
            "solar_atendida_periodo_kwh": atendida * c["dias"],
            "deficit_dia_kwh": max(0, diario - atendida),
            "cobertura_solar_pct": atendida / diario * 100,
            "implantacao_a_rs": implantacao_a, "implantacao_b_rs": implantacao_b,
            "energia_rede_rs": energia_rede, "manutencao_b_rs": manutencao_b,
            "total_a_rs": implantacao_a + energia_rede,
            "total_b_rs": implantacao_b + manutencao_b,
        }

    def falta_de_luz(self, consumo=None, carga_pct=100):
        """Autonomia noturna sem recarga, respeitando a reserva mínima da bateria."""
        resultado = self.calcular(consumo)
        carga = numero(carga_pct, 0, 100)
        s = self.dados["solar"]
        reserva = 1 - s["profundidade_descarga"]
        energia = s["bateria_kwh"] * max(0, carga / 100 - reserva) * s["eficiencia_inversor"]
        if not resultado["potencia_inversor_ok"]:
            energia = 0
        autonomia = energia * 1000 / resultado["potencia_w"]
        return {"carga_pct": carga, "energia_disponivel_kwh": energia,
                "autonomia_h": autonomia,
                "cobre_noite": autonomia >= resultado["consumo"]["horas_dia"] - 1e-9}

    def exibir(self, consumo=None):
        r = self.calcular(consumo)
        c = r["consumo"]
        print("\nCOMPARAÇÃO — MESMA ILUMINAÇÃO, MESMO PERÍODO")
        print("Estimativas didáticas da equipe; valores não são cotações ou garantias.")
        print(f"{c['lampadas']} lâmpadas de {formato(c['potencia_lampada_w'])} W; "
              f"{formato(c['horas_dia'])} h/noite; {c['dias']} dias.")
        print(f"Potência total: {formato(r['potencia_w'])} W.")
        print(f"Consumo: {formato(r['diario_kwh'], 3)} kWh/dia; "
              f"{formato(r['periodo_kwh'], 3)} kWh no período.")
        print("\nA — LED ligado à rede existente e segura")
        print(f"Iluminação e instalação comum: R$ {formato(r['implantacao_a_rs'])}.")
        print(f"Energia variável a R$ {formato(c['tarifa_kwh'])}/kWh: "
              f"R$ {formato(r['energia_rede_rs'])}.")
        print(f"Custo estimado A no período: R$ {formato(r['total_a_rs'])}.")
        print("Depende de rede disponível; sem bateria, não mantém luz numa interrupção.")
        print("\nB — Mesmos LEDs com solar isolado e bateria")
        print(f"Equipamento fixo: {formato(self.dados['solar']['painel_wp'], 0)} Wp; "
              f"bateria {formato(self.dados['solar']['bateria_kwh'])} kWh; "
              f"inversor {formato(self.dados['solar']['inversor_w'], 0)} W.")
        print(f"Com {formato(c['hsp'])} HSP: geração útil estimada "
              f"{formato(r['geracao_util_dia_kwh'], 3)} kWh/dia.")
        print(f"Energia útil de bateria cheia: {formato(r['bateria_util_kwh'], 3)} kWh.")
        print(f"Autonomia calculada com bateria cheia, sem recarga: "
              f"{formato(r['autonomia_cheia_h'])} h nesta carga.")
        print(f"Demanda noturna atendida no modelo: {formato(r['cobertura_solar_pct'], 1)}%.")
        print(f"Investimento B, incluindo iluminação: R$ {formato(r['implantacao_b_rs'])}.")
        print(f"Reserva proporcional de manutenção: R$ {formato(r['manutencao_b_rs'])}.")
        print(f"Custo estimado B no período: R$ {formato(r['total_b_rs'])}.")
        if r["solar_atende"]:
            print("B cobre a energia noturna calculada nas condições assumidas.")
            print(f"Até {formato(r['solar_atendida_periodo_kwh'], 3)} kWh de consumo da rede "
                  "poderiam ser substituídos no período; sem crédito por excedente.")
            menor = "A" if r["total_a_rs"] <= r["total_b_rs"] else "B"
            print(f"Com rede funcionando, {menor} tem menor custo estimado neste período.")
        else:
            print("ATENÇÃO: B NÃO atende toda a iluminação solicitada.")
            if not r["potencia_inversor_ok"]:
                print("A potência da carga excede o limite do inversor; atendimento considerado zero.")
            print(f"Déficit noturno: {formato(r['deficit_dia_kwh'], 3)} kWh/dia.")
            print("O custo B acima entrega serviço parcial; backup/redimensionamento não foi orçado.")
            print("Para a demanda completa, A depende de rede funcionando. Reveja B com um profissional.")
        print("\nORIENTAÇÃO")
        print("Solar com bateria pode ajudar na continuidade da luz, se instalado e carregado.")
        print("Priorize os pontos essenciais sem comprometer a segurança do abrigo.")
        print("Dias nublados e pouca carga reduzem a disponibilidade. Não há retorno financeiro garantido.")
        print("\nIMPACTOS E LIMITES")
        print("A usa a matriz elétrica disponível; não se supõe que a rede seja totalmente fóssil.")
        print("B usa recurso renovável e não queima combustível no uso, mas módulos e bateria têm "
              "impactos de fabricação, transporte e descarte; planeje reutilização e destinação adequada.")
        print("Não foi feita análise de ciclo de vida nem calculada redução de CO2.")
        print("Custos ilustrativos: não representam a conta completa ou projeto elétrico/luminotécnico.")
        print("Só iluminação; outras cargas e reposições não estão incluídas.")
        print("Fontes: MME, CEPEL/CRESESB, ANEEL e IEA-PVPS/IRENA; detalhes na opção 4.")

    def exibir_fontes(self):
        print(f"\nFONTES E PREMISSAS — revisão {self.dados['verificado_em']}")
        print(self.dados["origem"])
        for fonte in self.dados["referencias"]:
            print(f"\n{fonte['titulo']}\n{fonte['url']}\nUso: {fonte['uso']}")
        print("\nPREMISSAS")
        for premissa in self.dados["premissas"]:
            print(f"- {premissa}")
        print("\nORÇAMENTO SOLAR ADICIONAL — valores hipotéticos em R$")
        for item, valor in self.dados["custos"]["itens_solares_rs"].items():
            print(f"- {item.replace('_', ' ')}: {formato(valor)}")
        print("Instalação e avaliação de segurança devem ser feitas por profissional habilitado.")
        print("Documentação: documentacao/sers/README.md e modulos/energia/referencias.md.")


def ler_numero(rotulo, atual, minimo, maximo, inteiro=False):
    while True:
        texto = input(f"{rotulo} [{formato(atual, 0 if inteiro else 2)}]: ").strip()
        if texto.lower() == "v":
            return None
        if not texto:
            return atual
        try:
            return numero(texto, minimo, maximo, inteiro)
        except ValueError as erro:
            print(erro)


def menu_energia():
    try:
        calculadora = CalculadoraEnergia()
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as erro:
        print(f"\nMódulo de energia indisponível. Confira analise.json: {erro}")
        return
    consumo = dict(calculadora.dados["consumo"])
    print("\nMódulo de energia e sustentabilidade — SERS")
    print("Vamos estudar a iluminação noturna de um abrigo temporário.")
    print("Simulação educacional local, sem API e sem salvar suas entradas.")
    while True:
        print("\n1 - Comparar rede e solar com bateria")
        print("2 - Simular outro consumo, sol ou preço")
        print("3 - E se faltar luz? Ver duração da bateria")
        print("4 - Consultar fontes, orçamento e premissas")
        print("5 - Restaurar o exemplo inicial")
        print("0 - Voltar ao menu principal")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return
        if opcao == "1":
            calculadora.exibir(consumo)
        elif opcao == "2":
            print("\nEnter mantém o valor atual; v cancela sem alterar a simulação.")
            print("HSP resume a energia solar diária; não é a duração do dia.")
            print("Equipamentos e orçamento permanecem fixos para verificar seus limites.")
            novo = {}
            for chave, (rotulo, minimo, maximo, inteiro) in CAMPOS.items():
                valor = ler_numero(rotulo, consumo[chave], minimo, maximo, inteiro)
                if valor is None:
                    print("Simulação cancelada; valores anteriores mantidos.")
                    break
                novo[chave] = valor
            else:
                consumo = novo
                calculadora.exibir(consumo)
        elif opcao == "3":
            print("\nSem sol ou recarga durante a interrupção; Enter mantém 100%; v volta.")
            carga = ler_numero("Carga inicial da bateria (%)", 100, 0, 100)
            if carga is not None:
                r = calculadora.falta_de_luz(consumo, carga)
                print(f"Com {formato(carga, 1)}% de carga: autonomia de {formato(r['autonomia_h'])} h.")
                print("Reserva mínima preservada: "
                      f"{formato((1-calculadora.dados['solar']['profundidade_descarga'])*100, 0)}%.")
                print("Cobre a noite calculada." if r["cobre_noite"] else "NÃO cobre a noite calculada.")
                if not calculadora.calcular(consumo)["potencia_inversor_ok"]:
                    print("Carga acima da potência do inversor; não pode ser alimentada neste modelo.")
                print("É estimativa, não garantia; depende de carga real, temperatura e estado da bateria.")
        elif opcao == "4":
            calculadora.exibir_fontes()
        elif opcao == "5":
            consumo = dict(calculadora.dados["consumo"])
            print("Exemplo inicial restaurado: 20 lâmpadas, 9 W, 6 h/noite, 30 dias, 4 HSP e R$ 1/kWh.")
        else:
            print("Opção inválida. Escolha um número do menu.")

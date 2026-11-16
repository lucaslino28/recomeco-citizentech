"""Simulação educacional de iluminação. Usa somente a biblioteca padrão."""

import json
import hashlib
from datetime import datetime, timezone
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
        self.referencia_solar()
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

    def exibir_detalhes(self, consumo=None):
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
        ref = self.referencia_solar()
        print("\nREFERÊNCIA PÚBLICA — NASA POWER")
        print(ref["local"])
        print(ref["periodo"])
        print(f"Unidade original: {ref['unidade']}; equivalente numérico em HSP no plano horizontal.")
        print(f"Média anual: {formato(ref['hsp_anual'], 4)}; menor média mensal: "
              f"{ref['mes_menor']} = {formato(ref['hsp_menor'], 4)}.")
        print(ref["observacao"])
        print("A sequência de dias usa valores escolhidos para explorar o comportamento; não deriva uma previsão dessas médias.")
        print("Instalação e avaliação de segurança devem ser feitas por profissional habilitado.")
        print("Documentação: documentacao/sers/README.md e modulos/energia/referencias.md.")


    def referencia_solar(self):
        """Lê a cópia pública conferida; não faz chamadas de rede durante o uso."""
        ref = self.dados["referencia_solar"]
        caminho = PASTA / ref["arquivo"]
        conteudo = caminho.read_bytes()
        if hashlib.sha256(conteudo).hexdigest() != ref["sha256"]:
            raise ValueError("A cópia dos dados solares mudou; confira a origem e o hash.")
        dados = json.loads(conteudo)
        unidade = dados["parameters"]["ALLSKY_SFC_SW_DWN"]["units"]
        if unidade != "kW-hr/m^2/day":
            raise ValueError("Unidade solar inesperada; reveja a conversão para HSP.")
        valores = dados["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
        meses = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        mensais = {mes: numero(valores[mes], 0, 12) for mes in meses}
        menor = min(mensais, key=mensais.get)
        return {"local": ref["local"], "unidade": unidade,
                "periodo": dados["header"]["range"],
                "hsp_anual": numero(valores["ANN"], 0, 12),
                "mensais": mensais, "mes_menor": menor, "hsp_menor": mensais[menor],
                "observacao": ref["observacao"], "url": ref["url"]}

    def custos_operacao(self, consumo=None):
        """Equipamentos de AMBAS as opções já disponíveis, instalados e seguros."""
        r = self.calcular(consumo)
        adicional = sum(self.dados["custos"]["itens_solares_rs"].values())
        comum = r["implantacao_a_rs"]
        return {"a_operacao_rs": r["energia_rede_rs"],
                "b_operacao_rs": r["manutencao_b_rs"],
                "comparacao_equivalente": r["solar_atende"],
                "b_aquisicao_menos_30pct_rs": comum + adicional * 0.7 + r["manutencao_b_rs"],
                "b_aquisicao_mais_30pct_rs": comum + adicional * 1.3 + r["manutencao_b_rs"]}

    def simular_dias(self, hsps, consumo=None, carga_pct=100):
        """Balanço dia/noite em kWh equivalentes na saída do inversor.

        Usa lista, laço e acumulador. A geração já inclui perdas globais:
        não aplicamos novamente eficiência do inversor ao saldo ou ao consumo.
        """
        if not isinstance(hsps, (list, tuple)) or not 1 <= len(hsps) <= 14:
            raise ValueError("Use uma sequência de 1 a 14 dias.")
        sol = [numero(h, 0, 12) for h in hsps]
        carga = numero(carga_pct, 0, 100)
        r = self.calcular(consumo)
        s = self.dados["solar"]
        capacidade = s["bateria_kwh"] * s["eficiencia_inversor"]
        reserva = capacidade * (1 - s["profundidade_descarga"])
        saldo = capacidade * carga / 100
        saldo_inicial = saldo
        linhas = []
        for dia, hsp in enumerate(sol, 1):
            inicio = saldo
            geracao = s["painel_wp"] / 1000 * hsp * s["fator_util"]
            excedente = max(0, saldo + geracao - capacidade)
            saldo = min(capacidade, saldo + geracao)
            disponivel = max(0, saldo - reserva)
            atendida = min(r["diario_kwh"], disponivel) if r["potencia_inversor_ok"] else 0
            saldo -= atendida
            deficit = max(0, r["diario_kwh"] - atendida)
            linhas.append({"dia": dia, "hsp": hsp,
                           "carga_inicio_pct": inicio / capacidade * 100,
                           "geracao_util_kwh": geracao, "atendida_kwh": atendida,
                           "deficit_kwh": deficit, "excedente_kwh": excedente,
                           "saldo_final_kwh_equivalente": saldo,
                           "carga_final_pct": saldo / capacidade * 100})
        atendida_total = sum(linha["atendida_kwh"] for linha in linhas)
        demanda_total = r["diario_kwh"] * len(sol)
        return {"consumo": r["consumo"], "carga_inicial_pct": carga,
                "potencia_inversor_ok": r["potencia_inversor_ok"],
                "dias": linhas, "demanda_total_kwh": demanda_total,
                "atendida_total_kwh": atendida_total,
                "deficit_total_kwh": sum(linha["deficit_kwh"] for linha in linhas),
                "geracao_total_kwh": sum(linha["geracao_util_kwh"] for linha in linhas),
                "excedente_total_kwh": sum(linha["excedente_kwh"] for linha in linhas),
                "saldo_inicial_kwh_equivalente": saldo_inicial,
                "saldo_final_kwh_equivalente": saldo,
                "cobertura_pct": atendida_total / demanda_total * 100,
                "noites_completas": sum(linha["deficit_kwh"] < 1e-9 for linha in linhas)}

    def resumo(self, consumo=None):
        r = self.calcular(consumo)
        c = r["consumo"]
        linhas = [
            "COMPARAÇÃO — MESMA ILUMINAÇÃO, MESMO PERÍODO",
            f"{c['lampadas']} lâmpadas de {formato(c['potencia_lampada_w'])} W, "
            f"{formato(c['horas_dia'])} h/noite, {c['dias']} dias.",
            f"Demanda: {formato(r['potencia_w'])} W; {formato(r['diario_kwh'], 3)} kWh/dia; "
            f"{formato(r['periodo_kwh'], 3)} kWh no período.",
            "",
            f"A — REDE: custo de aquisição + uso estimado R$ {formato(r['total_a_rs'])}.",
            f"B — SOLAR + BATERIA: custo de aquisição + uso estimado R$ {formato(r['total_b_rs'])}.",
            f"B entrega {formato(r['cobertura_solar_pct'], 1)}% da demanda noturna no balanço diário.",
        ]
        if r["solar_atende"]:
            menor = "A — rede" if r["total_a_rs"] <= r["total_b_rs"] else "B — solar"
            linhas += [f"DECISÃO COM REDE DISPONÍVEL: {menor} tem menor custo estimado neste período.",
                       f"Até {formato(r['solar_atendida_periodo_kwh'], 3)} kWh da rede "
                       "poderiam ser substituídos, sem crédito por excedente."]
        else:
            linhas += ["ATENÇÃO: B NÃO atende toda a iluminação solicitada.",
                       f"Déficit: {formato(r['deficit_dia_kwh'], 3)} kWh/noite.",
                       "O custo B entrega serviço parcial; backup/redimensionamento não foi orçado."]
        if not r["potencia_inversor_ok"]:
            linhas.append("A carga excede a potência do inversor do exemplo; B não pode alimentá-la.")
        linhas += [
            f"Bateria cheia, sem recarga: até {formato(r['autonomia_cheia_h'])} h calculadas nesta carga.",
            "Para manter luz numa interrupção, consulte a carga inicial (3) e a sequência de dias (6).",
            "",
            "Valores de planejamento e referências: não são cotação, conta completa ou garantia.",
            "Só iluminação. Instalação real e iluminância precisam de avaliação profissional.",
            "Rede: mistura de fontes. Solar: renovável no uso; equipamentos têm impactos de fabricação e descarte.",
            "Não há cálculo de CO2 ou impacto zero. Priorize pontos essenciais sem comprometer a segurança.",
            "Fontes: MME, CEPEL/CRESESB, ANEEL, NASA POWER, fabricantes e IEA-PVPS/IRENA (opção 4).",
        ]
        return linhas

    def exibir(self, consumo=None):
        print("\n" + "\n".join(self.resumo(consumo)))

    def orientar(self, necessidade, consumo=None):
        r = self.calcular(consumo)
        c = r["consumo"]
        print("\nORIENTAÇÃO PARA SUA NECESSIDADE")
        if necessidade == "custo":
            self.exibir(consumo)
            print("O orçamento inclui comprar o conjunto agora; não se promete retorno financeiro.")
            print("Se já houver equipamentos, consulte a opção de operação no atendimento guiado.")
        elif necessidade == "continuidade":
            print(f"A rede sozinha não mantém a luz se o fornecimento for interrompido. "
                  f"Bateria cheia: {formato(r['autonomia_cheia_h'])} h calculadas.")
            if not r["potencia_inversor_ok"]:
                print("A carga excede a potência do inversor. Este conjunto não serve para esta demanda.")
            elif r["solar_atende"]:
                print("O balanço diário é suficiente nas hipóteses atuais; isso não garante vários dias sem sol.")
            else:
                print(f"Há déficit diário de {formato(r['deficit_dia_kwh'], 3)} kWh. "
                      "O conjunto não sustenta a demanda em uso repetido nessas condições.")
            print("Use a opção 3 para carga inicial e 6 para acompanhar noites sucessivas.")
        elif necessidade == "existentes":
            o = self.custos_operacao(consumo)
            print(f"Com AMBAS as instalações e equipamentos já disponíveis e seguros, em {c['dias']} dias:")
            print(f"A — energia variável da rede: R$ {formato(o['a_operacao_rs'])}.")
            print(f"B — reserva de manutenção: R$ {formato(o['b_operacao_rs'])}.")
            if o["comparacao_equivalente"]:
                menor = "A" if o["a_operacao_rs"] <= o["b_operacao_rs"] else "B"
                print(f"{menor} tem menor desembolso operacional modelado; o investimento anterior está excluído.")
            else:
                print("B entrega serviço parcial; esses valores não comparam atendimento equivalente.")
            print("Não é custo de vida útil: reposições, depreciação e outras parcelas da conta estão fora.")
            print(f"Sensibilidade na COMPRA NOVA de B, variando só investimento solar em ±30%: "
                  f"R$ {formato(o['b_aquisicao_menos_30pct_rs'])} a "
                  f"R$ {formato(o['b_aquisicao_mais_30pct_rs'])}.")
            print("Faixa hipotética de sensibilidade, não pesquisa de preços; mantenha demanda e período iguais.")
        elif necessidade == "calculos":
            self.exibir_detalhes(consumo)
            print("\nCOMO CONFERIR AS CONTAS")
            print(f"Consumo = {c['lampadas']} × {formato(c['potencia_lampada_w'])} W × "
                  f"{formato(c['horas_dia'])} h / 1000 = {formato(r['diario_kwh'], 3)} kWh/dia.")
            print(f"Geração útil = painel em kW × HSP × fator global = "
                  f"{formato(r['geracao_util_dia_kwh'], 3)} kWh/dia.")
            print("Bateria útil = capacidade nominal × descarga permitida × eficiência do inversor.")
            print("O fator global já considera perdas: não aplicar o inversor outra vez à geração.")
        else:
            raise ValueError("Necessidade desconhecida.")

    def exibir_sequencia(self, sequencia):
        print("\nBATERIA AO LONGO DOS DIAS — sequência hipotética, não previsão do tempo")
        print(f"Carga inicial: {formato(sequencia['carga_inicial_pct'], 1)}%. "
              "A geração entra durante o dia; o uso ocorre na noite seguinte.")
        print("Dia | HSP  | Gerado kWh | Luz kWh | Falta kWh | Carga após noite")
        for linha in sequencia["dias"]:
            print(f"{linha['dia']:>3} | {formato(linha['hsp']):>4} | "
                  f"{formato(linha['geracao_util_kwh'], 3):>10} | "
                  f"{formato(linha['atendida_kwh'], 3):>7} | "
                  f"{formato(linha['deficit_kwh'], 3):>9} | "
                  f"{formato(linha['carga_final_pct'], 1):>6}%")
        print(f"Noites completas: {sequencia['noites_completas']}/{len(sequencia['dias'])}; "
              f"cobertura acumulada: {formato(sequencia['cobertura_pct'], 1)}%.")
        print(f"Déficit total: {formato(sequencia['deficit_total_kwh'], 3)} kWh. "
              f"Excedente sem aproveitamento: {formato(sequencia['excedente_total_kwh'], 3)} kWh.")
        if not sequencia["potencia_inversor_ok"]:
            print("Carga acima da potência do inversor; não há fornecimento à iluminação neste conjunto.")
        print("A carga não é reiniciada a cada noite. O modelo só consome energia acima da reserva de 20%.")
        print("A carga final é uma aproximação energética; não inclui consumo em espera ou envelhecimento.")

    def exportar_relatorio(self, consumo=None, pasta=None, sequencia=None):
        """Exportação solicitada pelo usuário; não contém falas ou avaliações humanas."""
        comparacao = self.calcular(consumo)
        if sequencia is not None and sequencia.get("consumo") != comparacao["consumo"]:
            raise ValueError("A sequência não corresponde aos parâmetros atuais; execute-a novamente.")
        pasta = Path(pasta) if pasta else PASTA.parents[1] / "data/relatorios_sers"
        pasta.mkdir(parents=True, exist_ok=True)
        instante = datetime.now(timezone.utc)
        arquivo = pasta / f"sers_{instante.strftime('%Y%m%dT%H%M%S%fZ')}.txt"
        dados = {"tipo": "Relatório técnico de SERS; não é avaliação com usuários",
                 "versao": self.dados["versao"], "gerado_em_utc": instante.isoformat(),
                 "comparacao": comparacao, "operacao_e_sensibilidade": self.custos_operacao(consumo),
                 "referencia_publica": self.referencia_solar(),
                 "sequencia_se_executada": sequencia,
                 "origem": self.dados["origem"], "premissas": self.dados["premissas"],
                 "referencias": self.dados["referencias"]}
        texto = "RELATÓRIO TÉCNICO — RECOMEÇO / SERS\n\n" + "\n".join(self.resumo(consumo))
        texto += "\n\nDADOS PARA CONFERÊNCIA\n" + json.dumps(dados, ensure_ascii=False, indent=2, allow_nan=False)
        with arquivo.open("x", encoding="utf-8") as destino:
            destino.write(texto + "\n")
        return arquivo



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


def atendimento_guiado(calculadora, consumo):
    while True:
        print("\nQUAL É SUA NECESSIDADE?")
        print("1 - Quero entender qual opção custa menos")
        print("2 - Preciso manter a iluminação quando faltar luz")
        print("3 - Já tenho as duas instalações: comparar só a operação")
        print("4 - Quero conferir os cálculos passo a passo")
        print("5 - Usar o exemplo público de São Paulo, menor média mensal")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        necessidades = {"1": "custo", "2": "continuidade", "3": "existentes", "4": "calculos"}
        if opcao == "0":
            return consumo
        if opcao in necessidades:
            calculadora.orientar(necessidades[opcao], consumo)
        elif opcao == "5":
            ref = calculadora.referencia_solar()
            consumo = dict(consumo, hsp=ref["hsp_menor"])
            print(f"Referência aplicada: {ref['local']}; {ref['mes_menor']} = "
                  f"{formato(ref['hsp_menor'], 4)} HSP horizontais equivalentes.")
            print(ref["observacao"])
            print("Demanda, perdas e custos continuam estimados. Nenhuma condição foi generalizada para o Brasil.")
            calculadora.exibir(consumo)
        else:
            print("Opção inválida. Escolha um número do menu.")


def escolher_sequencia(calculadora, consumo):
    print("\nESCOLHA UMA SEQUÊNCIA DE SOL")
    print("1 - Cinco dias repetindo as HSP atuais")
    print("2 - Cinco dias com pouco sol: 4, 1, 0, 1 e 4 HSP")
    print("3 - Informar as HSP de cada dia (até 7 dias)")
    print("0 - Cancelar")
    while True:
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return None
        if opcao in ["1", "2", "3"]:
            break
        print("Opção inválida.")
    print("Enter mantém os valores sugeridos; v cancela.")
    if opcao == "1":
        hsps = [consumo["hsp"]] * 5
    elif opcao == "2":
        hsps = [4, 1, 0, 1, 4]
    else:
        quantidade = ler_numero("Quantidade de dias", 5, 1, 7, True)
        if quantidade is None:
            return None
        hsps = []
        for dia in range(1, quantidade + 1):
            hsp = ler_numero(f"HSP do dia {dia}", consumo["hsp"], 0, 12)
            if hsp is None:
                return None
            hsps.append(hsp)
    carga = ler_numero("Carga da bateria antes do primeiro dia (%)", 100, 0, 100)
    if carga is None:
        return None
    resultado = calculadora.simular_dias(hsps, consumo, carga)
    calculadora.exibir_sequencia(resultado)
    return resultado


def menu_energia():
    try:
        calculadora = CalculadoraEnergia()
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as erro:
        print(f"\nMódulo de energia indisponível. Confira analise.json e as fontes locais: {erro}")
        return
    consumo = dict(calculadora.dados["consumo"])
    ultima_sequencia = None
    print("\nMódulo de energia e sustentabilidade — SERS")
    print("Entenda o custo e a continuidade da iluminação de um abrigo temporário.")
    print("Comece em 1 para comparar ou em 7 para escolher sua necessidade.")
    print("Cálculos locais. Entradas só são salvas se você escolher exportar o relatório.")
    while True:
        print("\n1 - Comparar custos e ver a recomendação")
        print("2 - Ajustar consumo, condições de sol ou preço")
        print("3 - Quanto dura a bateria se faltar luz?")
        print("4 - Consultar fontes, dados públicos e premissas")
        print("5 - Restaurar o exemplo inicial")
        print("6 - Acompanhar a bateria durante vários dias")
        print("7 - Receber orientação pela minha necessidade")
        print("8 - Salvar relatório técnico desta análise")
        print("0 - Voltar ao menu principal")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return
        if opcao == "1":
            calculadora.exibir(consumo)
        elif opcao == "2":
            print("\nEnter mantém o valor atual; v cancela sem alterar a simulação.")
            print("HSP resume a energia solar diária; não é a duração do dia.")
            ref = calculadora.referencia_solar()
            print(f"Exemplo público horizontal de São Paulo: menor média mensal "
                  f"{formato(ref['hsp_menor'], 4)} HSP; o valor atual pode ser uma hipótese.")
            print("Equipamentos e orçamento permanecem fixos para verificar seus limites.")
            novo = {}
            for chave, (rotulo, minimo, maximo, inteiro) in CAMPOS.items():
                valor = ler_numero(rotulo, consumo[chave], minimo, maximo, inteiro)
                if valor is None:
                    print("Simulação cancelada; valores anteriores mantidos.")
                    break
                novo[chave] = valor
            else:
                antes = calculadora.calcular(consumo)
                depois = calculadora.calcular(novo)
                print(f"Consumo no período: antes {formato(antes['periodo_kwh'], 3)} kWh; "
                      f"agora {formato(depois['periodo_kwh'], 3)} kWh.")
                print("Mudar horas ou pontos altera o serviço; preserve a iluminação necessária à segurança.")
                consumo = novo
                ultima_sequencia = None
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
            ultima_sequencia = None
            print("Exemplo inicial restaurado: 20 lâmpadas, 9 W, 6 h/noite, 30 dias, 4 HSP e R$ 1/kWh.")
        elif opcao == "6":
            sequencia = escolher_sequencia(calculadora, consumo)
            if sequencia is not None:
                ultima_sequencia = sequencia
        elif opcao == "7":
            novo = atendimento_guiado(calculadora, consumo)
            if novo != consumo:
                ultima_sequencia = None
            consumo = novo
        elif opcao == "8":
            try:
                caminho = calculadora.exportar_relatorio(consumo, sequencia=ultima_sequencia)
                print(f"Relatório salvo em: {caminho}")
                print("Contém parâmetros, cálculos, fontes e a última sequência compatível; não é avaliação humana.")
            except OSError as erro:
                print(f"Não foi possível salvar o relatório: {erro}")
        else:
            print("Opção inválida. Escolha um número do menu.")

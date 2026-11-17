"""Regressão técnica de SERS; não representa testes com participantes."""

import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from modulos.energia.calculadora import CalculadoraEnergia, menu_energia, numero


RAIZ = Path(__file__).resolve().parents[1]


class TesteSERS(unittest.TestCase):
    def setUp(self):
        self.calculadora = CalculadoraEnergia()
        self.consumo = dict(self.calculadora.dados["consumo"])

    def menu(self, entradas):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(saida):
            menu_energia()
        return saida.getvalue()

    def test_caso_referencia_conferido_manualmente(self):
        r = self.calculadora.calcular()
        self.assertEqual(r["potencia_w"], 180)
        self.assertAlmostEqual(r["diario_kwh"], 1.08)
        self.assertAlmostEqual(r["periodo_kwh"], 32.4)
        self.assertAlmostEqual(r["geracao_util_dia_kwh"], 1.65)
        self.assertAlmostEqual(r["bateria_util_kwh"], 1.8432)
        self.assertAlmostEqual(r["autonomia_cheia_h"], 10.24)
        self.assertAlmostEqual(r["total_a_rs"], 532.4)
        self.assertAlmostEqual(r["total_b_rs"], 6910)
        self.assertTrue(r["solar_atende"])

    def test_mesmo_periodo_e_custo_comum_nas_duas_alternativas(self):
        self.consumo["dias"] = 60
        r = self.calculadora.calcular(self.consumo)
        self.assertAlmostEqual(r["periodo_kwh"], 64.8)
        self.assertAlmostEqual(r["total_a_rs"], 564.8)
        self.assertAlmostEqual(r["total_b_rs"], 6920)
        self.assertEqual(r["implantacao_b_rs"] - r["implantacao_a_rs"], 6400)

    def test_pouco_sol_nao_promete_atendimento_completo(self):
        self.consumo["hsp"] = 1
        r = self.calculadora.calcular(self.consumo)
        self.assertFalse(r["solar_atende"])
        self.assertAlmostEqual(r["solar_atendida_dia_kwh"], 0.4125)
        self.assertAlmostEqual(r["deficit_dia_kwh"], 0.6675)
        self.assertAlmostEqual(r["solar_atendida_periodo_kwh"], 12.375)
        with contextlib.redirect_stdout(io.StringIO()) as saida:
            self.calculadora.exibir(self.consumo)
        self.assertIn("serviço parcial", saida.getvalue())
        self.assertNotIn("poderiam ser substituídos", saida.getvalue())

    def test_sem_sol_nao_conta_carga_inicial_como_geracao_diaria(self):
        self.consumo["hsp"] = 0
        r = self.calculadora.calcular(self.consumo)
        self.assertEqual(r["solar_atendida_dia_kwh"], 0)
        self.assertAlmostEqual(r["autonomia_cheia_h"], 10.24)
        self.assertFalse(r["solar_atende"])

    def test_excesso_de_sol_nao_vira_credito_ou_energia_consumida(self):
        self.consumo["hsp"] = 12
        r = self.calculadora.calcular(self.consumo)
        self.assertGreater(r["geracao_util_dia_kwh"], r["diario_kwh"])
        self.assertAlmostEqual(r["solar_atendida_periodo_kwh"], 32.4)
        self.assertAlmostEqual(r["total_a_rs"], 532.4)

    def test_bateria_limita_luz_noturna_mesmo_com_sol_abundante(self):
        self.consumo.update(horas_dia=12, hsp=8)
        r = self.calculadora.calcular(self.consumo)
        self.assertFalse(r["solar_atende"])
        self.assertAlmostEqual(r["solar_atendida_dia_kwh"], 1.8432)
        self.assertAlmostEqual(r["deficit_dia_kwh"], 0.3168)

    def test_sobrecarga_do_inversor_nao_promete_autonomia(self):
        self.consumo["lampadas"] = 40
        r = self.calculadora.calcular(self.consumo)
        self.assertFalse(r["potencia_inversor_ok"])
        self.assertEqual(r["solar_atendida_dia_kwh"], 0)
        self.assertEqual(r["autonomia_cheia_h"], 0)
        self.assertFalse(self.calculadora.falta_de_luz(self.consumo)["cobre_noite"])

    def test_estado_de_carga_respeita_reserva_e_nao_duplica_perdas(self):
        cheia = self.calculadora.falta_de_luz(carga_pct=100)
        meia = self.calculadora.falta_de_luz(carga_pct=50)
        self.assertAlmostEqual(cheia["autonomia_h"], 10.24)
        self.assertTrue(cheia["cobre_noite"])
        self.assertAlmostEqual(meia["autonomia_h"], 3.84)
        self.assertFalse(meia["cobre_noite"])
        for carga in [0, 10, 20]:
            self.assertAlmostEqual(self.calculadora.falta_de_luz(carga_pct=carga)["autonomia_h"], 0)

    def test_consumo_menor_aumenta_autonomia_e_reduz_custo_variavel(self):
        self.consumo["lampadas"] = 10
        r = self.calculadora.calcular(self.consumo)
        self.assertAlmostEqual(r["autonomia_cheia_h"], 20.48)
        self.assertAlmostEqual(r["energia_rede_rs"], 16.2)

    def test_entradas_invalidas_nao_produzem_resultados(self):
        for valor in [True, None, [], "abc", "NaN", "inf", "-inf", "1e999", -1, 13]:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                numero(valor, 0, 12)
        self.assertEqual(numero("1,5", 0, 12), 1.5)
        with self.assertRaises(ValueError):
            numero("2,5", 1, 200, True)
        for chave, valor in [("lampadas", 0), ("horas_dia", 25), ("dias", 0), ("tarifa_kwh", -1)]:
            with self.subTest(chave=chave), self.assertRaises(ValueError):
                self.calculadora.calcular(dict(self.consumo, **{chave: valor}))
        with self.assertRaises(ValueError):
            self.calculadora.falta_de_luz(carga_pct=101)

    def test_tarifa_zero_e_decimal_sao_validos_sem_divisao_por_zero(self):
        self.consumo["tarifa_kwh"] = 0
        self.assertEqual(self.calculadora.calcular(self.consumo)["total_a_rs"], 500)
        self.consumo["tarifa_kwh"] = "0,5"
        self.assertAlmostEqual(self.calculadora.calcular(self.consumo)["energia_rede_rs"], 16.2)

    def test_base_invalida_e_ausente(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "analise.json"
            with self.assertRaises(OSError):
                CalculadoraEnergia(caminho)
            for valor in ["{", "[]", "{}"]:
                caminho.write_text(valor)
                with self.assertRaises((ValueError, KeyError)):
                    CalculadoraEnergia(caminho)
            for grupo, campo, valor in [("solar", "fator_util", 0),
                                        ("solar", "eficiencia_inversor", 1.1),
                                        ("solar", "bateria_kwh", "2.56"),
                                        ("consumo", "lampadas", True),
                                        ("custos", "iluminacao_comum_rs", "500")]:
                dados = json.loads(json.dumps(self.calculadora.dados))
                dados[grupo][campo] = valor
                caminho.write_text(json.dumps(dados))
                with self.subTest(campo=campo), self.assertRaises(ValueError):
                    CalculadoraEnergia(caminho)

    def test_menu_indisponivel_preserva_demais_modulos(self):
        with patch("modulos.energia.calculadora.CalculadoraEnergia", side_effect=ValueError("base inválida")):
            self.assertIn("indisponível", self.menu([]))

    def test_menu_simula_com_virgula_e_restaura_exemplo(self):
        texto = self.menu(["2", "", "", "", "", "1,0", "0,50", "5", "1", "0"])
        self.assertIn("B NÃO atende", texto)
        self.assertIn("Exemplo inicial restaurado", texto)
        self.assertIn("32,40", texto)
        self.assertIn("6.910,00", texto)

    def test_cancelar_nao_aplica_alteracao_parcial(self):
        texto = self.menu(["2", "10", "v", "1", "0"])
        self.assertIn("Simulação cancelada", texto)
        self.assertIn("20 lâmpadas", texto)
        self.assertNotIn("10 lâmpadas", texto)

    def test_menu_erros_retorno_e_avisos(self):
        texto = self.menu(["x", "2", "NaN", "v", "3", "-1", "50", "4", "0"])
        for esperado in ["Opção inválida", "entre", "3,84 h", "NÃO cobre", "https://", "PREMISSAS"]:
            self.assertIn(esperado, texto)

    def test_menu_integrado_independe_do_diretorio_e_nao_grava_atendimentos_sers(self):
        with tempfile.TemporaryDirectory() as pasta:
            processo = subprocess.run(
                [sys.executable, "-B", str(RAIZ / "main.py"), "--dados", pasta],
                input="3\n1\n3\n50\n0\n0\n", text=True, capture_output=True, cwd=pasta, timeout=10
            )
            self.assertEqual(processo.returncode, 0, processo.stderr)
            self.assertIn("Módulo de energia", processo.stdout)
            self.assertIn("532,40", processo.stdout)
            self.assertIn("3,84 h", processo.stdout)
            self.assertNotIn("Traceback", processo.stderr)
            historico = Path(pasta) / "historico.json"
            self.assertFalse(historico.exists() and json.loads(historico.read_text()))

    def test_referencia_publica_tem_periodo_unidade_e_meses_conferidos(self):
        ref = self.calculadora.referencia_solar()
        self.assertEqual(len(ref["mensais"]), 12)
        self.assertEqual(ref["unidade"], "kW-hr/m^2/day")
        self.assertIn("2001", ref["periodo"])
        self.assertIn("2025", ref["periodo"])
        self.assertEqual(ref["mes_menor"], "JUN")
        self.assertAlmostEqual(ref["hsp_menor"], 3.2578)
        self.assertAlmostEqual(ref["hsp_anual"], 4.5288)
        self.assertIn("horizontal", ref["observacao"])

    def test_copia_publica_modificada_nao_e_usada_silenciosamente(self):
        from unittest.mock import patch
        with patch("pathlib.Path.read_bytes", return_value=b'{}'):
            with self.assertRaisesRegex(ValueError, "mudou"):
                self.calculadora.referencia_solar()

    def test_custos_operacao_nao_repetem_investimento_inicial(self):
        r = self.calculadora.custos_operacao()
        self.assertAlmostEqual(r["a_operacao_rs"], 32.4)
        self.assertAlmostEqual(r["b_operacao_rs"], 10)
        self.assertAlmostEqual(r["b_aquisicao_menos_30pct_rs"], 4990)
        self.assertAlmostEqual(r["b_aquisicao_mais_30pct_rs"], 8830)
        self.assertTrue(r["comparacao_equivalente"])
        self.consumo["hsp"] = 0
        self.assertFalse(self.calculadora.custos_operacao(self.consumo)["comparacao_equivalente"])

    def test_sequencia_sem_sol_descarrega_bateria_sem_reiniciar_carga(self):
        r = self.calculadora.simular_dias([0, 0, 0], carga_pct=100)
        self.assertAlmostEqual(r["dias"][0]["atendida_kwh"], 1.08)
        self.assertAlmostEqual(r["dias"][1]["atendida_kwh"], 0.7632)
        self.assertAlmostEqual(r["dias"][2]["atendida_kwh"], 0)
        self.assertAlmostEqual(r["atendida_total_kwh"], 1.8432)
        self.assertAlmostEqual(r["dias"][-1]["carga_final_pct"], 20)
        self.assertEqual(r["noites_completas"], 1)

    def test_sequencia_pouco_sol_tem_tres_noites_completas(self):
        r = self.calculadora.simular_dias([4, 1, 0, 1, 4])
        self.assertEqual(r["noites_completas"], 3)
        self.assertAlmostEqual(r["deficit_total_kwh"], 1.6518)
        self.assertAlmostEqual(r["atendida_total_kwh"], 3.7482)
        self.assertAlmostEqual(r["cobertura_pct"], 69.4111111111)

    def test_sequencia_conserva_energia_e_nao_vende_excedente(self):
        for carga in [0, 10, 20, 50, 100]:
            for hsps in [[0, 0], [4, 1, 0, 1, 4], [12] * 7]:
                with self.subTest(carga=carga,hsps=hsps):
                    r = self.calculadora.simular_dias(hsps, carga_pct=carga)
                    entrada = r["saldo_inicial_kwh_equivalente"] + r["geracao_total_kwh"]
                    saida = r["saldo_final_kwh_equivalente"] + r["atendida_total_kwh"] + r["excedente_total_kwh"]
                    self.assertAlmostEqual(entrada, saida)
                    for dia in r["dias"]:
                        self.assertGreaterEqual(dia["carga_final_pct"], 0)
                        self.assertLessEqual(dia["carga_final_pct"], 100)
                        self.assertGreaterEqual(dia["deficit_kwh"], 0)
                        self.assertLessEqual(dia["atendida_kwh"], 1.08 + 1e-9)

    def test_bateria_vazia_primeiro_recompoe_reserva(self):
        r = self.calculadora.simular_dias([1], carga_pct=0)
        self.assertAlmostEqual(r["atendida_total_kwh"], 0)
        self.assertAlmostEqual(r["dias"][0]["carga_final_pct"], 17.9036458333)
        r = self.calculadora.simular_dias([1], carga_pct=20)
        self.assertAlmostEqual(r["atendida_total_kwh"], 0.4125)
        self.assertAlmostEqual(r["dias"][0]["carga_final_pct"], 20)

    def test_sequencia_nao_ignora_sobrecarga_do_inversor(self):
        self.consumo["lampadas"] = 40
        r = self.calculadora.simular_dias([4, 4], self.consumo)
        self.assertEqual(r["noites_completas"], 0)
        self.assertEqual(r["atendida_total_kwh"], 0)
        self.assertFalse(r["potencia_inversor_ok"])

    def test_sequencias_invalidas_sao_recusadas(self):
        for hsps in [[], [4] * 15, "4,1", [float("nan")], [-1], [13], [True]]:
            with self.subTest(hsps=hsps), self.assertRaises(ValueError):
                self.calculadora.simular_dias(hsps)

    def test_atendimento_guiado_aplica_referencia_sem_alterar_o_exemplo_do_arquivo(self):
        texto = self.menu(["7", "5", "2", "3", "4", "0", "5", "1", "0"])
        self.assertIn("Referência aplicada", texto)
        self.assertIn("3,2578", texto)
        self.assertIn("investimento anterior está excluído", texto)
        self.assertIn("COMO CONFERIR AS CONTAS", texto)
        self.assertIn("Exemplo inicial restaurado", texto)
        self.assertEqual(self.calculadora.dados["consumo"]["hsp"], 4)

    def test_menu_sequencia_customizada_cancelamento_e_zeros(self):
        texto = self.menu(["6", "x", "3", "2", "0", "0", "100", "6", "3", "v", "0"])
        self.assertIn("Opção inválida", texto)
        self.assertIn("Noites completas: 1/2", texto)
        self.assertIn("A carga não é reiniciada", texto)
        self.assertIn("excedente", texto.lower())

    def test_exporta_relatorio_tecnico_sem_atribuir_avaliacao_humana(self):
        with tempfile.TemporaryDirectory() as pasta:
            seq = self.calculadora.simular_dias([4, 1, 0])
            arquivo = self.calculadora.exportar_relatorio(pasta=pasta, sequencia=seq)
            texto = arquivo.read_text()
            self.assertIn("RELATÓRIO TÉCNICO", texto)
            self.assertIn("não é avaliação com usuários", texto)
            self.assertIn("https://", texto)
            self.assertIn('"sequencia_se_executada"', texto)
            outro = self.calculadora.exportar_relatorio(pasta=pasta)
            self.assertNotEqual(outro, arquivo)
            self.assertTrue(arquivo.exists())
            with self.assertRaisesRegex(ValueError, "não corresponde"):
                self.calculadora.exportar_relatorio(dict(self.consumo,hsp=1), pasta=pasta, sequencia=seq)

    def test_menu_descarta_sequencia_apos_mudar_parametros(self):
        with patch.object(CalculadoraEnergia, "exportar_relatorio", return_value=Path("relatorio.txt")) as salvar:
            self.menu(["6", "2", "", "2", "10", "", "", "", "", "", "8", "0"])
            self.assertIsNone(salvar.call_args.kwargs["sequencia"])
            self.assertEqual(salvar.call_args.args[0]["lampadas"], 10)

    def test_menu_relatorio_trata_falha_de_escrita(self):
        with patch.object(CalculadoraEnergia, "exportar_relatorio", side_effect=OSError("sem espaço")):
            self.assertIn("Não foi possível salvar", self.menu(["8", "0"]))

    def test_hsp_confundida_com_horas_de_sol_pode_ser_corrigida_antes_de_aplicar(self):
        with patch.object(CalculadoraEnergia, "exportar_relatorio", return_value=Path("relatorio.txt")) as salvar:
            texto = self.menu(["2", "10", "5", "9", "30", "12", "n", "4", "0,789", "8", "0"])
            consumo = salvar.call_args.args[0]
            self.assertEqual(consumo["hsp"], 4)
            self.assertEqual(consumo["tarifa_kwh"], 0.789)
            self.assertEqual(consumo["lampadas"], 10)
            self.assertIn("12 horas de claridade", texto)

    def test_hsp_alta_confirmada_preserva_o_cenario_original_da_avaliacao(self):
        with patch.object(CalculadoraEnergia, "exportar_relatorio", return_value=Path("relatorio.txt")) as salvar:
            texto = self.menu(["2", "10", "5", "9", "30", "12", "s", "0,789", "8", "0"])
            consumo = salvar.call_args.args[0]
            self.assertEqual(consumo["hsp"], 12)
            r = self.calculadora.calcular(consumo)
            self.assertAlmostEqual(r["periodo_kwh"], 13.5)
            self.assertAlmostEqual(r["total_a_rs"], 510.6515)
            self.assertIn("Valor mantido como hipótese", texto)

    def test_cancelar_confirmacao_de_hsp_nao_aplica_campos_anteriores(self):
        with patch.object(CalculadoraEnergia, "exportar_relatorio", return_value=Path("relatorio.txt")) as salvar:
            self.menu(["2", "10", "5", "9", "30", "12", "v", "8", "0"])
            self.assertEqual(salvar.call_args.args[0], self.calculadora.dados["consumo"])

    def test_hsp_alta_na_sequencia_tambem_pede_confirmacao_e_permite_correcao(self):
        with patch.object(CalculadoraEnergia, "exportar_relatorio", return_value=Path("relatorio.txt")) as salvar:
            self.menu(["6", "3", "1", "12", "talvez", "n", "1", "100", "8", "0"])
            seq = salvar.call_args.kwargs["sequencia"]
            self.assertEqual(len(seq["dias"]), 1)
            self.assertEqual(seq["dias"][0]["hsp"], 1)

    def test_hsp_zero_e_padrao_nao_exigem_confirmacao_adicional(self):
        from modulos.energia.calculadora import ler_hsp
        with patch("builtins.input", side_effect=["0"]):
            self.assertEqual(ler_hsp("HSP", 4), 0)
        with patch("builtins.input", side_effect=[""]):
            self.assertEqual(ler_hsp("HSP", 4), 4)

import contextlib
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from assistente import Assistente, ler_opcao
from base_conhecimento import BaseConhecimento, normalizar
from orientacao import Orientacao


RAIZ = Path(__file__).resolve().parents[1]


class TestePCP(unittest.TestCase):
    def setUp(self):
        self.temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporario.cleanup)
        self.pasta = Path(self.temporario.name)
        self.saida = io.StringIO()
        contexto = contextlib.redirect_stdout(self.saida)
        contexto.__enter__()
        self.addCleanup(contexto.__exit__, None, None, None)
        self.base = BaseConhecimento(RAIZ / "data/base_conhecimento.json")
        self.assertTrue(self.base.carregar())
        self.assistente = Assistente("Teste", self.base, self.pasta)

    def gravar_json(self, nome, dados):
        caminho = self.pasta / nome
        caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        return caminho

    def registrar(self, ajudou=True, encontrou=True, tentativas=1, registro=None):
        orientacao = self.base.orientacoes[0] if encontrou else None
        return self.assistente.registrar("pergunta", orientacao, encontrou,
                                         ajudou, tentativas, time.time(), registro)

    def executar_menu(self, entradas, dados=None, projeto=RAIZ):
        return subprocess.run(
            [sys.executable, "-B", str(projeto / "main.py"), "--dados", str(dados or self.pasta)],
            input=entradas, capture_output=True, text=True, cwd=self.pasta, timeout=10
        )

    def test_base_atende_minimos_e_ids_unicos(self):
        self.assertGreaterEqual(len(self.base.orientacoes), 10)
        self.assertGreaterEqual(len(self.base.categorias()), 3)
        self.assertEqual(len({o.id for o in self.base.orientacoes}), len(self.base.orientacoes))
        for orientacao in self.base.orientacoes:
            self.assertGreaterEqual(len({normalizar(c) for c in orientacao.palavras_chave}), 3)

    def test_normalizacao(self):
        self.assertEqual(normalizar(" ÁGUA,  EMERGÊNCIA! \n"), "agua emergencia")

    def test_composicao(self):
        self.assertIs(self.assistente.base, self.base)
        self.assertIsInstance(self.base.orientacoes[0], Orientacao)

    def test_exemplo_de_sete_pontos_do_enunciado(self):
        orientacao = Orientacao(99, "Saúde", "Fazer o Cartão Nacional de Saúde (Cartão SUS)",
                               ["cartao sus", "cartao do sus", "sus", "cns"], "", [], "", "", "")
        self.assertEqual(self.base.pontuar("Como faço o cartão do SUS?", orientacao), 7)

    def test_pontuacao_e_ordem(self):
        resultados = self.base.buscar("socorro emergência abrigo")
        self.assertEqual(resultados[0][0], 7)
        self.assertEqual(resultados[0][1].id, 1)
        self.assertEqual([p for p, _ in resultados], sorted([p for p, _ in resultados], reverse=True))

    def test_limites_de_palavras(self):
        self.assertEqual(self.base.pontuar("socorrista", self.base.orientacoes[0]), 0)

    def test_sem_correspondencia(self):
        self.assertEqual(self.base.buscar("astronomia galáctica"), [])

    def test_perguntas_previstas(self):
        exemplos = {
            "Onde encontro um abrigo?": 5,
            "Como posso pedir ajuda depois de uma enchente?": 1,
            "O que fazer se minha casa estiver em risco?": 3,
            "Como obter alertas da Defesa Civil?": 4,
            "Quais cuidados devo ter com água contaminada?": 7
        }
        for pergunta, esperado in exemplos.items():
            with self.subTest(pergunta=pergunta):
                self.assertEqual(self.base.buscar(pergunta)[0][1].id, esperado)

    def test_categoria_normalizada(self):
        itens = self.base.por_categoria("SAUDE E HIGIENE")
        self.assertTrue({7, 8, 9, 10, 13, 14}.issubset({o.id for o in itens}))
        self.assertTrue(all(o.categoria == "Saúde e higiene" for o in itens))

    def test_base_ausente(self):
        base = BaseConhecimento(self.pasta / "ausente.json")
        self.assertFalse(base.carregar())
        self.assertEqual(base.orientacoes, [])

    def test_base_json_corrompido_e_utf8_invalido(self):
        for conteudo in [b"{", b"\xff"]:
            caminho = self.pasta / "invalido.json"
            caminho.write_bytes(conteudo)
            base = BaseConhecimento(caminho)
            self.assertFalse(base.carregar())
            self.assertEqual(base.orientacoes, [])

    def test_base_raiz_invalida(self):
        base = BaseConhecimento(self.gravar_json("base.json", {}))
        self.assertFalse(base.carregar())

    def test_base_valida_registros_e_continua(self):
        valido = json.loads((RAIZ / "data/base_conhecimento.json").read_text())[0]
        invalidos = [None, 42, {}, dict(valido, id=True), dict(valido, titulo=[]),
                     dict(valido, palavras_chave=["socorro", None, "ajuda"]),
                     dict(valido, palavras_chave=["socorro", "socorro", "socorro"]),
                     dict(valido, documentos="CPF"), dict(valido, verificado_em="2026-02-30"),
                     dict(valido, fonte="javascript:alert(1)")]
        base = BaseConhecimento(self.gravar_json("base.json", invalidos + [valido, valido]))
        self.assertTrue(base.carregar())
        self.assertEqual(len(base.orientacoes), 1)

    def test_caminho_relativo_da_base_independe_do_cwd(self):
        base = BaseConhecimento("data/base_conhecimento.json")
        self.assertEqual(base.caminho, RAIZ / "data/base_conhecimento.json")

    def test_bloqueio_de_dados_pessoais(self):
        for pergunta in ["12345678", "1 2 3 4 5 6 7 8", "teste@example.invalid",
                         "Meu CPF é 123.456.789-09", "Me chamo Pessoa Fictícia",
                         "Meu endereço é um endereço fictício", "Meu telefone 123"]:
            with self.subTest(pergunta=pergunta):
                self.assertTrue(self.assistente.contem_dados_pessoais(pergunta))

    def test_perguntas_gerais_nao_sao_bloqueadas(self):
        for pergunta in ["Perdi meu RG na enchente", "Onde encontro um abrigo?", "Como tratar água?"]:
            self.assertFalse(self.assistente.contem_dados_pessoais(pergunta))

    def test_pergunta_bloqueada_nao_vira_atendimento(self):
        with patch("builtins.input", side_effect=["Meu CPF é 123.456.789-09", "0"]):
            self.assistente.perguntar()
        self.assertEqual(self.assistente.historico, [])
        self.assertNotIn("123.456.789-09", self.saida.getvalue())
        self.assertFalse(self.assistente.caminho_historico.exists())

    def test_texto_identificavel_que_escapa_do_filtro_nao_e_persistido(self):
        pergunta = "Sou Pessoa Fictícia da Silva e preciso de abrigo"
        with patch("builtins.input", side_effect=[pergunta, "s", "0"]):
            self.assistente.perguntar()
        self.assistente.exportar_csv()
        for caminho in [self.assistente.caminho_historico, self.assistente.caminho_csv]:
            texto = caminho.read_text()
            self.assertNotIn("Pessoa Fictícia", texto)
            self.assertNotIn(pergunta, texto)
            self.assertIn("texto livre omitido", texto)
        self.assertNotIn("Pessoa Fictícia", self.saida.getvalue())

    def test_pergunta_vazia_sem_sentido_e_longa(self):
        with patch("builtins.input", side_effect=["", "???", "a" * 501, "0"]):
            self.assistente.perguntar()
        self.assertEqual(self.assistente.historico, [])

    def test_confianca_media_e_alta(self):
        with patch("builtins.input", side_effect=["abrigo", "s", "socorro emergencia", "s", "0"]):
            self.assistente.perguntar()
        self.assertIn("MÉDIA (3 pontos na busca por palavras)", self.saida.getvalue())
        self.assertIn("ALTA (7 pontos na busca por palavras)", self.saida.getvalue())

    def test_exibe_ate_duas_alternativas(self):
        with patch("builtins.input", side_effect=["socorro emergência abrigo agua potavel tetano", "s", "0"]):
            self.assistente.perguntar()
        alternativas = self.saida.getvalue().split("Outras orientações relacionadas:")[1]
        self.assertEqual(sum(linha.startswith("- ") for linha in alternativas.splitlines()), 2)

    def test_reformulacao_conta_no_mesmo_atendimento(self):
        with patch("builtins.input", side_effect=["astronomia", "1", "abrigo", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(len(self.assistente.historico), 1)
        self.assertEqual(self.assistente.historico[0]["tentativas"], 2)
        self.assertTrue(self.assistente.historico[0]["ajudou"])

    def test_nova_duvida_cria_outro_atendimento(self):
        with patch("builtins.input", side_effect=["astronomia", "2", "abrigo", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(len(self.assistente.historico), 2)
        self.assertFalse(self.assistente.historico[0]["encontrou"])

    def test_resposta_nao_ajudou_e_reformulacao(self):
        with patch("builtins.input", side_effect=["abrigo", "n", "1", "socorro", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(len(self.assistente.historico), 1)
        self.assertEqual(self.assistente.historico[0]["tentativas"], 2)
        self.assertEqual(self.assistente.historico[0]["id_orientacao"], 1)

    def test_dado_bloqueado_na_reformulacao_nao_conta_tentativa(self):
        with patch("builtins.input", side_effect=["astronomia", "1", "12345678", "abrigo", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(self.assistente.historico[0]["tentativas"], 2)

    def test_confirmacao_invalida_e_retorno(self):
        with patch("builtins.input", side_effect=["", "talvez", "0"]):
            self.assertIsNone(self.assistente.confirmar())

    def test_retorno_durante_confirmacao(self):
        with patch("builtins.input", side_effect=["abrigo", "0"]):
            self.assistente.perguntar()
        self.assertFalse(self.assistente.historico[0]["ajudou"])

    def test_entrada_unicode_e_numero_muito_longo(self):
        with patch("builtins.input", side_effect=["²", "x", "9" * 5000, "999", "1"]):
            self.assertEqual(ler_opcao("Escolha: ", 3), 1)

    def test_navegacao_categoria_e_retorno(self):
        with patch("builtins.input", side_effect=["²", "1", "x", "1", "s", "0", "0"]):
            self.assistente.navegar()
        self.assertEqual(self.assistente.historico[0]["origem"], "categoria")
        self.assertTrue(self.assistente.historico[0]["ajudou"])

    def test_indicadores_vazios(self):
        indicadores = self.assistente.calcular_indicadores()
        self.assertEqual(indicadores["total"], 0)
        self.assertIsNone(indicadores["facilidade_media"])
        self.assistente.indicadores()
        self.assertIn("Nenhum atendimento registrado", self.saida.getvalue())

    def test_indicadores_e_nota_por_sessao(self):
        for _ in range(3):
            registro = self.registrar()
            registro["facilidade"] = 5
            registro["tempo_segundos"] = 10
        self.assistente.salvar_historico()
        outro = Assistente("Outra sessão", self.base, self.pasta)
        registro = outro.registrar("pergunta", None, False, False, 3, time.time())
        registro["facilidade"] = 1
        registro["tempo_segundos"] = 30
        indicadores = outro.calcular_indicadores()
        self.assertEqual(indicadores["total"], 4)
        self.assertEqual(indicadores["encontrados_percentual"], 75)
        self.assertEqual(indicadores["ajudaram_percentual"], 75)
        self.assertEqual(indicadores["tentativas_media"], 1.5)
        self.assertEqual(indicadores["tempo_medio_segundos"], 15)
        self.assertEqual(indicadores["facilidade_media"], 3)
        self.assertEqual(indicadores["sessoes_avaliadas"], 2)

    def test_facilidade_validada_e_persistida(self):
        self.registrar()
        with patch("builtins.input", side_effect=["x", "6", "5"]):
            self.assistente.avaliar_facilidade()
        outro = Assistente("Reaberto", self.base, self.pasta)
        self.assertEqual(outro.calcular_indicadores()["facilidade_media"], 5)

    def test_facilidade_pode_ser_omitida(self):
        self.registrar()
        with patch("builtins.input", return_value="0"):
            self.assistente.avaliar_facilidade()
        self.assertIsNone(self.assistente.historico[0]["facilidade"])

    def test_migracao_legada_preserva_metricas_e_remove_texto_e_campos_extras(self):
        registro = self.registrar()
        registro.pop("sessao")
        registro["facilidade"] = 5
        registro["pergunta"] = '=HYPERLINK("https://example.invalid";"Pessoa Fictícia")'
        registro["nome"] = "Pessoa Fictícia"
        self.gravar_json("historico.json", [registro])
        outro = Assistente("Migrado", self.base, self.pasta)
        self.assertEqual(len(outro.historico), 1)
        self.assertTrue(outro.historico[0]["ajudou"])
        self.assertEqual(outro.historico[0]["facilidade"], 5)
        self.assertIsNone(outro.calcular_indicadores()["facilidade_media"])
        outro.exportar_csv()
        for nome in ["historico.json", "atendimentos.csv"]:
            texto = (self.pasta / nome).read_text()
            self.assertNotIn("Pessoa Fictícia", texto)
            self.assertNotIn("HYPERLINK", texto)

    def test_historico_com_registros_invalidos(self):
        valido = dict(self.registrar())
        invalidos = [42, None, {}, dict(valido, tempo_segundos="abc"),
                     dict(valido, tempo_segundos=float("nan")), dict(valido, tentativas=True),
                     dict(valido, encontrou="sim"), dict(valido, origem="=formula"),
                     dict(valido, data="Pessoa Fictícia"), dict(valido, id_orientacao="123")]
        self.gravar_json("historico.json", invalidos + [valido])
        outro = Assistente("Limpo", self.base, self.pasta)
        self.assertEqual(outro.calcular_indicadores()["total"], 1)
        outro.indicadores()

    def test_recarregar_historico_nao_duplica_atendimentos(self):
        self.registrar()
        self.assistente.carregar_historico()
        self.assistente.carregar_historico()
        self.assertEqual(len(self.assistente.historico), 1)

    def test_historico_utf8_invalido_e_preservado(self):
        caminho = self.pasta / "historico.json"
        caminho.write_bytes(b"\xff")
        outro = Assistente("Inválido", self.base, self.pasta)
        self.assertFalse(outro.pode_salvar_historico)
        self.assertEqual(caminho.read_bytes(), b"\xff")

    def test_historico_corrompido_preservado_sem_sobrescrever_csv(self):
        for conteudo in ["{", "{}"]:
            (self.pasta / "historico.json").write_text(conteudo)
            (self.pasta / "atendimentos.csv").write_text("CSV anterior")
            outro = Assistente("Corrompido", self.base, self.pasta)
            outro.registrar("pergunta", None, False, False, 1, time.time())
            self.assertFalse(outro.exportar_csv())
            self.assertEqual((self.pasta / "historico.json").read_text(), conteudo)
            self.assertEqual((self.pasta / "atendimentos.csv").read_text(), "CSV anterior")
            self.assertEqual(outro.calcular_indicadores()["total"], 1)

    def test_csv_tem_campos_e_uma_linha_por_atendimento(self):
        self.registrar()
        self.registrar(ajudou=False, encontrou=False)
        self.assertTrue(self.assistente.exportar_csv())
        with self.assistente.caminho_csv.open(newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            linhas = list(leitor)
            self.assertIn("sessao", leitor.fieldnames)
        self.assertEqual(len(linhas), 2)
        self.assertTrue(all(linha["pergunta"].startswith(("Orientação", "Sem correspondência")) for linha in linhas))

    def test_falha_de_gravacao_preserva_historico_anterior(self):
        self.registrar()
        anterior = self.assistente.caminho_historico.read_text()
        with patch.object(Path, "replace", side_effect=OSError):
            self.assertFalse(self.assistente.salvar_historico())
        self.assertEqual(self.assistente.caminho_historico.read_text(), anterior)

    def test_falha_de_exportacao_preserva_csv_anterior(self):
        self.assistente.caminho_csv.write_text("CSV anterior")
        with patch.object(Path, "replace", side_effect=OSError):
            self.assertFalse(self.assistente.exportar_csv())
        self.assertEqual(self.assistente.caminho_csv.read_text(), "CSV anterior")

    def test_exibicao_transparente(self):
        self.base.orientacoes[0].exibir()
        texto = self.saida.getvalue()
        for esperado in ["Fonte:", "Verificado em:", "NÃO é um canal oficial", "Onde:", "Documentos necessários"]:
            self.assertIn(esperado, texto)

    def test_menu_completo_de_outro_diretorio(self):
        processo = self.executar_menu("x\n2\n3\n4\n1\n0\n0\n")
        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn("Base carregada: 30 orientações", processo.stdout)
        self.assertNotIn("DEBUG", processo.stdout)
        self.assertIn("Módulo de documentação pessoal", processo.stdout)
        self.assertIn("Módulo de energia", processo.stdout)
        self.assertTrue((self.pasta / "atendimentos.csv").exists())

    def test_menu_atendimento_avaliacao_e_csv(self):
        processo = self.executar_menu("1\n1\nabrigo\ns\n0\n0\n4\n0\n5\n")
        self.assertEqual(processo.returncode, 0, processo.stderr)
        historico = json.loads((self.pasta / "historico.json").read_text())
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]["facilidade"], 5)
        self.assertTrue(historico[0]["ajudou"])

    def test_eof_na_confirmacao_preserva_atendimento(self):
        processo = self.executar_menu("1\n1\nabrigo\n")
        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertNotIn("Traceback", processo.stderr)
        historico = json.loads((self.pasta / "historico.json").read_text())
        self.assertEqual(len(historico), 1)
        self.assertFalse(historico[0]["ajudou"])
        self.assertTrue((self.pasta / "atendimentos.csv").exists())

    def test_menu_com_base_ausente(self):
        projeto = self.pasta / "sem_base"
        projeto.mkdir()
        for nome in ["main.py", "assistente.py", "base_conhecimento.py", "orientacao.py"]:
            (projeto / nome).write_bytes((RAIZ / nome).read_bytes())
        processo = self.executar_menu("1\n0\n", self.pasta / "dados_isolados", projeto)
        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn("orientações estão indisponíveis", processo.stdout)

    def test_base_com_passos_e_campos_opcionais_invalidos(self):
        valido = json.loads((RAIZ / "data/base_conhecimento.json").read_text())[0]
        self.assertTrue(self.base.registro_valido(valido))
        for campo, valor in [("passos", "texto"), ("passos", [None]),
                             ("observacao", []), ("assuntos", [42]), ("desastres", [None])]:
            with self.subTest(campo=campo, valor=valor):
                self.assertFalse(self.base.registro_valido(dict(valido, **{campo: valor})))

    def test_base_legada_sem_campos_opcionais(self):
        registro = json.loads((RAIZ / "data/base_conhecimento.json").read_text())[0]
        for campo in ["passos", "observacao", "assuntos", "desastres"]:
            registro.pop(campo)
        base = BaseConhecimento(self.gravar_json("legada.json", [registro]))
        self.assertTrue(base.carregar())
        self.assertEqual(base.orientacoes[0].passos, [])

    def test_ambiguidade_alimentos_pergunta_antes_de_responder(self):
        with patch("builtins.input", side_effect=["alimentos", "2", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(self.assistente.historico[0]["id_orientacao"], 11)
        self.assertEqual(self.assistente.historico[0]["tentativas"], 1)
        texto = self.saida.getvalue()
        self.assertIn("mais de um assunto", texto)
        self.assertNotIn("Alimentos atingidos por água de enchente", texto)

    def test_ambiguidade_pode_ser_recusada(self):
        with patch("builtins.input", side_effect=["alimentos", "0", "0"]):
            self.assistente.perguntar()
        self.assertFalse(self.assistente.historico[0]["encontrou"])
        self.assertNotIn("Alimentos atingidos por água de enchente", self.saida.getvalue())

    def test_alternativa_aberta_atualiza_mesmo_atendimento(self):
        with patch("builtins.input", side_effect=["Onde consigo água potável?", "n", "4", "1", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(len(self.assistente.historico), 1)
        self.assertEqual(self.assistente.historico[0]["id_orientacao"], 7)
        self.assertEqual(self.assistente.historico[0]["tentativas"], 2)
        self.assertTrue(self.assistente.historico[0]["ajudou"])

    def test_sem_resultado_pode_abrir_categoria_no_mesmo_atendimento(self):
        with patch("builtins.input", side_effect=["astronomia", "3", "1", "1", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(len(self.assistente.historico), 1)
        self.assertEqual(self.assistente.historico[0]["id_orientacao"], 5)
        self.assertEqual(self.assistente.historico[0]["tentativas"], 2)
        self.assertNotIn("Confiança: ALTA", self.saida.getvalue())

    def test_sugestao_de_digitacao_exige_confirmacao(self):
        self.assertEqual(self.base.buscar("soccoro"), [])
        with patch("builtins.input", side_effect=["soccoro", "1", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(self.assistente.historico[0]["id_orientacao"], 1)
        self.assertIn("Não achei uma correspondência exata", self.saida.getvalue())
        self.assertNotIn("Confiança:", self.saida.getvalue())

    def test_sugestao_nao_aceita_nao_e_resposta_encontrada(self):
        with patch("builtins.input", side_effect=["soccoro", "0", "0"]):
            self.assistente.perguntar()
        self.assertFalse(self.assistente.historico[0]["encontrou"])

    def test_assunto_agua_diferencia_tratamento_e_abastecimento(self):
        self.assertEqual([o.id for o in self.base.sugerir("água")], [7, 11, 14])
        with patch("builtins.input", side_effect=["água", "2", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual(self.assistente.historico[0]["id_orientacao"], 11)

    def test_continuacao_exige_confirmacao_do_assunto(self):
        with patch("builtins.input", side_effect=["abrigo", "s", "E quais documentos preciso levar?", "1", "s", "0"]):
            self.assistente.perguntar()
        self.assertEqual([r["id_orientacao"] for r in self.assistente.historico], [5, 5])
        self.assertIn("Sua dúvida continua sobre o assunto anterior", self.saida.getvalue())
        self.assertIs(self.assistente.ultima_orientacao, self.base.orientacoes[4])

    def test_exemplos_nao_contam_como_atendimento(self):
        with patch("builtins.input", side_effect=["?", "0"]):
            self.assistente.perguntar()
        self.assertEqual(self.assistente.historico, [])

    def test_confirmacao_por_numero(self):
        with patch("builtins.input", return_value="1"):
            self.assertTrue(self.assistente.confirmar())
        with patch("builtins.input", return_value="2"):
            self.assertFalse(self.assistente.confirmar())

    def test_perguntas_naturais_e_intencoes(self):
        casos = json.loads((RAIZ / "testes/casos_perguntas_pcp.json").read_text())
        for caso in casos:
            with self.subTest(pergunta=caso["pergunta"]):
                resultados = self.base.buscar(caso["pergunta"])
                if caso["modo"] == "resposta":
                    self.assertTrue(resultados)
                    self.assertEqual(resultados[0][1].id, caso["ids"][0])
                    self.assertTrue(len(resultados) == 1 or resultados[0][0] - resultados[1][0] > 1)
                elif caso["modo"] == "esclarecer":
                    ids = [o.id for p, o in resultados if resultados[0][0] - p <= 1][:3]
                    self.assertEqual(set(ids), set(caso["ids"]))
                elif caso["modo"] == "sugerir":
                    self.assertEqual(resultados, [])
                    self.assertEqual([o.id for o in self.base.sugerir(caso["pergunta"])], caso["ids"])
                else:
                    self.assertEqual(resultados, [])
                    self.assertEqual(self.base.sugerir(caso["pergunta"]), [])

    def test_eof_durante_esclarecimento_nao_inventa_orientacao(self):
        processo = self.executar_menu("1\n1\nalimentos\n")
        self.assertEqual(processo.returncode, 0, processo.stderr)
        registro = json.loads((self.pasta / "historico.json").read_text())[0]
        self.assertFalse(registro["encontrou"])
        self.assertIsNone(registro["id_orientacao"])

    def test_privacidade_tambem_na_sugestao_guiada(self):
        with patch("builtins.input", side_effect=["água", "2", "1", "0"]):
            self.assistente.perguntar()
        self.assistente.exportar_csv()
        conteudo = self.assistente.caminho_historico.read_text()
        self.assertNotIn('"água"', conteudo)
        self.assertNotIn("ultima_orientacao", conteudo)
        self.assertIn("texto livre omitido", conteudo)

    def test_tipos_de_desastre_e_apoio_compartilhado(self):
        tipos = self.base.tipos_desastre()
        self.assertEqual(len(tipos), 9)
        self.assertNotIn("Apoio geral", tipos)
        self.assertIn("Calor intenso", tipos)
        calor = self.base.por_tipo_desastre("CALOR INTENSO")
        self.assertEqual([o.id for o in calor[:2]], [25, 26])
        self.assertIn(5, [o.id for o in calor])
        self.assertNotIn(13, [o.id for o in calor])

    def test_tipo_inexistente_nao_retorna_apoio_como_se_fosse_cobertura(self):
        self.assertEqual(self.base.por_tipo_desastre("terremotos"), [])

    def test_base_legada_sem_classificacao_de_desastres(self):
        registro = json.loads((RAIZ / "data/base_conhecimento.json").read_text())[0]
        registro.pop("desastres")
        base = BaseConhecimento(self.gravar_json("sem_temas.json", [registro]))
        self.assertTrue(base.carregar())
        self.assertEqual(base.tipos_desastre(), [])
        assistente = Assistente("Legado", base, self.pasta / "isolado")
        self.assertIsNone(assistente.escolher_tipo_desastre())

    def test_navegacao_por_desastre_sem_texto_pessoal(self):
        indice = self.base.tipos_desastre().index("Calor intenso") + 1
        with patch("builtins.input", side_effect=[str(indice), "1", "s", "0"]):
            self.assistente.navegar(por_desastre=True)
        self.assertEqual(len(self.assistente.historico), 1)
        registro = self.assistente.historico[0]
        self.assertEqual(registro["id_orientacao"], 25)
        self.assertEqual(registro["origem"], "categoria")
        self.assertEqual(registro["tentativas"], 1)
        self.assertTrue(registro["ajudou"])
        self.assertNotIn("Confiança:", self.saida.getvalue())

    def test_retorno_do_tipo_sem_escolher_orientacao_nao_cria_atendimento(self):
        with patch("builtins.input", side_effect=["1", "0", "0"]):
            self.assistente.navegar(por_desastre=True)
        self.assertEqual(self.assistente.historico, [])

    def test_menu_completo_por_tipo_de_desastre(self):
        indice = self.base.tipos_desastre().index("Vendavais") + 1
        processo = self.executar_menu(f"1\n4\n{indice}\n1\ns\n0\n0\n0\n4\n")
        self.assertEqual(processo.returncode, 0, processo.stderr)
        historico = json.loads((self.pasta / "historico.json").read_text())
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]["id_orientacao"], 20)
        self.assertEqual(historico[0]["facilidade"], 4)

    def test_comandos_e_exemplos_nao_limitados_a_enchentes(self):
        processo = self.executar_menu("1\n3\n0\n0\n")
        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn("Orientações sobre desastres", processo.stdout)
        self.assertIn("tipo de desastre", processo.stdout)
        self.assertIn("incêndio na vegetação", processo.stdout)
        self.assertNotIn("ORIENTAÇÕES APÓS ENCHENTES", processo.stdout)

    def test_sugestoes_nao_usam_palavras_comuns_como_contexto(self):
        self.assertEqual(self.base.sugerir("Como faço um bolo?"), [])
        self.assertEqual([o.id for o in self.base.sugerir("tempestade")], [20, 21, 22])
        self.assertEqual([o.id for o in self.base.sugerir("soccoro")], [1])

    def test_sinais_de_alerta_do_calor_tem_encaminhamento(self):
        resultados = self.base.buscar("Meu avô está passando mal com o calor")
        self.assertEqual(resultados[0][1].id, 26)
        orientacao = resultados[0][1]
        self.assertIn("192", " ".join(orientacao.passos))
        self.assertIn("não diagnostica", orientacao.observacao)

    def test_casos_multidesastres(self):
        casos = json.loads((RAIZ / "testes/casos_desastres_pcp.json").read_text())
        for caso in casos:
            with self.subTest(pergunta=caso["pergunta"]):
                resultados = self.base.buscar(caso["pergunta"])
                if caso["modo"] == "resposta":
                    self.assertTrue(resultados)
                    self.assertEqual(resultados[0][1].id, caso["ids"][0])
                    self.assertTrue(len(resultados) == 1 or resultados[0][0] - resultados[1][0] > 1)
                elif caso["modo"] == "esclarecer":
                    self.assertTrue(resultados)
                    proximos = [o.id for p, o in resultados if resultados[0][0] - p <= 1][:3]
                    self.assertEqual(set(proximos), set(caso["ids"]))
                elif caso["modo"] == "sugerir":
                    self.assertEqual(resultados, [])
                    self.assertEqual([o.id for o in self.base.sugerir(caso["pergunta"])], caso["ids"])
                else:
                    self.assertEqual(resultados, [])
                    self.assertEqual(self.base.sugerir(caso["pergunta"]), [])


if __name__ == "__main__":
    unittest.main()

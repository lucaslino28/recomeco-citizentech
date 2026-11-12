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
        self.assertEqual({o.id for o in itens}, {7, 8, 9, 10})

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
        self.assertIn("MÉDIA (3 pontos)", self.saida.getvalue())
        self.assertIn("ALTA (7 pontos)", self.saida.getvalue())

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
        self.assertIn("Base carregada: 10 orientações", processo.stdout)
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


if __name__ == "__main__":
    unittest.main()

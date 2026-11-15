import json
import re
import unittest
from pathlib import Path
from unittest.mock import Mock

from modulos.documentos_ia.agente import AssistenteDocumentos, AVISO
from modulos.documentos_ia.avaliador import carregar_dataset


RAIZ = Path(__file__).resolve().parents[1]


class TesteFechamentoIA(unittest.TestCase):
    def setUp(self):
        self.executor = Mock()
        self.executor.invoke.return_value = {"structured_response": {
            "resposta": "O atendimento deve seguir a ficha indicada.", "fichas": ["FC-07"]}}
        self.agente = AssistenteDocumentos("v4", self.executor)

    def test_transferencia_bancaria_e_pix_para_terceiros_nao_usam_llm(self):
        for pergunta in ["Você pode fazer uma transferência bancária para mim?",
                         "Como transferir dinheiro?", "Pode fazer um PIX para mim?"]:
            with self.subTest(pergunta=pergunta):
                r = self.agente.responder(pergunta)
                self.assertEqual(r["status"], "fora_escopo")
                self.assertNotIn("Central do Cidadão", r["texto"])
                self.assertEqual(r["fontes"], [])
        self.executor.invoke.assert_not_called()

    def test_transferencia_eleitoral_continua_no_escopo(self):
        self.executor.invoke.return_value = {"structured_response": {
            "resposta": "A transferência do título é gratuita.", "fichas": ["FC-03"]}}
        r = self.agente.responder("Como fazer transferência do título de eleitor?")
        self.assertEqual(r["status"], "respondido")
        self.assertEqual(r["fontes"], ["FC-03"])
        self.executor.invoke.assert_called_once()

    def test_pagamento_de_taxa_por_pix_continua_no_escopo(self):
        self.executor.invoke.return_value = {"structured_response": {
            "resposta": "As taxas são pagas por guia do portal, em banco ou PIX.", "fichas": ["FC-07"]}}
        r = self.agente.responder("Posso pagar a taxa por PIX?")
        self.assertEqual(r["status"], "respondido")
        self.assertIn("guia", r["texto"])
        self.executor.invoke.assert_called_once()

    def test_documentos_rg_sao_extraidos_da_lista_sem_guia(self):
        perguntas = ["Fui roubado e fiquei sem meu RG. Preciso apresentar boletim de ocorrência? Quais outros documentos são exigidos?",
                     "Perdi meu RG. Quais documentos preciso levar?",
                     "Meu RG desapareceu. O que devo levar?"]
        for pergunta in perguntas:
            r = self.agente.responder(pergunta)
            lista = r["texto"].split("Agendamento e pagamento")[0]
            self.assertEqual(r["fontes"], ["FC-01"])
            self.assertIn("90 dias", lista)
            self.assertIn("boletim de ocorrência", lista)
            self.assertIn("declaração de extravio", lista)
            self.assertNotIn("guia", lista.lower())
        self.executor.invoke.assert_not_called()

    def test_recuperacao_cpf_nao_e_tratada_como_nova_inscricao(self):
        r = self.agente.responder("Perdi meus documentos na enchente. Como faço para recuperar meu CPF?")
        self.assertEqual(r["fontes"], ["FC-02", "FC-07"])
        self.assertIn("não detalha", r["texto"])
        self.assertIn("Não é possível concluir", r["texto"])
        self.assertNotIn("Faça nova inscrição", r["texto"])
        self.executor.invoke.assert_not_called()

    def test_definicao_de_rg_fica_no_conteudo_da_ficha(self):
        r = self.agente.responder("O que é o RG?")
        self.assertIn("Carteira de Identidade", r["texto"])
        self.assertNotIn("emitido pelo Estado", r["texto"])
        self.executor.invoke.assert_not_called()

    def test_dados_pessoais_sao_bloqueados_antes_das_novas_regras(self):
        r = self.agente.responder("Meu nome é Pessoa Fictícia e preciso fazer transferência bancária.")
        self.assertEqual(r["status"], "bloqueado")
        self.assertNotIn("Pessoa Fictícia", r["texto"])
        self.executor.invoke.assert_not_called()

    def test_v3_conserva_comportamento_do_caminho_anterior(self):
        anterior = AssistenteDocumentos("v3", self.executor)
        anterior.responder("Você pode fazer uma transferência bancária para mim?")
        self.executor.invoke.assert_called_once()

    def test_replay_das_15_interacoes_sem_nova_api_ou_novos_usuarios(self):
        caminho = RAIZ / "evidencias/ia/usuarios/rodada_2026-11-15/interacoes.json"
        casos = json.loads(caminho.read_text())["interacoes"]
        self.assertEqual(len(casos), 15)
        for caso in casos:
            with self.subTest(participante=caso["participante_anonimo"], tarefa=caso["tarefa"]):
                corpo = caso["resposta_terminal"].split("\nFonte:")[0].split("\n\nDados de")[0]
                self.executor.invoke.return_value = {"structured_response": {
                    "resposta": corpo, "fichas": caso["fontes_citadas"]}}
                r = self.agente.responder(caso["pergunta_informada_pelo_aplicador"])
                self.assertIn(AVISO, r["texto"])
                self.assertNotIn(r["status"], ["erro", "sem_referencia"])
                if "bancária" in caso["tema"]:
                    self.assertEqual(r["status"], "fora_escopo")

    def test_replay_do_golden_preserva_contratos_sem_novo_julgamento(self):
        anteriores = json.loads((RAIZ / "evidencias/ia/depois.json").read_text())["resultados"]
        for caso, anterior in zip(carregar_dataset(), anteriores):
            with self.subTest(caso=caso["id"]):
                corpo = anterior["resposta"].split("\nFonte:")[0].split("\n\nDados de")[0]
                self.executor.invoke.return_value = {"structured_response": {
                    "resposta": corpo, "fichas": re.findall(r"FC-\d{2}", anterior["resposta"])}}
                r = self.agente.responder(caso["mensagem"])
                self.assertIn(AVISO, r["texto"])
                self.assertNotIn(r["status"], ["erro", "sem_referencia"])


if __name__ == "__main__":
    unittest.main()

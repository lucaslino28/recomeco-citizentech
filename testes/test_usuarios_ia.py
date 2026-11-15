import csv
import tempfile
import unittest
from pathlib import Path

from testes.analisar_usuarios_ia import analisar, CAMPOS_NOTAS, CAMPOS_TAREFAS


class TesteIndicadoresUsuariosIA(unittest.TestCase):
    def setUp(self):
        self.temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporario.cleanup)
        self.pasta = Path(self.temporario.name)
        self.tarefas = []
        for participante, tempos in [("P01", [10, 20, 30]), ("P02", [20, 30, 40])]:
            for numero, tempo in enumerate(tempos, 1):
                self.tarefas.append([participante, f"T{numero:02d}", tempo, 1, 0])
        self.notas = [["P01", 1, 1, 1, 1, 1], ["P02", 5, 5, 5, 5, 5]]

    def gravar(self):
        for nome, campos, dados in [("tarefas.csv", CAMPOS_TAREFAS, self.tarefas),
                                    ("questionario.csv", CAMPOS_NOTAS, self.notas)]:
            with (self.pasta / nome).open("w", encoding="utf-8", newline="") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(campos)
                escritor.writerows(dados)

    def test_medias_sinteticas_e_preservacao_dos_csvs(self):
        self.gravar()
        antes = {p.name: p.read_bytes() for p in self.pasta.glob("*.csv")}
        resultado = analisar(self.pasta)
        self.assertEqual(resultado["tarefas"], 6)
        self.assertEqual(resultado["avaliacoes_individuais"], 10)
        self.assertEqual(resultado["tempo_medio_segundos"], 25)
        self.assertEqual(resultado["media_questionario"], 3)
        self.assertEqual(resultado["conclusao_percentual"], 100)
        self.assertFalse(resultado["minimo_cinco_participantes_registrados"])
        self.assertEqual(antes, {p.name: p.read_bytes() for p in self.pasta.glob("*.csv")})

    def test_rejeita_tarefa_duplicada(self):
        self.tarefas.append(self.tarefas[0])
        self.gravar()
        with self.assertRaisesRegex(ValueError, "duplicada"):
            analisar(self.pasta)

    def test_rejeita_nota_fora_da_escala(self):
        self.notas[0][2] = 6
        self.gravar()
        with self.assertRaisesRegex(ValueError, "entre 1 e 5"):
            analisar(self.pasta)

    def test_rejeita_questionario_de_participante_sem_tarefas(self):
        self.notas[0][0] = "P03"
        self.gravar()
        with self.assertRaisesRegex(ValueError, "coincidir"):
            analisar(self.pasta)


if __name__ == "__main__":
    unittest.main()

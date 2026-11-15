import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from difflib import get_close_matches

from orientacao import Orientacao


def normalizar(texto):
    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        letra for letra in texto
        if not unicodedata.combining(letra)
    )

    texto = re.sub(r"[^a-z0-9\s]", " ", texto)

    return " ".join(texto.split())


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        if not self.caminho.is_absolute():
            self.caminho = Path(__file__).resolve().parent / self.caminho
        self.orientacoes = []

    def registro_valido(self, registro):
        if not isinstance(registro, dict):
            return False

        textos = ["categoria", "titulo", "resposta", "onde", "fonte", "verificado_em"]
        if any(not isinstance(registro.get(campo), str) or not registro[campo].strip()
               for campo in textos):
            return False

        if type(registro.get("id")) is not int or registro["id"] < 1:
            return False

        for campo in ["palavras_chave", "documentos"]:
            itens = registro.get(campo)
            if not isinstance(itens, list):
                return False
            if any(not isinstance(item, str) or not item.strip() for item in itens):
                return False

        chaves = {normalizar(chave) for chave in registro["palavras_chave"]}
        if "" in chaves or len(chaves) < 3:
            return False

        for campo in ["passos", "assuntos", "desastres"]:
            itens = registro.get(campo, [])
            if not isinstance(itens, list) or any(not isinstance(p, str) or not p.strip() for p in itens):
                return False
        if not isinstance(registro.get("observacao", ""), str):
            return False

        try:
            data = date.fromisoformat(registro["verificado_em"])
            fonte = urlparse(registro["fonte"])
            return (data.isoformat() == registro["verificado_em"]
                    and fonte.scheme in ["https", "http"] and bool(fonte.hostname)
                    and fonte.username is None and fonte.password is None)
        except ValueError:
            return False

    def carregar(self):
        self.orientacoes = []

        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if not isinstance(dados, list):
                print("Erro: a base deve conter uma lista.")
                return False

            campos = [
                "id", "categoria", "titulo",
                "palavras_chave", "resposta", "documentos",
                "onde", "fonte", "verificado_em"
            ]

            ids = set()
            for registro in dados:
                if not self.registro_valido(registro) or registro["id"] in ids:
                    print("Aviso: orientação inválida ou com ID repetido ignorada.")
                    continue

                orientacao = Orientacao(**{
                    campo: registro[campo] for campo in campos
                }, passos=registro.get("passos", []), observacao=registro.get("observacao", ""),
                   assuntos=registro.get("assuntos", []), desastres=registro.get("desastres", []))

                self.orientacoes.append(orientacao)
                ids.add(orientacao.id)

            print(
                f"Base carregada: {len(self.orientacoes)} orientações."
            )
            if len(self.orientacoes) < 10 or len(self.categorias()) < 3:
                print("Aviso: a base não atende ao mínimo de 10 orientações e 3 categorias.")
            return bool(self.orientacoes)

        except FileNotFoundError:
            print("Erro: arquivo da base não encontrado.")

        except json.JSONDecodeError:
            print("Erro: arquivo JSON inválido.")

        except (OSError, UnicodeError):
            print("Erro: não foi possível ler a base de conhecimento.")

        return False

    def categorias(self):
        categorias = set()

        for orientacao in self.orientacoes:
            categorias.add(orientacao.categoria)

        return sorted(categorias)

    def por_categoria(self, categoria):
        resultado = []

        for orientacao in self.orientacoes:
            if normalizar(orientacao.categoria) == normalizar(categoria):
                resultado.append(orientacao)

        return resultado

    def tipos_desastre(self):
        tipos = set()
        for orientacao in self.orientacoes:
            tipos.update(tipo for tipo in orientacao.desastres if tipo != "Apoio geral")
        return sorted(tipos)

    def por_tipo_desastre(self, tipo):
        especificas = []
        apoio = []
        for orientacao in self.orientacoes:
            if any(normalizar(tema) == normalizar(tipo) for tema in orientacao.desastres):
                especificas.append(orientacao)
            elif "Apoio geral" in orientacao.desastres:
                apoio.append(orientacao)
        # Uma orientação exclusiva do evento vem antes de cuidados compartilhados.
        especificas.sort(key=lambda orientacao: len(orientacao.desastres))
        return especificas + apoio if especificas else []

    def pontuar(self, pergunta, orientacao):
        pergunta_normalizada = normalizar(pergunta)
        titulo_normalizado = normalizar(orientacao.titulo)

        pontos = 0

        # Cada palavra-chave encontrada vale 3 pontos.
        palavras_chave = set(
            normalizar(chave)
            for chave in orientacao.palavras_chave
        )

        for chave in palavras_chave:
            if chave and f" {chave} " in f" {pergunta_normalizada} ":
                pontos += 3

        # Palavras de 4 ou mais letras presentes no título valem 1 ponto.
        palavras_pergunta = set(pergunta_normalizada.split())
        palavras_titulo = set(titulo_normalizado.split())

        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []

        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)

            if pontos >= 3:
                resultados.append((pontos, orientacao))

        resultados.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return resultados

    def sugerir(self, pergunta):
        # Sem alterar a pontuação: sugestões só são abertas após escolha da pessoa.
        tema = f" {normalizar(pergunta)} "
        diretas = [o for o in self.orientacoes
                   if any(f" {normalizar(a)} " in tema for a in o.assuntos)]
        if diretas:
            return diretas[:3]
        palavras_comuns = {"como", "onde", "para", "pela", "pelo", "esse", "essa", "isso",
                           "quero", "posso", "fazer", "tenho", "depois", "antes", "preciso",
                           "minha", "minhas", "meus", "qual", "quais", "esta", "estao",
                           "estou", "estamos", "tendo", "acontecendo", "cidade", "meu",
                           "pode", "devo", "seria", "sobre", "aqui", "ainda", "muito"}
        palavras = [p for p in normalizar(pergunta).split()
                    if 4 <= len(p) <= 30 and p not in palavras_comuns]
        exatas = []
        aproximadas = []
        for orientacao in self.orientacoes:
            termos = set(" ".join(normalizar(c) for c in orientacao.palavras_chave).split())
            termos = {p for p in termos if len(p) >= 4 and p not in palavras_comuns}
            if any(p in termos for p in palavras):
                exatas.append(orientacao)
            elif any(get_close_matches(p, sorted(termos), n=1, cutoff=0.84) for p in palavras):
                aproximadas.append(orientacao)
        return (exatas + aproximadas)[:3]

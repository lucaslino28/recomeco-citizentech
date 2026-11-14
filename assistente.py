import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from base_conhecimento import normalizar


def ler_opcao(mensagem, limite):
    while True:
        try:
            opcao = int(input(mensagem).strip())
            if 0 <= opcao <= limite:
                return opcao
        except ValueError:
            pass
        print(f"Opção inválida. Digite um número de 0 a {limite}.")


class Assistente:
    def __init__(self, nome, base, pasta_dados=None):
        self.nome = nome
        self.base = base
        pasta = Path(pasta_dados) if pasta_dados is not None else Path("data")
        if not pasta.is_absolute():
            pasta = Path(__file__).resolve().parent / pasta
        self.caminho_historico = pasta / "historico.json"
        self.caminho_csv = pasta / "atendimentos.csv"
        self.historico = []
        self.atendimentos_sessao = []
        self.sessao = uuid4().hex
        self.ultima_orientacao = None
        self.pode_salvar_historico = True
        self.carregar_historico()

    def rotulo_pergunta(self, id_orientacao):
        if id_orientacao is None:
            return "Sem correspondência; texto livre omitido."
        return f"Orientação {id_orientacao}; texto livre omitido."

    def validar_registro(self, registro):
        if not isinstance(registro, dict):
            return None
        if registro.get("origem") not in ["pergunta", "categoria"]:
            return None
        if type(registro.get("encontrou")) is not bool or type(registro.get("ajudou")) is not bool:
            return None
        if registro["ajudou"] and not registro["encontrou"]:
            return None
        tentativas = registro.get("tentativas")
        tempo = registro.get("tempo_segundos")
        if type(tentativas) is not int or tentativas < 1:
            return None
        if type(tempo) not in [int, float] or not 0 <= tempo <= 365 * 24 * 3600:
            return None
        identificador = registro.get("id_orientacao")
        if registro["encontrou"]:
            if type(identificador) is not int or identificador < 1:
                return None
        elif identificador is not None:
            return None
        try:
            data = datetime.fromisoformat(registro["data"]).isoformat(timespec="seconds")
        except (KeyError, TypeError, ValueError):
            return None
        nota = registro.get("facilidade")
        if nota is not None and (type(nota) is not int or not 1 <= nota <= 5):
            nota = None
        sessao = registro.get("sessao")
        if not isinstance(sessao, str) or not re.fullmatch(r"[a-f0-9]{32}", sessao):
            sessao = None

        # Reconstrói apenas campos controlados; nunca reaproveita texto livre legado.
        return {
            "data": data,
            "origem": registro["origem"],
            "pergunta": self.rotulo_pergunta(identificador),
            "id_orientacao": identificador,
            "encontrou": registro["encontrou"],
            "ajudou": registro["ajudou"],
            "tentativas": tentativas,
            "tempo_segundos": round(tempo, 1),
            "facilidade": nota,
            "sessao": sessao
        }

    def carregar_historico(self):
        self.historico = []
        self.pode_salvar_historico = True
        try:
            with self.caminho_historico.open(encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError
        except FileNotFoundError:
            return
        except (ValueError, UnicodeError, OSError):
            self.pode_salvar_historico = False
            print("Aviso: histórico ilegível. O arquivo foi preservado.")
            print("Novos atendimentos ficarão na memória até corrigir o arquivo e reiniciar.")
            return

        for registro in dados:
            validado = self.validar_registro(registro)
            if validado is not None:
                self.historico.append(validado)
        ignorados = len(dados) - len(self.historico)
        if ignorados:
            print(f"Aviso: {ignorados} registro(s) inválido(s) ignorado(s) nos indicadores.")
        if self.historico != dados:
            print("Aviso: histórico revisado; texto livre removido e campos validados.")
            self.salvar_historico()

    def salvar_historico(self):
        if not self.pode_salvar_historico:
            print("Histórico não salvo: corrija o arquivo ilegível antes de reiniciar.")
            return False
        temporario = self.caminho_historico.with_suffix(".json.tmp")
        try:
            self.caminho_historico.parent.mkdir(parents=True, exist_ok=True)
            with temporario.open("w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=4, allow_nan=False)
                arquivo.write("\n")
            temporario.replace(self.caminho_historico)
            return True
        except (OSError, ValueError):
            print("Não foi possível salvar o histórico. Os dados continuam na memória.")
            return False

    def contem_dados_pessoais(self, texto):
        # O limite conta todos os dígitos da mensagem, mesmo separados por pontuação.
        if sum(letra.isdigit() for letra in texto) >= 8 or "@" in texto:
            return True
        texto = normalizar(texto)
        expressoes = [
            "meu nome e", "me chamo", "meu cpf e", "meu rg e",
            "meu endereco", "moro na", "moro no", "resido na", "resido no",
            "meu telefone", "meu celular", "meu email", "meu e mail",
            "sou chamado", "sou chamada", "meu filho se chama", "me identifico como"
        ]
        if any(expressao in texto for expressao in expressoes):
            return True
        if re.search(r"\b(meu|minha) (cpf|rg|telefone|celular|cnh)\s+\d", texto):
            return True
        return False

    def confirmar(self):
        while True:
            resposta = input("\nEssa orientação respondeu sua dúvida? (s/1 = sim, n/2 = não, 0 = voltar): ").strip().lower()
            if resposta in ["s", "1"]:
                return True
            if resposta in ["n", "2"]:
                return False
            if resposta == "0":
                return None
            print("Digite s ou 1 para sim, n ou 2 para não, ou 0 para voltar.")

    def registrar(self, origem, orientacao, encontrou, ajudou, tentativas, inicio, registro=None):
        identificador = orientacao.id if orientacao else None
        dados = {
            "data": datetime.now().astimezone().isoformat(timespec="seconds"),
            "origem": origem,
            "pergunta": self.rotulo_pergunta(identificador),
            "id_orientacao": identificador,
            "encontrou": encontrou,
            "ajudou": ajudou is True,
            "tentativas": tentativas,
            "tempo_segundos": round(max(0, time.time() - inicio), 1),
            "facilidade": None,
            "sessao": self.sessao
        }
        if registro is None:
            registro = dados
            self.historico.append(registro)
            self.atendimentos_sessao.append(registro)
        else:
            registro.update(dados)
        self.salvar_historico()
        return registro

    def exemplos(self):
        print("\nVocê pode perguntar, por exemplo:")
        print("- Fiquei sem ter onde dormir depois da inundação.")
        print("- O barranco está cedendo. O que fazer?")
        print("- Como me proteger de raios ou vento forte?")
        print("- O que fazer durante uma seca ou onda de calor?")
        print("- Há um incêndio na vegetação perto de casa.")
        print("- Preciso de alimentos e acolhimento após um desastre.")
        print("Digite ? para ver estes exemplos novamente ou 0 para voltar.")

    def escolher_lista(self, orientacoes, mensagem):
        print(f"\n{mensagem}")
        for numero, orientacao in enumerate(orientacoes, 1):
            print(f"{numero} - {orientacao.titulo}")
        print("0 - Nenhum destes / voltar")
        escolha = ler_opcao("Escolha o assunto: ", len(orientacoes))
        return orientacoes[escolha - 1] if escolha else None

    def escolher_categoria(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Nenhuma categoria disponível.")
            return None
        while True:
            print("\nSobre qual assunto você precisa de orientação?")
            for numero, categoria in enumerate(categorias, 1):
                print(f"{numero} - {categoria}")
            print("0 - Voltar")
            escolha = ler_opcao("Escolha uma categoria: ", len(categorias))
            if escolha == 0:
                return None
            orientacao = self.escolher_lista(
                self.base.por_categoria(categorias[escolha - 1]), "Escolha a situação mais parecida com a sua:"
            )
            if orientacao is not None:
                return orientacao

    def escolher_resultado(self, resultados):
        proximos = [(p, o) for p, o in resultados if resultados[0][0] - p <= 1][:3]
        if len(proximos) == 1:
            return resultados[0]
        orientacao = self.escolher_lista(
            [o for _, o in proximos],
            "Encontrei mais de um assunto possível. Qual deles responde melhor à sua dúvida?"
        )
        for pontos, candidata in proximos:
            if candidata is orientacao:
                return pontos, orientacao
        return None, None

    def escolher_tipo_desastre(self):
        tipos = self.base.tipos_desastre()
        if not tipos:
            print("Nenhum tipo de desastre disponível nesta base.")
            return None
        while True:
            print("\nQual situação você quer consultar?")
            for numero, tipo in enumerate(tipos, 1):
                print(f"{numero} - {tipo}")
            print("0 - Voltar")
            escolha = ler_opcao("Escolha o tipo de situação: ", len(tipos))
            if escolha == 0:
                return None
            orientacao = self.escolher_lista(self.base.por_tipo_desastre(tipos[escolha - 1]),
                                             "Escolha uma orientação ou um serviço de apoio:")
            if orientacao is not None:
                return orientacao

    def atender(self, orientacao, pontos, alternativas, registro, inicio):
        while True:
            registro = self.registrar(registro["origem"], orientacao, orientacao is not None,
                                      False, registro["tentativas"], inicio, registro)
            if orientacao is not None:
                if pontos is not None:
                    confianca = "ALTA" if pontos >= 6 else "MÉDIA"
                    print(f"\nConfiança: {confianca} ({pontos} pontos na busca por palavras)")
                else:
                    print("\nOrientação aberta pela sua escolha de assunto.")
                orientacao.exibir()
                if alternativas:
                    print("\nOutras orientações relacionadas:")
                    for _, alternativa in alternativas:
                        print(f"- {alternativa.titulo}")
                    print("Se a resposta não ajudar, você poderá abrir uma delas.")
                ajudou = self.confirmar()
                registro["ajudou"] = ajudou is True
                registro["tempo_segundos"] = round(max(0, time.time() - inicio), 1)
                self.salvar_historico()
                if ajudou is None:
                    return "voltar"
                if ajudou:
                    self.ultima_orientacao = orientacao
                    return "nova"
            else:
                print("\nNão encontrei uma orientação confirmada para essa dúvida.")
                print("Tente outras palavras ou escolha um assunto abaixo.")

            print("\nComo você quer continuar?")
            print("1 - Explicar a mesma dúvida de outro jeito")
            print("2 - Encerrar este atendimento e fazer outra pergunta")
            print("3 - Escolher um assunto nas categorias")
            if alternativas:
                print("4 - Abrir outra orientação relacionada")
            print("0 - Voltar")
            while True:
                opcao = ler_opcao("Escolha uma opção: ", 4 if alternativas else 3)
                if opcao == 0:
                    return "voltar"
                if opcao == 1:
                    return "reformular"
                if opcao == 2:
                    return "nova"
                if opcao == 3:
                    escolhida = self.escolher_categoria()
                    novos_pontos = None
                else:
                    escolhida = self.escolher_lista([o for _, o in alternativas], "Qual orientação deseja abrir?")
                    novos_pontos = next((p for p, o in alternativas if o is escolhida), None)
                if escolhida is not None:
                    if orientacao is not None:
                        alternativas = [(pontos, orientacao)] + [(p, o) for p, o in alternativas if o is not escolhida]
                    alternativas = [(p, o) for p, o in alternativas if o is not escolhida][:2]
                    orientacao, pontos = escolhida, novos_pontos
                    registro["tentativas"] += 1
                    break
                print("Escolha como continuar (1 = reformular, 2 = nova dúvida, 3 = categorias, 0 = voltar).")

    def perguntar(self):
        print("\nVou buscar orientações oficiais sobre desastres no Brasil.")
        print("Não informe dados pessoais. Endereços, vagas e atendimento local precisam ser confirmados no município.")
        self.exemplos()
        while True:
            inicio = time.time()
            tentativas = 0
            registro = None
            while True:
                pergunta = input("\nQual é sua dúvida? (0 para voltar, ? para exemplos): ").strip()
                if pergunta == "0":
                    return
                if pergunta == "?":
                    self.exemplos()
                    continue
                if self.contem_dados_pessoais(pergunta):
                    print("Atenção: não informe dados pessoais. Reescreva sua pergunta.")
                    continue
                if not normalizar(pergunta) or len(pergunta) > 500:
                    print("Digite uma pergunta com letras ou números e até 500 caracteres.")
                    continue
                tentativas += 1
                registro = self.registrar("pergunta", None, False, False, tentativas, inicio, registro)
                resultados = self.base.buscar(pergunta)
                pontos, orientacao = None, None
                if resultados:
                    pontos, orientacao = self.escolher_resultado(resultados)
                else:
                    continuacao = any(termo in normalizar(pergunta) for termo in
                                      ["quais documentos", "o que levar", "onde procuro", "qual a fonte"])
                    if continuacao and self.ultima_orientacao is not None:
                        orientacao = self.escolher_lista([self.ultima_orientacao],
                                                        "Sua dúvida continua sobre o assunto anterior?")
                    else:
                        sugestoes = self.base.sugerir(pergunta)
                        if sugestoes:
                            orientacao = self.escolher_lista(sugestoes,
                                "Não achei uma correspondência exata. Você está perguntando sobre um destes assuntos?")
                alternativas = [(p, o) for p, o in resultados if o is not orientacao][:2]
                acao = self.atender(orientacao, pontos, alternativas, registro, inicio)
                tentativas = registro["tentativas"]
                if acao == "voltar":
                    return
                if acao == "nova":
                    break

    def navegar(self, por_desastre=False):
        while True:
            inicio = time.time()
            orientacao = self.escolher_tipo_desastre() if por_desastre else self.escolher_categoria()
            if orientacao is None:
                return
            registro = self.registrar("categoria", orientacao, True, False, 1, inicio)
            acao = self.atender(orientacao, None, [], registro, inicio)
            if acao == "voltar":
                return
            if acao == "reformular":
                self.perguntar()
                return

    def avaliar_facilidade(self):
        if not self.atendimentos_sessao:
            return
        nota = ler_opcao("\nDe 1 a 5, qual a facilidade de uso? (0 para não avaliar): ", 5)
        if nota == 0:
            return
        for registro in self.atendimentos_sessao:
            registro["facilidade"] = nota
        self.salvar_historico()
        print("Obrigado pela avaliação!")

    def calcular_indicadores(self):
        total = len(self.historico)
        notas_por_sessao = {}
        for registro in self.historico:
            if registro["sessao"] and registro["facilidade"] is not None:
                notas_por_sessao[registro["sessao"]] = registro["facilidade"]
        notas = list(notas_por_sessao.values())
        return {
            "total": total,
            "encontrados_percentual": sum(r["encontrou"] for r in self.historico) / total * 100 if total else 0,
            "ajudaram_percentual": sum(r["ajudou"] for r in self.historico) / total * 100 if total else 0,
            "tempo_medio_segundos": sum(r["tempo_segundos"] for r in self.historico) / total if total else 0,
            "tentativas_media": sum(r["tentativas"] for r in self.historico) / total if total else 0,
            "facilidade_media": sum(notas) / len(notas) if notas else None,
            "sessoes_avaliadas": len(notas),
            "sem_solucao": [r for r in self.historico if not r["ajudou"]]
        }

    def indicadores(self):
        indicadores = self.calcular_indicadores()
        print("\nIndicadores de atendimento:")
        if indicadores["total"] == 0:
            print("Nenhum atendimento registrado.")
            return
        print(f"Total de atendimentos: {indicadores['total']}")
        print(f"Resposta encontrada: {indicadores['encontrados_percentual']:.1f}%")
        print(f"Taxa de acerto (ajudou): {indicadores['ajudaram_percentual']:.1f}%")
        print(f"Tempo médio por atendimento: {indicadores['tempo_medio_segundos']:.1f} segundos")
        print(f"Tentativas por atendimento: {indicadores['tentativas_media']:.1f}")
        if indicadores["facilidade_media"] is not None:
            print(f"Facilidade de uso: {indicadores['facilidade_media']:.1f}/5 "
                  f"({indicadores['sessoes_avaliadas']} sessão(ões) avaliada(s))")
        else:
            print("Facilidade de uso: ainda não avaliada por sessão")
        print("\nDúvidas sem solução (resumos sem texto pessoal):")
        if not indicadores["sem_solucao"]:
            print("Nenhuma.")
        for registro in indicadores["sem_solucao"]:
            print(f"- {registro['pergunta']}")

    def exportar_csv(self):
        if not self.pode_salvar_historico:
            print("CSV existente preservado: o histórico precisa ser corrigido.")
            return False
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                  "ajudou", "tentativas", "tempo_segundos", "facilidade", "sessao"]
        temporario = self.caminho_csv.with_suffix(".csv.tmp")
        try:
            self.caminho_csv.parent.mkdir(parents=True, exist_ok=True)
            with temporario.open("w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos, lineterminator="\n")
                escritor.writeheader()
                for registro in self.historico:
                    validado = self.validar_registro(registro)
                    if validado is not None:
                        escritor.writerow(validado)
            temporario.replace(self.caminho_csv)
            print("\nCSV de atendimentos exportado.")
            return True
        except OSError:
            print("Não foi possível exportar o CSV.")
            return False

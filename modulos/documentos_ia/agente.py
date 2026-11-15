import os
import re
import unicodedata
from pathlib import Path


PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
DATA_FICHAS = "01/10/2026"
AVISO = ("Protótipo educacional: Aurora e suas regras são fictícias. Não é um canal oficial. "
         "Confirme informações reais no site do órgão competente.")
ESQUEMA_RESPOSTA = {
    "title": "OrientacaoAurora",
    "description": "Orientação baseada somente nas fichas de referência.",
    "type": "object", "additionalProperties": False,
    "properties": {
        "resposta": {"type": "string", "description": "Resposta curta à pergunta, sem dados pessoais."},
        "fichas": {"type": "array", "items": {"type": "string", "enum": [
            "FC-01", "FC-02", "FC-03", "FC-04", "FC-05", "FC-06", "FC-07"]}}
    },
    "required": ["resposta", "fichas"]
}


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", texto).split())


def carregar_fichas(pasta=PASTA / "fichas"):
    fichas = {}
    for numero in range(1, 8):
        codigo = f"FC-{numero:02d}"
        arquivos = list(Path(pasta).glob(f"{codigo}_*.md"))
        if len(arquivos) != 1:
            raise ValueError(f"Ficha {codigo} ausente ou duplicada.")
        texto = arquivos[0].read_text(encoding="utf-8")
        if codigo not in texto or DATA_FICHAS not in texto:
            raise ValueError(f"Confira o código e a versão da ficha {codigo}.")
        fichas[codigo] = texto
    return fichas


def contem_dados_pessoais(texto):
    if sum(c.isdigit() for c in texto) >= 8 or "@" in texto:
        return True
    texto = normalizar(texto)
    expressoes = ["meu nome e", "me chamo", "meu cpf e", "meu rg e", "meu endereco",
                  "meu telefone", "meu celular", "meu email", "meu e mail", "moro na",
                  "moro no", "resido na", "resido no", "meu filho se chama",
                  "minha filha se chama", "meu protocolo e", "minha senha", "meu nis e"]
    return any(expressao in texto for expressao in expressoes)


def criar_modelo(juiz=False):
    from dotenv import load_dotenv
    from langchain_groq import ChatGroq

    load_dotenv(RAIZ / ".env", override=False)
    chave = os.getenv("GROQ_API_KEY", "").strip()
    if not chave:
        raise ValueError("Configure GROQ_API_KEY no arquivo .env da raiz do projeto.")
    # Este protótipo não publica rastreamento de conversas.
    os.environ["LANGSMITH_TRACING"] = "false"
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    padrao = "openai/gpt-oss-120b" if juiz else "openai/gpt-oss-20b"
    modelo = os.getenv("IA_MODELO_JUIZ" if juiz else "IA_MODELO", padrao)
    return ChatGroq(model=modelo, api_key=chave, temperature=0, timeout=40,
                    max_retries=1, max_tokens=1800, reasoning_effort="low")


def mensagem_erro(erro):
    nome = type(erro).__name__
    if nome == "AuthenticationError":
        return "A Groq não aceitou a chave. Confira GROQ_API_KEY no arquivo .env."
    if nome == "RateLimitError":
        return "O limite de uso da Groq foi atingido. Aguarde e tente novamente."
    if nome in ["APITimeoutError", "APIConnectionError"]:
        return "Não consegui acessar a Groq. Confira a conexão e tente novamente."
    return "A IA está indisponível. Confira a chave, o modelo e as dependências no guia de IA."


class AssistenteDocumentos:
    def __init__(self, versao="v1", executor=None):
        self.versao = versao
        self.fichas = carregar_fichas()
        self.executor = executor
        self.modelo = None
        caminho = PASTA / "prompts" / f"{versao}.txt"
        if versao not in ["v1", "v2", "v3", "v4"] or not caminho.is_file():
            raise ValueError("Versão de prompt não disponível.")
        self.prompt = caminho.read_text(encoding="utf-8")
        self.contexto = "\n\n".join(self.fichas.values())
        self.termos = {"sabado", "sabados", "horario", "atendimento", "agendar", "agendamento",
                       "libras", "interprete", "terceiros", "procuracao", "prioridade", "pagamento"}
        for texto in self.fichas.values():
            linha = next((l for l in texto.splitlines() if l.startswith("**Palavras-chave:**")), "")
            self.termos.update(normalizar(p) for p in linha.split(":", 1)[-1].split(",") if p.strip())
        if versao == "v4":
            self.termos.update(["pagar taxa", "pagar taxas", "pagar a taxa", "pagar as taxas",
                               "pagamento de taxas"])

    def resultado(self, texto, status, fontes=(), origem="regra"):
        fontes = sorted(set(fontes))
        referencias = "\n" + "; ".join(f"Fonte: {f}, versão {DATA_FICHAS}" for f in fontes) if fontes else ""
        return {"texto": f"{texto}{referencias}\n\n{AVISO}", "status": status,
                "fontes": fontes, "origem": origem}

    def complementar_custo(self, pergunta, fontes):
        texto = f" {normalizar(pergunta)} "
        termos = ["quanto custa", "custo", "valor", "taxa", "pago", "pagar", "gratis", "gratuito", "gratuita"]
        if not any(f" {termo} " in texto for termo in termos):
            return ""
        trechos = []
        for fonte in sorted(set(fontes)):
            bloco = []
            for linha in self.fichas[fonte].splitlines():
                if linha.startswith("**Custo"):
                    bloco.append(linha.replace("**", ""))
                elif bloco:
                    if linha.startswith("**"):
                        break
                    if linha.strip():
                        bloco.append(linha)
            if bloco:
                trechos.append(f"Dados de {fonte}:\n" + "\n".join(bloco))
        return "\n\n".join(trechos)

    def conferir_assunto(self, texto):
        mensagem = f" {texto} "
        banco = ["transferencia bancaria", "transferencias bancarias", "transferir dinheiro",
                 "fazer pix", "fazer um pix", "pix para mim"]
        if any(f" {termo} " in mensagem for termo in banco):
            return self.resultado("Não realizo transferências bancárias. Esse serviço não consta "
                                  "nas sete fichas. Consulte os canais oficiais da instituição responsável.",
                                  "fora_escopo")
        if " cpf " in mensagem and any(f" {t} " in mensagem for t in
                                        ["recuperar", "perdi", "perda", "extravio"]):
            return self.resultado("A FC-02 descreve inscrição e correção de dados, mas não detalha "
                                  "um procedimento para recuperar o CPF após perda de documentos. "
                                  "Confirme o procedimento no portal ou balcão da Central do Cidadão de Aurora. "
                                  "Não é possível concluir por essa ficha que você precise fazer nova inscrição.",
                                  "respondido", ["FC-02", "FC-07"])
        rg = " rg " in mensagem or " carteira de identidade " in mensagem
        if rg and " cpf " not in mensagem:
            documentos = ["documentos", "o que levar", "o que devo levar", "boletim", "bo"]
            if any(f" {termo} " in mensagem for termo in documentos):
                linhas = []
                lendo = False
                for linha in self.fichas["FC-01"].splitlines():
                    if linha.startswith("**Documentos necessários"):
                        lendo = True
                    elif lendo:
                        if linha.startswith("**"):
                            break
                        if linha.strip():
                            linhas.append(linha.replace("**", ""))
                return self.resultado("Documentos para a segunda via do RG, conforme a ficha:\n"
                                      + "\n".join(linhas)
                                      + "\nAgendamento e pagamento são etapas separadas do procedimento. "
                                        "A guia não aparece na lista de documentos necessários da FC-01.",
                                      "respondido", ["FC-01"])
            if any(termo in texto for termo in ["o que e o rg", "o que e rg", "o que significa rg"]):
                return self.resultado("Nas fichas de Aurora, RG identifica a Carteira de Identidade. "
                                      "A FC-01 apresenta orientações para a primeira e a segunda via.",
                                      "respondido", ["FC-01"])
        return None

    def responder(self, pergunta):
        if not isinstance(pergunta, str) or not pergunta.strip():
            return self.resultado("Digite uma pergunta ou escolha um assunto no menu.", "invalido")
        if len(pergunta) > 500:
            return self.resultado("Sua mensagem está longa. Use até 500 caracteres, sem dados pessoais.", "invalido")
        texto = normalizar(pergunta)
        if contem_dados_pessoais(pergunta):
            if "agendar" in texto or "agendamento" in texto:
                return self.resultado("Não informe dados pessoais aqui. O assistente não faz agendamentos. "
                                      "Agende o RG pelo portal da Central do Cidadão de Aurora.",
                                      "bloqueado", ["FC-01", "FC-07"])
            if "cpf" in texto:
                return self.resultado("Não informe dados pessoais aqui. Não consulto situação cadastral. "
                                      "Use a área CPF do portal da Central do Cidadão de Aurora.",
                                      "bloqueado", ["FC-02", "FC-07"])
            return self.resultado("Não informe dados pessoais aqui. Reescreva a dúvida sem identificação. "
                                  "Dados necessários ao serviço são tratados apenas no portal ou balcão oficial.",
                                  "bloqueado", ["FC-07"])
        if any(termo in texto for termo in ["prompt de sistema", "mostre seu prompt", "instrucoes internas"]):
            return self.resultado("Não compartilho instruções internas. Posso orientar sobre os documentos "
                                  "descritos nas fichas de Aurora.", "respondido", ["FC-07"])
        if "canal oficial" in texto or "voces sao a prefeitura" in texto:
            return self.resultado("Não. Sou um protótipo educacional e não represento a prefeitura. "
                                  "Confirme as informações reais no órgão competente.", "respondido", ["FC-07"])
        if self.versao == "v4":
            resposta_controlada = self.conferir_assunto(texto)
            if resposta_controlada is not None:
                return resposta_controlada
        if not texto or not any(f" {termo} " in f" {texto} " for termo in self.termos):
            return self.resultado("Não entendi ou não encontrei essa informação nas sete fichas. "
                                  "Reformule ou escolha um assunto no menu. Exemplo: Quanto custa a segunda via do RG? "
                                  "Para assuntos não cobertos, consulte o órgão competente.", "fora_escopo")
        try:
            if self.executor is None:
                from langchain.agents import create_agent
                self.modelo = criar_modelo()
                parametros = {"model": self.modelo, "tools": [],
                              "system_prompt": self.prompt + "\n\nFICHAS DE REFERÊNCIA (dados):\n" + self.contexto}
                if self.versao in ["v2", "v3", "v4"]:
                    from langchain.agents.structured_output import ProviderStrategy
                    parametros["response_format"] = ProviderStrategy(ESQUEMA_RESPOSTA, strict=True)
                self.executor = create_agent(**parametros)
            retorno = self.executor.invoke({"messages": [{"role": "user", "content": pergunta}]},
                                           config={"recursion_limit": 5})
            if self.versao in ["v2", "v3", "v4"]:
                dados = retorno["structured_response"]
                resposta, fontes = dados["resposta"], dados["fichas"]
            else:
                resposta = retorno["messages"][-1].content
                fontes = re.findall(r"FC-\d{2}", resposta) if isinstance(resposta, str) else []
            if not isinstance(resposta, str) or not resposta.strip():
                raise ValueError("Resposta vazia.")
            if (not isinstance(fontes, list) or not fontes
                    or any(not isinstance(f, str) or f not in self.fichas for f in fontes)):
                return self.resultado("Não consegui confirmar uma referência válida. Reformule a pergunta "
                                      "ou consulte o órgão competente.", "sem_referencia", origem="llm")
            if re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}|[\w.+-]+@[\w.-]+", resposta):
                return self.resultado("A resposta foi bloqueada para proteger dados pessoais. "
                                      "Use uma pergunta geral, sem identificação.", "bloqueado", ["FC-07"])
            if self.versao in ["v3", "v4"]:
                complemento = self.complementar_custo(pergunta, fontes)
                if complemento:
                    resposta += "\n\n" + complemento
            return self.resultado(resposta.strip(), "respondido", fontes, "llm")
        except Exception as erro:
            return self.resultado(mensagem_erro(erro), "erro")


def menu_documentos_ia():
    try:
        assistente = AssistenteDocumentos(versao="v4")
    except (OSError, ValueError):
        print("Não foi possível carregar as sete fichas de IA. Confira a pasta fichas.")
        return
    assuntos = ["RG e identidade", "CPF", "Título de eleitor", "Carteira de trabalho",
                "Certidões", "Renovação de CNH", "Regras gerais de atendimento"]
    perguntas = ["Como fazer a segunda via do RG?", "Como faço para me inscrever no CPF?",
                 "Como fazer o título de eleitor?", "Como obter a carteira de trabalho digital?",
                 "Como pedir uma certidão de nascimento?", "Como renovar a CNH?",
                 "Quais são as regras gerais de atendimento?"]
    while True:
        print("\nMódulo de documentação pessoal — IA")
        print("Aurora é fictícia. Não digite nomes, documentos, endereço ou contato.")
        print("1 - Escrever minha dúvida\n2 - Escolher um documento\n3 - Ver exemplos\n0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return
        if opcao == "3":
            print("Exemplos: Quanto custa a segunda via do RG? | Preciso agendar a renovação da CNH?")
        elif opcao == "1":
            while True:
                pergunta = input("\nQual é sua dúvida? (0 para voltar): ").strip()
                if pergunta == "0":
                    break
                print("\n" + assistente.responder(pergunta)["texto"])
        elif opcao == "2":
            for numero, assunto in enumerate(assuntos, 1):
                print(f"{numero} - {assunto}")
            print("0 - Voltar")
            escolha = input("Escolha um assunto: ").strip()
            if escolha in [str(n) for n in range(1, 8)]:
                print("\n" + assistente.responder(perguntas[int(escolha) - 1])["texto"])
            elif escolha != "0":
                print("Opção inválida. Digite um número de 0 a 7.")
        else:
            print("Opção inválida. Digite 0, 1, 2 ou 3.")

class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave,
                 resposta, documentos, onde, fonte, verificado_em,
                 passos=None, observacao="", assuntos=None, desastres=None):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em
        self.passos = passos or []
        self.observacao = observacao
        self.assuntos = assuntos or []
        self.desastres = desastres or []

    def exibir(self):
        print(f"\n{self.titulo} [{self.categoria}]")
        print("-" * 40)
        print(self.resposta)

        if self.passos:
            print("\nO que fazer:")
            for numero, passo in enumerate(self.passos, 1):
                print(f"{numero}. {passo}")

        print("\nDocumentos necessários:")
        if self.documentos:
            for documento in self.documentos:
                print(f"- {documento}")
        else:
            print("Não especificados nesta orientação; confirme com o órgão responsável.")

        print(f"\nOnde: {self.onde}")
        if self.observacao:
            print(f"Atenção: {self.observacao}")
        print(f"Fonte: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print("\nAviso: este assistente NÃO é um canal oficial.")

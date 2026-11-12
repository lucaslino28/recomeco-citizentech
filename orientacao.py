class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave,
                 resposta, documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        print(f"\n{self.titulo} [{self.categoria}]")
        print("-" * 40)
        print(self.resposta)

        print("\nDocumentos necessários:")
        if self.documentos:
            for documento in self.documentos:
                print(f"- {documento}")
        else:
            print("Não há exigência documental informada nesta orientação.")
            print("Confirme os requisitos com o órgão responsável.")

        print(f"\nOnde: {self.onde}")
        print(f"Fonte: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print("\nAviso: este assistente NÃO é um canal oficial.")

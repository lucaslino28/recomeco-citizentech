import argparse

from base_conhecimento import BaseConhecimento
from assistente import Assistente


def menu_pcp(assistente):
    if not assistente.base.orientacoes:
        print("\nAs orientações estão indisponíveis. Confira a base de conhecimento.")
        return
    while True:
        print("\nORIENTAÇÕES APÓS ENCHENTES")
        print("1 - Fazer uma pergunta")
        print("2 - Consultar por categorias")
        print("0 - Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()
        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "0":
            return
        else:
            print("\nOpção inválida. Tente novamente.")


def menu_principal(pasta_dados=None):
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()
    assistente = Assistente("RECOMEÇO", base, pasta_dados)
    print("\nProtótipo educacional. Não é um canal oficial nem de emergência.")
    print("Não informe nome, documentos, telefone, endereço ou outros dados pessoais.")
    print("O texto digitado não é salvo; os registros usam apenas rótulos de orientação.")
    try:
        while True:
            print("\n========================================")
            print("                RECOMEÇO")
            print("             CITIZEN ASSIST AI")
            print("========================================")
            print("1 - Orientações após enchentes")
            print("2 - Documentação pessoal (IA)")
            print("3 - Energia e sustentabilidade")
            print("4 - Indicadores de atendimento")
            print("0 - Encerrar")
            print("========================================")
            opcao = input("\nEscolha uma opção: ").strip()
            if opcao == "1":
                menu_pcp(assistente)
            elif opcao == "2":
                print("\nMódulo de documentação pessoal.")
                print("Funcionalidade em desenvolvimento.")
            elif opcao == "3":
                print("\nMódulo de energia e sustentabilidade.")
                print("Funcionalidade em desenvolvimento.")
            elif opcao == "4":
                assistente.indicadores()
                assistente.exportar_csv()
            elif opcao == "0":
                assistente.avaliar_facilidade()
                print("\nObrigado por utilizar o RECOMEÇO!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado. Atendimentos sem confirmação permanecem sem solução.")
    finally:
        assistente.exportar_csv()


if __name__ == "__main__":
    argumentos = argparse.ArgumentParser(description="RECOMEÇO — orientações após enchentes")
    argumentos.add_argument("--dados", help="Pasta separada para histórico e CSV, por exemplo em testes externos")
    opcoes = argumentos.parse_args()
    menu_principal(opcoes.dados)

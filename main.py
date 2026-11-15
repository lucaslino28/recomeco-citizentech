import argparse
from datetime import date

from base_conhecimento import BaseConhecimento
from assistente import Assistente


def menu_pcp(assistente):
    if not assistente.base.orientacoes:
        print("\nAs orientações estão indisponíveis. Confira a base de conhecimento.")
        return
    while True:
        print("\nORIENTAÇÕES SOBRE DESASTRES")
        print("1 - Escrever minha dúvida")
        print("2 - Escolher um assunto passo a passo")
        print("3 - Ver exemplos de perguntas")
        print("4 - Escolher o tipo de desastre")
        print("0 - Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()
        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.exemplos()
        elif opcao == "4":
            assistente.navegar(por_desastre=True)
        elif opcao == "0":
            return
        else:
            print("\nOpção inválida. Tente novamente.")


def menu_principal(pasta_dados=None, data_indicadores=None):
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
            print("1 - Orientações sobre desastres")
            print("2 - Documentação pessoal (IA)")
            print("3 - Energia e sustentabilidade")
            print("4 - Indicadores de atendimento")
            print("0 - Encerrar")
            print("========================================")
            opcao = input("\nEscolha uma opção: ").strip()
            if opcao == "1":
                menu_pcp(assistente)
            elif opcao == "2":
                from modulos.documentos_ia.agente import menu_documentos_ia
                menu_documentos_ia()
            elif opcao == "3":
                print("\nMódulo de energia e sustentabilidade.")
                print("Funcionalidade em desenvolvimento.")
            elif opcao == "4":
                assistente.indicadores(data_indicadores)
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
    argumentos = argparse.ArgumentParser(description="RECOMEÇO — orientações sobre desastres no Brasil")
    argumentos.add_argument("--dados", help="Pasta separada para histórico e CSV, por exemplo em testes externos")
    argumentos.add_argument("--data-indicadores", type=date.fromisoformat, metavar="AAAA-MM-DD",
                            help="Filtrar a exibição dos indicadores por data; o CSV continua completo")
    opcoes = argumentos.parse_args()
    menu_principal(opcoes.dados, opcoes.data_indicadores)

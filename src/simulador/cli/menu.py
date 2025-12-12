from simulador.utils import clear


def exibir_menu():
    """Menu principal retorna um int da escolha."""
    print("\n--- Simulador de compras ---")
    print("\n--- Carrinho ---")
    print("- 1 - Adicionar produtos ao carrinho.")
    print("- 2 - Ver produtos no carrinho.")
    print("- 3 - Editar ou remover produto do carrinho.")
    print("- 4 - Fechar a compra é gerar o cupom fiscal.")
    print()
    print("\n--- Estoque ---")
    print("- 5 - Lista de produtos disponíveis.")
    print("- 6 - Adicionar produtos ao estoque.")
    print("- 7 - Remover produtos do estoque.")
    print("- 8 - Alterar produto no estoque.")
    print("- 9 - Sair.")
    try:
        return int(input("\nEscolha: ").strip())
    except ValueError:
        clear()
        print("\nDigite um valor valido")
        return 0

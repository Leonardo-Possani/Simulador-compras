from utils import clear

def exibir_menu():
    """Menu principal retorna um int da escolha"""
    print("\n--- Simulador de compras ---")
    print("- 1 - Lista de produtos disponíveis.")
    print("- 2 - Adicionar produtos ao carrinho.")
    print("- 3 - Ver produtos no carrinho")
    print("- 4 - Cupom fiscal")
    print("- 5 - Sair.")
    try:
        return int(input("\nEscolha: ").strip())
    except ValueError:
        clear()
        print("\nDigite um valor valido")
        return 0



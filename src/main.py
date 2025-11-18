from menu import exibir_menu
from produtos import carregar_produtos
from carrinho import (
        lista_existe,
        adicionar_ao_carrinho,
        mostra_carrinho,
        carregar_carrinho,
)
from cupom import cupom_fiscal
from utils import clear


def main():
    """Main controla o fluxo da aplicação"""
    produtos = carregar_produtos()
    carrinho = carregar_carrinho()
    while True:
        escolha = exibir_menu()
        match escolha:
            case 5:
                clear()
                print("\nSaindo...")
                break
            case 1:
                clear()
                for produto, valor in produtos.items():
                    print(f"Produto: {produto:<6} R${valor:.2f}")

            case 2:
                print(adicionar_ao_carrinho(produtos, carrinho))

            case 3:
                if lista_existe(carrinho):
                    mostra_carrinho(produtos, carrinho)
                else:
                    clear()
                    print("Adicione produtos ao carrinho.")
            case 4:
                if lista_existe(carrinho):
                    cupom_fiscal(produtos, carrinho)
                else:
                    clear()
                    print("Adicione produtos ao carrinho.")


if __name__ == "__main__":
    main()

from .menu import exibir_menu
from .estoque import (
    carregar_produtos,
    adicionar_produto_estoque,
    produtos_disponivei_estoque,
    remover_produto_estoque,
    editar_produto_estoque,
)
from .carrinho import (
    lista_existe,
    adicionar_ao_carrinho,
    mostra_carrinho,
    carregar_carrinho,
    editar_remover_carrinho,
)
from .cupom import cupom_fiscal
from .utils import clear


def main():
    """Main controla o fluxo da aplicação."""

    estoque = carregar_produtos()
    carrinho = carregar_carrinho()
    while True:
        escolha = exibir_menu()
        match escolha:
            case 9:
                clear()
                print("\nSaindo...")
                break
            case 5:
                clear()
                produtos_disponivei_estoque(estoque)
            case 1:
                resposta = adicionar_ao_carrinho(estoque, carrinho)
                print(resposta)

            case 2:
                if lista_existe(carrinho):
                    mostra_carrinho(carrinho)
                else:
                    clear()
                    print("Adicione produtos ao carrinho.")
            case 3:
                if lista_existe(carrinho):
                    editar_remover_carrinho(carrinho, estoque)
                else:
                    clear()
                    print("Adicione produtos ao carrinho.")
            case 4:
                if lista_existe(carrinho):
                    cupom_fiscal(carrinho, estoque)
                else:
                    clear()
                    print("Adicione produtos ao carrinho.")
            case 6:
                adicionar_produto_estoque(estoque)
            case 7:
                clear()
                remover_produto_estoque(estoque)
            case 8:
                clear()
                editar_produto_estoque(estoque)


if __name__ == "__main__":
    main()

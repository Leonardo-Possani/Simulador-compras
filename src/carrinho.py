from utils import clear
from estoque import produtos_disponivei_estoque
import json


def carregar_carrinho():
    """Carrega o arquivo carrinho.json"""
    with open("../data/carrinho.json", "r", encoding="utf-8") as f:
        carrinho = json.load(f)
    return carrinho

def gravar_carrinho(carrinho):
    with open("../data/carrinho.json", "w", encoding="utf-8") as f:
        json.dump(carrinho, f, indent=4, ensure_ascii=False)


def limpar_carrinho():
    """Limpa os itens do carrinho, atribuindo uma lista []."""
    with open("../data/carrinho.json", "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)
    return []


def lista_existe(lista):
    """Verifica se tem produtos cadastrados no carrinho."""
    return bool(lista)


def adicionar_ao_carrinho(estoque, carrinho):
    """Adiciona produto e quantidade ao carrinho retorna string confirmando ou apontando o erro."""
    clear()
    produtos_disponivei_estoque(estoque)
    try:
        adicionar = int(input("\nNúmero do produto: ").strip())
        qtd = int(input("Quantidade: ").strip())
        if adicionar <= 0 or qtd <= 0:
            print("\nDigite um valor maior que zero.")
            return
    except ValueError:
        print("\nDigite um valor valido.")
        return
    indice = adicionar - 1
    produto_original = estoque[indice]
    produto_carrinho = produto_original.copy()
    produto_carrinho["qtd"] = qtd
    nome = produto_carrinho["produto"]
    produto_carrinho["indice"] = indice
    carrinho.append(produto_carrinho)
    gravar_carrinho(carrinho)
    clear()
    return f"\nProduto: {nome} undades: {qtd} foram adicionados ao carrinho. "


def mostra_carrinho(carrinho):
    """Mostra os produtos do carrinho, valores, quantidade e total com desconto."""
    clear()
    print("\n--- Produtos no carrinho ---\n")

    total_bruto = 0
    for produto in carrinho:
        nome = produto["produto"]
        qtd = produto["qtd"]
        preco = produto["preco"]
        subtotal = qtd * preco
        total_bruto += subtotal
        print(f" - {nome:<10} x{qtd:<3} Subtotal: R${subtotal:.2f}")

    print("\nTotal sem descontos: R${:.2f}".format(total_bruto))

    # descontos
    match total_bruto:
        case n if n > 50:
            total_final = total_bruto * 0.90
            print(f"Desconto de 10% aplicado. Total final: R${total_final:.2f}")
        case n if n > 30:
            total_final = total_bruto * 0.95
            print(f"Desconto de 5% aplicado. Total final: R${total_final:.2f}")
        case _:
            print("Nenhum desconto aplicado.")

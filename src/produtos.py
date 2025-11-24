import json
from utils import clear


def carregar_produtos():
    """Carrega o arquivo produtos.json e atribuia estoque."""
    with open("../data/produtos.json", "r", encoding="utf-8") as f:
        estoque = json.load(f)
    return estoque


def produtos_disponivei_estoque(estoque):
    """Exibe os produtos disponíveis no estoque."""
    print("\n--- Produtos disponíveis ---")
    print()
    for i, produto in enumerate(estoque, start=1):
        print(
            f"{i} | {produto['produto']} | quantidade: {produto['qtd']} | preço: R${produto['preco']:.2f}"
        )


def adicionar_produto_estoque(estoque):
    """Adiciona produtos ao estoque, salva no json."""
    clear()
    produto = input("\nNome do produto: ").strip().lower()
    if not produto:
        return "\nDigite o nome do produto."
    try:
        qtd = int(input("Unidades: ").strip())
        if qtd <= 0:
            clear()
            return "\nA quantidade deve ser maior que zero."
        preco = float(input("Preço por unidade: ").strip())
        if preco <= 0:
            clear()
            return "\nO preço deve ser maior que zero."
    except ValueError:
        clear()
        return "\nDigite um número valido."

    estoque.append({"produto": produto, "qtd": qtd, "preco": preco})
    with open("../data/produtos.json", "w", encoding="utf-8") as f:
        json.dump(estoque, f, indent=4, ensure_ascii=False)
    clear()
    return "\nProduto cadastrado com sucesso !"


def remover_produto_estoque(estoque):
    """Exibe os produtos no estoque, remove produtos do estoque."""
    produtos_disponivei_estoque(estoque)
    try:
        remover = int(
            input("\nNumero de indice do produto que deseja remover.").strip()
        )
        if remover <= 0:
            print("\nDigite um número maior que zero.")
            return 0
    except ValueError:
        print("\nDigite um número valido.")

    estoque.pop(remover - 1)
    with open("../data/produtos.json", "w", encoding="utf-8") as f:
        json.dump(estoque, f, indent=4, ensure_ascii=False)
    print("\nProduto removido com sucesso !")

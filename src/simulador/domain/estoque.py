import json
from simulador.utils import clear


def carregar_produtos():
    """Carrega o arquivo produtos.json e atribuia estoque."""
    with open("../../data/produtos.json", "r", encoding="utf-8") as f:
        estoque = json.load(f)
    return estoque


def gravar_estoque_json(estoque):
    """Grava modificações no estoque no arquivo json, produtos.json."""
    with open("../../data/produtos.json", "w", encoding="utf-8") as f:
        json.dump(estoque, f, indent=4, ensure_ascii=False)


def produtos_disponivei_estoque(estoque):
    """Exibe os produtos disponíveis no estoque."""
    print("\n--- Produtos disponíveis ---")
    print()
    for i, produto in enumerate(estoque, start=1):
        print(
            f"{i} | {produto['produto']} | Qtd: {produto['qtd']} | preço: R${produto['preco']:.2f}"
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
    gravar_estoque_json(estoque)
    clear()
    return "\nProduto cadastrado com sucesso !"


def remover_produto_estoque(estoque):
    """Exibe os produtos no estoque, remove produtos do estoque."""
    produtos_disponivei_estoque(estoque)
    try:
        remover = int(
                input("\nProduto: ").strip()
        )
        if remover <= 0:
            print("\nDigite um número maior que zero.")
            return
    except ValueError:
        print("\nDigite um número valido.")
        return

    estoque.pop(remover - 1)
    gravar_estoque_json(estoque)
    print("\nProduto removido com sucesso !")


def editar_produto_estoque(estoque):
    """Edita Nome, qtd e preço de um produto individual mente, se o usuario não digitar nada ele manten os valores antigos."""
    produtos_disponivei_estoque(estoque)
    print("\nEscolha o produto:")

    try:
        editar = input("Produto: ").strip()
        if not editar.isdigit():
            clear()
            print("Digite um número válido.")
            return
        editar = int(editar)
        if editar <= 0 or editar > len(estoque):
            clear()
            print("Produto inexistente.")
            return
    except ValueError:
        clear()
        print("Entrada inválida.")
        return

    indice = editar - 1
    produto = estoque[indice]

    nome_atual = produto["produto"]
    qtd_atual = produto["qtd"]
    preco_atual = produto["preco"]

    novo_nome = input(f"Nome do produto [{nome_atual}]: ").strip()
    if novo_nome == "":
        novo_nome = nome_atual

    entrada_qtd = input(f"Quantidade [{qtd_atual}]: ").strip()
    if entrada_qtd == "":
        nova_qtd = qtd_atual
    else:
        if not entrada_qtd.isdigit():
            print("Quantidate inválida.")
            return
        nova_qtd = int(entrada_qtd)
        if nova_qtd < 0:
            print("Digite um valor positivo.")
            return

    entrada_preco = input(f"Preço [{preco_atual}]: ").strip()
    if entrada_preco == "":
        novo_preco = preco_atual
    else:
        try:
            novo_preco = float(entrada_preco)
        except ValueError:
            print("Preço inválido.")
            return
        if novo_preco < 0:
            print("Preço não pode ser negativo.")
            return

    estoque[indice]["produto"] = novo_nome
    estoque[indice]["qtd"] = nova_qtd
    estoque[indice]["preco"] = novo_preco

    gravar_estoque_json(estoque)

    clear()
    print("Estoque alterado com sucesso")


def cupom_modifica_qtd_estoque(carrinho, estoque):
    for produto in carrinho:
        qtd = produto["qtd"]
        indice = produto["indice"]
        qtd_atual = estoque[indice]["qtd"]
        nova_qtd = qtd_atual - qtd
        estoque[indice]["qtd"] = nova_qtd
    gravar_estoque_json(estoque)

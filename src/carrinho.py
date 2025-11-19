from utils import clear
import json


def carregar_carrinho():
    with open("../data/carrinho.json", "r", encoding="utf-8") as f:
        lista_compras = json.load(f)
    return lista_compras

def limpar_carrinho():
    with open("../data/carrinho.json", "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)
        f.flush()


def lista_existe(lista):
    """Verifica se tem produtos cadastrados no carrinho"""
    return bool(lista)


def adicionar_ao_carrinho(produtos, carrinho):
    """Adiciona produto e quantidade a lista_compras retorna string confirmando ou apontando o erro"""
    produto = input("\nProduto: ").strip().lower()
    if produto not in produtos:
        clear()
        return f"\nO Produto: {produto} não está na lista de produtos disponíveis."
    try:
        quantidade = int(input("Quantidade: ").strip())
        if quantidade <= 0:
            clear()
            return "\nA quantidade deve ser maior que zero."
    except ValueError:
        clear()
        return "\nDigite um número valido."
    carrinho.append({"produto": produto, "qtd": quantidade})
    with open("../data/carrinho.json", "w", encoding="utf-8") as f:
        json.dump(carrinho, f, indent=4, ensure_ascii=False)
    clear()
    return "\nProduto adicionado ao carrinho com sucesso !"


def mostra_carrinho(produtos, carrinho):
    """Mostra os produtos do carrinho, valores individuais e total com desconto."""
    clear()
    print("\n--- Produtos no carrinho ---\n")

    total_bruto = 0
    for item in carrinho:
        nome = item["produto"]
        qtd = item["qtd"]
        preco = produtos[nome]
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

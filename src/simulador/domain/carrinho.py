
def adicionar_item(carrinho, estoque, indice, quantidade):
    novo_carrinho = []
    if len(carrinho) > 0:
        novo_item = {}
        for item in carrinho:
            if item["indice"] == indice:
                item["qtd"] + 2
            novo_item = item
            novo_carrinho = carrinho
        return novo_item, None, novo_carrinho

    else:        
        produto = estoque[indice]
        nome = produto["produto"]
        preco = produto["preco"]
        item = {"produto": nome, "preco": preco, "qtd": quantidade, "indice": indice}
        return item, None





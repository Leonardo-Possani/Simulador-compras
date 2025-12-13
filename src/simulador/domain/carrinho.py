
def adicionar_item(carrinho, estoque, indice, quantidade):
    qtd_estoque = estoque[indice]["estoque"]   
    if quantidade <= 0:
        return None, "erro de quantidade", carrinho

    for item in carrinho:
        if item["indice"] == indice:
            qtd_atual_carrinho = item["qtd"] + quantidade
            if qtd_atual_carrinho > qtd_estoque:
                return None, "Erro quantidade indisponível no estoque.", carrinho
                
            item["qtd"] += quantidade
            return item, None, carrinho
        
    produto = estoque[indice]
    nome = produto["produto"]
    preco = produto["preco"]
    item = {"produto": nome, "preco": preco, "qtd": quantidade, "indice": indice}
    return item, None, carrinho





def item_existe_no_carrinho(carrinho, indice):
    for item in carrinho:
        if item["indice"] == indice:
            return item
    return None


def valida_indice_no_estoque(estoque, indice):
    if not 0 <= indice < len(estoque):
        return "erro"
    return None


def valida_qtd_atual_carrinho_menor_estoque(qtd_existente_carrinho, quantidade, qtd_estoque):
    if qtd_existente_carrinho + quantidade > qtd_estoque:
        return "erro"
    return None


def adicionar_item(carrinho, estoque, indice, quantidade):
        
    estoque_validado = valida_indice_no_estoque(estoque, indice)
    if estoque_validado == "erro":
        return None, "Erro indice inexistente.", carrinho

    qtd_estoque = estoque[indice]["estoque"]

    if quantidade <= 0:
        return None, "erro de quantidade", carrinho

    item = item_existe_no_carrinho(carrinho, indice)

    if item:
        qtd_existente_carrinho = item["qtd"]
        qtd_atual_carrinho_validado = valida_qtd_atual_carrinho_menor_estoque(qtd_existente_carrinho, quantidade, qtd_estoque)
        if qtd_atual_carrinho_validado == "erro":
            return None, "Erro quantidade indisponível no estoque.", carrinho
            
        item["qtd"] += quantidade
        return item, None, carrinho

    produto = estoque[indice]
    nome = produto["produto"]
    preco = produto["preco"]
    item = {"produto": nome, "preco": preco, "qtd": quantidade, "indice": indice}
    return item, None, carrinho


def remover_item(carrinho, indice):
    item = item_existe_no_carrinho(carrinho, indice)
    if item: 
        item_removido = carrinho.pop(indice)
        return item_removido, None, carrinho
    return None, "erro, item inexistente.", carrinho



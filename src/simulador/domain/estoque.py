def valida_estoque_para_venda(itens_vendidos, estoque):

    for item in itens_vendidos:

        indice = item["indice"]
        qtd = item["qtd"]

        if estoque[indice]["estoque"] < qtd:
            return {"ok": False, "data": None, "error": "estoque insuficiente"}
    return {"ok": True, "data": True, "error": None}


def venda_concluindo_baixar_estoque(itens_vendidos, estoque):

    estoque_atualizado = estoque.copy()
    
    for item in itens_vendidos:
        
        indice = item["indice"]
        qtd = item["qtd"]
        
        estoque_atualizado[indice]["estoque"] -= qtd

    return {"ok": True, "data": {"estoque_atualizado": estoque_atualizado}, "error": None}


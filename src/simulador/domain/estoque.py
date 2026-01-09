

def venda_concluida_baixar_estoque(itens_vendidos, estoque):

    estoque_atualizado = estoque.copy()
    
    for item in itens_vendidos:
        
        indice = item["indice"]
        qtd = item["qtd"]
        
        estoque_atualizado[indice]["estoque"] -= qtd

    return estoque_atualizado, None


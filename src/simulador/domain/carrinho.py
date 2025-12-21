# Buscar


def item_existe_no_carrinho(carrinho, indice):
    for item in carrinho:
        if item["indice"] == indice:
            return item
    return None


# Validações


def valida_indice_no_estoque(estoque, indice):
    if not 0 <= indice < len(estoque):
        return True
    return False


def valida_qtd_atual_carrinho_menor_estoque(qtd_existente_carrinho, quantidade, qtd_estoque):
    if qtd_existente_carrinho + quantidade > qtd_estoque:
        return True
    return False


# Mutações do carrinho

def remover_item(carrinho, indice):

    item = item_existe_no_carrinho(carrinho, indice)
    if item: 
        carrinho.remove(item)
        return item, None, carrinho
    return None, "indice inexistente.", carrinho


def adicionar_item(carrinho, estoque, indice, quantidade):
        
    estoque_validado = valida_indice_no_estoque(estoque, indice)
    if estoque_validado:
        return None, "indice inexistente.", carrinho

    qtd_estoque = estoque[indice]["estoque"]

    if quantidade <= 0:
        return None, "quantidade indisponível", carrinho

    item = item_existe_no_carrinho(carrinho, indice)

    if item:
        qtd_existente_carrinho = item["qtd"]
        qtd_atual_carrinho_validado = valida_qtd_atual_carrinho_menor_estoque(qtd_existente_carrinho, quantidade, qtd_estoque)
        if qtd_atual_carrinho_validado:
            return None, "quantidade indisponível", carrinho
            
        item["qtd"] += quantidade
        return item, None, carrinho

    produto = estoque[indice]
    nome = produto["produto"]
    preco = produto["preco"]
    item = {"produto": nome, "preco": preco, "qtd": quantidade, "indice": indice}
    return item, None, carrinho


# Cálculos financeiros


def calcular_total(carrinho):

    total = 0

    for item in carrinho:
        total += item["preco"] * item["qtd"]
    
    return total


def calcular_desconto(total, desconto):

    total_de_desconto = total * (desconto / 100)
    total_com_desconto = total - total_de_desconto
    return total_com_desconto


def aplica_taxa(total, taxa):

    total_com_taxa = total + taxa
    return total_com_taxa

# Orquestração


def total_final(carrinho, desconto, taxa):

    total_bruto = calcular_total(carrinho)
    total_com_desconto = calcular_desconto(total_bruto, desconto)
    total_final = total_com_desconto + taxa
    return total_final
    






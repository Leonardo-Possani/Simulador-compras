from simulador.domain.result import Result

# Buscar


def item_existe_no_carrinho(carrinho: list[dict], indice: int) -> Result[dict]:
    for item in carrinho:
        if item["indice"] == indice:
            return Result(ok=True, data=item)
    return Result(ok=False)


# Validações


def valida_indice_no_estoque(estoque, indice):
    if not 0 <= indice < len(estoque):
        return False
    return True


def valida_qtd_atual_carrinho_menor_estoque(qtd_existente_carrinho, quantidade, qtd_estoque):
    if qtd_existente_carrinho + quantidade > qtd_estoque:
        return False
    return True


# Mutações do carrinho


def remover_item(carrinho, indice):

    resultado = item_existe_no_carrinho(carrinho, indice)
    item = resultado.data
    if resultado.ok:
        carrinho.remove(item)
        return {"ok": True, "data": {"item": item}, "error": None}
    return {"ok": False, "data": None, "error": "indice inexistente"}


def adicionar_item(carrinho, estoque, indice, quantidade):

    estoque_validado = valida_indice_no_estoque(estoque, indice)
    if not estoque_validado:
        return {"ok": False, "data": None, "error": "indice inexistente"}

    qtd_estoque = estoque[indice]["estoque"]

    if quantidade <= 0:
        return {"ok": False, "data": None, "error": "quantidade indisponível"}

    resultado = item_existe_no_carrinho(carrinho, indice)
    item = resultado.data

    if resultado.ok:
        qtd_existente_carrinho = item["qtd"]
        qtd_atual_carrinho_validado = valida_qtd_atual_carrinho_menor_estoque(
            qtd_existente_carrinho, quantidade, qtd_estoque
        )
        if not qtd_atual_carrinho_validado:
            return {"ok": False, "data": None, "error": "quantidade indisponível"}

        item["qtd"] += quantidade
        return {"ok": True, "data": {"item": item, "carrinho": carrinho}, "error": None}

    produto = estoque[indice]
    nome = produto["produto"]
    preco = produto["preco"]
    item = {"produto": nome, "preco": preco, "qtd": quantidade, "indice": indice}
    carrinho.append(item)
    return {"ok": True, "data": {"item": item, "carrinho": carrinho}, "error": None}


# Cálculos financeiros


def calcular_total(carrinho):

    total = 0

    for item in carrinho:
        total += item["preco"] * item["qtd"]

    return {"ok": True, "data": {"total": total}, "error": None}


def calcular_desconto(total, desconto):

    total_de_desconto = total * (desconto / 100)
    total_com_desconto = total - total_de_desconto
    return {"ok": True, "data": {"total_com_desconto": total_com_desconto}, "error": None}


def aplica_taxa(total, taxa):

    total_com_taxa = total + taxa
    return {"ok": True, "data": {"total_com_taxa": total_com_taxa}, "error": None}


# Orquestração


def total_final(carrinho, desconto, taxa):

    resultado = calcular_total(carrinho)
    total_bruto = resultado["data"]["total"]
    resultado = calcular_desconto(total_bruto, desconto)
    total_com_desconto = resultado["data"]["total_com_desconto"]
    total_final = total_com_desconto + taxa
    return {"ok": True, "data": {"total_final": total_final}, "error": None}

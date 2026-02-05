from simulador.domain.entities import ItemCarrinho, ResultadoCarrinho
from simulador.domain.result import Result

# Buscar


def item_existe_no_carrinho(carrinho: list[ItemCarrinho], indice: int) -> Result[ItemCarrinho | None]:
    for item in carrinho:
        if item.indice == indice:
            return Result(ok=True, data=item)
    return Result(ok=False)


# Validações


def valida_indice_no_estoque(estoque: list[dict], indice: int) -> Result[bool]:
    if 0 <= indice < len(estoque):
        return Result(ok=True)
    return Result(ok=False)


def valida_qtd_atual_carrinho_menor_estoque(qtd_existente_carrinho: int, quantidade: int, qtd_estoque: int) -> Result[bool]:
    if qtd_existente_carrinho + quantidade > qtd_estoque:
        return Result(ok=False)
    return Result(ok=True)


# Mutações do carrinho


def adicionar_item(carrinho: list[ItemCarrinho], estoque: list[dict], indice: int, quantidade: int) -> Result[ResultadoCarrinho]:

    resultado = valida_indice_no_estoque(estoque, indice)
    if not resultado.ok:
        return Result(ok=False, error="indice inexistente") 

    qtd_estoque = estoque[indice]["estoque"]

    if quantidade <= 0:
        return Result(ok=False, error="quantidade indisponível") 

    resultado = item_existe_no_carrinho(carrinho, indice)
    item = resultado.data

    if resultado.ok:
        qtd_existente_carrinho = item.qtd
        resultado = valida_qtd_atual_carrinho_menor_estoque(
            qtd_existente_carrinho, quantidade, qtd_estoque
        )
        if not resultado.ok:
            return Result(ok=False, error="quantidade indisponível")

        item.qtd += quantidade
        return Result(ok=True, data=ResultadoCarrinho(item, carrinho))

    produto = estoque[indice]
    item = ItemCarrinho(
            produto=produto["produto"],
            preco=produto["preco"],
            qtd=quantidade,
            indice=indice
            )
    # nome = produto["produto"]
    # preco = produto["preco"]
    # item = {"produto": nome, "preco": preco, "qtd": quantidade, "indice": indice}
    carrinho.append(item)
    return Result(ok=True, data=ResultadoCarrinho(item, carrinho)) 


def remover_item(carrinho: list[dict], indice: int) -> Result[dict]:

    resultado = item_existe_no_carrinho(carrinho, indice)
    item = resultado.data
    if resultado.ok:
        carrinho.remove(item)
        return Result(ok=True, data=item)
    # {"ok": True, "data": {"item": item}, "error": None}
    return Result(ok=False, error="indice inexistente")
    # {"ok": False, "data": None, "error": "indice inexistente"}


# Cálculos financeiros


def calcular_total(carrinho: list[dict]) -> Result[float]:

    total = 0

    for item in carrinho:
        total += item["preco"] * item["qtd"]

    return Result(ok=True, data=total)

    # {"ok": True, "data": {"total": total}, "error": None}


def calcular_desconto(total: float, desconto: int) -> Result[float]:

    total_de_desconto = total * (desconto / 100)
    total_com_desconto = total - total_de_desconto
    return Result(ok=True, data=total_com_desconto) 
    # {"ok": True, "data": {"total_com_desconto": total_com_desconto}, "error": None}


def aplica_taxa(total: float, taxa: int) -> Result[float]:

    total_com_taxa = total + taxa
    return Result(ok=True, data=total_com_taxa) 
    # {"ok": True, "data": {"total_com_taxa": total_com_taxa}, "error": None}


# Orquestração


def total_final(carrinho: list[dict], desconto: int, taxa: int) -> Result[float]:

    resultado = calcular_total(carrinho)
    total_bruto = resultado.data
    resultado = calcular_desconto(total_bruto, desconto)
    total_com_desconto = resultado.data
    total_final = total_com_desconto + taxa
    return Result(ok=True, data=total_final) 
    # {"ok": True, "data": {"total_final": total_final}, "error": None}

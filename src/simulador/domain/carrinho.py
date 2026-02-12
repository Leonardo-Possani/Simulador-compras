from simulador.domain.entities import ItemCarrinho, ResultadoCarrinho
from simulador.domain.exceptions import IndiceInexistenteError, QuantidadeInvalidaError
# Buscar


def item_existe_no_carrinho(carrinho: list[ItemCarrinho], indice: int) -> ItemCarrinho | None:
    for item in carrinho:
        if item.indice == indice:
            return item
    return None

# Validações

def valida_indice_no_estoque(estoque: list[dict], indice: int) -> None:
    if indice < 0 or indice >= len(estoque):
        raise IndiceInexistenteError()


def valida_qtd_atual_carrinho_menor_estoque(qtd_existente_carrinho: int, quantidade: int, qtd_estoque: int) -> None:
    if qtd_existente_carrinho + quantidade > qtd_estoque:
        raise QuantidadeInvalidaError()


def valida_qtd_negativa_ou_zero_adicionada_no_carrinho(quantidade: int) -> None:
    if quantidade <= 0:
        raise QuantidadeInvalidaError()

# Mutações do carrinho


def adicionar_item(carrinho: list[ItemCarrinho], estoque: list[dict], indice: int, quantidade: int) -> ResultadoCarrinho:

    valida_indice_no_estoque(estoque, indice)

    valida_qtd_negativa_ou_zero_adicionada_no_carrinho(quantidade)

    item = item_existe_no_carrinho(carrinho, indice)

    qtd_estoque = estoque[indice]["estoque"]

    if item:
        qtd_existente_carrinho = item.qtd
        valida_qtd_atual_carrinho_menor_estoque(
            qtd_existente_carrinho, quantidade, qtd_estoque)
        item.qtd += quantidade
        return ResultadoCarrinho(item, carrinho)

    produto = estoque[indice]
    item = ItemCarrinho(
        produto=produto["produto"],
        preco=produto["preco"],
        qtd=quantidade,
        indice=indice
    )
    carrinho.append(item)
    return ResultadoCarrinho(item, carrinho)


def remover_item(carrinho: list[ItemCarrinho], indice: int) -> ResultadoCarrinho:

    item = item_existe_no_carrinho(carrinho, indice)
    if item:
        carrinho.remove(item)
        return ResultadoCarrinho(item, carrinho)

    raise IndiceInexistenteError()


# Cálculos financeiros


def calcular_total(carrinho: list[ItemCarrinho]) -> float:

    total = 0

    for item in carrinho:
        total += item.preco * item.qtd

    return total


def calcular_desconto(total: float, desconto: int) -> float:

    total_de_desconto = total * (desconto / 100)
    total_com_desconto = total - total_de_desconto
    return total_com_desconto


def aplica_taxa(total: float, taxa: int) -> float:
    total_com_taxa = total + taxa
    return total_com_taxa


# Orquestração


def total_final(carrinho: list[ItemCarrinho], desconto: int, taxa: int) -> float:

    total_bruto = calcular_total(carrinho)
    total_com_desconto = calcular_desconto(total_bruto, desconto)
    total_final = total_com_desconto + taxa
    return total_final

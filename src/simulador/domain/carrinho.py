from simulador.domain import estoque as etq

from simulador.domain.entities import ItemCarrinho, Produto, ResultadoCarrinho
from simulador.domain.exceptions import (
    CarrinhoInvalidoError,
    DescontoInvalidoError,
    ProdutoIdInexistenteError,
    QuantidadeInvalidaError,
    TaxaInvalidaError,
)


# Buscar


def item_existe_no_carrinho(carrinho: list[ItemCarrinho], produto_id: int) -> ItemCarrinho | None:
    for item in carrinho:
        if item.produto_id == produto_id:
            return item
    return None


# Validações


def valida_qtd_negativa_ou_zero_adicionada_no_carrinho(quantidade: int) -> None:
    if quantidade <= 0:
        raise QuantidadeInvalidaError()


def nao_permite_produto_id_duplicado_no_carrinho(carrinho: list[ItemCarrinho]) -> None:

    ids = [item.produto_id for item in carrinho]
    if len(ids) != len(set(ids)):
        raise CarrinhoInvalidoError()

# Mutações do carrinho


def adicionar_item(
    carrinho: list[ItemCarrinho], estoque: list[Produto], produto_id: int, quantidade: int
) -> ResultadoCarrinho:

    item = etq.valida_produto_id_retorna_produto_estoque(estoque, produto_id)
    produto = item
    qtd_estoque = item.estoque

    valida_qtd_negativa_ou_zero_adicionada_no_carrinho(quantidade)

    item = item_existe_no_carrinho(carrinho, produto_id)

    if item:
        qtd_existente_carrinho = item.qtd
        etq.valida_qtd_atual_carrinho_menor_estoque(qtd_existente_carrinho, quantidade, qtd_estoque)
        item.qtd += quantidade
        return ResultadoCarrinho(item, carrinho)

    if quantidade > qtd_estoque:
        raise QuantidadeInvalidaError()

    etq.valida_produto_estoque(produto)
    item = ItemCarrinho(
        produto=produto.produto, preco=produto.preco, qtd=quantidade, produto_id=produto_id
    )
    carrinho.append(item)
    return ResultadoCarrinho(item, carrinho)


def remover_item(carrinho: list[ItemCarrinho], produto_id: int) -> ResultadoCarrinho:

    item = item_existe_no_carrinho(carrinho, produto_id)
    if item:
        carrinho.remove(item)
        return ResultadoCarrinho(item, carrinho)

    raise ProdutoIdInexistenteError()


# Cálculos financeiros


def calcular_total(carrinho: list[ItemCarrinho]) -> float:

    total = 0

    for item in carrinho:
        total += item.preco * item.qtd

    return total


def calcular_desconto(total: float, desconto: int) -> float:
    if desconto < 0 or desconto > 100:
        raise DescontoInvalidoError()
    total_de_desconto = total * (desconto / 100)
    total_com_desconto = total - total_de_desconto
    return total_com_desconto


def aplica_taxa(total: float, taxa: int) -> float:
    if taxa < 0:
        raise TaxaInvalidaError()
    total_com_taxa = total + taxa
    return total_com_taxa


# Orquestração


def total_final(carrinho: list[ItemCarrinho], desconto: int, taxa: int) -> float:

    total_bruto = calcular_total(carrinho)
    total_com_desconto = calcular_desconto(total_bruto, desconto)
    total_final = total_com_desconto + taxa
    return total_final

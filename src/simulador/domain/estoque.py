import copy

from simulador.domain.entities import ItemVendido, Produto
from simulador.domain.exceptions import (
    EstoqueInsuficienteError,
    NomeInvalidoError,
    PrecoInvalidoError,
)


def valida_estoque_para_venda(itens_vendidos: tuple[ItemVendido], estoque: list[Produto]) -> bool:

    for item in itens_vendidos:
        indice = item.indice
        qtd = item.qtd
        valida_produto_estoque(estoque[indice])
        if estoque[indice].estoque < qtd:
            raise EstoqueInsuficienteError()
    return True


def valida_produto_estoque(produto: Produto) -> None:

    if not produto.produto:
        raise NomeInvalidoError()
    if produto.preco <= 0:
        raise PrecoInvalidoError()
    if produto.estoque <= 0:
        raise EstoqueInsuficienteError()
    

def venda_concluindo_baixar_estoque(itens_vendidos: list[dict], estoque: list[Produto]) -> list[Produto]:

    estoque_atualizado = copy.deepcopy(estoque)

    for item in itens_vendidos:
        indice = item.indice
        qtd = item.qtd

        estoque_atualizado[indice].estoque -= qtd

    return estoque_atualizado

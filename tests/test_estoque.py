

import pytest


from simulador.domain.entities import Produto
from simulador.domain import estoque as etq
from simulador.domain.exceptions import EstoqueInsuficienteError


def test_valida_estoque_para_venda():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=2),
        Produto(produto="teclado", preco=49.90, estoque=0)
    ]

    itens_vendidos = [
        {"indice": 0, "qtd": 3},
        {"indice": 1, "qtd": 1},
    ]

    with pytest.raises(EstoqueInsuficienteError):
        etq.valida_estoque_para_venda(itens_vendidos, estoque)


def test_venda_concluindo_baixar_estoque():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10),
        Produto(produto="teclado", preco=49.90, estoque=10)
    ]

    itens_vendidos = [
        {"indice": 0, "qtd": 3},
        {"indice": 1, "qtd": 1},
    ]

    resultado = etq.venda_concluindo_baixar_estoque(itens_vendidos, estoque)

    assert len(resultado) == len(estoque)
    assert resultado[0].estoque == 7
    assert resultado[1].estoque == 9
    assert resultado[0].produto == "mouse"
    assert resultado[1].produto == "teclado"

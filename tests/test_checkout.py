
from copy import deepcopy

import pytest

from simulador.application import checkout as chek
from simulador.domain.entities import ItemCarrinho, Produto
from simulador.domain.exceptions import EstoqueInsuficienteError


def test_fluxo_finalizar_venda():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10),
        Produto(produto="teclado", preco=49.90, estoque=10),
    ]

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    resultado = chek.finalizar_venda(carrinho, estoque, desconto=0, taxa=0, pagamento="credito", valor_pago=110)

    assert resultado.estoque_atualizado[0].estoque == 7
    assert resultado.venda.total_final == 110


def test_fluxo_finalizar_venda_erro_estoque_insuficiente():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=2),
        Produto(produto="teclado", preco=49.90, estoque=10),
    ]
    estoque_copia = deepcopy(estoque)

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]
    carrinho_copia = deepcopy(carrinho)
    
    with pytest.raises(EstoqueInsuficienteError):
        chek.finalizar_venda(carrinho_copia, estoque_copia, desconto=0, taxa=0, pagamento="dinheiro", valor_pago=110)


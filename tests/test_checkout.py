from copy import deepcopy

import pytest

from simulador.application import checkout as chek
from simulador.domain import estoque as etq
from simulador.domain.entities import ItemCarrinho, Produto
from simulador.domain.exceptions import (
    CarrinhoInvalidoError,
    EstoqueInsuficienteError,
    MetodoInvalidoError,
)


def test_fluxo_finalizar_venda():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10, produto_id=15),
        Produto(produto="teclado", preco=49.90, estoque=10, produto_id=1),
    ]

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=15),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]

    resultado = chek.finalizar_venda(carrinho, estoque, desconto=0, taxa=0, pagamento="credito", valor_pago=110)
    produto_novo = etq.valida_produto_id_retorna_produto_estoque(resultado.estoque_atualizado, produto_id=15)
    produto_original = etq.valida_produto_id_retorna_produto_estoque(estoque, produto_id=15)

    assert produto_novo.estoque == 7
    assert resultado.venda.total_final == 110
    assert produto_original.estoque == 10
    assert resultado.estoque_atualizado is not estoque
    assert produto_original is not produto_novo


def test_fluxo_finalizar_venda_erro_estoque_insuficiente():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=2, produto_id=36),
        Produto(produto="teclado", preco=49.90, estoque=10, produto_id=1),
    ]
    estoque_copia = deepcopy(estoque)

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=36),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]
    carrinho_copia = deepcopy(carrinho)
    
    with pytest.raises(EstoqueInsuficienteError):
        chek.finalizar_venda(carrinho_copia, estoque_copia, desconto=0, taxa=0, pagamento="dinheiro", valor_pago=110)
    
    assert estoque_copia == estoque
    assert carrinho_copia == carrinho
 

def test_fluxo_finalizar_venda_nao_permite_produto_id_duplicado_no_carrinho():
 
    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10, produto_id=36),
        Produto(produto="teclado", preco=49.90, estoque=10, produto_id=1),
    ]

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=36),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]
    
    with pytest.raises(CarrinhoInvalidoError):
        chek.finalizar_venda(carrinho, estoque, desconto=0, taxa=0, pagamento="dinheiro", valor_pago=110)

    assert estoque[1].estoque == 10


def test_fluxo_finalizar_venda_nao_permite_metodo_pagamento_invalido():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10, produto_id=36),
        Produto(produto="teclado", preco=49.90, estoque=10, produto_id=1),
    ]
    estoque_copia = deepcopy(estoque)

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=36),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]
    carrinho_copia = deepcopy(carrinho)
    
    with pytest.raises(MetodoInvalidoError):
        chek.finalizar_venda(carrinho_copia, estoque_copia, desconto=0, taxa=0, pagamento="pix", valor_pago=110)
    
    assert estoque_copia == estoque
    assert carrinho_copia == carrinho


import pytest

from simulador.domain import estoque as etq
from simulador.domain.entities import ItemVendido, Produto
from simulador.domain.exceptions import (
    EstoqueInsuficienteError,
    NomeInvalidoError,
    PrecoInvalidoError,
)


def test_valida_estoque_para_venda():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10),
        Produto(produto="", preco=20.0, estoque=2),
        Produto(produto="mouse", preco=-10, estoque=2),
        Produto(produto="mouse", preco=10, estoque=-1),
        Produto(produto="mouse", preco=0, estoque=-1),
        Produto(produto="mouse", preco=10, estoque=0),
        Produto(produto="mouse", preco=10, estoque=5)
    ]

    itens_vendidos = (
        ItemVendido(indice=0, qtd=3),
        ItemVendido(indice=1, qtd=1),
        ItemVendido(indice=2, qtd=1),
    )

    itens_vendidos1 = (
        ItemVendido(indice=0, qtd=3),
        ItemVendido(indice=2, qtd=1),
    )

    itens_vendidos2 = (
        ItemVendido(indice=0, qtd=3),
        ItemVendido(indice=3, qtd=1),
    )
    
    itens_vendidos3 = (
        ItemVendido(indice=0, qtd=3),
        ItemVendido(indice=4, qtd=1),
    )
    
    itens_vendidos4 = (
        ItemVendido(indice=0, qtd=3),
        ItemVendido(indice=5, qtd=1),
    )
    itens_vendidos5 = (
        ItemVendido(indice=0, qtd=3),
        ItemVendido(indice=6, qtd=6),
    )   

    with pytest.raises(NomeInvalidoError):
        etq.valida_estoque_para_venda(itens_vendidos, estoque)         

    with pytest.raises(PrecoInvalidoError):
        etq.valida_estoque_para_venda(itens_vendidos1, estoque)         
    
    with pytest.raises(EstoqueInsuficienteError):
        etq.valida_estoque_para_venda(itens_vendidos2, estoque)

    with pytest.raises(PrecoInvalidoError):
        etq.valida_estoque_para_venda(itens_vendidos3, estoque)
        
    with pytest.raises(EstoqueInsuficienteError):
        etq.valida_estoque_para_venda(itens_vendidos4, estoque)
        
    with pytest.raises(EstoqueInsuficienteError):
        etq.valida_estoque_para_venda(itens_vendidos5, estoque)


def test_valida_erros_de_produto_estoque():

    produto1 = Produto(produto="", preco=20.0, estoque=2)
    produto2 = Produto(produto="mouse", preco=-10, estoque=2)
    produto3 = Produto(produto="mouse", preco=10, estoque=-1)
    produto4 = Produto(produto="mouse", preco=0, estoque=-1)
    produto5 = Produto(produto="mouse", preco=10, estoque=0)

    with pytest.raises(NomeInvalidoError):
        etq.valida_produto_estoque(produto1)

    with pytest.raises(PrecoInvalidoError):
        etq.valida_produto_estoque(produto2)

    with pytest.raises(EstoqueInsuficienteError):
        etq.valida_produto_estoque(produto3)

    with pytest.raises(PrecoInvalidoError):
        etq.valida_produto_estoque(produto4)

    with pytest.raises(EstoqueInsuficienteError):
        etq.valida_produto_estoque(produto5)


def test_caminho_feliz_valida_produto_estoque():

    produto = Produto(produto="mouse", preco=20.0, estoque=2)

    assert etq.valida_produto_estoque(produto) is None


def test_venda_concluindo_baixar_estoque():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10),
        Produto(produto="teclado", preco=49.90, estoque=10),
    ]

    itens_vendidos = (
            ItemVendido(indice=0, qtd=3),
            ItemVendido(indice=1, qtd=1)
            )

    resultado = etq.venda_concluindo_baixar_estoque(itens_vendidos, estoque)

    assert len(resultado) == len(estoque)
    assert resultado[0].estoque == 7
    assert resultado[1].estoque == 9
    assert resultado[0].produto == "mouse"
    assert resultado[1].produto == "teclado"

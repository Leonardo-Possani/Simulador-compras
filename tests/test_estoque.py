import pytest

from simulador.domain import estoque as etq
from simulador.domain.entities import ItemVendido, Produto
from simulador.domain.exceptions import (
    EstoqueInsuficienteError,
    ProdutoIdInexistenteError,
    NomeInvalidoError,
    PrecoInvalidoError,
)


def test_valida_indice_no_estoque():

    estoque = [
        Produto(produto="teclado", preco=59.0, estoque=10, produto_id=0),
        Produto(produto="cadeira", preco=990.0, estoque=2, produto_id=51),
        Produto(produto="mouse", preco=25, estoque=2, produto_id=36),
    ]

    with pytest.raises(ProdutoIdInexistenteError):
        etq.valida_produto_id_retorna_produto_estoque(estoque, produto_id=2)

    resultado = etq.valida_produto_id_retorna_produto_estoque(estoque, produto_id=36)

    assert resultado.produto == "mouse"


def test_valida_estoque_para_venda():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10, produto_id=0),
        Produto(produto="", preco=20.0, estoque=2, produto_id=1),
        Produto(produto="mouse", preco=-10, estoque=2, produto_id=2),
        Produto(produto="mouse", preco=10, estoque=-1, produto_id=3),
        Produto(produto="mouse", preco=0, estoque=-1, produto_id=4),
        Produto(produto="mouse", preco=10, estoque=0, produto_id=5),
        Produto(produto="mouse", preco=10, estoque=5, produto_id=6),
    ]

    itens_vendidos = (
        ItemVendido(produto_id=0, qtd=3),
        ItemVendido(produto_id=1, qtd=1),
        ItemVendido(produto_id=2, qtd=1),
    )

    itens_vendidos1 = (
        ItemVendido(produto_id=0, qtd=3),
        ItemVendido(produto_id=2, qtd=1),
    )

    itens_vendidos2 = (
        ItemVendido(produto_id=0, qtd=3),
        ItemVendido(produto_id=3, qtd=1),
    )

    itens_vendidos3 = (
        ItemVendido(produto_id=0, qtd=3),
        ItemVendido(produto_id=4, qtd=1),
    )

    itens_vendidos4 = (
        ItemVendido(produto_id=0, qtd=3),
        ItemVendido(produto_id=5, qtd=1),
    )
    itens_vendidos5 = (
        ItemVendido(produto_id=0, qtd=3),
        ItemVendido(produto_id=6, qtd=6),
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

    produto1 = Produto(produto="", preco=20.0, estoque=2, produto_id=0)
    produto2 = Produto(produto="mouse", preco=-10, estoque=2, produto_id=0)
    produto3 = Produto(produto="mouse", preco=10, estoque=-1, produto_id=0)
    produto4 = Produto(produto="mouse", preco=0, estoque=-1, produto_id=0)
    produto5 = Produto(produto="mouse", preco=10, estoque=0, produto_id=0)

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

    produto = Produto(produto="mouse", preco=20.0, estoque=2, produto_id=0)

    assert etq.valida_produto_estoque(produto) is None


def test_venda_concluindo_baixar_estoque():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10, produto_id=0),
        Produto(produto="teclado", preco=49.90, estoque=10, produto_id=1),
    ]

    itens_vendidos = (ItemVendido(produto_id=0, qtd=3), ItemVendido(produto_id=1, qtd=1))

    resultado = etq.venda_concluindo_baixar_estoque(itens_vendidos, estoque)

    produto0 = etq.valida_produto_id_retorna_produto_estoque(resultado, produto_id=0)
    produto1 = etq.valida_produto_id_retorna_produto_estoque(resultado, produto_id=1)

    assert produto0.estoque == 7
    assert produto1.estoque == 9
    assert produto0.produto == "mouse"
    assert produto1.produto == "teclado"
    assert estoque is not resultado


def test_baixar_qtd_do_estoque():

    estoque = [
        Produto(produto="mouse", preco=20.0, estoque=10, produto_id=87),
        Produto(produto="teclado", preco=25.0, estoque=10, produto_id=18),
        Produto(produto="cadeira", preco=990.99, estoque=10, produto_id=48),
    ]

    resultado_novo_estoque = etq.baixar_qtd_do_estoque(estoque, produto_id=48, qtd=5)

    produto_novo = etq.valida_produto_id_retorna_produto_estoque(
        resultado_novo_estoque, produto_id=48
    )
    produto_original = etq.valida_produto_id_retorna_produto_estoque(estoque, produto_id=48)

    assert produto_novo.estoque == 5
    assert produto_original.estoque == 10
    assert produto_original is not produto_novo

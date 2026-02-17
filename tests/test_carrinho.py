import pytest


from simulador.domain.exceptions import (
    DescontoInvalidoError,
    IndiceInexistenteError,
    QuantidadeInvalidaError,
    TaxaInvalidaError,
)
from simulador.domain import carrinho as carr
from simulador.domain.entities import ItemCarrinho


def test_adicionar_item_valido():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []
    resultado = carr.adicionar_item(carrinho, estoque, 0, 3)

    item = resultado.item
    assert item.produto == "mouse"
    assert item.preco == 20.0
    assert item.qtd == 3
    assert item.indice == 0

    assert len(resultado.carrinho) == 1


def test_adicionar_mesmo_item_soma_quantidade():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
    ]

    resultado = carr.adicionar_item(carrinho, estoque, 0, 2)

    assert resultado.item.qtd == 5
    assert len(resultado.carrinho) == 1


def test_nao_permite_quantidade_menor_ou_igual_zero():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []

    with pytest.raises(QuantidadeInvalidaError):
        carr.adicionar_item(carrinho, estoque, 0, 0)


def test_nao_permite_adicionar_qtd_maior_que_estoque():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 5}]
    carrinho = []

    with pytest.raises(QuantidadeInvalidaError):
        carr.adicionar_item(carrinho, estoque, 0, 6)


def test_nao_permite_quantidade_maior_que_estoque():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 5}]
    carrinho = [
        ItemCarrinho(produto="nouse", preco=20.0, qtd=3, indice=0),
    ]

    with pytest.raises(QuantidadeInvalidaError):
        carr.adicionar_item(carrinho, estoque, 0, 3)


def test_nao_permite_indice_invalido():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []
    with pytest.raises(IndiceInexistenteError):
        carr.adicionar_item(carrinho, estoque, -1, 1)


def test_remove_item_do_carrinho():
    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    resultado = carr.remover_item(carrinho, 0)

    assert resultado.item.produto == "mouse"
    assert len(carrinho) == 1
    assert carrinho[0].produto == "teclado"


def test_nao_remove_item_inexistente_do_carrinho():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]
    with pytest.raises(IndiceInexistenteError):
        carr.remover_item(carrinho, 2)


def test_remove_item_com_ordem_diferente_do_indice():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    resultado = carr.remover_item(carrinho, 0)

    assert resultado.item.produto == "mouse"
    assert len(carrinho) == 1
    assert carrinho[0].produto == "teclado"


def test_calcular_total_bruto_do_carrinho():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=2, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]
    resultado = carr.calcular_total(carrinho)
    assert resultado == 90.0


def test_calcular_carrinho_vazio():

    carrinho = []

    resultado = carr.calcular_total(carrinho)

    assert resultado == 0


def test_aplicar_desconto_no_carrinho():

    resultado = carr.calcular_desconto(100, 17)

    assert resultado == 83.0


def test_tratar_desconto_zero():

    resultado = carr.calcular_desconto(100, 0)

    assert resultado == 100


def test_nao_permite_desconto_negativo():

    with pytest.raises(DescontoInvalidoError):
        carr.calcular_desconto(100, -15)


def test_nao_permite_desconto_maior_cem():

    with pytest.raises(DescontoInvalidoError):
        carr.calcular_desconto(100, 101)


def test_aplica_taxa_no_valor_final():

    resultado = carr.aplica_taxa(100, 35)

    assert resultado == 135


def test_taxa_zero_nao_deve_alterar_total():

    resultado = carr.aplica_taxa(100, 0)

    assert resultado == 100


def test_nao_permite_taxa_negativa():

    with pytest.raises(TaxaInvalidaError):
        carr.aplica_taxa(100, -15)


def test_total_final_menos_descontos_mais_taxas():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=2, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    resultado = carr.total_final(carrinho, 5, 8)

    assert resultado == 93.5


def test_validar_total_sem_descomtos_sem_taxa():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    resultado = carr.total_final(carrinho, 0, 0)

    assert resultado == 110

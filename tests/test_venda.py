import pytest

from simulador.domain import venda as vd
from simulador.domain.entities import ItemCarrinho, Venda
from simulador.domain.exceptions import (
    CarrinhoInvalidoError,
    DinheiroInsuficienteError,
    ValorIncorretoError,
)


def test_nao_permite_fechar_venda_com_carrinho_vazio():

    carrinho = []
    with pytest.raises(CarrinhoInvalidoError):
        vd.fechar_venda_com_carrinho_valido(carrinho)


def test_fechar_venda_com_carrinho_valido():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)

    assert resultado.itens == carrinho


def test_venda_calcula_total():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)

    assert resultado.total == 110


def test_venda_com_desconto():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    venda = Venda(itens=carrinho, total=110)

    resultado = vd.aplicar_desconto(venda, 10)

    assert resultado.total_com_desconto == 99


def test_aplicar_taxa_na_venda():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99)

    resultado = vd.aplicar_taxa_venda(venda, 15)

    assert resultado.total_final == 114


def test_registrar_pagamento_venda():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99, total_final=114)

    resultado = vd.registrar_pagamento(venda, "credito")

    assert resultado.pagamento == "credito"


def test_pagamento_em_dinheiro_calcula_troca():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="dinheiro"
    )

    resultado = vd.venda_paga_no_dinheiro(venda, valor_pago=120)

    assert resultado.troco == 6


def test_pagamento_em_dinheiro_menor_que_total_final():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="dinheiro"
    )

    with pytest.raises(DinheiroInsuficienteError):
        vd.venda_paga_no_dinheiro(venda, valor_pago=100)


def test_dinheiro_exato():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="dinheiro"
    )

    resultado = vd.venda_paga_no_dinheiro(venda, valor_pago=114)

    assert resultado.troco is None


def test_pagamento_debito():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="debito"
    )

    resultado = vd.venda_paga_no_debito(venda, valor_pago=114)

    assert resultado.total_final == resultado.valor_pago


def test_pagamento_debito_valor_pago_incorreto():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="debito"
    )

    with pytest.raises(ValorIncorretoError):
        vd.venda_paga_no_debito(venda, valor_pago=110)


def test_pagamento_em_credido_a_vista():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="credito"
    )

    resultado = vd.venda_paga_no_credito(venda, valor_pago=114)

    assert resultado.total_final == resultado.valor_pago


def test_credito_com_valor_incorreto():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="credito"
    )
    with pytest.raises(ValorIncorretoError):
        vd.venda_paga_no_credito(venda, valor_pago=100)


def test_processar_pagamento():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="credito"
    )

    resultado = vd.processar_pagamento(venda, valor_pago=114)

    assert resultado.total_final == resultado.valor_pago


def test_extrair_itens_vendidos():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, indice=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, indice=1),
    ]

    venda = Venda(
        itens=carrinho,
        total=110,
        total_com_desconto=99,
        total_final=114,
        pagamento="credito",
        valor_pago=114,
    )

    resultado = vd.extrair_itens_vendidos(venda)

    assert len(resultado) == 2
    assert resultado[0]["indice"] == 0
    assert resultado[1]["indice"] == 1
    assert resultado[0]["qtd"] == 3
    assert resultado[1]["qtd"] == 1

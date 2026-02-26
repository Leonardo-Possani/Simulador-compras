from dataclasses import FrozenInstanceError
import pytest

from simulador.domain import venda as vd
from simulador.domain.types import MetodoPagamento
from simulador.domain.entities import ItemCarrinho, Venda, ItemVendaFechada
from simulador.domain.exceptions import (
    CarrinhoInvalidoError,
    DescontoInvalidoError,
    DinheiroInsuficienteError,
    MetodoInvalidoError,
    SequenciaVendaInvalidaError,
    TaxaInvalidaError,
    ValorIncorretoError,
)


def test_nao_permite_fechar_venda_com_carrinho_vazio():

    carrinho = []
    with pytest.raises(CarrinhoInvalidoError):
        vd.fechar_venda_com_carrinho_valido(carrinho)


def test_fechar_venda_com_carrinho_valido():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]

    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)

    assert isinstance(resultado.itens, tuple)
    assert resultado.itens[0] is not carrinho[0]


def test_fechar_venda_garante_imutabilidade_do_carrinho():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]

    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)
    carrinho[0].qtd = 99
    assert resultado.itens[0].qtd == 3


def test_fechar_venda_nao_permite_mutar_resultado_itens():
    
    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]

    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)
    
    with pytest.raises(TypeError):
        resultado.itens[0] = ItemCarrinho(produto="bolsa", preco=10.0, qtd=8, produto_id=3)


def test_fechar_venda_nao_permite_editar_item_do_carrinho():
    
    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]
    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)
    
    with pytest.raises(FrozenInstanceError):
        resultado.itens[0].qtd = 1


def test_venda_calcula_total():

    carrinho = [
        ItemCarrinho(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemCarrinho(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    ]

    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)

    assert resultado.total == 110


def test_venda_com_desconto():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110)

    resultado = vd.aplicar_desconto(venda, 10)

    assert resultado.total_com_desconto == 99


def test_venda_nao_permite_desconto_negativo():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110)

    with pytest.raises(DescontoInvalidoError):
        vd.aplicar_desconto(venda, -15)


def test_venda_nao_permite_desconto_maior_que_cem():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )
    venda = Venda(itens=carrinho, total=110)

    with pytest.raises(DescontoInvalidoError):
        vd.aplicar_desconto(venda, 110)


def test_venda_valida_total_com_desconto_calculado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )
    venda = Venda(itens=carrinho, total=110)

    with pytest.raises(SequenciaVendaInvalidaError):
        vd.valida_total_com_desconto_calculado(venda)


def test_aplicar_taxa_so_roda_se_tiver_total_com_desconto_calculado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(
        itens=carrinho,
        total=110,
    )

    with pytest.raises(SequenciaVendaInvalidaError):
        vd.aplicar_taxa_venda(venda, 15)


def test_aplicar_taxa_na_venda():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99)

    resultado = vd.aplicar_taxa_venda(venda, 15)

    assert resultado.total_final == 114


def test_venda_nao_permite_taxa_negativa():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99)
    with pytest.raises(TaxaInvalidaError):
        vd.aplicar_taxa_venda(venda, -15)


def test_venda_valida_total_final_calculado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99)

    with pytest.raises(SequenciaVendaInvalidaError):
        vd.valida_total_final_calculado(venda)


def test_venda_so_registra_pagamento_se_tiver_total_final_calculado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )  

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99)

    with pytest.raises(SequenciaVendaInvalidaError):
        vd.registrar_pagamento(venda, MetodoPagamento.DEBITO)


def test_registrar_pagamento_venda():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99, total_final=114)

    resultado = vd.registrar_pagamento(venda, MetodoPagamento.CREDITO)

    assert resultado.pagamento == MetodoPagamento.CREDITO
    assert isinstance(resultado.pagamento, MetodoPagamento)


def test_valida_metodo_de_pagamento():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99, total_final=114)

    with pytest.raises(MetodoInvalidoError):
        vd.registrar_pagamento(venda, "pix")


def test_venda_em_dinheiro_valida_total_final_calculado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99)

    with pytest.raises(SequenciaVendaInvalidaError):
        vd.venda_paga_no_dinheiro(venda, valor_pago=114)


def test_pagamento_em_dinheiro_calcula_troca():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento=MetodoPagamento.DINHEIRO
    )

    resultado = vd.venda_paga_no_dinheiro(venda, valor_pago=120)

    assert resultado.troco == 6


def test_pagamento_em_dinheiro_menor_que_total_final():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento=MetodoPagamento.DINHEIRO
    )

    with pytest.raises(DinheiroInsuficienteError):
        vd.venda_paga_no_dinheiro(venda, valor_pago=100)


def test_dinheiro_exato():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento=MetodoPagamento.DINHEIRO
    )

    resultado = vd.venda_paga_no_dinheiro(venda, valor_pago=114)

    assert resultado.troco is None


def test_venda_em_debito_valida_total_final_calculado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99)

    with pytest.raises(SequenciaVendaInvalidaError):
        vd.venda_paga_no_debito(venda, valor_pago=114)


def test_pagamento_debito():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento=MetodoPagamento.DEBITO
    )

    resultado = vd.venda_paga_no_debito(venda, valor_pago=114)

    assert resultado.total_final == resultado.valor_pago


def test_pagamento_debito_valor_pago_incorreto():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento=MetodoPagamento.DEBITO
    )

    with pytest.raises(ValorIncorretoError):
        vd.venda_paga_no_debito(venda, valor_pago=110)


def test_venda_em_credito_valida_total_final_calculado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99)

    with pytest.raises(SequenciaVendaInvalidaError):
        vd.venda_paga_no_credito(venda, valor_pago=114)


def test_pagamento_em_credido_a_vista():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento=MetodoPagamento.CREDITO
    )

    resultado = vd.venda_paga_no_credito(venda, valor_pago=114)

    assert resultado.total_final == resultado.valor_pago


def test_credito_com_valor_incorreto():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )
    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento=MetodoPagamento.CREDITO
    )
    with pytest.raises(ValorIncorretoError):
        vd.venda_paga_no_credito(venda, valor_pago=100)


def test_processar_pagamento():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento=MetodoPagamento.CREDITO
    )

    resultado = vd.processar_pagamento(venda, valor_pago=114)

    assert resultado.total_final == resultado.valor_pago


def test_processar_pagamento_valida_metodo_de_pagamento_criado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99, total_final=114)

    with pytest.raises(SequenciaVendaInvalidaError):
        vd.processar_pagamento(venda, valor_pago=114)


def test_processar_pagamento_nao_permite_metodo_invalido():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(
        itens=carrinho, total=110, total_com_desconto=99, total_final=114, pagamento="Pix"
    )
    with pytest.raises(MetodoInvalidoError):
        vd.processar_pagamento(venda, valor_pago=114)


def test_processar_pagamento_valida_total_final_calculado():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(itens=carrinho, total=110, total_com_desconto=99, pagamento=MetodoPagamento.DINHEIRO)
    with pytest.raises(SequenciaVendaInvalidaError):
        vd.processar_pagamento(venda, valor_pago=114)


def test_extrair_itens_vendidos():

    carrinho = (
        ItemVendaFechada(produto="mouse", preco=20.0, qtd=3, produto_id=0),
        ItemVendaFechada(produto="teclado", preco=50.0, qtd=1, produto_id=1),
    )

    venda = Venda(
        itens=carrinho,
        total=110,
        total_com_desconto=99,
        total_final=114,
        pagamento=MetodoPagamento.CREDITO,
        valor_pago=114,
    )

    resultado = vd.extrair_itens_vendidos(venda)

    assert len(resultado) == 2
    assert resultado[0].produto_id == 0
    assert resultado[1].produto_id == 1
    assert resultado[0].qtd == 3
    assert resultado[1].qtd == 1

from simulador.domain import venda as vd


def test_nao_permite_fechar_venda_com_carrinho_vazio():

    carrinho = []

    venda, erro = vd.fechar_venda(carrinho)

    assert venda is None
    assert erro is not None


def test_fechar_venda_com_carrinho_valido():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda, erro = vd.fechar_venda(carrinho)

    assert venda is not None
    assert erro is None
    assert venda["itens"] == carrinho


def test_venda_calcula_total():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda, erro = vd.fechar_venda(carrinho)

    assert erro is None
    assert venda["total"] == 110


def test_venda_com_desconto():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {"itens": carrinho, "total": 110}

    venda_com_desconto, erro = vd.aplicar_desconto(venda, 10)

    assert venda_com_desconto["total_com_desconto"] == 99
    assert erro is None


def test_aplicar_taxa_na_venda():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {"itens": carrinho, "total": 110, "total_com_desconto": 99}

    nova_venda_com_taxa, erro = vd.aplicar_taxa_venda(venda, 15)

    assert erro is None
    assert nova_venda_com_taxa["total_final"] == 114


def test_registrar_pagamento_venda():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {"itens": carrinho, "total": 110, "total_com_desconto": 99, "total_final": 114}

    venda_paga, erro = vd.registrar_pagamento(venda, "credito")

    assert erro is None
    assert venda_paga["pagamento"] == "credito"


def test_pagamento_em_dinheiro_calcula_troca():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "dinheiro",
    }

    venda_com_troco, erro = vd.venda_paga_no_dinheiro(venda, valor_pago=120)

    assert venda_com_troco["troco"] == 6
    assert erro is None


def test_pagamento_em_dinheiro_menor_que_total_final():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "dinheiro",
    }

    venda_com_erro, erro = vd.venda_paga_no_dinheiro(venda, valor_pago=100)

    assert venda_com_erro is None
    assert erro is not None


def test_dinheiro_exato():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "dinheiro",
    }

    venda_paga, erro = vd.venda_paga_no_dinheiro(venda, valor_pago=114)

    assert erro is None
    assert "troco" not in venda_paga


def test_pagamento_debito():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "debito",
    }

    venda_debito, erro = vd.venda_paga_no_debito(venda, valor_pago=114)

    assert erro is None
    assert venda_debito["total_final"] == venda_debito["valor_pago"]


def test_pagamento_debito_valor_pago_incorreto():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "debito",
    }

    venda_debito_com_erro, erro = vd.venda_paga_no_debito(venda, valor_pago=110)

    assert erro is not None
    assert venda_debito_com_erro is None


def test_pagamento_em_cretido_a_vista():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "credito",
    }

    venda_credito, erro = vd.venda_paga_no_credito(venda, valor_pago=114)

    assert erro is None
    assert venda_credito["total_final"] == venda_credito["valor_pago"]


def test_credito_com_valor_incorreto():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "credito",
    }

    venda_com_erro, erro = vd.venda_paga_no_credito(venda, valor_pago=100)

    assert erro is not None
    assert venda_com_erro is None


def test_processar_pagamento():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "credito",
    }

    venda_processada, erro = vd.processar_pagamento(venda, valor_pago=114)

    assert erro is None
    assert venda_processada["total_final"] == venda_processada["valor_pago"]

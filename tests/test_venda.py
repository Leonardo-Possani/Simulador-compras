from simulador.domain import venda as vd


def test_nao_permite_fechar_venda_com_carrinho_vazio():

    carrinho = []

    resultado = vd.fechar_venda(carrinho)

    assert resultado["ok"] is False
    assert resultado["error"] == "carrinho vazio"
    # assert venda is None
    # assert erro is not None


def test_fechar_venda_com_carrinho_valido():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    resultado = vd.fechar_venda(carrinho)

    assert resultado["ok"] is True
    assert resultado["error"] is None
    assert resultado["data"]["venda"]["itens"] == carrinho

    # assert venda is not None
    # assert erro is None
    # assert venda["itens"] == carrinho


def test_venda_calcula_total():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    resultado = vd.fechar_venda(carrinho)

    assert resultado["ok"] is True
    assert resultado["error"] is None
    assert resultado["data"]["venda"]["total"] == 110

    # assert erro is None
    # assert venda["total"] == 110


def test_venda_com_desconto():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {"itens": carrinho, "total": 110}

    resultado = vd.aplicar_desconto(venda, 10)

    assert resultado["ok"] is True
    assert resultado["data"]["venda"]["total_com_desconto"] == 99
    assert resultado["error"] is None

    # assert venda_com_desconto["total_com_desconto"] == 99
    # assert erro is None


def test_aplicar_taxa_na_venda():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {"itens": carrinho, "total": 110, "total_com_desconto": 99}

    resultado = vd.aplicar_taxa_venda(venda, 15)
    
    assert resultado["ok"] is True
    assert resultado["error"] is None
    assert resultado["data"]["venda"]["total_final"] == 114

    # assert erro is None
    # assert nova_venda_com_taxa["total_final"] == 114


def test_registrar_pagamento_venda():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    venda = {"itens": carrinho, "total": 110, "total_com_desconto": 99, "total_final": 114}

    resultado = vd.registrar_pagamento(venda, "credito")

    assert resultado["ok"] is True
    assert resultado["error"] is None
    assert resultado["data"]["venda"]["pagamento"] == "credito"

    # assert erro is None
    # assert venda_paga["pagamento"] == "credito"


def test_pagamento_em_dinheiro_calcula_troca():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1}
    ]

    venda = {
        "itens": carrinho,
        "total": 110,
        "total_com_desconto": 99,
        "total_final": 114,
        "pagamento": "dinheiro",
    }

    resultado = vd.venda_paga_no_dinheiro(venda, valor_pago=120)

    assert resultado["ok"] is True
    assert resultado["data"]["venda"]["troco"] == 6
    assert resultado["error"] is None
    # assert venda_com_troco["troco"] == 6
    # assert erro is None


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

    resultado = vd.venda_paga_no_dinheiro(venda, valor_pago=100)

    assert resultado["ok"] is False
    assert resultado["data"] is None
    assert resultado["error"] == "dinheiro insuficiente"

    # assert venda_com_erro is None
    # assert erro is not None


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

    resultado = vd.venda_paga_no_dinheiro(venda, valor_pago=114)
    
    assert resultado["ok"] is True
    assert resultado["error"] is None
    assert "troco" not in resultado["data"]["venda"]

    # assert erro is None
    # assert "troco" not in venda_paga


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

    resultado = vd.venda_paga_no_debito(venda, valor_pago=114)
    
    assert resultado["ok"] is True
    assert resultado["error"] is None
    assert resultado["data"]["venda"]["total_final"] == resultado["data"]["venda"]["valor_pago"]

    # assert erro is None
    # assert venda_debito["total_final"] == venda_debito["valor_pago"]


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

    resultado = vd.venda_paga_no_debito(venda, valor_pago=110)
    
    assert resultado["ok"] is False
    assert resultado["data"] is None
    assert resultado["error"] == "valor incorreto"

    # assert erro is not None
    # assert venda_debito_com_erro is None


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

    resultado = vd.venda_paga_no_credito(venda, valor_pago=114)

    assert resultado["ok"] is True
    assert resultado["data"]["venda"]["total_final"] == resultado["data"]["venda"]["valor_pago"]
    assert resultado["error"] is None

    # assert erro is None
    # assert venda_credito["total_final"] == venda_credito["valor_pago"]


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

    resultado = vd.venda_paga_no_credito(venda, valor_pago=100)

    assert resultado["ok"] is False
    assert resultado["data"] is None
    assert resultado["error"] == "valor incorreto"

    # assert erro is not None
    # assert venda_com_erro is None


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

    resultado = vd.processar_pagamento(venda, valor_pago=114)
    
    assert resultado["ok"] is True
    assert resultado["data"]["venda"]["total_final"] == resultado["data"]["venda"]["valor_pago"]
    assert resultado["error"] is None

    # assert erro is None
    # assert venda_processada["total_final"] == venda_processada["valor_pago"]


def test_extrair_itens_vendidos():

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
        "valor_pago": 114
    }

    resultado = vd.extrair_itens_vendidos(venda)

    assert resultado["ok"] is True
    assert resultado["error"] is None
    assert len(resultado["data"]["itens_vendidos"]) == 2
    assert resultado["data"]["itens_vendidos"][0]["indice"] == 0
    assert resultado["data"]["itens_vendidos"][1]["indice"] == 1
    assert resultado["data"]["itens_vendidos"][0]["qtd"] == 3
    assert resultado["data"]["itens_vendidos"][1]["qtd"] == 1

    # assert erro is None
    # assert len(itens_vendidos) == 2
    # assert itens_vendidos[0]["indice"] == 0
    # assert itens_vendidos[1]["indice"] == 1
    # assert itens_vendidos[0]["qtd"] == 3
    # assert itens_vendidos[1]["qtd"] == 1




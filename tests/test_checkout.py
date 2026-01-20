from copy import deepcopy

from simulador.application import checkout as chek


def test_fluxo_finalizar_venda():

    estoque = [
        {"produto": "mouse", "preco": 20.0, "estoque": 10},
        {"produto": "teclado", "preco": 49.90, "estoque": 10},
    ]

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    resultado = chek.finalizar_venda(carrinho, estoque, desconto=0, taxa=0, pagamento="credito", valor_pago=110)

    assert resultado["ok"] is True
    assert resultado["data"]["estoque"][0]["estoque"] == 7
    assert resultado["data"]["venda"]["total_final"] == 110
    assert resultado["error"] is None


def test_fluxo_finalizar_venda_erro_estoque_insuficiente():

    estoque = [
        {"produto": "mouse", "preco": 20.0, "estoque": 2},
        {"produto": "teclado", "preco": 49.90, "estoque": 10},
    ]
    estoque_copia = deepcopy(estoque)

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]
    carrinho_copia = deepcopy(carrinho)

    resultado = chek.finalizar_venda(carrinho_copia, estoque_copia, desconto=0, taxa=0, pagamento="dinheiro", valor_pago=110)

    assert resultado["ok"] is False
    assert resultado["error"] == "estoque insuficiente"
    assert estoque == estoque_copia
    assert carrinho == carrinho_copia

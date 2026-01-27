from simulador.domain import estoque as etq


def test_valida_estoque_para_venda():

    estoque = [
        {"produto": "mouse", "preco": 20.0, "estoque": 2},
        {"produto": "teclado", "preco": 49.90, "estoque": 10},
    ]

    itens_vendidos = [
        {"indice": 0, "qtd": 3},
        {"indice": 1, "qtd": 1},
    ]

    resultado = etq.valida_estoque_para_venda(itens_vendidos, estoque)

    assert resultado["ok"] is False
    assert resultado["data"] is None
    assert resultado["error"] == "estoque insuficiente"

   
def test_venda_concluindo_baixar_estoque():

    estoque = [
        {"produto": "mouse", "preco": 20.0, "estoque": 10},
        {"produto": "teclado", "preco": 49.90, "estoque": 10},
    ]

    itens_vendidos = [
        {"indice": 0, "qtd": 3},
        {"indice": 1, "qtd": 1},
    ]

    resultado = etq.venda_concluindo_baixar_estoque(itens_vendidos, estoque)

    assert resultado["ok"] is True
    assert len(resultado["data"]["estoque_atualizado"]) == len(estoque)
    assert resultado["data"]["estoque_atualizado"][0]["estoque"] == 7
    assert resultado["data"]["estoque_atualizado"][1]["estoque"] == 9
    assert resultado["data"]["estoque_atualizado"][0]["produto"] == "mouse"
    assert resultado["data"]["estoque_atualizado"][1]["produto"] == "teclado"
    assert resultado["error"] is None


    

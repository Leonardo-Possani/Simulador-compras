from simulador.domain import estoque as etq


def test_venda_concluida_baixar_estoque():

    estoque = [
            {"produto": "mouse", "preco": 20.0, "estoque": 10},
            {"produto": "teclado", "preco": 49.90, "estoque": 10},
    ]

    itens_vendidos = [
        {"indice": 0, "qtd": 3},
        {"indice": 1, "qtd": 1},
    ]

    estoque_atualizado, erro = etq.venda_concluida_baixar_estoque(itens_vendidos, estoque)

    assert erro is None
    assert len(estoque_atualizado) == len(estoque)
    assert estoque_atualizado[0]["estoque"] == 7
    assert estoque_atualizado[1]["estoque"] == 9
    assert estoque_atualizado[0]["produto"] == "mouse"
    assert estoque_atualizado[1]["produto"] == "teclado"
    

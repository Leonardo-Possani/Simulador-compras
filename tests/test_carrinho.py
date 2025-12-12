from simulador.domain import carrinho as carr


def test_adicionar_item_valido():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]

    item, erro = carr.adicionar_item(estoque, 0, 3)

    assert item is not None
    assert erro is None
    assert item["produto"] == "mouse"
    assert item["preco"] == 20.0
    assert item["qtd"] == 3
    assert item["indice"] == 0 

def test_adicionar_mesmo_item_soma_quantidade():
    
    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = [{"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0}]

    item, erro, novo_carrinho = carr.adicionar_item(carrinho, estoque, 0, 2)

    assert erro is None
    assert item["qtd"] == 5
    assert len(novo_carrinho) == 1


from simulador.domain import carrinho as carr


def test_adicionar_item_valido():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []
    item, erro, novo_carrinho = carr.adicionar_item(carrinho, estoque, 0, 3)

    assert item is not None
    assert erro is None
    assert item["produto"] == "mouse"
    assert item["preco"] == 20.0
    assert item["qtd"] == 3
    assert item["indice"] == 0 
    assert novo_carrinho == carrinho


def test_adicionar_mesmo_item_soma_quantidade():
    
    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = [{"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0}]

    item, erro, novo_carrinho = carr.adicionar_item(carrinho, estoque, 0, 2)

    assert erro is None
    assert item["qtd"] == 5
    assert len(novo_carrinho) == 1


def test_nao_permite_quantidade_menor_ou_igual_zero():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []

    item, erro, novo_carrinho = carr.adicionar_item(carrinho, estoque, 0, 0)

    assert item is None
    assert erro is not None
    assert novo_carrinho == carrinho


def test_nao_permite_quantidade_maior_que_estoque():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 5}]
    carrinho = [{"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0}]

    item, erro, novo_carrinho = carr.adicionar_item(carrinho, estoque, 0, 3)

    assert item is None
    assert erro is not None
    assert novo_carrinho == carrinho
    

def test_nao_permite_indice_invalido():
    
    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []
    
    item, erro, novo_carrinho = carr.adicionar_item(carrinho, estoque, -1, 1)

    assert item is None
    assert erro is not None
    assert novo_carrinho == carrinho 


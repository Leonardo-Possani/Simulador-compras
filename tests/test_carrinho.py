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


def test_remove_item_do_carrinho():
    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    item, erro, novo_carrinho = carr.remover_item(carrinho, 0)

    assert erro is None
    assert item["produto"] == "mouse"
    assert len(novo_carrinho) == 1
    assert novo_carrinho[0]["produto"] == "teclado"


def test_nao_remove_item_inexistente_do_carrinho():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    item, erro, novo_carrinho = carr.remover_item(carrinho, 2)

    assert item is None
    assert erro is not None
    assert novo_carrinho == carrinho


def test_temove_item_com_ordem_diferente_do_indice():

    carrinho = [
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
    ]
    
    item, erro, novo_carrinho = carr.remover_item(carrinho, 0)

    assert erro is None
    assert item["produto"] == "mouse"
    assert len(novo_carrinho) == 1
    assert novo_carrinho[0]["produto"] == "teclado"


def test_calcular_total_bruto_do_carrinho():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 2, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    total = carr.calcular_total(carrinho)
    
    assert total == 90.0


def test_calcular_carrinho_vazio():
    
    carrinho = []

    total = carr.calcular_total(carrinho)

    assert total == 0


def test_aplicar_desconto_no_carrinho():

    total_com_desconto = carr.calcular_desconto(100, 17)

    assert total_com_desconto == 83.0


def test_tratar_desconto_zero():

    total_com_desconto = carr.calcular_desconto(100, 0)

    assert total_com_desconto == 100


def test_aplica_taxa_no_valor_final():

    total_com_taxa = carr.aplica_taxa(100, 35)

    assert total_com_taxa == 135


def test_taxa_zero_nao_deve_alterar_total():

    total_com_taxa = carr.aplica_taxa(100, 0)

    assert total_com_taxa == 100


def test_total_final_menos_descontos_mais_taxas():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 2, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    total_final = carr.total_final(carrinho, 5, 8)

    assert total_final == 93.5


def test_validar_total_sem_descomtos_sem_taxa():
    
    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    total_final = carr.total_final(carrinho, 0, 0)

    assert total_final == 110

    



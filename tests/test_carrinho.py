from simulador.domain import carrinho as carr


def test_adicionar_item_valido():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []
    resultado = carr.adicionar_item(carrinho, estoque, 0, 3)

    assert resultado.ok is True
    assert resultado.data["item"] is not None
    assert resultado.error is None
    assert resultado.data["item"]["produto"] == "mouse"
    assert resultado.data["item"]["preco"] == 20.0
    assert resultado.data["item"]["qtd"] == 3
    assert resultado.data["item"]["indice"] == 0
    assert resultado.data["carrinho"][0]["produto"] == "mouse"
    assert len(carrinho) == 1


def test_adicionar_mesmo_item_soma_quantidade():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = [{"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0}]

    resultado = carr.adicionar_item(carrinho, estoque, 0, 2)

    assert resultado.ok is True
    assert resultado.error is None
    assert resultado.data["item"]["qtd"] == 5
    assert len(resultado.data["carrinho"]) == 1


def test_nao_permite_quantidade_menor_ou_igual_zero():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []

    resultado = carr.adicionar_item(carrinho, estoque, 0, 0)

    assert resultado.ok is False
    assert resultado.data is None
    assert resultado.error == "quantidade indisponível"
    assert len(carrinho) == 0


def test_nao_permite_quantidade_maior_que_estoque():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 5}]
    carrinho = [{"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0}]

    resultado = carr.adicionar_item(carrinho, estoque, 0, 3)

    assert resultado.ok is False
    assert resultado.data is None
    assert carrinho == carrinho
    assert resultado.error == "quantidade indisponível"


def test_nao_permite_indice_invalido():

    estoque = [{"produto": "mouse", "preco": 20.0, "estoque": 10}]
    carrinho = []

    resultado = carr.adicionar_item(carrinho, estoque, -1, 1)

    assert resultado.ok is False
    assert resultado.data is None
    assert resultado.error == "indice inexistente"
    assert carrinho == carrinho


def test_remove_item_do_carrinho():
    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    resultado = carr.remover_item(carrinho, 0)

    assert resultado.ok is True
    assert resultado.data["produto"] == "mouse"
    assert len(carrinho) == 1
    assert carrinho[0]["produto"] == "teclado"


def test_nao_remove_item_inexistente_do_carrinho():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    resultado = carr.remover_item(carrinho, 2)

    assert resultado.ok is False
    assert resultado.data is None
    assert carrinho == carrinho
    assert resultado.error == "indice inexistente"


def test_remove_item_com_ordem_diferente_do_indice():

    carrinho = [
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
    ]

    resultado = carr.remover_item(carrinho, 0)

    assert resultado.ok is True
    assert resultado.data["produto"] == "mouse"
    assert len(carrinho) == 1
    assert carrinho[0]["produto"] == "teclado"


def test_calcular_total_bruto_do_carrinho():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 2, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    resultado = carr.calcular_total(carrinho)

    assert resultado.ok is True
    assert resultado.data == 90.0
    assert resultado.error is None


def test_calcular_carrinho_vazio():

    carrinho = []

    resultado = carr.calcular_total(carrinho)

    assert resultado.ok is True
    assert resultado.data == 0
    assert resultado.error is None


def test_aplicar_desconto_no_carrinho():

    resultado = carr.calcular_desconto(100, 17)

    assert resultado.ok is True
    assert resultado.data == 83.0
    assert resultado.error is None


def test_tratar_desconto_zero():

    resultado = carr.calcular_desconto(100, 0)

    assert resultado.ok is True
    assert resultado.data == 100
    assert resultado.error is None


def test_aplica_taxa_no_valor_final():

    resultado = carr.aplica_taxa(100, 35)

    assert resultado.ok is True
    assert resultado.data == 135
    assert resultado.error is None


def test_taxa_zero_nao_deve_alterar_total():

    resultado = carr.aplica_taxa(100, 0)

    assert resultado.ok is True
    assert resultado.data == 100
    assert resultado.error is None


def test_total_final_menos_descontos_mais_taxas():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 2, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    resultado = carr.total_final(carrinho, 5, 8)

    assert resultado.ok is True
    assert resultado.data == 93.5
    assert resultado.error is None


def test_validar_total_sem_descomtos_sem_taxa():

    carrinho = [
        {"produto": "mouse", "preco": 20.0, "qtd": 3, "indice": 0},
        {"produto": "teclado", "preco": 50.0, "qtd": 1, "indice": 1},
    ]

    resultado = carr.total_final(carrinho, 0, 0)

    assert resultado.ok is True
    assert resultado.data == 110
    assert resultado.error is None

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

    venda = {
            "itens": carrinho, 
            "total": 110,
            "total_com_desconto": 99
            }

    nova_venda_com_taxa, erro = vd.aplicar_taxa_venda(venda, 15)

    assert erro is None
    assert nova_venda_com_taxa["total_final"] == 114




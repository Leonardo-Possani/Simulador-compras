import json

def carregar_produtos():
    with open("../data/produtos.json", "r", encoding="utf-8") as f:
        produtos = json.load(f)
    return produtos  

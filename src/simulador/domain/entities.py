from dataclasses import dataclass


@dataclass
class ItemCarrinho:
    indice: int
    produto: str
    preco: float
    qtd: int


@dataclass
class ResultadoCarrinho:
    item: ItemCarrinho
    carrinho: list[ItemCarrinho]


"""
@dataclass(frozen=True)
class ProdutoEstoque:
    produto: str
    preco: float
    estoque: int
"""
   

@dataclass(frozen=True)
class Venda:
    itens: list[ItemCarrinho]
    total: float
    total_com_desconto: float | None = None
    total_final: float | None = None
    troco: float | None = None 

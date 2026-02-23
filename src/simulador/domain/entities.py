from dataclasses import dataclass

from simulador.domain.types import MetodoPagamento

# Carrinho


@dataclass
class ItemCarrinho:
    produto_id: int
    produto: str
    preco: float
    qtd: int


@dataclass
class ResultadoCarrinho:
    item: ItemCarrinho
    carrinho: list[ItemCarrinho]


# Estoque


@dataclass
class Produto:
    produto: str 
    preco: float 
    estoque: int
    produto_id: int


@dataclass(frozen=True)
class Estoque:
    estoque: list[Produto]

# Venda


@dataclass(frozen=True)
class Venda:
    itens: tuple[ItemCarrinho]
    total: float

    total_com_desconto: float | None = None
    total_final: float | None = None

    pagamento: MetodoPagamento | None = None
    valor_pago: float | None = None
    troco: float | None = None


@dataclass(frozen=True)
class ItemVendido:
    produto_id: int
    qtd: int


@dataclass(frozen=True)
class ResultadoVenda:
    venda: Venda
    estoque_atualizado: list[Produto]


   

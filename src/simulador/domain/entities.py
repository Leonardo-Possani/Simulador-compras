from dataclasses import dataclass

# Carrinho


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


# Venda


@dataclass(frozen=True)
class Venda:
    itens: tuple[ItemCarrinho]
    total: float

    total_com_desconto: float | None = None
    total_final: float | None = None

    pagamento: str | None = None
    valor_pago: float | None = None
    troco: float | None = None


@dataclass(frozen=True)
class ResultadoVenda:
    venda: Venda
    estoque_atualizado: list | None = None


# Estoque


@dataclass
class Produto:
    produto: str | None = None
    preco: float | None = None
    estoque: int | None = None


@dataclass(frozen=True)
class Estoque:
    estoque: list[Produto]

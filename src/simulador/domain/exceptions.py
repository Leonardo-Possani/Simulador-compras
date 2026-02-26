
# Domain

class DomainError(Exception):
    pass

# Carrinho


class CarrinhoError(DomainError):
    pass


class TaxaInvalidaError(CarrinhoError):
    pass


class QuantidadeInvalidaError(CarrinhoError):
    pass


class DescontoInvalidoError(CarrinhoError):
    pass


# Estoque

class EstoqueError(DomainError):
    pass


class PrecoInvalidoError(EstoqueError):
    pass


class EstoqueInsuficienteError(EstoqueError):
    pass


class ProdutoIdInexistenteError(EstoqueError):
    pass


class NomeInvalidoError(EstoqueError):
    pass


# Venda

class VendaError(DomainError):
    pass


class CarrinhoInvalidoError(VendaError):
    pass


class DinheiroInsuficienteError(VendaError):
    pass


class ValorIncorretoError(VendaError):
    pass


class MetodoInvalidoError(VendaError):
    pass


class SequenciaVendaInvalidaError(VendaError):
    pass

from simulador.domain.exceptions import (
    
    CarrinhoInvalidoError,
    DescontoInvalidoError,
    DinheiroInsuficienteError,
    DomainError,
    CarrinhoError,
    EstoqueError,
    EstoqueInsuficienteError,
    SequenciaVendaInvalidaError,
    TaxaInvalidaError,
    ValorIncorretoError,
    VendaError,
    QuantidadeInvalidaError,
    ProdutoIdInexistenteError,
    PrecoInvalidoError,
    MetodoInvalidoError,
    NomeInvalidoError


)


def test_hierarquia_excecoes_dominio():
    
    assert issubclass(CarrinhoError, DomainError)
    assert issubclass(QuantidadeInvalidaError, CarrinhoError)
    assert issubclass(TaxaInvalidaError, CarrinhoError)
    assert issubclass(DescontoInvalidoError, CarrinhoError)

    assert issubclass(EstoqueError, DomainError)
    assert issubclass(ProdutoIdInexistenteError, EstoqueError)
    assert issubclass(PrecoInvalidoError, EstoqueError)
    assert issubclass(EstoqueInsuficienteError, EstoqueError)
    assert issubclass(NomeInvalidoError, EstoqueError)

    assert issubclass(VendaError, DomainError)
    assert issubclass(MetodoInvalidoError, VendaError)
    assert issubclass(SequenciaVendaInvalidaError, VendaError)
    assert issubclass(ValorIncorretoError, VendaError)
    assert issubclass(DinheiroInsuficienteError, VendaError)
    assert issubclass(CarrinhoInvalidoError, VendaError)


import copy

from simulador.domain.entities import ItemVendido, Produto
from simulador.domain.exceptions import (
    EstoqueInsuficienteError,
    NomeInvalidoError,
    PrecoInvalidoError,
    ProdutoIdInexistenteError,
    QuantidadeInvalidaError,
)


def baixar_qtd_do_estoque(estoque: list[Produto], produto_id: int, qtd: int) -> list[Produto]:
    
    if qtd <= 0:
        raise QuantidadeInvalidaError()
    estoque_copia = copy.deepcopy(estoque)

    produto = valida_produto_id_retorna_produto_estoque(estoque_copia, produto_id)

    produto.estoque -= qtd

    return estoque_copia


def valida_produto_id_retorna_produto_estoque(estoque: list[Produto], produto_id: int) -> Produto:

    if produto_id < 0:
        raise ProdutoIdInexistenteError()
    for item in estoque:
        if produto_id == item.produto_id:
            return item
    else:
        raise ProdutoIdInexistenteError()    
            

def valida_qtd_atual_carrinho_menor_estoque(
    qtd_existente_carrinho: int, quantidade: int, qtd_estoque: int
) -> None:
    if qtd_existente_carrinho + quantidade > qtd_estoque:
        raise QuantidadeInvalidaError()


def valida_estoque_para_venda(itens_vendidos: tuple[ItemVendido, ...], estoque: list[Produto]) -> bool:

    for item in itens_vendidos:
        if item.qtd <= 0:
            raise QuantidadeInvalidaError()
        produto = valida_produto_id_retorna_produto_estoque(estoque, item.produto_id)
        valida_produto_estoque(produto)
        if produto.estoque < item.qtd:
            raise EstoqueInsuficienteError()
    return True
  

def valida_produto_estoque(produto: Produto) -> None:

    if not produto.produto:
        raise NomeInvalidoError()
    if produto.preco <= 0:
        raise PrecoInvalidoError()
    if produto.estoque <= 0:
        raise EstoqueInsuficienteError()
    

def venda_concluindo_baixar_estoque(itens_vendidos: tuple[ItemVendido, ...], estoque: list[Produto]) -> list[Produto]:
    
    novo_estoque_final = estoque
    for item in itens_vendidos:
        novo_estoque_baixado = baixar_qtd_do_estoque(novo_estoque_final, item.produto_id, item.qtd)
        novo_estoque_final = novo_estoque_baixado
        
    return novo_estoque_final




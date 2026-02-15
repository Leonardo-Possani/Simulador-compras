from simulador.domain.exceptions import EstoqueInsuficienteError
from simulador.domain.entities import Produto


def valida_estoque_para_venda(itens_vendidos: list[dict], estoque: Estoque[list[Produto]]) -> bool:

    for item in itens_vendidos:
        indice = item["indice"]
        qtd = item["qtd"]

        if estoque[indice].estoque < qtd:
            raise EstoqueInsuficienteError()
    return True


def venda_concluindo_baixar_estoque(itens_vendidos: list[dict], estoque: list[dict]) -> dict:

    estoque_atualizado = estoque.copy()

    for item in itens_vendidos:
        indice = item["indice"]
        qtd = item["qtd"]

        estoque_atualizado[indice].estoque -= qtd

    return estoque_atualizado

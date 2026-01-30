from simulador.domain.result import Result


def valida_estoque_para_venda(itens_vendidos: list[dict], estoque: list[dict]) -> Result[bool]:

    for item in itens_vendidos:
        indice = item["indice"]
        qtd = item["qtd"]

        if estoque[indice]["estoque"] < qtd:
            return Result(ok=False, error="estoque insuficiente")
    return Result(ok=True)


def venda_concluindo_baixar_estoque(
    itens_vendidos: list[dict], estoque: list[dict]
) -> Result[dict]:

    estoque_atualizado = estoque.copy()

    for item in itens_vendidos:
        indice = item["indice"]
        qtd = item["qtd"]

        estoque_atualizado[indice]["estoque"] -= qtd

    return Result(ok=True, data=estoque_atualizado)

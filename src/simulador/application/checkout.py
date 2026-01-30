from simulador.domain import estoque as etq
from simulador.domain import venda as vd
from simulador.domain.result import Result


def finalizar_venda(
    carrinho: list[dict],
    estoque: list[dict],
    desconto: int,
    taxa: int,
    pagamento: str,
    valor_pago: float,
) -> Result[dict]:

    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)

    if resultado.error is not None:
        return Result(ok=False, error=resultado.error) 

    resultado = vd.aplicar_desconto(resultado.data, desconto)

    if resultado.error is not None:
        return Result(ok=False, error=resultado.error) 

    resultado = vd.aplicar_taxa_venda(resultado.data, taxa)

    if resultado.error is not None:
        return Result(ok=False, error=resultado.error)

    resultado = vd.registrar_pagamento(resultado.data, pagamento)

    if resultado.error is not None:
        return Result(ok=False, error=resultado.error)

    resultado = vd.processar_pagamento(resultado.data, valor_pago)
    venda_processada = resultado.data

    if resultado.error is not None:
        return Result(ok=False, error=resultado.error)

    resultado = vd.extrair_itens_vendidos(resultado.data)
    itens_vendidos = resultado.data

    if resultado.error is not None:
        return Result(ok=False, error=resultado.error)

    resultado = etq.valida_estoque_para_venda(resultado.data, estoque)

    if not resultado.ok:
        return Result(ok=False, error=resultado.error)

    resultado = etq.venda_concluindo_baixar_estoque(itens_vendidos, estoque)
    estoque_atualizado = resultado.data

    if resultado.error is not None:
        return Result(ok=False, error=resultado.error)

    return Result(ok=True, data={"venda": venda_processada, "estoque": estoque_atualizado})




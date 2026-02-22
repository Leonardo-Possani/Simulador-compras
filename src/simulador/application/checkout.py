from simulador.domain import estoque as etq
from simulador.domain import venda as vd
from simulador.domain.entities import ItemCarrinho, Produto, ResultadoVenda


def finalizar_venda(
    carrinho: list[ItemCarrinho],
    estoque: list[Produto],
    desconto: int,
    taxa: int,
    pagamento: str,
    valor_pago: float,
) -> ResultadoVenda:
    
    resultado = vd.fechar_venda_com_carrinho_valido(carrinho)

    resultado = vd.aplicar_desconto(resultado, desconto)

    resultado = vd.aplicar_taxa_venda(resultado, taxa)

    resultado = vd.registrar_pagamento(resultado, pagamento)

    resultado = vd.processar_pagamento(resultado, valor_pago)
    venda_processada = resultado

    resultado = vd.extrair_itens_vendidos(resultado)
    itens_vendidos = resultado

    resultado = etq.valida_estoque_para_venda(resultado, estoque)

    resultado = etq.venda_concluindo_baixar_estoque(itens_vendidos, estoque)
    estoque_atualizado = resultado

    return ResultadoVenda(venda_processada, estoque_atualizado)

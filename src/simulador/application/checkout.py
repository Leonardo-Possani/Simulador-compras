from simulador.domain import estoque as etq
from simulador.domain import venda as vd


def finalizar_venda(carrinho, estoque, desconto, taxa, pagamento, valor_pago):

    resultado = vd.fechar_venda(carrinho)

    if resultado["error"] is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }
    
    resultado = vd.aplicar_desconto(resultado["data"]["venda"], desconto)

    if resultado["error"] is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }

    resultado = vd.aplicar_taxa_venda(resultado["data"]["venda"], taxa)

    if resultado["error"] is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }

    resultado = vd.registrar_pagamento(resultado["data"]["venda"], pagamento)

    if resultado["error"] is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }

    resultado = vd.processar_pagamento(resultado["data"]["venda"], valor_pago)
    venda_processada = resultado["data"]["venda"]
    
    if resultado["error"] is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }

    resultado = vd.extrair_itens_vendidos(resultado["data"]["venda"])
    itens_vendidos = resultado["data"]["itens_vendidos"]

    if resultado["error"] is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }

    resultado = etq.valida_estoque_para_venda(resultado["data"]["itens_vendidos"], estoque)

    if not resultado["ok"]:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }

    resultado = etq.venda_concluindo_baixar_estoque(itens_vendidos, estoque)
    estoque_atualizado = resultado["data"]["estoque_atualizado"]

    if resultado["error"] is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }

    return {
                "ok": True,
                "data": {
                            "venda": venda_processada,
                            "estoque": estoque_atualizado
                        },
                "error": None
            }






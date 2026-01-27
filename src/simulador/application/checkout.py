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

    if resultado["error"] is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": resultado["error"]
                }

    estoque_para_venda_valido, erro = etq.valida_estoque_para_venda(resultado["data"]["itens_vendidos"], estoque)

    if not estoque_para_venda_valido:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    estoque_atualizado, erro = etq.venda_concluindo_baixar_estoque(resultado["data"]["itens_vendidos"], estoque)

    if erro is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    return {
                "ok": True,
                "data": {
                            "venda": venda_processada,
                            "estoque": estoque_atualizado
                        },
                "error": None
            }






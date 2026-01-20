from simulador.domain import estoque as etq
from simulador.domain import venda as vd


def finalizar_venda(carrinho, estoque, desconto, taxa, pagamento, valor_pago):

    venda, erro = vd.fechar_venda(carrinho)

    if erro is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    venda_com_desconto, erro = vd.aplicar_desconto(venda, desconto)

    if erro is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    venda_com_taxa, erro = vd.aplicar_taxa_venda(venda_com_desconto, taxa)

    if erro is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    venda_com_metodo_de_pagamento, erro = vd.registrar_pagamento(venda_com_taxa, pagamento)

    if erro is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    venda_processada, erro = vd.processar_pagamento(venda_com_metodo_de_pagamento, valor_pago)

    if erro is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    itens_vendidos, erro = vd.extrair_itens_vendidos(venda_processada)

    if erro is not None:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    estoque_para_venda_valido, erro = etq.valida_estoque_para_venda(itens_vendidos, estoque)

    if not estoque_para_venda_valido:
        return {
                    "ok": False,
                    "data": None,
                    "error": erro
                }

    estoque_atualizado, erro = etq.venda_concluindo_baixar_estoque(itens_vendidos, estoque)

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






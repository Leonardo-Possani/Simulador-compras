from simulador.domain import carrinho as carr


def fechar_venda(carrinho):

    if not carrinho:
        return {"ok": False, "data": None, "error": "carrinho vazio"}
    else:
        resultado = carr.calcular_total(carrinho)
        total = resultado["data"]["total"]
        return {"ok": True, "data": {"venda": {"itens": carrinho, "total": total}}, "error": None} 
    # {"itens": carrinho, "total": total}, None


def aplicar_desconto(venda, desconto):

    nova_venda_com_desconto = venda.copy()

    total_bruto = nova_venda_com_desconto["total"]
    resultado = carr.calcular_desconto(total_bruto, desconto)
    total_venda_com_desconto = resultado["data"]["total_com_desconto"]
    nova_venda_com_desconto["total_com_desconto"] = total_venda_com_desconto
    return {"ok": True, "data": {"venda": nova_venda_com_desconto}, "error": None}


def aplicar_taxa_venda(venda, taxa):

    nova_venda_com_taxa = venda.copy()
    total = nova_venda_com_taxa["total_com_desconto"]
    resultado = carr.aplica_taxa(total, taxa)
    total_com_taxa = resultado["data"]["total_com_taxa"]
    nova_venda_com_taxa["total_final"] = total_com_taxa
    return {"ok": True, "data": {"venda": nova_venda_com_taxa}, "error": None}


def registrar_pagamento(venda, pagamento):

    venda_paga = venda.copy()
    venda_paga["pagamento"] = pagamento
    return {"ok": True, "data": {"venda": venda_paga}, "error": None}


def venda_paga_no_dinheiro(venda, valor_pago):

    nova_venda_com_troco = venda.copy()
    tipo_de_venda = nova_venda_com_troco["pagamento"]
    total_final = nova_venda_com_troco["total_final"]

    if tipo_de_venda == "dinheiro" and total_final <= valor_pago:
        if total_final == valor_pago:
            return {"ok": True, "data": {"venda": nova_venda_com_troco}, "error": None}

        nova_venda_com_troco["troco"] = valor_pago - total_final
        return {"ok": True, "data": {"venda": nova_venda_com_troco}, "error": None}

    if total_final > valor_pago:
        return {"ok": False, "data": None, "error": "dinheiro insuficiente"}


def venda_paga_no_debito(venda, valor_pago):

    venda_debito = venda.copy()
    if venda_debito["pagamento"] == "debito":
        if venda_debito["total_final"] == valor_pago:
            venda_debito["valor_pago"] = valor_pago
            return {"ok": True, "data": {"venda": venda_debito}, "error": None}

        if valor_pago != venda_debito["total_final"]:
            return {"ok": False, "data": None, "error": "valor incorreto"}


def venda_paga_no_credito(venda, valor_pago):

    venda_credito = venda.copy()
    if venda_credito["pagamento"] == "credito":
        if venda_credito["total_final"] == valor_pago:
            venda_credito["valor_pago"] = valor_pago
            return {"ok": True, "data": {"venda": venda_credito}, "error": None}

        if valor_pago != venda_credito["total_final"]:
            return {"ok": False, "data": None, "error": "valor incorreto"}


def processar_pagamento(venda, valor_pago):

    venda_a_processar = venda.copy()
    if venda_a_processar["pagamento"] == "dinheiro":
        resultado = venda_paga_no_dinheiro(venda_a_processar, valor_pago)
        return resultado

    elif venda_a_processar["pagamento"] == "debito":
        resultado = venda_paga_no_debito(venda_a_processar, valor_pago)
        return resultado

    elif venda_a_processar["pagamento"] == "credito":
        resultado = venda_paga_no_credito(venda_a_processar, valor_pago)
        return resultado

    else:
        return None, "metodo inválido"


def extrair_itens_vendidos(venda):

    itens_vendidos = []
    carrinho = venda["itens"]

    for itens in carrinho:
        item = {"indice": itens["indice"], "qtd": itens["qtd"]}
        itens_vendidos.append(item)
    
    return {"ok": True, "data": {"itens_vendidos": itens_vendidos}, "error": None}

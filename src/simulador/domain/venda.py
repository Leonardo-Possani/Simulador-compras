from simulador.domain import carrinho as carr


def fechar_venda(carrinho):

    if not carrinho:
        return None, "carrinho vazio"
    else:
        total = carr.calcular_total(carrinho)
        return {"itens": carrinho, "total": total}, None


def aplicar_desconto(venda, desconto):

    nova_venda_com_desconto = venda.copy()

    total_bruto = nova_venda_com_desconto["total"]
    total_venda_com_desconto = carr.calcular_desconto(total_bruto, desconto)
    nova_venda_com_desconto["total_com_desconto"] = total_venda_com_desconto
    return nova_venda_com_desconto, None


def aplicar_taxa_venda(venda, taxa):

    nova_venda_com_taxa = venda.copy()
    total = nova_venda_com_taxa["total_com_desconto"]
    total_com_taxa = carr.aplica_taxa(total, taxa)
    nova_venda_com_taxa["total_final"] = total_com_taxa
    return nova_venda_com_taxa, None


def registrar_pagamento(venda, pagamento):

    venda_paga = venda.copy()
    venda_paga["pagamento"] = pagamento
    return venda_paga, None


def venda_paga_no_dinheiro(venda, valor_pago):

    nova_venda_com_troco = venda.copy()
    tipo_de_venda = nova_venda_com_troco["pagamento"]
    total_final = nova_venda_com_troco["total_final"]

    if tipo_de_venda == "dinheiro" and total_final <= valor_pago:
        if total_final == valor_pago:
            return nova_venda_com_troco, None

        nova_venda_com_troco["troco"] = valor_pago - total_final
        return nova_venda_com_troco, None

    if total_final > valor_pago:
        return None, "dinheiro insuficiente"


def venda_paga_no_debito(venda, valor_pago):

    venda_debito = venda.copy()
    if venda_debito["pagamento"] == "debito":
        if venda_debito["total_final"] == valor_pago:
            venda_debito["valor_pago"] = valor_pago
            return venda_debito, None

        if valor_pago != venda_debito["total_final"]:
            return None, "valor incorreto"


def venda_paga_no_credito(venda, valor_pago):

    venda_credito = venda.copy()
    if venda_credito["pagamento"] == "credito":
        if venda_credito["total_final"] == valor_pago:
            venda_credito["valor_pago"] = valor_pago
            return venda_credito, None

        if valor_pago != venda_credito["total_final"]:
            return None, "valor incorreto"


def processar_pagamento(venda, valor_pago):

    venda_a_processar = venda.copy()
    if venda_a_processar["pagamento"] == "dinheiro":
        venda_processada, erro = venda_paga_no_dinheiro(venda_a_processar, valor_pago)
        return venda_processada, erro

    elif venda_a_processar["pagamento"] == "debito":
        venda_processada, erro = venda_paga_no_debito(venda_a_processar, valor_pago)
        return venda_processada, erro

    elif venda_a_processar["pagamento"] == "credito":
        venda_processada, erro = venda_paga_no_credito(venda_a_processar, valor_pago)
        return venda_processada, erro

    else:
        return None, "metodo inválido"


def extrair_itens_vendidos(venda):

    itens_vendidos = []
    carrinho = venda["itens"]

    for itens in carrinho:
        item = {"indice": itens["indice"], "qtd": itens["qtd"]}
        itens_vendidos.append(item)
    
    return itens_vendidos, None

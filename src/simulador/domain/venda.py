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


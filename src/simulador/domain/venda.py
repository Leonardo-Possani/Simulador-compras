from simulador.domain import carrinho as carr
from simulador.domain.result import Result


def fechar_venda_com_carrinho_valido(carrinho: list[dict]) -> Result[dict]:

    if not carrinho:
        return Result(ok=False, error="carrinho vazio")
    else:
        resultado = carr.calcular_total(carrinho)
        total = resultado.data
        return Result(ok=True, data={"itens": carrinho, "total": total})


def aplicar_desconto(venda: dict, desconto: int) -> Result[dict]:

    nova_venda_com_desconto = venda.copy()

    total_bruto = nova_venda_com_desconto["total"]
    resultado = carr.calcular_desconto(total_bruto, desconto)
    total_venda_com_desconto = resultado.data
    nova_venda_com_desconto["total_com_desconto"] = total_venda_com_desconto
    return Result(ok=True, data=nova_venda_com_desconto)


def aplicar_taxa_venda(venda: dict, taxa: int) -> Result[dict]:

    nova_venda_com_taxa = venda.copy()
    total = nova_venda_com_taxa["total_com_desconto"]
    resultado = carr.aplica_taxa(total, taxa)
    total_com_taxa = resultado.data
    nova_venda_com_taxa["total_final"] = total_com_taxa
    return Result(ok=True, data=nova_venda_com_taxa)


def registrar_pagamento(venda: dict, pagamento: str) -> Result[dict]:

    venda_paga = venda.copy()
    venda_paga["pagamento"] = pagamento
    return Result(ok=True, data=venda_paga) 


def venda_paga_no_dinheiro(venda: dict, valor_pago: float) -> Result[dict]:

    nova_venda_com_troco = venda.copy()
    tipo_de_venda = nova_venda_com_troco["pagamento"]
    total_final = nova_venda_com_troco["total_final"]

    if tipo_de_venda == "dinheiro" and total_final <= valor_pago:
        if total_final == valor_pago:
            return Result(ok=True, data=nova_venda_com_troco) 

        nova_venda_com_troco["troco"] = valor_pago - total_final
        return Result(ok=True, data=nova_venda_com_troco)

    if total_final > valor_pago:
        return Result(ok=False, error="dinheiro insuficiente")
    
    return Result(ok=False, error="metodo inválido")    
        

def venda_paga_no_debito(venda: dict, valor_pago: int) -> Result[dict]:

    venda_debito = venda.copy()
    if venda_debito["pagamento"] == "debito":
        if venda_debito["total_final"] == valor_pago:
            venda_debito["valor_pago"] = valor_pago
            return Result(ok=True, data=venda_debito) 

        if valor_pago != venda_debito["total_final"]:
            return Result(ok=False, error="valor incorreto") 
    
    return Result(ok=False, error="metodo inválido")    


def venda_paga_no_credito(venda: dict, valor_pago: int) -> Result[dict]:

    venda_credito = venda.copy()
    if venda_credito["pagamento"] == "credito":
        if venda_credito["total_final"] == valor_pago:
            venda_credito["valor_pago"] = valor_pago
            return Result(ok=True, data=venda_credito) 

        if valor_pago != venda_credito["total_final"]:
            return Result(ok=False, error="valor incorreto")
    return Result(ok=False, error="metodo inválido")    


def processar_pagamento(venda: dict, valor_pago: int) -> Result[dict]:

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
        return Result(ok=False, error="metodo inválido") 
    # {"ok": False, "data": None, "error": "metodo inválido"}


def extrair_itens_vendidos(venda: dict) -> Result[dict]:

    itens_vendidos = []
    carrinho = venda["itens"]

    for itens in carrinho:
        item = {"indice": itens["indice"], "qtd": itens["qtd"]}
        itens_vendidos.append(item)
    
    return Result(ok=True, data=itens_vendidos) 

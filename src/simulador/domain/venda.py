from simulador.domain import carrinho as carr
from simulador.domain.result import Result
from simulador.domain.entities import ItemCarrinho, Venda
from dataclasses import replace


def fechar_venda_com_carrinho_valido(carrinho: list[ItemCarrinho]) -> Result[Venda]:

    if not carrinho:
        return Result(ok=False, error="carrinho vazio")
    else:
        resultado = carr.calcular_total(carrinho)
        total = resultado.data
        return Result(ok=True, data=Venda(itens=carrinho, total=total))


def aplicar_desconto(venda: Venda, desconto: int) -> Result[Venda]:

    resultado = carr.calcular_desconto(venda.total, desconto)
    total_venda_com_desconto = resultado.data
    nova_venda = replace(
        venda,
        total_com_desconto=total_venda_com_desconto
    )

    return Result(ok=True, data=nova_venda)


def aplicar_taxa_venda(venda: Venda, taxa: int) -> Result[Venda]:

    resultado = carr.aplica_taxa(venda.total_com_desconto, taxa)
    total_com_taxa = resultado.data
    nova_venda = replace(
        venda,
        total_final=total_com_taxa
    )
    return Result(ok=True, data=nova_venda)


def registrar_pagamento(venda: Venda, pagamento: str) -> Result[Venda]:

    nova_venda = replace(
        venda,
        pagamento=pagamento
    )
    return Result(ok=True, data=nova_venda) 


def venda_paga_no_dinheiro(venda: Venda, valor_pago: float) -> Result[Venda]:

    nova_venda = replace(venda)

    if nova_venda.pagamento == "dinheiro" and nova_venda.total_final <= valor_pago:
        if nova_venda.total_final == valor_pago:
            return Result(ok=True, data=nova_venda) 

        nova_venda.troco = valor_pago - nova_venda.total_final
        return Result(ok=True, data=nova_venda)

    if nova_venda.total_final > valor_pago:
        return Result(ok=False, error="dinheiro insuficiente")
    
    return Result(ok=False, error="metodo inválido")    
        

def venda_paga_no_debito(venda: Venda, valor_pago: int) -> Result[Venda]:

    venda_debito = replace(venda)
    if venda_debito.pagamento == "debito":
        if venda_debito.total_final == valor_pago:
            venda_debito.valor_pago = valor_pago
            return Result(ok=True, data=venda_debito) 

        if valor_pago != venda_debito.total_final:
            return Result(ok=False, error="valor incorreto") 
    
    return Result(ok=False, error="metodo inválido")    


def venda_paga_no_credito(venda: Venda, valor_pago: int) -> Result[Venda]:

    venda_credito = replace(venda)
    if venda_credito.pagamento == "credito":
        if venda_credito.total_final == valor_pago:
            venda_credito.valor_pago = valor_pago
            return Result(ok=True, data=venda_credito) 

        if valor_pago != venda_credito.total_final:
            return Result(ok=False, error="valor incorreto")
    return Result(ok=False, error="metodo inválido")    


def processar_pagamento(venda: Venda, valor_pago: int) -> Result[Venda]:

    if venda.pagamento == "dinheiro":
        resultado = venda_paga_no_dinheiro(venda, valor_pago)
        return resultado

    elif venda.pagamento == "debito":
        resultado = venda_paga_no_debito(venda, valor_pago)
        return resultado

    elif venda.pagamento == "credito":
        resultado = venda_paga_no_credito(venda, valor_pago)
        return resultado

    else:
        return Result(ok=False, error="metodo inválido") 


def extrair_itens_vendidos(venda: Venda) -> Result[list[dict]]:

    itens_vendidos = []
    carrinho = venda.itens

    for itens in carrinho:
        item = {"indice": itens.indice, "qtd": itens.qtd}
        itens_vendidos.append(item)
    
    return Result(ok=True, data=itens_vendidos) 

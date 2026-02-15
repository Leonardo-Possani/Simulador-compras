from dataclasses import replace

from simulador.domain import carrinho as carr
from simulador.domain.entities import ItemCarrinho, Venda
from simulador.domain.exceptions import (
    CarrinhoInvalidoError,
    DinheiroInsuficienteError,
    MetodoInvalidoError,
    ValorIncorretoError,
)


def fechar_venda_com_carrinho_valido(carrinho: list[ItemCarrinho]) -> Venda:

    if not carrinho:
        raise CarrinhoInvalidoError()
    else:
        total = carr.calcular_total(carrinho)
        return Venda(itens=carrinho, total=total)


def aplicar_desconto(venda: Venda, desconto: int) -> Venda:

    total_venda_com_desconto = carr.calcular_desconto(venda.total, desconto)
    nova_venda = replace(venda, total_com_desconto=total_venda_com_desconto)

    return nova_venda


def aplicar_taxa_venda(venda: Venda, taxa: int) -> Venda:

    total_com_taxa = carr.aplica_taxa(venda.total_com_desconto, taxa)

    nova_venda = replace(venda, total_final=total_com_taxa)
    return nova_venda


def registrar_pagamento(venda: Venda, pagamento: str) -> Venda:

    nova_venda = replace(venda, pagamento=pagamento)
    return nova_venda


def venda_paga_no_dinheiro(venda: Venda, valor_pago: float) -> Venda:

    if venda.pagamento == "dinheiro" and venda.total_final <= valor_pago:
        if venda.total_final == valor_pago:
            return venda
        nova_venda = replace(venda, troco=valor_pago - venda.total_final)
        return nova_venda

    if venda.total_final > valor_pago:
        raise DinheiroInsuficienteError()

    raise MetodoInvalidoError()


def venda_paga_no_debito(venda: Venda, valor_pago: int) -> Venda:

    if venda.pagamento == "debito":
        if venda.total_final == valor_pago:
            nova_venda = replace(venda, valor_pago=valor_pago)
            return nova_venda

        if valor_pago != venda.total_final:
            raise ValorIncorretoError()

    raise MetodoInvalidoError()


def venda_paga_no_credito(venda: Venda, valor_pago: int) -> Venda:

    if venda.pagamento == "credito":
        if venda.total_final == valor_pago:
            nova_venda = replace(venda, valor_pago=valor_pago)
            return nova_venda

        if valor_pago != venda.total_final:
            raise ValorIncorretoError()
    raise MetodoInvalidoError()


def processar_pagamento(venda: Venda, valor_pago: int) -> Venda:

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
        raise MetodoInvalidoError()


def extrair_itens_vendidos(venda: Venda) -> list[dict]:

    itens_vendidos = []
    carrinho = venda.itens

    for itens in carrinho:
        item = {"indice": itens.indice, "qtd": itens.qtd}
        itens_vendidos.append(item)

    return itens_vendidos

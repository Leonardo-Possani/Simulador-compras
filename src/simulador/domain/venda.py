import copy
from dataclasses import replace

from simulador.domain import carrinho as carr
from simulador.domain.types import MetodoPagamento
from simulador.domain.entities import ItemCarrinho, ItemVendaFechada, ItemVendido, Venda
from simulador.domain.exceptions import (
    CarrinhoInvalidoError,
    DinheiroInsuficienteError,
    MetodoInvalidoError,
    SequenciaVendaInvalidaError,
    ValorIncorretoError,
)


def valida_metodo_de_pagamento(pagamento: str | MetodoPagamento | None) -> MetodoPagamento:

    if pagamento is None:
        raise SequenciaVendaInvalidaError()
    if pagamento not in MetodoPagamento:
        raise MetodoInvalidoError()
    return MetodoPagamento(pagamento)


def valida_total_com_desconto_calculado(venda: Venda) -> None:

    if venda.total_com_desconto is None:
        raise SequenciaVendaInvalidaError()


def valida_total_final_calculado(venda: Venda) -> None:

    if venda.total_final is None:
        raise SequenciaVendaInvalidaError()


def garante_item_vendido_imutavel(carrinho: list[ItemCarrinho]) -> list[ItemVendaFechada]:
    
    novo_carrinho = []
    for item in carrinho:
        novo_item = ItemVendaFechada(produto=item.produto, preco=item.preco, qtd=item.qtd, produto_id=item.produto_id)
        novo_carrinho.append(novo_item)
    return novo_carrinho


def fechar_venda_com_carrinho_valido(carrinho: list[ItemCarrinho]) -> Venda:

    if not carrinho:
        raise CarrinhoInvalidoError()
    else:
        total = carr.calcular_total(carrinho)
        carrinho_copia = copy.deepcopy(carrinho)
        carrinho_item_imutavel = garante_item_vendido_imutavel(carrinho_copia)
        carrinho_final = tuple(carrinho_item_imutavel)
        return Venda(itens=carrinho_final, total=total)


def aplicar_desconto(venda: Venda, desconto: int) -> Venda:

    total_venda_com_desconto = carr.calcular_desconto(venda.total, desconto)
    nova_venda = replace(venda, total_com_desconto=total_venda_com_desconto)

    return nova_venda


def aplicar_taxa_venda(venda: Venda, taxa: int) -> Venda:

    valida_total_com_desconto_calculado(venda)
    total_com_taxa = carr.aplica_taxa(venda.total_com_desconto, taxa)
    nova_venda = replace(venda, total_final=total_com_taxa)
    return nova_venda


def registrar_pagamento(venda: Venda, pagamento: MetodoPagamento) -> Venda:

    valida_total_final_calculado(venda)
    metodo = valida_metodo_de_pagamento(pagamento)
    nova_venda = replace(venda, pagamento=metodo)
    return nova_venda


def venda_paga_no_dinheiro(venda: Venda, valor_pago: float) -> Venda:

    valida_total_final_calculado(venda)
    if venda.pagamento == MetodoPagamento.DINHEIRO and venda.total_final <= valor_pago:
        if venda.total_final == valor_pago:
            return venda
        nova_venda = replace(venda, troco=valor_pago - venda.total_final)
        return nova_venda

    if venda.total_final > valor_pago:
        raise DinheiroInsuficienteError()

    raise MetodoInvalidoError()


def venda_paga_no_debito(venda: Venda, valor_pago: int) -> Venda:

    valida_total_final_calculado(venda)
    if venda.pagamento == MetodoPagamento.DEBITO:
        if venda.total_final == valor_pago:
            nova_venda = replace(venda, valor_pago=valor_pago)
            return nova_venda

        if valor_pago != venda.total_final:
            raise ValorIncorretoError()

    raise MetodoInvalidoError()


def venda_paga_no_credito(venda: Venda, valor_pago: int) -> Venda:

    valida_total_final_calculado(venda)
    if venda.pagamento == MetodoPagamento.CREDITO:
        if venda.total_final == valor_pago:
            nova_venda = replace(venda, valor_pago=valor_pago)
            return nova_venda

        if valor_pago != venda.total_final:
            raise ValorIncorretoError()
    raise MetodoInvalidoError()


def processar_pagamento(venda: Venda, valor_pago: int) -> Venda:
    valida_total_final_calculado(venda)
    valida_metodo_de_pagamento(venda.pagamento)
    if venda.pagamento == MetodoPagamento.DINHEIRO:
        resultado = venda_paga_no_dinheiro(venda, valor_pago)
        return resultado

    elif venda.pagamento == MetodoPagamento.DEBITO:
        resultado = venda_paga_no_debito(venda, valor_pago)
        return resultado

    elif venda.pagamento == MetodoPagamento.CREDITO:
        resultado = venda_paga_no_credito(venda, valor_pago)
        return resultado


def extrair_itens_vendidos(venda: Venda) -> tuple[ItemVendido, ...]:

    itens_vendidos = []
    carrinho = venda.itens

    for itens in carrinho:
        item = ItemVendido(produto_id=itens.produto_id, qtd=itens.qtd)
        itens_vendidos.append(item)
    
    itens_vendidos_final = tuple(itens_vendidos)

    return itens_vendidos_final 

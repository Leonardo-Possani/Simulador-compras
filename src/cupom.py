from utils import clear
from carrinho import limpar_carrinho
from estoque import cupom_modifica_qtd_estoque 


def cupom_fiscal(carrinho, estoque):
    """gera o cupom fiscal, limpa o carrinho.json, limpa o carrinho na memoria."""
    clear()
    print("\n" + "-" * 60)
    print("               PAYTHON ENTERPRISE")
    print("             CNPJ: 00.000.000/0001-00")
    print("               CUPOM FISCAL")
    print("\n" + "-" * 60)

    print("ITEM | PRODUTO     | QTD | PREÇO UNIT | SUBTOTAL")
    print("\n" + "-" * 60)
    total_bruto = 0
    desconto = 0
    for index, produto in enumerate(carrinho, start=1):
        nome = produto["produto"]
        qtd = produto["qtd"]
        preco = produto["preco"]
        subtotal = qtd * preco
        total_bruto += subtotal
        print(
            f"{index:<4} | {nome:<11} | {qtd:<3} | R${preco:5.2f} | R${subtotal:<6.2f}"
        )
    """ aplica o desconto """
    match total_bruto:
        case n if n > 50:
            total_final = total_bruto * 0.90
            desconto = 10.00
        case n if n > 30:
            total_final = total_bruto * 0.95 
            desconto = 5.00
        case _:
            total_final = total_bruto
            desconto = 0

    print("\n" + "-" * 60)
    print()
    print(f"{'TOTAL BRUTO:':<30} R${total_bruto:.2f}")
    print(f"{'DESCONTO:':<30} {desconto}%")
    print(f"{'VALOR FINAL A PAGAR:':<30} R${total_final:.2f}")
    print()
    print("\n" + "-" * 60)

    print("OBRIGADO PELA PREFERÊNCIA! VOLTE SEMPRE ")
    cupom_modifica_qtd_estoque(carrinho, estoque)
    limpar_carrinho()
    carrinho.clear()

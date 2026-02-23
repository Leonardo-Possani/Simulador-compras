from enum import Enum


class MetodoPagamento(str, Enum):
    CREDITO = "credito"
    DEBITO = "debito"
    DINHEIRO = "dinheiro"

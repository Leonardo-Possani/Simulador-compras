import os
import platform


def clear():
    """Limpa a tela."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

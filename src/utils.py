import os
import platform


def clear():
    """limpa a tela"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")



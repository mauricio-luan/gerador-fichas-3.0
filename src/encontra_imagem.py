import sys
import os

def encontrar_imagem(nome_arquivo):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS # type: ignore
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, nome_arquivo)
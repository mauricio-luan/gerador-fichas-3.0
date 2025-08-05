import sys
import os
import logging

logger = logging.getLogger('gerador-fichas-3.0.encontra_imagem')

def encontrar_imagem(nome_arquivo):
    logger.info(f'Procurando imagem: {nome_arquivo}')
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS # type: ignore
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, nome_arquivo)
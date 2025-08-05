import logging
import sys

def configurar_logger(nome_logger='gerador-fichas-3.0'):
    logger = logging.getLogger(nome_logger)
    logger.setLevel(logging.DEBUG) # Define o nível mais baixo para o logger

    # Evitar que logs sejam duplicados se a função for chamada múltiplas vezes
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s] - %(message)s')

    # Handler para o console (exibe INFO e acima)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO) # Apenas INFO ou mais graves irão para o console
    console_handler.setFormatter(formatter)

    # Handler para o arquivo (salva TUDO, desde DEBUG)
    file_handler = logging.FileHandler('app.log', mode='w') # 'w' para reescrever o arquivo a cada execução
    file_handler.setLevel(logging.DEBUG) # Tudo a partir de DEBUG será salvo no arquivo
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
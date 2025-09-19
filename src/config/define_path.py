import sys
from pathlib import Path


def define_path(relative_path: str) -> Path:
    """
    Retorna o caminho absoluto para a imagem, seja em
    desenvolvimento ou como executável PyInstaller
    """
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(__file__).parent.parent

    return base_path / relative_path

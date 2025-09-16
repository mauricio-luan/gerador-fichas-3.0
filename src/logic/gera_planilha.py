from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.drawing.image import Image
import logging

logger = logging.getLogger("gerador-fichas-3.0.gera_planilha")


def gerar_planilha_estilizada(dados, arquivo_excel, caminho_imagem):
    """Gera a ficha de implantação com os dados do cliente"""
    logger.debug("Iniciando criacao da planilha")

    wb = Workbook()
    ws = wb.active
    ws.title = "Sitef"  # type: ignore

    fonte_negrito = Font(bold=True)
    fonte_branca = Font(color="FFFFFF", bold=True)
    fonte_cinza_claro = Font(color="808080", bold=True)
    alinhamento_central = Alignment(
        horizontal="center", vertical="center", wrap_text=True
    )
    alinhamento_esquerda = Alignment(
        horizontal="left", vertical="center", wrap_text=True
    )
    borda_fina = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )
    preenchimento_cabecalho = PatternFill(
        start_color="171717", end_color="171717", fill_type="solid"
    )
    preenchimento_secoes = PatternFill(
        start_color="CCCCCC", end_color="CCCCCC", fill_type="solid"
    )

    ws.column_dimensions["A"].width = 17  # type: ignore
    ws.column_dimensions["B"].width = 50  # type: ignore

    ws["A1"].value = "PAYER"  # type: ignore
    ws["A1"].font = fonte_branca  # type: ignore
    ws["A1"].alignment = alinhamento_central  # type: ignore
    ws["A1"].fill = preenchimento_cabecalho  # type: ignore
    ws["A1"].border = borda_fina  # type: ignore

    img = Image(caminho_imagem)
    img.width = 120
    img.height = 19
    ws.add_image(img, "A1")  # type: ignore

    ws["B1"].value = "FICHA DE IMPLANTAÇÃO"  # type: ignore
    ws["B1"].font = fonte_branca  # type: ignore
    ws["B1"].alignment = alinhamento_central  # type: ignore
    ws["B1"].fill = preenchimento_cabecalho  # type: ignore
    ws["B1"].border = borda_fina  # type: ignore

    linha_atual = 2
    for chave, valor in dados.items():
        if chave == "Conta":
            ws.merge_cells(f"A{linha_atual}:B{linha_atual}")  # type: ignore
            ws[f"A{linha_atual}"].value = "DADOS PAYER"  # type: ignore
            ws[f"A{linha_atual}"].font = fonte_negrito  # type: ignore
            ws[f"A{linha_atual}"].alignment = alinhamento_central  # type: ignore
            ws[f"A{linha_atual}"].fill = preenchimento_secoes  # type: ignore
            ws[f"A{linha_atual}"].border = borda_fina  # type: ignore
            linha_atual += 1

        ws[f"A{linha_atual}"].value = chave.upper()  # type: ignore
        ws[f"A{linha_atual}"].font = fonte_cinza_claro  # type: ignore
        ws[f"A{linha_atual}"].border = borda_fina  # type: ignore
        ws[f"A{linha_atual}"].alignment = alinhamento_central  # type: ignore

        ws[f"B{linha_atual}"].value = valor  # type: ignore
        ws[f"B{linha_atual}"].border = borda_fina  # type: ignore
        ws[f"B{linha_atual}"].alignment = alinhamento_esquerda  # type: ignore

        if linha_atual in range(13, 18):
            ws[f"B{linha_atual}"].alignment = alinhamento_central  # type: ignore
            ws.column_dimensions["B"].width = 48  # type: ignore

        linha_atual += 1

    wb.save(arquivo_excel)
    logger.info(f"salva em: {arquivo_excel}")

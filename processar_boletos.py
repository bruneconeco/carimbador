import os
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter
import io
import datetime
import os


# configurações
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\Lucas\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def gerar_nome_saida():
    import os
    import datetime

    agora = datetime.datetime.now()
    nome = agora.strftime("boletos_carimbados_%Y-%m-%d_%H-%M.pdf")

    # caminho automático da Área de Trabalho
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # caminho completo para salvar o PDF lá
    return os.path.join(desktop_path, nome)

    # cria a pasta se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # retorna caminho completo
    return os.path.join(pasta_saida, nome)

# cria o carimbo no ponto exato
def criar_carimbo(contrato):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    texto = f"CTO {contrato}"
    c.setFont("Helvetica-Bold", 12)
    x = 300
    y = 800
    c.drawString(x, y, texto)
    c.save()
    buffer.seek(0)
    return PdfReader(buffer)

# busca contrato na planilha com base no OCR
def buscar_contrato_por_ocr(imagem, df):
    texto = pytesseract.image_to_string(imagem, lang="eng").lower()
    for _, linha in df.iterrows():
        nome = str(linha["Inquilino"]).lower()
        endereco = str(linha["Endereço"]).lower()
        if nome in texto or endereco in texto:
            return linha["Contrato/Unidade"]
    return "NÃO ENCONTRADO"

# processa boletos e carimba cada página
def carimbar_boletos(pdf_path, planilha_path, output_path):
    df = pd.read_excel(planilha_path)
    df.columns = df.columns.str.strip()

    pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    original_pdf = PdfReader(pdf_path)
    writer = PdfWriter()

    for i, (imagem, pagina_original) in enumerate(zip(pages, original_pdf.pages), 1):
        contrato = buscar_contrato_por_ocr(imagem, df)
        carimbo = criar_carimbo(contrato)
        pagina_original.merge_page(carimbo.pages[0])
        writer.add_page(pagina_original)
        print(f"✅ Página {i}: CTO → {contrato}")

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"\n📄 PDF carimbado salvo como: {output_path}")

# execução direta
if __name__ == "__main__":
    PLANILHA = "base_contratos.xlsx"
    PDF_ENTRADA = "entrada_boletos/boletos.pdf"  
    PDF_SAIDA = gerar_nome_saida()
    carimbar_boletos(PDF_ENTRADA, PLANILHA, PDF_SAIDA)
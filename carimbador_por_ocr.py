import os
import io
import datetime
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter
from PIL import Image
import pandas as pd
import unidecode
import fitz
import re


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"


def normalizar(texto):
    texto = texto.lower()
    texto = unidecode.unidecode(texto)
    texto = ''.join(c for c in texto if c.isalnum() or c.isspace())
    return texto.strip()


def extrair_imagens_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return [Image.frombytes("RGB", [p.get_pixmap(dpi=300).width, p.get_pixmap(dpi=300).height], p.get_pixmap(dpi=300).samples) for p in doc]


def extrair_endereco_inquilino(texto):
    texto_limpo = normalizar(texto)
    endereco, inquilino = "", ""

    match_end = re.search(r"(fianca|fiança)\s+([\w\s\-.,/]{5,})", texto_limpo)
    match_inq = re.search(r"(garantido[s]?)\s+([\w\s\-.,/]{5,})", texto_limpo)

    if match_end:
        endereco = match_end.group(2).strip()
    if match_inq:
        inquilino = match_inq.group(2).strip()

    return endereco, inquilino


def buscar_contrato(df, endereco_ocr, inquilino_ocr):
    for _, linha in df.iterrows():
        if normalizar(str(linha["Endereço"])) in endereco_ocr and normalizar(str(linha["Inquilino"])) in inquilino_ocr:
            return linha["Contrato/Unidade"]
    return None


def criar_carimbo(texto):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, 800, f"CTO {texto}")
    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


def carimbar_boletos(pdf_path, planilha_path):
    df = pd.read_excel(planilha_path)
    df.columns = [col.strip() for col in df.columns]

    if not all(col in df.columns for col in ["Endereço", "Inquilino", "Contrato/Unidade"]):
        raise ValueError("A planilha precisa conter: Endereço, Inquilino, Contrato/Unidade")

    reader = PdfReader(pdf_path)
    imagens = extrair_imagens_pdf(pdf_path)
    writer_carimbados = PdfWriter()
    writer_ignorados = PdfWriter()

    total_carimbados, total_ignorados = 0, 0

    for i, (page, imagem) in enumerate(zip(reader.pages, imagens)):
        texto_ocr = pytesseract.image_to_string(imagem, lang="por")
        endereco, inquilino = extrair_endereco_inquilino(texto_ocr)
        contrato = buscar_contrato(df, endereco, inquilino)

        print(f"\n[🔍] Página {i+1}")
        print(f"Endereço: {endereco or '⚠️ Não encontrado'}")
        print(f"Inquilino: {inquilino or '⚠️ Não encontrado'}")

        if contrato:
            carimbo_pdf = criar_carimbo(contrato)
            page.merge_page(carimbo_pdf.pages[0])
            writer_carimbados.add_page(page)
            total_carimbados += 1
            print(f"[✔] Carimbada com CTO {contrato}")
        else:
            writer_ignorados.add_page(page)
            total_ignorados += 1
            print(f"[✘] Ignorada — dados não reconhecidos")

    
    nome_base = datetime.datetime.now().strftime("boletos_%Y-%m-%d_%H-%M")
    caminho = os.path.join(os.path.expanduser("~"), "Desktop")

    with open(os.path.join(caminho, f"{nome_base}_carimbados.pdf"), "wb") as f:
        writer_carimbados.write(f)
    with open(os.path.join(caminho, f"{nome_base}_ignorados.pdf"), "wb") as f:
        writer_ignorados.write(f)

    print("\n📊 Resumo final:")
    print(f"- Total de páginas: {total_carimbados + total_ignorados}")
    print(f"- Carimbadas: {total_carimbados}")
    print(f"- Ignoradas: {total_ignorados}")
    print("\n📁 Arquivos salvos na Área de Trabalho.")

    return total_carimbados, total_ignorados  


if __name__ == "__main__":
    PLANILHA = "base_contratos.xlsx"
    PDF_ENTRADA = "entrada_boletos/boletos.pdf"
    carimbar_boletos(PDF_ENTRADA, PLANILHA)

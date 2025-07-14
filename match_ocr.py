import pandas as pd
from pdf2image import convert_from_path
import pytesseract

# ativa Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# função para extrair texto do boleto
def ocr_pdf(path_pdf):
    pages = convert_from_path(
        path_pdf,
        dpi=300,
        poppler_path=r"C:\Users\Lucas\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    )
    texto = ""
    for img in pages:
        texto += pytesseract.image_to_string(img, lang="eng") + "\n"
    return texto

# verifica correspondência com a planilha
def buscar_contrato(texto_extraido, df):
    texto_lower = texto_extraido.lower()
    for _, linha in df.iterrows():
        nome = str(linha["Inquilino"]).lower()
        endereco = str(linha["Endereço"]).lower() 
        if nome in texto_lower or endereco in texto_lower:
            return linha
    return None

if __name__ == "__main__":
    # carrega a planilha e limpa nomes de colunas
    df = pd.read_excel("base_contratos.xlsx")
    df.columns = df.columns.str.strip()

    # extrai texto do PDF
    texto = ocr_pdf("boleto_teste.pdf")

    # busca correspondência
    resultado = buscar_contrato(texto, df)

    if resultado is not None:
        print("\n✅ Contrato encontrado:")
        print(resultado)
    else:
        print("\n❌ Nenhuma correspondência encontrada. Tente verificar o nome ou endereço na planilha.")

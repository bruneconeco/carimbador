import pytesseract
from pdf2image import convert_from_path

# Caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_pdf(path_pdf):
    pages = convert_from_path(
        path_pdf,
        dpi=300,
        poppler_path=r"C:\Users\Lucas\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    )
    texto_total = ""
    for i, img in enumerate(pages, 1):
        txt = pytesseract.image_to_string(img, lang="eng")
        print(f"Página {i}: {len(txt)} caracteres OCR")
        texto_total += txt + "\n"
    return texto_total

if __name__ == "__main__":
    resultado = ocr_pdf("boleto_teste.pdf")
    print("\n--- Trecho extraído ---\n")
    print(resultado[:800])

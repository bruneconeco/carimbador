import os
import fitz  


print("Pasta atual:", os.getcwd())
print("Arquivos na pasta:", os.listdir())

def extract_text_from_pdf(path):
    print(f"\nAbrindo {path}…")
    text = ""
    with fitz.open(path) as doc:
        print("Número de páginas:", doc.page_count)
        for i, page in enumerate(doc, start=1):
            page_text = page.get_text()
            print(f"  – Página {i}: {len(page_text)} caracteres extraídos")
            text += page_text
    return text

if __name__ == "__main__":
    arquivo = "boleto_teste.pdf"
    texto = extract_text_from_pdf(arquivo)
    print("\nTrecho do texto extraído:")
    print(texto[:500] or "(texto vazio!)")
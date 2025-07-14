import os

pasta_bin = r"C:\Users\Lucas\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"


caminho_pdfinfo = os.path.join(pasta_bin, "pdfinfo.exe")

print("Arquivo existe?", os.path.isfile(caminho_pdfinfo))
print("Conteúdo de bin:", os.listdir(pasta_bin))
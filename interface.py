import tkinter as tk
from tkinter import filedialog, messagebox
from processar_boletos import carimbar_boletos, gerar_nome_saida

def selecionar_pdf():
    caminho = filedialog.askopenfilename(title="Selecione o PDF dos boletos", filetypes=[("PDF Files", "*.pdf")])
    entrada_pdf.set(caminho)

def selecionar_planilha():
    caminho = filedialog.askopenfilename(title="Selecione a planilha de contratos", filetypes=[("Excel Files", "*.xlsx")])
    entrada_planilha.set(caminho)


def processar():
    pdf = entrada_pdf.get()
    xlsx = entrada_planilha.get()
    if not pdf or not xlsx:
        messagebox.showwarning("Aviso", "Selecione os dois arquivos antes de processar.")
        return

    output_path = gerar_nome_saida()
    carimbar_boletos(pdf, xlsx, output_path)
    messagebox.showinfo("Sucesso", "Boletos carimbados com sucesso!")
    print(f"✅ PDF carimbado foi salvo em: {os.path.abspath(output_path)}")


# interface
import os
import sys
import tkinter as tk

janela = tk.Tk()  

if getattr(sys, 'frozen', False):
    caminho_base = sys._MEIPASS
else:
    caminho_base = os.path.dirname(__file__)

janela.iconbitmap(os.path.join(caminho_base, "logo.ico"))

janela.title("Carimbador de Boletos")
janela.geometry("500x250")

entrada_pdf = tk.StringVar()
entrada_planilha = tk.StringVar()

tk.Label(janela, text="PDF de Boletos:").pack(pady=5)
tk.Entry(janela, textvariable=entrada_pdf, width=60).pack()
tk.Button(janela, text="Selecionar PDF", command=selecionar_pdf).pack(pady=5)

tk.Label(janela, text="Planilha de Contratos:").pack(pady=5)
tk.Entry(janela, textvariable=entrada_planilha, width=60).pack()
tk.Button(janela, text="Selecionar Planilha", command=selecionar_planilha).pack(pady=5)

tk.Button(janela, text="🖋️ Processar Boletos", command=processar, bg="green", fg="white").pack(pady=15)

janela.mainloop()


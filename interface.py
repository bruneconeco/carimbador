import tkinter as tk
from tkinter import filedialog, messagebox
from carimbador_por_ocr import carimbar_boletos 
import os
import sys

def selecionar_pdf():
    caminho_pdf.set(filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")]))

def selecionar_planilha():
    caminho_planilha.set(filedialog.askopenfilename(filetypes=[("Planilhas Excel", "*.xlsx")]))

def executar_carimbador():
    if not caminho_pdf.get() or not caminho_planilha.get():
        messagebox.showwarning("Aviso", "Selecione o PDF e a planilha de contratos.")
        return
    try:
        total_carimbados, total_ignorados = carimbar_boletos(caminho_pdf.get(), caminho_planilha.get())
        messagebox.showinfo("Processamento Concluído",
                            f"✅ Carimbados: {total_carimbados}\n✘ Ignorados: {total_ignorados}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))


if hasattr(sys, "_MEIPASS"):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.abspath(".")

icone_path = os.path.join(base_dir, "icone.ico")

janela = tk.Tk()
janela.title("Carimbador de Boletos")
janela.geometry("420x220")
janela.resizable(False, False)
janela.iconbitmap(icone_path)

caminho_pdf = tk.StringVar()
caminho_planilha = tk.StringVar()

tk.Label(janela, text="PDF de Boletos:", font=("Helvetica", 10)).pack(pady=(10, 0))
tk.Entry(janela, textvariable=caminho_pdf, width=50).pack()
tk.Button(janela, text="Escolher PDF", command=selecionar_pdf).pack(pady=5)

tk.Label(janela, text="Planilha de Contratos:", font=("Helvetica", 10)).pack()
tk.Entry(janela, textvariable=caminho_planilha, width=50).pack()
tk.Button(janela, text="Escolher Planilha", command=selecionar_planilha).pack(pady=5)

tk.Button(janela, text="Carimbar boletos", command=executar_carimbador, bg="green", fg="white").pack(pady=10)

janela.mainloop()

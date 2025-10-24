import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re
import pdfplumber
import requests
from datetime import datetime







janela=tk.Tk()
janela.title("Verificador de Feriados")
janela.geometry("600x420")


frame = ttk.Frame(janela, padding=10)
frame.pack(fill="both", expand=True)

botao_pdf = ttk.Button(frame, text="Selecionar PDF", command=selecionar_pdf)
botao_pdf.pack(pady=6)

cols = ("Data", "Status")
tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True, pady=8)

botao_verificar = ttk.Button(frame, text="Verificar feriados", command=lambda: messagebox.showinfo("Info", "."), state="disabled")
botao_verificar.pack(pady=6)

label_info = ttk.Label(frame, text="Formato procurado: YYYY/dd/mm. Clique em 'Selecionar PDF' para começar.")
label_info.pack(pady=4)

janela.mainloop()

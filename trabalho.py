import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re
import pdfplumber
import requests
from datetime import datetime


def extrair_datas(texto):
    if not texto:
        return []
    padrao = r'\b\d{4}-\d{2}-\d{2}\b'
    return re.findall(padrao, texto)


def ler_pdf(caminho):
    try:
        texto = ""
        with pdfplumber.open(caminho) as pdf:
            for pagina in pdf.pages:
                pagina_texto = pagina.extract_text()
                if pagina_texto:
                    texto += pagina_texto + "\n"
        return texto
    except Exception as e:
        raise RuntimeError(f"Erro ao ler PDF: {e}")


def atualizar_tabela(datas, feriados=None):
    for item in tree.get_children():
        tree.delete(item)
    for data in datas:
        status = "Aguardando verificação..."
        if feriados:  # Se feriados for fornecido, verifique se a data é feriado
            for feriado in feriados:
                if feriado['date'] == data:
                    status = "É feriado!"
                    break
            else:
                status = "Não é feriado"
        tree.insert("", "end", values=(data, status))


def selecionar_pdf():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if not caminho:
        return
    try:
        texto = ler_pdf(caminho)
    except Exception as e:
        messagebox.showerror("Erro ao abrir PDF", str(e))
        return
    datas = extrair_datas(texto)
    if not datas:
        messagebox.showinfo("Nenhuma data encontrada", "Nenhuma data foi detectada no PDF.")
        atualizar_tabela([], [])
        return
    datas_unicas = list(set(datas))  # Remover datas duplicadas
    atualizar_tabela(datas_unicas)
    botao_verificar.config(state="normal")


def buscar_feriados_ano(ano, datas_pdf):
    try:
        url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/BR"
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        feriados = resposta.json()
        feriados_filtrados = []
        print(f"Feriados de {ano}:")
        for f in feriados:
            if f['date'] in datas_pdf:
                print(f"  - {f['date']} → {f['localName']}")
                feriados_filtrados.append(f)
        return feriados_filtrados
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de conexão", f"Não foi possível conectar à API:\n{e}")
        return []
    except Exception as e:
        messagebox.showerror("Erro inesperado", str(e))
        return []


def verificar_feriados():
    itens = tree.get_children()
    if not itens:
        messagebox.showinfo("Aviso", "Nenhuma data disponível para verificar.")
        return
    datas = [tree.item(i)["values"][0] for i in itens]
    anos = sorted(set(d.split("-")[0] for d in datas))
    
    # Buscar os feriados de todos os anos
    feriados_totais = []
    for ano in anos:
        feriados_totais.extend(buscar_feriados_ano(ano, datas))
    
    # Atualizar a tabela com o status dos feriados
    atualizar_tabela(datas, feriados_totais)


janela = tk.Tk()
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

botao_verificar = ttk.Button(frame, text="Verificar feriados", command=verificar_feriados, state="disabled")
botao_verificar.pack(pady=6)

label_info = ttk.Label(frame, text="Formato procurado: YYYY-MM-DD. Clique em 'Selecionar PDF' para começar.")
label_info.pack(pady=4)

janela.mainloop()

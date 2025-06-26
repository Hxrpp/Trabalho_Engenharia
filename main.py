import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import calculos  # importa suas funções de cálculo

def somente_numeros(char):
    if char == "":
        return True
    return all(c.isdigit() or c in [".", ","] for c in char) and char.count('.') <= 1 and char.count(',') <= 1

def calcular():
    try:
        analise = combo.get()
        if analise == "Umidade":
            resultado = calculos.umidade(
                float(entry1.get().replace(",", ".")),
                float(entry2.get().replace(",", "."))
            )
            messagebox.showinfo("Resultado", f"Umidade: {resultado:.2f}%")

        elif analise == "Cinzas":
            resultado = calculos.cinzas(
                float(entry1.get().replace(",", ".")),
                float(entry2.get().replace(",", "."))
            )
            messagebox.showinfo("Resultado", f"Cinzas: {resultado:.2f}%")

        elif analise == "Proteínas (Kjeldahl)":
            resultado = calculos.proteinas_kjeldahl(
                float(entry1.get().replace(",", ".")),
                float(entry2.get().replace(",", ".")),
                float(entry3.get().replace(",", "."))
            )
            messagebox.showinfo("Resultado", f"Proteína: {resultado:.2f}%")

        elif analise == "Lipídios (Soxhlet)":
            resultado = calculos.lipidios_soxhlet(
                float(entry1.get().replace(",", ".")),
                float(entry2.get().replace(",", "."))
            )
            messagebox.showinfo("Resultado", f"Lipídios: {resultado:.2f}%")

        elif analise == "pH":
            valor_ph = float(entry1.get().replace(",", "."))
            tipo = calculos.ph(valor_ph)
            messagebox.showinfo("Resultado", f"pH: {valor_ph:.2f} - Solução {tipo}")

        elif analise == "Acidez Titulável":
            resultado = calculos.acidez_titulavel(
                float(entry1.get().replace(",", ".")),
                float(entry2.get().replace(",", ".")),
                float(entry3.get().replace(",", ".")),
                float(entry4.get().replace(",", "."))
            )
            messagebox.showinfo("Resultado", f"Acidez Titulável: {resultado:.2f}%")

        elif analise == "Densidade":
            resultado = calculos.densidade(
                float(entry1.get().replace(",", ".")),
                float(entry2.get().replace(",", "."))
            )
            messagebox.showinfo("Resultado", f"Densidade: {resultado:.2f} g/mL")

        else:
            messagebox.showwarning("Erro", "Selecione uma análise válida.")

    except ValueError:
        messagebox.showerror("Erro", "Preencha todos os campos com valores numéricos válidos.")

def atualizar_campos(event=None):
    analise = combo.get()
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    campos = {
        "Umidade": ["Peso inicial (g)", "Peso final (g)"],
        "Cinzas": ["Peso amostra (g)", "Peso resíduo (g)"],
        "Proteínas (Kjeldahl)": ["Volume HCl (mL)", "Fator de correção", "Peso amostra (g)"],
        "Lipídios (Soxhlet)": ["Peso resíduo (g)", "Peso amostra (g)"],
        "pH": ["Valor de pH"],
        "Acidez Titulável": ["Volume NaOH (mL)", "Normalidade", "Fator do ácido", "Peso amostra (g)"],
        "Densidade": ["Massa (g)", "Volume (mL)"]
    }

    entradas = campos.get(analise, [])

    global entry1, entry2, entry3, entry4
    entry1 = entry2 = entry3 = entry4 = None

    for i, label in enumerate(entradas):
        lbl = tb.Label(frame_inputs, text=label)
        lbl.grid(row=i, column=0, pady=6, sticky="w")

        vcmd = (root.register(somente_numeros), "%P")
        entry = tb.Entry(frame_inputs, bootstyle="info", validate="key", validatecommand=vcmd)
        entry.grid(row=i, column=1, pady=6, sticky="ew")

        if i == 0: entry1 = entry
        elif i == 1: entry2 = entry
        elif i == 2: entry3 = entry
        elif i == 3: entry4 = entry
    frame_inputs.columnconfigure(1, weight=1)

# Janela principal
root = tb.Window(themename="flatly")
root.title("Cálculo de Fórmulas - Análise de Alimentos")
root.geometry("480x530")
root.resizable(True, True)

# Cabeçalho
header = tb.Frame(root, bootstyle="dark", padding=10)
header.pack(side="top", fill="x")
label_header = tb.Label(header, text="Cálculo Automático de Fórmulas",
                        font=("Segoe UI", 14, "bold"), bootstyle="inverse-dark")
label_header.pack()

# Seleção de análise
frm_top = tb.Frame(root, padding=15)
frm_top.pack(fill="x")
label = tb.Label(frm_top, text="Selecione o tipo de análise:", font=("Segoe UI", 12, "bold"))
label.pack(side="left")
combo = tb.Combobox(frm_top, values=[
    "Umidade", "Cinzas", "Proteínas (Kjeldahl)", "Lipídios (Soxhlet)", "pH", "Acidez Titulável", "Densidade"
], state="readonly", bootstyle="secondary")
combo.pack(side="right", fill="x", expand=True, padx=(10,0))
combo.bind("<<ComboboxSelected>>", atualizar_campos)

# Área de entrada dinâmica
frame_inputs = tb.Frame(root, padding=15)
frame_inputs.pack(fill="both", expand=True)

# Botão calcular
btn_calcular = tb.Button(root, text="Calcular", bootstyle="success", command=calcular)
btn_calcular.pack(pady=15, ipadx=15, ipady=8)

# Imagem decorativa (se houver)
try:
    img = Image.open("tubo_ensaio.png")
    nova_largura = 150
    largura_original, altura_original = img.size
    nova_altura = int((nova_largura / largura_original) * altura_original)
    img = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    label_img = tb.Label(root, image=img_tk)
    label_img.pack(side="bottom", pady=10)
except FileNotFoundError:
    messagebox.showwarning("Imagem não encontrada", "Arquivo 'tubo_ensaio.png' não foi encontrado na pasta.")

root.mainloop()
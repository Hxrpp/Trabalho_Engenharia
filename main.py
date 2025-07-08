import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import calculos

def somente_numeros(char):
    if char == "":
        return True
    return all(c.isdigit() or c in [".", ","] for c in char) and char.count('.') <= 1 and char.count(',') <= 1

def calcular():
    try:
        analise = combo.get()

        if analise == "Umidade":
            peso_inicial = float(entry1.get().replace(",", "."))
            peso_final = float(entry2.get().replace(",", "."))

            if peso_inicial <= 0 or peso_final < 0:
                raise ValueError

            resultado = calculos.umidade(peso_inicial, peso_final)
            formula = "((Peso inicial - Peso final) / Peso inicial) × 100"
            messagebox.showinfo("Resultado", f"Umidade: {resultado:.2f}%\n\nFórmula usada:\n{formula}")

        elif analise == "Cinzas":
            peso_amostra = float(entry1.get().replace(",", "."))
            peso_residuo = float(entry2.get().replace(",", "."))

            if peso_amostra <= 0 or peso_residuo < 0:
                raise ValueError

            resultado = calculos.cinzas(peso_amostra, peso_residuo)
            formula = "(Peso resíduo / Peso amostra) × 100"
            messagebox.showinfo("Resultado", f"Cinzas: {resultado:.2f}%\n\nFórmula usada:\n{formula}")

        elif analise == "Proteínas (Kjeldahl)":
            volume = float(entry1.get().replace(",", "."))
            fator = float(entry2.get().replace(",", "."))
            peso_amostra = float(entry3.get().replace(",", "."))

            if volume < 0 or fator <= 0 or peso_amostra <= 0:
                raise ValueError

            resultado = calculos.proteinas_kjeldahl(volume, fator, peso_amostra)
            formula = "(Volume × Fator × 1.4007) / Peso da amostra"
            messagebox.showinfo("Resultado", f"Proteína: {resultado:.2f}%\n\nFórmula usada:\n{formula}")

        elif analise == "Lipídios (Soxhlet)":
            peso_residuo = float(entry1.get().replace(",", "."))
            peso_amostra = float(entry2.get().replace(",", "."))

            if peso_residuo < 0 or peso_amostra <= 0:
                raise ValueError

            resultado = calculos.lipidios_soxhlet(peso_residuo, peso_amostra)
            formula = "(Peso resíduo / Peso amostra) × 100"
            messagebox.showinfo("Resultado", f"Lipídios: {resultado:.2f}%\n\nFórmula usada:\n{formula}")

        elif analise == "pH":
            valor_ph = float(entry1.get().replace(",", "."))
            tipo = calculos.ph(valor_ph)
            messagebox.showinfo("Resultado", f"pH: {valor_ph:.2f} - Solução {tipo}\n\nFórmula: Interpretação de escala de pH")

        elif analise == "Acidez Titulável":
            volume = float(entry1.get().replace(",", "."))
            normalidade = float(entry2.get().replace(",", "."))
            fator = float(entry3.get().replace(",", "."))
            peso_amostra = float(entry4.get().replace(",", "."))

            if volume < 0 or normalidade <= 0 or fator <= 0 or peso_amostra <= 0:
                raise ValueError

            resultado = calculos.acidez_titulavel(volume, normalidade, fator, peso_amostra)
            formula = "(Volume × Normalidade × Fator × 100) / Peso da amostra"
            messagebox.showinfo("Resultado", f"Acidez Titulável: {resultado:.2f}%\n\nFórmula usada:\n{formula}")

        elif analise == "Densidade":
            massa = float(entry1.get().replace(",", "."))
            volume = float(entry2.get().replace(",", "."))

            if massa <= 0 or volume <= 0:
                raise ValueError

            resultado = calculos.densidade(massa, volume)
            formula = "Massa / Volume"
            messagebox.showinfo("Resultado", f"Densidade: {resultado:.2f} g/mL\n\nFórmula usada:\n{formula}")

        else:
            messagebox.showwarning("Erro", "Selecione uma análise válida.")

    except ValueError:
        messagebox.showerror("Erro", "Preencha todos os campos com valores numéricos válidos e não negativos.")

def atualizar_campos(event=None):
    analise = combo.get()
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    campos = {
        "Umidade": [("Peso inicial (g)", "10.0"), ("Peso final (g)", "8.5")],
        "Cinzas": [("Peso amostra (g)", "5.0"), ("Peso resíduo (g)", "0.3")],
        "Proteínas (Kjeldahl)": [("Volume HCl (mL)", "10.0"), ("Fator de correção", "0.1"), ("Peso amostra (g)", "0.5")],
        "Lipídios (Soxhlet)": [("Peso resíduo (g)", "2.5"), ("Peso amostra (g)", "5.0")],
        "pH": [("Valor de pH", "6.8")],
        "Acidez Titulável": [("Volume NaOH (mL)", "10.0"), ("Normalidade", "0.1"), ("Fator do ácido", "0.064"), ("Peso amostra (g)", "0.5")],
        "Densidade": [("Massa (g)", "10.0"), ("Volume (mL)", "5.0")]
    }

    entradas = campos.get(analise, [])

    global entry1, entry2, entry3, entry4
    entry1 = entry2 = entry3 = entry4 = None

    for i, (label_text, default_value) in enumerate(entradas):
        lbl = tb.Label(frame_inputs, text=label_text)
        lbl.grid(row=i, column=0, pady=6, sticky="w")

        vcmd = (root.register(somente_numeros), "%P")
        entry = tb.Entry(frame_inputs, bootstyle="info", validate="key", validatecommand=vcmd)
        entry.insert(0, default_value)
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

# Header
header = tb.Frame(root, bootstyle="dark", padding=10)
header.pack(side="top", fill="x")
label_header = tb.Label(header, text="Cálculo Automático de Fórmulas 2.0",
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
combo.pack(side="right", fill="x", expand=True, padx=(10, 0))
combo.bind("<<ComboboxSelected>>", atualizar_campos)

# Área de entrada
frame_inputs = tb.Frame(root, padding=15)
frame_inputs.pack(fill="both", expand=True)

# Botão calcular
btn_calcular = tb.Button(root, text="Calcular", bootstyle="success", command=calcular)
btn_calcular.pack(pady=15, ipadx=15, ipady=8)

# Imagem dos tubos de ensaio:
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
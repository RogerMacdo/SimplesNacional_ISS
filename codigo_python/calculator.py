import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Função para calcular a alíquota
def calcular_aliquota():
    try:
        receita_bruta = float(entry_receita_bruta.get().replace(',', '.'))
        anexo = combo_anexo.get()
        aplica_fator_r = var_fator_r.get()
        fator_r = 0
        if aplica_fator_r:
            fator_r = float(entry_fator_r.get().replace(',', '.'))
        
        if aplica_fator_r and fator_r >= 0.28:
            anexo = 'Anexo V'
        
        aliquota_efetiva = calcular_aliquota_efetiva(receita_bruta, anexo)
        result.set(f'{aliquota_efetiva:.3f}%')
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para calcular a alíquota efetiva com base no anexo
def calcular_aliquota_efetiva(receita_bruta, anexo):
    if anexo == 'Anexo III':
        return calcular_aliquota_anexo_iii(receita_bruta)
    elif anexo == 'Anexo IV':
        return calcular_aliquota_anexo_iv(receita_bruta)
    elif anexo == 'Anexo V':
        return calcular_aliquota_anexo_v(receita_bruta)
    else:
        return 0

# Função para calcular a alíquota do Anexo III
def calcular_aliquota_anexo_iii(receita_bruta):
    faixas = [
        (180000.00, 0.06, 0.0, 33.50),
        (360000.00, 0.112, 9360.0, 32.00),
        (720000.00, 0.135, 17640.0, 32.50),
        (1800000.00, 0.16, 35640.0, 32.50),
        (3600000.00, 0.21, 125640.0, 33.50),
        (4800000.00, 0.33, 648000.0, 5.00)
    ]
    for faixa in faixas:
        if receita_bruta <= faixa[0]:
            aliquota_nominal = faixa[1]
            parcela_deduzir = faixa[2]
            issqn_percentual = faixa[3] / 100
            aliquota_efetiva = ((receita_bruta * aliquota_nominal) - parcela_deduzir) / receita_bruta * 100
            aliquota_efetiva_issqn = aliquota_efetiva * issqn_percentual
            return aliquota_efetiva_issqn

# Função para calcular a alíquota do Anexo IV
def calcular_aliquota_anexo_iv(receita_bruta):
    faixas = [
        (180000.00, 0.045, 0.0, 44.50),
        (360000.00, 0.09, 8100.0, 40.00),
        (720000.00, 0.102, 12420.0, 40.00),
        (1800000.00, 0.14, 39780.0, 40.00),
        (3600000.00, 0.22, 183780.0, 40.00),
        (4800000.00, 0.33, 828000.0, 5.00)
    ]
    for faixa in faixas:
        if receita_bruta <= faixa[0]:
            aliquota_nominal = faixa[1]
            parcela_deduzir = faixa[2]
            issqn_percentual = faixa[3] / 100
            aliquota_efetiva = ((receita_bruta * aliquota_nominal) - parcela_deduzir) / receita_bruta * 100
            
            if faixa[0] == 3600000.00 and aliquota_efetiva > 12.5:
                issqn_percentual = 5.00 / 100
            
            aliquota_efetiva_issqn = aliquota_efetiva * issqn_percentual
            return aliquota_efetiva_issqn

# Função para calcular a alíquota do Anexo V
def calcular_aliquota_anexo_v(receita_bruta):
    faixas = [
        (180000.00, 0.155, 0.0, 14.00),
        (360000.00, 0.18, 4500.0, 17.00),
        (720000.00, 0.195, 9900.0, 19.00),
        (1800000.00, 0.205, 17100.0, 19.00),
        (3600000.00, 0.23, 62100.0, 23.50),
        (4800000.00, 0.305, 540000.0, 15.50)
    ]
    for faixa in faixas:
        if receita_bruta <= faixa[0]:
            aliquota_nominal = faixa[1]
            parcela_deduzir = faixa[2]
            issqn_percentual = faixa[3] / 100
            aliquota_efetiva = ((receita_bruta * aliquota_nominal) - parcela_deduzir) / receita_bruta * 100
            aliquota_efetiva_issqn = aliquota_efetiva * issqn_percentual
            return aliquota_efetiva_issqn

# Função para limpar os dados
def limpar_dados():
    entry_receita_bruta.delete(0, tk.END)
    combo_anexo.set('')
    var_fator_r.set(False)
    entry_fator_r.delete(0, tk.END)
    entry_fator_r.config(state='disabled')
    result.set('')

# Função para alternar a ativação do campo Fator R
def toggle_fator_r():
    if var_fator_r.get():
        entry_fator_r.config(state='normal')
    else:
        entry_fator_r.config(state='disabled')

# Configuração da Interface
root = tk.Tk()
root.title("Calculadora Simples Nacional")
root.geometry("390x844")  # Dimensões aproximadas de um iPhone 13
root.configure(bg='#000000')

frame = tk.Frame(root, bg='#000000')
frame.pack(pady=20, padx=20, fill='both', expand=True)

# Campo Receita Bruta RBT12
tk.Label(frame, text="Receita Bruta RBT12:", bg='#000000', fg='#ffffff', 
         font=("Arial", 16)).grid(row=0, column=0, sticky=tk.W, columnspan=2)
entry_receita_bruta = tk.Entry(frame, font=("Arial", 20), bg='#333333', fg='#ffffff', 
                              borderwidth=0, justify='right')
entry_receita_bruta.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky='ew')

# Seleção do Anexo
tk.Label(frame, text="Anexo:", bg='#000000', fg='#ffffff', 
         font=("Arial", 16)).grid(row=2, column=0, sticky=tk.W, columnspan=2)
combo_anexo = ttk.Combobox(frame, values=["Anexo III", "Anexo IV", "Anexo V"], font=("Arial", 20), 
                          style="TCombobox")
combo_anexo.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky='ew')

# Checkbox e Campo Fator R
var_fator_r = tk.BooleanVar()
chk_fator_r = tk.Checkbutton(frame, text="Aplicar Fator R:", variable=var_fator_r, 
                            bg='#000000', fg='#ffffff', activebackground='#000000', 
                            activeforeground='#ffffff', font=("Arial", 16), 
                            command=toggle_fator_r, selectcolor="#333333")
chk_fator_r.grid(row=4, column=0, sticky=tk.W, columnspan=2)

entry_fator_r = tk.Entry(frame, font=("Arial", 20), bg='#333333', fg='#ffffff', 
                              borderwidth=0, justify='right', state='disabled')
entry_fator_r.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky='ew')

# Botões
btn_calcular = tk.Button(frame, text="Aliq%", command=calcular_aliquota, 
                        bg='#ff9500', fg='#ffffff', width=4, height=2, 
                        borderwidth=0, highlightthickness=0, font=("Arial", 22, 'bold'), 
                        relief="flat")
btn_calcular.grid(row=6, column=0, padx=5, pady=10, ipadx=5, ipady=5)

btn_limpar = tk.Button(frame, text="CE", command=limpar_dados, bg='#a6a6a6', 
                       fg='#000000', width=4, height=2, borderwidth=0, 
                       highlightthickness=0, font=("Arial", 22, 'bold'), 
                       relief="flat")
btn_limpar.grid(row=6, column=1, padx=5, pady=10, ipadx=5, ipady=5)

# Resultado
result = tk.StringVar()
result.set('')
lbl_result = tk.Label(frame, textvariable=result, font=("Arial", 36), 
                    bg='#000000', fg='#ffffff', justify='right')
lbl_result.grid(row=7, columnspan=2, pady=10, sticky='ew')

# Estilo para o Combobox
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="#333333", background="#333333", 
                foreground="#ffffff", arrowcolor="#ffffff", 
                selectbackground="#ff9500", selectforeground="#ffffff")

root.mainloop()

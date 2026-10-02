import tkinter as tk
from tkinter import messagebox

dashboard = tk.Tk()
dashboard.title("DASHBOARD")
dashboard.geometry("400x500")

lista = tk.Listbox(dashboard)
lista.grid(row=0, column=0, rowspan=100, padx=10, pady=10, sticky="nsew")

# --- CARREGAR TAREFAS AO ABRIR ---
try:
    with open("tarefas.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            tarefa = linha.strip()
            if tarefa:
                lista.insert(tk.END, tarefa)
except FileNotFoundError:
    pass

painel_direita = tk.Frame(dashboard)
painel_direita.grid(row=0, column=1, sticky="n")


# --- FUNÇÃO DEDICADA PARA SALVAR ---
def salvar_tarefas():
    todas_as_tarefas = lista.get(0, tk.END)
    with open("tarefas.txt", "w", encoding="utf-8") as arquivo:
        for tarefa in todas_as_tarefas:
            arquivo.write(tarefa + "\n")


def adicionar():
    item = campo_texto.get().strip()
    if item:
        lista.insert(tk.END, "- " + item)
        campo_texto.delete(0, tk.END)
        salvar_tarefas()  # <--- Salva automaticamente no arquivo ao adicionar!


campo_texto = tk.Entry(painel_direita, width=25)
campo_texto.grid(row=0, column=1)

botao_adicionar = tk.Button(
    painel_direita, text="Adicionar", width=25, command=adicionar
)
botao_adicionar.grid(row=1, column=1, pady=(10, 10))


def excluir():
    selecao = lista.curselection()
    if selecao:
        lista.delete(selecao[0])  # Usa selecao[0]
        salvar_tarefas()  # <--- Salva automaticamente no arquivo ao excluir!
    else:
        messagebox.showerror(
            title="Erro de Seleção",
            message="Selecione uma tarefa na lista antes de excluir!",
        )


botao_excluir = tk.Button(
    painel_direita, text="Excluir", width=25, command=excluir
)
botao_excluir.grid(row=2, column=1)

# Configurações de layout
dashboard.grid_columnconfigure(0, weight=1)
dashboard.grid_rowconfigure(0, weight=1)

dashboard.mainloop()
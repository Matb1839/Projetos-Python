import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk


janela = tk.Tk()
janela.title("Monitor de Despesas")
janela.geometry("1000x700")

#janela.grid_columnconfigure(0, weight=1)

#Frame
frame=tk.Frame(janela)

despesas = {}

#lista de despesas do mes selecionado
lista = tk.Listbox(janela,font=("Arial",15))
janela.grid_columnconfigure(1, weight=1)


#combobox para selecionar o mês
meses = ["Janeiro",
         "Fevereiro",
         "Março",
         "Abril",
         "Maio",
         "Junho",
         "Julho",
         "Agosto",
         "Setembro",
         "Outubro",
         "Novembro",
         "Dezembro"]


combo_meses = ttk.Combobox(frame,values=meses)
label_combobox = tk.Label(frame,text="Mês referente : ",font=("Arial",15))
combo_meses.bind("<<ComboboxSelected>>", lambda e: carregar_despesas())

######lendo .txt para mostrar as despesas cadastradas
### formato---    MES -- categoria : valor
def carregar_despesas():
    lista.delete(0, tk.END)

    # Dicionário para acumular os valores por categoria no gráfico
    despesas_mes = {}
    mes_atual = combo_meses.get()

    try:
        with open("despesas.txt", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue

                if mes_atual in linha:
                    # 1. Insere na Listbox apenas UMA vez
                    lista.insert(tk.END, linha)

                    # 2. Processa os dados para o gráfico de pizza
                    if "--" in linha and ":" in linha:
                        _, resto = linha.split("--")
                        categoria, valor_str = resto.split(":")

                        categoria = categoria.strip()
                        valor_float = float(valor_str.strip())

                        # Soma o valor no dicionário da categoria
                        if categoria in despesas_mes:
                            despesas_mes[categoria] += valor_float
                        else:
                            despesas_mes[categoria] = valor_float

    except FileNotFoundError:
        pass

    # 3. Chama a atualização do gráfico com o dicionário filtrado
    #atualizar_grafico(despesas_mes) 

carregar_despesas()

############## Funcao Adicionar #################
def adicionar():
    despesa = combo_meses.get()+" -- "+combobox_categorias.get()+" : "+"R$ " +entrada.get()
    with open("despesas.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(despesa + "\n")
    carregar_despesas()

############### Fim funcao adicionar#############


categorias = ["Alimentação", "Transporte", "Lazer", "Contas"]
valores = [450.00, 150.00, 200.00, 800.00]


#caixa de digitacao de despesas
entrada = tk.Entry(frame,font=("Arial",20),width=5)
label_entrada = tk.Label(frame,text="Valor a ser adicionado :",font=("Arial",15))

#natureza da despesa a ser adicionada
combobox_categorias = ttk.Combobox(frame,values=categorias)
label_categorias = tk.Label(frame,text="Categoria da despesa",font=("Arial",15))

#botao de adicionar despesa
botao_adicionar = tk.Button(frame,text="ADICIONAR",font=("Arial",15),command=adicionar)

#botao de excluir despesa
botao_excluir = tk.Button(frame,text="EXCLUIR",font=("Arial",15))



figura, ax = plt.subplots(figsize=(5, 4))
ax.pie(
    valores,
    labels=categorias,
    autopct="%1.1f%%",
    startangle=90,
    colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
)
ax.set_title("Distribuição de Gastos")

canvas = FigureCanvasTkAgg(figura, master=janela)
canvas.draw()
canvas_widget = canvas.get_tk_widget()



#organizacao das posicoes
canvas_widget.grid(row=0,column=0,pady=10)
lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
frame.grid(row=1,column=0)
label_combobox.grid(row=0,column=0)
combo_meses.grid(pady=10,row=0,column=1)
label_entrada.grid(row=1,column=0)
entrada.grid(row=1,column=1)
label_categorias.grid(row=2,column=0)
combobox_categorias.grid(row=2,column=1)
botao_adicionar.grid(row=3,column=0,pady=[10,10])
botao_excluir.grid(row=3,column=1,pady=[10,10])

janela.mainloop()

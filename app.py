import ttkbootstrap as ttk # Importando a biblioteca ttkbootstrap
from ttkbootstrap.constants import * # Importando as constantes do ttkbootstrap
from tkinter import messagebox # Importando a biblioteca messagebox do tkinter
from tkinter import Listbox # Importando a biblioteca Listbox do tkinter
from  datetime import datetime # Importando a biblioteca datetime para manipulação de datas e horas
import json # Importando a biblioteca json para manipulação de arquivos JSON

# Array com as lista de tarefas
tarefas = []
ARQUIVO_TAREFAS = "tarefas.json" # Nome do arquivo JSON onde as tarefas serão salvas

def salvar_tarefas():
    with open(ARQUIVO_TAREFAS, "w") as f:
        json.dump(tarefas, f)

def carregar_tarefas():
    global tarefas
    try:
        with open(ARQUIVO_TAREFAS, "r") as f:
            tarefas = json.load(f)
    except FileNotFoundError:
        tarefas = []

# Função para adicionar uma tarefa
def adicionar_tarefa():
    texto = entrada.get() # Pegando as tarefas digitadas pelo usuário
    if texto.strip() != "":
        tarefas.append(texto) # Adicionando a tarefa ao array
        entrada.delete(0, 'end') # Limpando o campo de entrada
        atualizar_lista() # Atualizando a lista de tarefas (Nesse caso a lista é atualizada pra incluir a nova tarefa)
        salvar_tarefas() # Salvando as tarefas no arquivo JSON
    else:
        messagebox.showerror("Erro", "Digite uma tarefa válida!")

# Função para remover uma tarefa da lista
def remover_tarefa():
    try:
        indice = lista.curselection()[0] # Pegando o índice da tarefa selecionada
        tarefas.pop(indice) # Removendo a tarefa do array
        atualizar_lista() # Atualizando a lista de tarefas ( Nesse caso a lista é atualizada pra remover a tarefa selecionada)
        salvar_tarefas() # Salvando as alterações de tarefas no arquivo JSON
    except:
        messagebox.showerrror("Atenção!", "Selecione uma tarefa para remover!") # Mensagem de erro caso o usuário não selecione uma tarefa

# Função para atualizar a lista de tarefas
def atualizar_lista():
    lista.delete(0, 'end') # Limpando a lista de tarefas
    for i, tarefa in enumerate(tarefas):
        lista.insert('end', tarefa) 
        if "[Concluído]" in tarefa:
            lista.itemconfig(i, foreground="green") # Alterando a cor de fundo da tarefa concluída
        else:
            lista.itemconfig(i, foreground="white") # Alterando a cor de fundo da tarefa não concluída

# Função para marcar uma tarefa como concluída

def marcar_concluida():
    try:
        indice = lista.curselection()[0] # Pegando o índice da tarefa selecionada
        tarefa = tarefas[indice] # Pegando a tarefa selecionada
        if " [Concluído] ✅" not in tarefa:
            tarefas[indice] = tarefa + " [Concluído] ✅" # Adicionando a tag de concluído
            atualizar_lista() # Atualizando a lista de tarefas
            salvar_tarefas() # Salvando as alterações de tarefas no arquivo JSON
        else:
            messagebox.showinfo("Atenção!", "Essa tarefa já está marcada como concluída!") # Mensagem de erro caso a tarefa já esteja concluída
    except:
        messagebox.showerror("Atenção!", "Selecione uma tarefa para marcar como concluída!")

# Função para desmarcar uma tarefa como concluída
def desmarcar_concluida():
    try:
        indice = lista.curselection()[0] # Pegando o índice da tarefa selecionada
        tarefa = tarefas[indice]  # Pegando a tarefa selecionada
        if " [Concluído]" in tarefa:
            tarefas[indice] = tarefa.replace(" [Concluído] ✅", "")
            atualizar_lista()
            salvar_tarefas() # Salvando as alterações de tarefas no arquivo JSON
        else:
            messagebox.showinfo("Atenção!", "Essa tarefa ainda não foi concluída!") # Mensagem de erro caso a tarefa ainda não esteja concluída
    except:
        messagebox.showerror("Atenção!", "Selecione uma tarefa para desmarcar como concluída!")

# Função para exibir a data e hora atual
def atualizar_relogio():
    agora = datetime.now() # Pegando a data e hora atual
    texto = agora.strftime("Data: %d/%m/%Y \n Hora: %H:%M:%S") # Formatando a data e hora
    label_relogio.config(text=texto) # Atualizando o texto do label com a data e hora atual
    label_relogio.after(1000, atualizar_relogio) # atualiza a cada 1000 ms (1 segundo)

# ------------------- Estilização da janela principal -------------------

app = ttk.Window(title="Lista de Tarefas", themename="darkly", size=(400, 600)) # Criando a janela principal

label_relogio = ttk.Label(app, text="", font=("Arial", 12)) # Criando o label para exibir a data e hora atual
label_relogio.pack(pady=5) # Adicionando o label na janela

entrada = ttk.Entry(app, width=40) # Criando o campo de entrada de texto
entrada.pack(pady=10) # Adicionando o campo de entrada na janela

botao_adicionar = ttk.Button(app, text="Adicionar tarefa", command=adicionar_tarefa) # Criando o botão de adicionar tarefa
botao_adicionar.pack(pady=5) # Adicionando o botão de adicionar tarefa na janela

botao_remover = ttk.Button(app, text="Remover tarefa", command=remover_tarefa) # Criando o botão de remover tarefa
botao_remover.pack(pady=5) # Adicionando o botão de remover tarefa na janela

botao_atualizar = ttk.Button(app, text="Atualizar lista", command=atualizar_lista) # Criando o botão de atualizar lista
botao_atualizar.pack(pady=5) # Adicionando o botão de atualizar lista na janela

lista = Listbox(app, width=40, height=15) # Criando a lista de tarefas
lista.pack(pady=10) # Adicionando a lista de tarefas na janela

botao_concluida = ttk.Button(app, text="Marcar como concluída", command=marcar_concluida) # Criando o botão de marcar tarefa como concluída
botao_concluida.pack(side="left", padx=(35, 5), pady=0) # Adicionando o botão de marcar tarefa como concluída na janela

botao_remover_concluidda = ttk.Button(app, text="Desmarcar como concluída", command=desmarcar_concluida) # Criando o botão de desmarcar tarefa como concluída
botao_remover_concluidda.pack(side="left", padx=(5, 0), pady=0)  # Adicionando o botão de desmarcar tarefa como concluída na janela

atualizar_relogio() # Chamando a função para atualizar o relógio

carregar_tarefas()     # <-- Adiciona essa linha
atualizar_lista()

app.mainloop() # Iniciando o loop da janela principal
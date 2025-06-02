import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import Listbox
from datetime import datetime
import json
import os

# Variáveis globais
tarefas = []
ARQUIVO_TAREFAS = "tarefas.json"

# Funções de tarefas
def salvar_tarefas():
    with open(ARQUIVO_TAREFAS, "w") as f:
        json.dump(tarefas, f)

def carregar_tarefas():
    global tarefas
    try:
        with open(ARQUIVO_TAREFAS, "r") as f:
            conteudo = json.load(f)
            # Garante que o conteúdo é uma lista
            if isinstance(conteudo, list):
                tarefas = conteudo
            else:
                tarefas = []
    except (FileNotFoundError, json.JSONDecodeError):
        tarefas = []

def adicionar_tarefa():
    texto = entrada.get()
    if texto.strip() != "":
        tarefas.append(texto)
        entrada.delete(0, 'end')
        atualizar_lista()
        salvar_tarefas()
    else:
        messagebox.showerror("Erro", "Digite uma tarefa válida!")

def remover_tarefa():
    try:
        indice = lista.curselection()[0]
        tarefas.pop(indice)
        atualizar_lista()
        salvar_tarefas()
    except:
        messagebox.showerror("Atenção!", "Selecione uma tarefa para remover!")

def atualizar_lista():
    lista.delete(0, 'end')
    for i, tarefa in enumerate(tarefas):
        lista.insert('end', tarefa)
        if "[Concluído]" in tarefa:
            lista.itemconfig(i, foreground="green")
        else:
            lista.itemconfig(i, foreground="white")

def marcar_concluida():
    try:
        indice = lista.curselection()[0]
        tarefa = tarefas[indice]
        if " [Concluído] ✅" not in tarefa:
            tarefas[indice] = tarefa + " [Concluído] ✅"
            atualizar_lista()
            salvar_tarefas()
        else:
            messagebox.showinfo("Atenção!", "Essa tarefa já está marcada como concluída!")
    except:
        messagebox.showerror("Atenção!", "Selecione uma tarefa para marcar como concluída!")

def desmarcar_concluida():
    try:
        indice = lista.curselection()[0]
        tarefa = tarefas[indice]
        if " [Concluído]" in tarefa:
            tarefas[indice] = tarefa.replace(" [Concluído] ✅", "")
            atualizar_lista()
            salvar_tarefas()
        else:
            messagebox.showinfo("Atenção!", "Essa tarefa ainda não foi concluída!")
    except:
        messagebox.showerror("Atenção!", "Selecione uma tarefa para desmarcar como concluída!")

# Funções de usuários
def carregar_usuarios():
    if not os.path.exists("usuarios.json"):
        return {}
    with open("usuarios.json", "r") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return {}

def salvar_usuarios(login, senha):
    usuarios = carregar_usuarios()
    usuarios[login] = senha
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f)

def criar_conta():
    login = entrada_novo_login.get()
    senha = entrada_nova_senha.get()
    confirmar_senha = entrada_confirmar_senha.get()

    if senha != confirmar_senha:
        messagebox.showerror("Erro", "Senhas não coincidem!")
        return

    usuarios = carregar_usuarios()
    if login in usuarios:
        messagebox.showerror("Erro", "Usuário já cadastrado!")
        return
    salvar_usuarios(login, senha)
    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    mostrar_login()

def fazer_login():
    login = entrada_login.get()
    senha = entrada_senha.get()
    usuarios = carregar_usuarios()
    if login in usuarios and usuarios[login] == senha:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        frame_Login.pack_forget()
        frame_tarefas.pack(pady=10)
        entrada_login.delete(0, 'end')
        entrada_senha.delete(0, 'end')
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")

# Funções de navegação
def mostrar_login():
    frame_cadastro.pack_forget()
    frame_tarefas.pack_forget()
    frame_Login.pack(pady=50)

def mostra_cadastro():
    frame_Login.pack_forget()
    frame_cadastro.pack(pady=30)

# Função para o relógio
def atualizar_relogio():
    agora = datetime.now()
    texto = agora.strftime("Data: %d/%m/%Y \n Hora: %H:%M:%S")
    label_relogio.config(text=texto)
    label_relogio.after(1000, atualizar_relogio)

# ---------- INTERFACE GRÁFICA ----------
app = ttk.Window(title="Lista de Tarefas", themename="darkly", size=(400, 600))

# -------- Tela de Login --------
frame_Login = ttk.Frame(app)

lbl_login = ttk.Label(frame_Login, text="Login", font=("Arial", 16))
lbl_login.pack(pady=10)
entrada_login = ttk.Entry(frame_Login, width=30)
entrada_login.pack(pady=10)

lbl_senha = ttk.Label(frame_Login, text="Senha", font=("Arial", 16))
lbl_senha.pack(pady=10)
entrada_senha = ttk.Entry(frame_Login, show="*", width=30)
entrada_senha.pack(pady=10)

btn_login = ttk.Button(frame_Login, text="Entrar", command=fazer_login)
btn_login.pack(pady=10)

btn_ir_cadastro = ttk.Button(frame_Login, text="Criar uma conta", command=mostra_cadastro)
btn_ir_cadastro.pack(pady=10)

# -------- Tela de Cadastro --------
frame_cadastro = ttk.Frame(app)

lbl_novo_login = ttk.Label(frame_cadastro, text="Novo Usuário", font=("Arial", 16))
lbl_novo_login.pack(pady=10)
entrada_novo_login = ttk.Entry(frame_cadastro, width=30)
entrada_novo_login.pack(pady=10)

lbl_nova_senha = ttk.Label(frame_cadastro, text="Nova Senha", font=("Arial", 16))
lbl_nova_senha.pack(pady=10)
entrada_nova_senha = ttk.Entry(frame_cadastro, show="*", width=30)
entrada_nova_senha.pack(pady=10)

lbl_confirmar_senha = ttk.Label(frame_cadastro, text="Confirmar Senha", font=("Arial", 16))
lbl_confirmar_senha.pack(pady=10)
entrada_confirmar_senha = ttk.Entry(frame_cadastro, show="*", width=30)
entrada_confirmar_senha.pack(pady=10)

btn_criar_conta = ttk.Button(frame_cadastro, text="Criar Conta", command=criar_conta)
btn_criar_conta.pack(pady=10)

btn_voltar_login = ttk.Button(frame_cadastro, text="Voltar para Login", command=mostrar_login)
btn_voltar_login.pack(pady=10)

# -------- Tela de Tarefas --------
frame_tarefas = ttk.Frame(app)

label_relogio = ttk.Label(frame_tarefas, text="", font=("Arial", 12))
label_relogio.pack(pady=5)

entrada = ttk.Entry(frame_tarefas, width=40)
entrada.pack(pady=10)

botao_adicionar = ttk.Button(frame_tarefas, text="Adicionar tarefa", command=adicionar_tarefa)
botao_adicionar.pack(pady=5)

botao_remover = ttk.Button(frame_tarefas, text="Remover tarefa", command=remover_tarefa)
botao_remover.pack(pady=5)

botao_atualizar = ttk.Button(frame_tarefas, text="Atualizar lista", command=atualizar_lista)
botao_atualizar.pack(pady=5)

lista = Listbox(frame_tarefas, width=40, height=15)
lista.pack(pady=10)

botao_concluida = ttk.Button(frame_tarefas, text="Marcar como concluída", command=marcar_concluida)
botao_concluida.pack(side="left", padx=(35, 5), pady=5)

botao_remover_concluida = ttk.Button(frame_tarefas, text="Desmarcar como concluída", command=desmarcar_concluida)
botao_remover_concluida.pack(side="left", padx=(5, 0), pady=5)

btn_logout = ttk.Button(frame_tarefas, text="Sair", command=mostrar_login)
btn_logout.pack(pady=10)

# Inicialização
carregar_tarefas()
atualizar_lista()
atualizar_relogio()
mostrar_login()

app.mainloop()

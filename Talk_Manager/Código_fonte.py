import tkinter as tk
from tkinter import messagebox
import json

# Nome do arquivo para salvar as tarefas
TASKS_FILE = "tasks.json"

def load_tasks():

    """Carrega as tarefas do arquivo JSON."""
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks():

    """Salva as tarefas no arquivo JSON."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

def add_task():

    """Adiciona uma nova tarefa à lista."""
    task = task_entry.get()
    if task:
        tasks.append(task)
        update_listbox()
        save_tasks()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Digite uma tarefa!")

def remove_task():

    """Remove a tarefa selecionada."""
    try:
        selected_index = task_listbox.curselection()[0]
        del tasks[selected_index]
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")

def update_listbox():
    
    """Atualiza a lista de tarefas exibida na interface."""
    
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

# Criar janela principal
root = tk.Tk()
root.title("Gerenciador de Tarefas")
root.geometry("400x400")

# Lista de tarefas carregadas do arquivo
tasks = load_tasks()

# Criar widgets
frame = tk.Frame(root)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=40)
task_entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="Adicionar", command=add_task)
add_button.pack(side=tk.RIGHT)

task_listbox = tk.Listbox(root, width=50, height=15)
task_listbox.pack(pady=10)

remove_button = tk.Button(root, text="Remover Selecionada", command=remove_task)
remove_button.pack()

# Atualiza a lista ao iniciar
task_listbox.bind("<Double-Button-1>", lambda event: remove_task())
update_listbox()

# Iniciar o loop principal da interface gráfica
root.mainloop()

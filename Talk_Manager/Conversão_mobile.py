from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListAdapter
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
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

def save_tasks(tasks):

    """Salva as tarefas no arquivo JSON."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

class TaskManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.tasks = load_tasks()
        
        self.task_input = TextInput(hint_text="Digite uma tarefa")
        self.add_widget(self.task_input)
        
        self.add_button = Button(text="Adicionar")
        self.add_button.bind(on_press=self.add_task)
        self.add_widget(self.add_button)
        
        self.task_list = ListView()
        self.refresh_list()
        self.add_widget(self.task_list)
        
        self.remove_button = Button(text="Remover Selecionada")
        self.remove_button.bind(on_press=self.remove_task)
        self.add_widget(self.remove_button)
    
    def add_task(self, instance):
        task = self.task_input.text.strip()
        if task:
            self.tasks.append(task)
            self.task_input.text = ""
            self.refresh_list()
            save_tasks(self.tasks)
    
    def remove_task(self, instance):
        if self.tasks:
            self.tasks.pop()
            self.refresh_list()
            save_tasks(self.tasks)
    
    def refresh_list(self):
        self.task_list.adapter = ListAdapter(data=self.tasks, cls=Button)

class TaskManagerApp(App):
    def build(self):
        return TaskManager()

if __name__ == "__main__":
    TaskManagerApp().run()

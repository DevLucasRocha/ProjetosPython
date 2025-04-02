import tkinter as tk
from tkinter import font
import math

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        
        # Variável do Display
        self.expressao = ""
        self.var_display = tk.StringVar()
        self.var_display.set("")
        
        # Criar interface
        self.criar_interface()

        # Atalhos do Teclado
        self.root.bind('<Return>', lambda event: self.calcular())  # Pressionar Enter
        self.root.bind('<Key>', self.tecla_pressionada)  # Digitação de teclas
    
    def criar_interface(self):
        """Cria o display e os botões"""
        frame_display = tk.Frame(self.root)
        frame_display.pack(pady=10)

        # Display de Entrada
        self.display = tk.Entry(
            frame_display, 
            textvariable=self.var_display, 
            font=font.Font(size=20), 
            borderwidth=2, 
            relief='solid', 
            justify='right'
        )
        self.display.pack(fill='both', ipady=10)

        # Frame dos Botões
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=10)

        botoes = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('C', '0', '=', '+')
        ]

        for linha, valores in enumerate(botoes):
            for coluna, texto in enumerate(valores):
                btn = tk.Button(
                    frame_botoes, text=texto, font=font.Font(size=15),
                    command=lambda t=texto: self.clique_botao(t),
                    width=5, height=2
                )
                btn.grid(row=linha, column=coluna, padx=5, pady=5)

        # Adicionando tecla de Backspace
        btn_backspace = tk.Button(
            self.root, text="←", font=font.Font(size=15),
            command=self.apagar_ultimo, width=5, height=2
        )
        btn_backspace.pack(pady=5)

    def tecla_pressionada(self, event):
        """Captura entrada do teclado"""
        tecla = event.char

        if tecla.isdigit() or tecla in "+-*/.":
            self.adicionar_expressao(tecla)
        elif tecla == '\r':  # Enter
            self.calcular()
        elif tecla == '\b':  # Backspace
            self.apagar_ultimo()

    def clique_botao(self, valor):
        """Manipula os botões pressionados"""
        if valor == '=':
            self.calcular()
        elif valor == 'C':
            self.limpar_display()
        else:
            self.adicionar_expressao(valor)

    def adicionar_expressao(self, valor):
        """Adiciona valores ao display"""
        self.expressao += valor
        self.var_display.set(self.expressao)

    def apagar_ultimo(self):
        """Remove o último caractere digitado"""
        self.expressao = self.expressao[:-1]
        self.var_display.set(self.expressao)

    def limpar_display(self):
        """Limpa a expressão no display"""
        self.expressao = ""
        self.var_display.set("")

    def calcular(self):
        """Executa a operação matemática"""
        try:
            resultado = eval(self.expressao, {"__builtins__": None}, {"math": math})
            self.var_display.set(str(resultado))
            self.expressao = str(resultado)
        except:
            self.var_display.set("Erro")
            self.expressao = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()

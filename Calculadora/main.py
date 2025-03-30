import tkinter as tk # para criação da interface gráfica
from tkinter import font # para formatação de texto
import math # para cálculos matemáticos
import pygame # para reprodução de música
from PIL import Image, ImageTk # para manipulação de imagens
import os # para manipulação de arquivos e diretórios

class CalculadoraDBZ: # classe principal
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator Ball Z")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        
        # Cores DBZ
        self.COR_FUNDO = '#2a2a2a'
        self.COR_BOTOES = '#ff8c00'  # Laranja
        self.COR_BOTOES_ESPECIAIS = '#00bfff'  # Azul
        self.COR_TEXTO = '#ffffff'
        self.COR_DISPLAY = '#1e1e1e'
        self.COR_DESTAQUE = '#ffd700'  # Amarelo DBZ
        
        # Inicializar pygame para música
        pygame.mixer.init()
        self.musica_ligada = False
        
        # Carregar assets
        self.carregar_assets()
        
        # Variáveis de estado
        self.expressao = ""
        self.historico = []
        
        # Configurar interface
        self.criar_interface()
        
        # Tocar música automaticamente
        self.toggle_musica()
    
    def carregar_assets(self):
        """Carrega imagens e verifica arquivos"""
        try:
            # Verifica se arquivos existem
            if not os.path.exists("dbz_logo.png"):
                raise FileNotFoundError
            
            # Carrega logo DBZ
            img_dbz = Image.open("dbz_logo.png")
            img_dbz = img_dbz.resize((250, 100), Image.LANCZOS)
            self.dbz_logo = ImageTk.PhotoImage(img_dbz)
            
            # Tenta carregar imagem de fundo
            if os.path.exists("dbz_bg.jpg"):
                bg_img = Image.open("dbz_bg.jpg")
                bg_img = bg_img.resize((400, 650), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(bg_img)
            else:
                self.bg_image = None
                
        except Exception as e:
            print(f"Erro ao carregar assets: {e}")
            self.dbz_logo = None
            self.bg_image = None
    
    def criar_interface(self):
        # Cria todos os elementos visuais"""
    
        # Canvas principal
        self.canvas = tk.Canvas(self.root, bg=self.COR_FUNDO, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Fundo com imagem ou cor sólida
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw')
        else:
            self.canvas.config(bg=self.COR_FUNDO)
        
        # Logo DBZ
        if self.dbz_logo:
            self.canvas.create_image(200, 60, image=self.dbz_logo)
        
        # Frame principal
        main_frame = tk.Frame(self.canvas, bg='')
        main_frame.place(relx=0.5, rely=0.55, anchor='center', width=380, height=500)
        
        # Display (visor)
        self.var_display = tk.StringVar()
        self.var_display.set("0")
        
        display = tk.Entry(
            main_frame,
            textvariable=self.var_display,
            font=font.Font(family='Arial Black', size=20),
            borderwidth=0,
            relief='flat',
            justify='right',
            bg=self.COR_DISPLAY,
            fg=self.COR_DESTAQUE,
            insertbackground='#ff0000'
        )
        display.pack(fill='x', ipady=10, pady=(0, 15))
        
        # Frame de botões
        botoes_frame = tk.Frame(main_frame, bg='')
        botoes_frame.pack(expand=True, fill='both')
        
        # Botões numéricos e operações
        botoes = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0), ('√', 4, 1), ('^', 4, 2), ('%', 4, 3)
        ]
        
        for (texto, linha, coluna) in botoes:
            btn = tk.Button(
                botoes_frame,
                text=texto,
                font=font.Font(family='Arial Black', size=12),
                command=lambda t=texto: self.clique_botao(t),
                borderwidth=3,
                relief='raised',
                bg=self.COR_BOTOES,
                fg=self.COR_TEXTO,
                activebackground=self.COR_DESTAQUE,
                activeforeground='#000000'
            )
            btn.grid(
                row=linha,
                column=coluna,
                sticky='nsew',
                padx=2,
                pady=2,
                ipadx=5,
                ipady=10
            )
            botoes_frame.grid_columnconfigure(coluna, weight=1)
            botoes_frame.grid_rowconfigure(linha, weight=1)
        
        # Botão de música
        self.btn_musica = tk.Button(
            self.canvas,
            text="🔊 ON",
            command=self.toggle_musica,
            font=font.Font(size=10),
            bg=self.COR_DESTAQUE,
            fg='#000000',
            borderwidth=2,
            relief='raised'
        )
        self.btn_musica.place(x=10, y=10, width=60, height=30)
        
        # Frame do histórico
        historico_frame = tk.Frame(main_frame, bg='')
        historico_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        tk.Label(
            historico_frame,
            text="Histórico:",
            font=font.Font(family='Arial Black', size=10),
            fg=self.COR_DESTAQUE,
            bg=''
        ).pack(anchor='w')
        
        self.historico_text = tk.Text(
            historico_frame,
            height=5,
            font=font.Font(size=9),
            bg=self.COR_DISPLAY,
            fg=self.COR_TEXTO,
            state='disabled',
            wrap='word'
        )
        self.historico_text.pack(fill='both', expand=True)
        
        # Botão para limpar histórico
        tk.Button(
            historico_frame,
            text="Limpar Histórico",
            command=self.limpar_historico,
            font=font.Font(size=9),
            bg=self.COR_BOTOES,
            fg=self.COR_TEXTO,
            activebackground=self.COR_DESTAQUE
        ).pack(fill='x', pady=(5, 0))
    
    def toggle_musica(self):
        """Liga/desliga a música tema"""
        try:
            if self.musica_ligada:
                pygame.mixer.music.stop()
                self.btn_musica.config(text="🔇 OFF")
            else:
                if os.path.exists("dbz_cha-la.mp3"):
                    pygame.mixer.music.load("dbz_cha-la.mp3")
                    pygame.mixer.music.play(loops=-1)
                self.btn_musica.config(text="🔊 ON")
            self.musica_ligada = not self.musica_ligada
        except Exception as e:
            print(f"Erro na música: {e}")
            self.btn_musica.config(text="❌ Erro")
    
    def clique_botao(self, valor):
        """Gerencia cliques nos botões"""
        if valor == '=':
            self.calcular()
        elif valor == 'C':
            self.limpar_display()
        elif valor == '√':
            self.adicionar_expressao('math.sqrt(')
        elif valor == '^':
            self.adicionar_expressao('**')
        else:
            self.adicionar_expressao(valor)
    
    def adicionar_expressao(self, valor):
        """Atualiza a expressão no display"""
        if self.var_display.get() == "0" and valor not in ['*', '/', '+', '-', '**', 'math.sqrt(']:
            self.expressao = valor
        else:
            self.expressao += valor
        self.var_display.set(self.expressao)
    
    def limpar_display(self):
        """Reseta o display"""
        self.expressao = ""
        self.var_display.set("0")
    
    def calcular(self):
        """Executa o cálculo"""
        try:
            expressao_segura = self.expressao.replace('^', '**')
            
            if not expressao_segura.strip():
                return
            
            resultado = eval(expressao_segura, {'__builtins__': None, 'math': math})
            
            if isinstance(resultado, float):
                resultado = round(resultado, 10)
            
            self.var_display.set(str(resultado))
            
            entrada_historico = f"{self.expressao} = {resultado}"
            self.historico.append(entrada_historico)
            self.atualizar_historico()
            
            self.expressao = str(resultado)
        
        except Exception as e:
            self.var_display.set("Erro")
            self.expressao = ""
    
    def atualizar_historico(self):

        """Atualiza a exibição do histórico"""
        self.historico_text.config(state='normal')
        self.historico_text.delete(1.0, tk.END)
        
        for item in reversed(self.historico[-8:]):
            self.historico_text.insert(tk.END, item + '\n')
        
        self.historico_text.config(state='disabled')
        self.historico_text.yview(tk.END)
    
    def limpar_historico(self):

        """Limpa todo o histórico"""
        self.historico = []
        self.atualizar_historico()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraDBZ(root)
    root.mainloop()
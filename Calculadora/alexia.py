import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

# Inicializa o mecanismo de fala
alexia = pyttsx3.init()
alexia.setProperty('rate', 160)  # velocidade da fala

def falar(texto):
    alexia.say(texto)
    alexia.runAndWait()

def ouvir_comando():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio = reconhecedor.listen(source)
        try:
            comando = reconhecedor.recognize_google(audio, language='pt-BR')
            comando = comando.lower()
            print(f"Você disse: {comando}")
            return comando
        except sr.UnknownValueError:
            print("Não entendi. Pode repetir?")
            return ""
        except sr.RequestError:
            print("Erro ao acessar o serviço de reconhecimento.")
            return ""

def executar_comando(comando):
    if 'tocar' in comando:
        musica = comando.replace('tocar', '')
        falar(f"Tocando {musica}")
        pywhatkit.playonyt(musica)
    elif 'horas' in comando or 'hora' in comando:
        hora = datetime.datetime.now().strftime('%H:%M')
        falar(f"Agora são {hora}")
    elif 'quem é' in comando:
        pessoa = comando.replace('quem é', '')
        info = wikipedia.summary(pessoa, 1, auto_suggest=False)
        print(info)
        falar(info)
    elif 'seu nome' in comando:
        falar("Meu nome é Alexia, prazer em te conhecer!")
    elif 'sair' in comando or 'desligar' in comando:
        falar("Até logo!")
        exit()
    else:
        falar("Desculpe, não entendi o comando.")

# Loop principal
falar("Olá, eu sou a Alexia. Como posso te ajudar?")
while True:
    comando = ouvir_comando()
    if comando:
        executar_comando(comando)

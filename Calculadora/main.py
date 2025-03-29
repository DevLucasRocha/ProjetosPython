from flask import Flask, request, jsonify
from datetime import datetime
import math

app = Flask(__name__)

class Calculadora:
    def __init__(self):
        self.historico = []
    
    def adicionar_ao_historico(self, operacao, resultado):
        registro = {
            'operacao': operacao,
            'resultado': resultado,
            'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.historico.append(registro)
        # Limitar histórico aos 100 últimos registros
        if len(self.historico) > 100:
            self.historico.pop(0)
    
    def somar(self, a, b):
        resultado = a + b
        self.adicionar_ao_historico(f"{a} + {b}", resultado)
        return resultado
    
    def subtrair(self, a, b):
        resultado = a - b
        self.adicionar_ao_historico(f"{a} - {b}", resultado)
        return resultado
    
    def multiplicar(self, a, b):
        resultado = a * b
        self.adicionar_ao_historico(f"{a} * {b}", resultado)
        return resultado
    
    def dividir(self, a, b):
        if b == 0:
            raise ValueError("Divisão por zero não é permitida")
        resultado = a / b
        self.adicionar_ao_historico(f"{a} / {b}", resultado)
        return resultado
    
    def potencia(self, base, expoente):
        resultado = base ** expoente
        self.adicionar_ao_historico(f"{base} ^ {expoente}", resultado)
        return resultado
    
    def raiz_quadrada(self, a):
        if a < 0:
            raise ValueError("Raiz quadrada de número negativo não é permitida")
        resultado = math.sqrt(a)
        self.adicionar_ao_historico(f"√{a}", resultado)
        return resultado
    
    def porcentagem(self, valor, percentual):
        resultado = (valor * percentual) / 100
        self.adicionar_ao_historico(f"{percentual}% de {valor}", resultado)
        return resultado
    
    def obter_historico(self):
        return self.historico
    
    def limpar_historico(self):
        self.historico = []
        return True

calculadora = Calculadora()

@app.route('/api/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    operacao = data.get('operacao')
    a = data.get('a')
    b = data.get('b', None)  # b é opcional para algumas operações
    
    try:
        a = float(a)
        if b is not None:
            b = float(b)
        
        if operacao == 'somar':
            resultado = calculadora.somar(a, b)
        elif operacao == 'subtrair':
            resultado = calculadora.subtrair(a, b)
        elif operacao == 'multiplicar':
            resultado = calculadora.multiplicar(a, b)
        elif operacao == 'dividir':
            resultado = calculadora.dividir(a, b)
        elif operacao == 'potencia':
            resultado = calculadora.potencia(a, b)
        elif operacao == 'raiz_quadrada':
            resultado = calculadora.raiz_quadrada(a)
        elif operacao == 'porcentagem':
            resultado = calculadora.porcentagem(a, b)
        else:
            return jsonify({'erro': 'Operação não suportada'}), 400
        
        return jsonify({
            'resultado': resultado,
            'operacao': operacao,
            'status': 'sucesso'
        })
    
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Ocorreu um erro durante o cálculo'}), 500

@app.route('/api/historico', methods=['GET'])
def obter_historico():
    return jsonify(calculadora.obter_historico())

@app.route('/api/limpar_historico', methods=['POST'])
def limpar_historico():
    calculadora.limpar_historico()
    return jsonify({'status': 'Histórico limpo com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
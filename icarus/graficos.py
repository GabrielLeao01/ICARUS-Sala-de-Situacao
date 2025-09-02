import os
import json

class Graficos:
    def __init__(self, grafico_id=None, recurso_id=None, grafico_data=None):
        self.grafico_id = grafico_id
        self.recurso_id = recurso_id
        self.grafico_data = grafico_data

    @staticmethod
    def listar_graficos():
        pasta = os.path.join(os.path.dirname(__file__), '..', 'graficos')
        arquivos = [f for f in os.listdir(pasta) if f.endswith('.json')]
        return [os.path.splitext(f)[0] for f in arquivos]

    @staticmethod
    def obter_grafico(grafico_id):
        pasta = os.path.join(os.path.dirname(__file__), '..', 'graficos')
        caminho = os.path.join(pasta, f'{grafico_id}.json')
        if not os.path.exists(caminho):
            return None
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def plotar_grafico(data):
        return data

    @staticmethod
    def filtrar_info_grafico(data):
        return data

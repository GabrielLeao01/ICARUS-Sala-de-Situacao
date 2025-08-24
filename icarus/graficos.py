class Graficos:
    def __init__(self, grafico_id, recurso_id, grafico_data):
        self.grafico_id = grafico_id
        self.recurso_id = recurso_id
        self.grafico_data = grafico_data

    @staticmethod
    def listar_graficos():
        return []

    @staticmethod
    def obter_grafico(grafico_id):
        return None

    @staticmethod
    def plotar_grafico(data):
        pass

    @staticmethod
    def filtrar_info_grafico(data):
        pass

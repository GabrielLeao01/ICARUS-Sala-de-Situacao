from dash import html

class Alerta:
    def __init__(self, coordenada_alerta, gravidade, descricao):
        self.coordenada_alerta = coordenada_alerta
        self.gravidade = gravidade
        self.descricao = descricao

    @staticmethod
    def definir_gravidade(row):
        return row.get("gravidade", 1)

    @staticmethod
    def exibir_alertas(gdf):
        alertas = []
        for _, row in gdf.iterrows():
            nome = row.get("nome_area", "Região não identificada")
            alerta = html.Div(f"⚠️ {nome}", style={
                "backgroundColor": "#FFF3CD",
                "padding": "10px",
                "borderRadius": "6px",
                "border": "1px solid #FFEEBA",
                "marginBottom": "8px",
                "color": "#856404"
            })
            alertas.append(alerta)
        return alertas

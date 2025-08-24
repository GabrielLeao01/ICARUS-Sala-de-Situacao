import pandas as pd
import plotly.express as px

class Recursos:
    def __init__(self, df_original, df_reestruturado):
        self.df_original = df_original
        self.df_reestruturado = df_reestruturado
        self.df_ativo = df_reestruturado.copy()

    def listar_recursos(self):
        return self.df_ativo["nome"].dropna().unique().tolist()

    def selecionar_recurso(self, nome):
        return self.df_ativo[self.df_ativo["nome"] == nome]

    def obter_mapa_recurso(self, unidade_dropdown=None):
        dados_filtrados = self.df_ativo.copy()
        if unidade_dropdown:
            dados_filtrados = dados_filtrados[dados_filtrados["nome"] == unidade_dropdown]
        fig = px.scatter_mapbox(
            dados_filtrados,
            lat="latitude",
            lon="longitude",
            hover_name="nome",
            hover_data=dados_filtrados.columns.tolist(),
            zoom=11,
            center={"lat": -25.429, "lon": -49.271},
            mapbox_style="carto-positron"
        )
        fig.update_layout(autosize=True, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def obter_reestruturacao_proposta(self, acatar):
        if acatar:
            self.df_ativo = self.df_reestruturado.copy()
        else:
            self.df_ativo = self.df_original.copy()
        return self.listar_recursos()

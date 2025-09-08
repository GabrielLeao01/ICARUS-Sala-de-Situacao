import os
import pandas as pd
import plotly.express as px

class Recursos:

    @staticmethod
    def atualizar_unidades_popup_controle(recurso, n_acatar_list, n_rejeitar_list):
        import dash
        from dash import html
        import dash_bootstrap_components as dbc
        from datetime import datetime
        import os
        ctx = dash.callback_context
        opcoes = []
        popup = None
        controle = {"atualizar": 0, "usar_reestruturado": False, "recurso": recurso}
        if not recurso:
            return [], None, controle
        if ctx.triggered:
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-acatar" in prop_id:
                controle = {"atualizar": datetime.now().timestamp(), "usar_reestruturado": True, "recurso": recurso}
                return dash.no_update, None, controle
            elif "btn-rejeitar" in prop_id:
                controle = {"atualizar": datetime.now().timestamp(), "usar_reestruturado": False, "recurso": recurso}
                return dash.no_update, None, controle
        df = Recursos.carregar_dados_recurso(recurso, usar_reestruturado=False)
        if df is not None and "nome" in df.columns:
            opcoes = [{"label": nome, "value": nome} for nome in sorted(df["nome"].unique())]
        base_path = os.path.join("shapefiles", "gerenciamento_recursos", recurso, "reestruturada")
        existe_reestruturado = any(f.endswith(".csv") for f in os.listdir(base_path)) if os.path.exists(base_path) else False
        if existe_reestruturado:
            popup = html.Div([
                dbc.Alert([
                    f"Alterações foram feitas na alocação de unidades de {recurso}, deseja acatar?",
                    dbc.Button("Sim", id={"type": "btn-acatar", "index": recurso}, color="success", className="ms-3 me-2", n_clicks=0),
                    dbc.Button("Não", id={"type": "btn-rejeitar", "index": recurso}, color="danger", n_clicks=0)
                ], color="grey", dismissable=False, className="mt-4 mb-2")
            ])
        return opcoes, popup, controle

    @staticmethod
    def obter_mapa_recurso(unidade_dropdown, controle):
        import plotly.graph_objs as go
        import plotly.express as px
        if not controle or "recurso" not in controle:
            return go.Figure()
        recurso = controle["recurso"]
        usar_reestruturado = controle.get("usar_reestruturado", False)
        df = Recursos.carregar_dados_recurso(recurso, usar_reestruturado=usar_reestruturado)
        if df is not None and unidade_dropdown:
            df_sel = df[df["nome"] == unidade_dropdown]
            if not df_sel.empty and "latitude" in df_sel.columns and "longitude" in df_sel.columns:
                fig = px.scatter_mapbox(
                    df_sel,
                    lat="latitude",
                    lon="longitude",
                    hover_name="nome",
                    zoom=12,
                    height=500
                )
                fig.update_layout(mapbox_style="carto-positron",autosize=True, margin={"r": 0, "t": 0, "l": 0, "b": 0})
                return fig
        if df is not None and "latitude" in df.columns and "longitude" in df.columns:
            fig = px.scatter_mapbox(
                df,
                lat="latitude",
                lon="longitude",
                hover_name="nome",
                zoom=11,
                height=500
            )
            fig.update_layout(mapbox_style="carto-positron",autosize=True, margin={"r": 0, "t": 0, "l": 0, "b": 0})
            return fig
        return go.Figure()
    
    def __init__(self, df_original, df_reestruturado):
        self.df_original = df_original
        self.df_reestruturado = df_reestruturado
        self.df_ativo = df_reestruturado.copy()

    @staticmethod
    def listar_recursos():
        base_path = os.path.join("shapefiles", "gerenciamento_recursos")
        return [nome for nome in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, nome))]

    @staticmethod
    def carregar_dados_recurso(recurso, usar_reestruturado=False):
        base_path = os.path.join("shapefiles", "gerenciamento_recursos", recurso)
        if usar_reestruturado:
            path = os.path.join(base_path, "reestruturada", f"unidades_de_{recurso}_reestruturadas.csv")
            if not os.path.exists(path):
                path = os.path.join(base_path, "atual", f"unidades-{recurso}.csv")
        else:
            path = os.path.join(base_path, "atual", f"unidades-{recurso}.csv")
        if os.path.exists(path):
            return pd.read_csv(path)
        return None


    def selecionar_recurso(self, nome):
        return self.df_ativo[self.df_ativo["nome"] == nome]


    def obter_reestruturacao_proposta(self, acatar):
        if acatar:
            self.df_ativo = self.df_reestruturado.copy()
        else:
            self.df_ativo = self.df_original.copy()
        return self.listar_recursos()

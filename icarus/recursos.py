import os
import pandas as pd
import plotly.express as px

import plotly.graph_objs as go
import geopandas as gpd
from shapely import wkt


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
        base_path = os.path.join("shapefiles", "gerenciamento_recursos", recurso, "reestruturada")
        existe_reestruturado = any(os.path.isfile(os.path.join(base_path, f)) for f in os.listdir(base_path)) if os.path.exists(base_path) else False
        if existe_reestruturado:
            popup = html.Div([
                dbc.Alert([
                    f"Alterações foram feitas no recurso {recurso}, deseja acatar?",
                    dbc.Button("Sim", id={"type": "btn-acatar", "index": recurso}, color="success", className="ms-3 me-2", n_clicks=0),
                    dbc.Button("Não", id={"type": "btn-rejeitar", "index": recurso}, color="danger", n_clicks=0)
                ], color="grey", dismissable=False, className="mt-4 mb-2")
            ])
        controle["usar_reestruturado"] = existe_reestruturado

        df = Recursos.carregar_dados_recurso(recurso, usar_reestruturado=controle["usar_reestruturado"])
        if df is not None and "nome" in df.columns:
            opcoes = [{"label": nome, "value": nome} for nome in sorted(df["nome"].unique())]
        return opcoes, popup, controle

    @staticmethod
    def obter_mapa_recurso(unidade_dropdown, controle):
        if not controle or "recurso" not in controle:
            return go.Figure()
        recurso = controle["recurso"]
        usar_reestruturado = controle.get("usar_reestruturado", True)
        if not recurso:
            return go.Figure()

        base_dir = os.path.join("shapefiles", "gerenciamento_recursos", recurso)

        def try_shapefile(subfolder):
            import glob as _glob
            shp_glob = _glob.glob(os.path.join(base_dir, subfolder, "*.shp"))
            if not shp_glob:
                return None
            try:
                gdf = gpd.read_file(shp_glob[0])
            except Exception:
                return None
            try:
                if gdf.crs and gdf.crs.to_string() != "EPSG:4326":
                    gdf = gdf.to_crs(epsg=4326)
            except Exception:
                pass
            try:
                gdf["geometry"] = gdf["geometry"].simplify(0.0005, preserve_topology=True)
            except Exception:
                pass
            return gdf

        gdf = None
        if usar_reestruturado:
            gdf = try_shapefile("reestruturada")
            if gdf is None:
                gdf = try_shapefile("atual")
        else:
            gdf = try_shapefile("atual")
            if gdf is None:
                gdf = try_shapefile("reestruturada")

        if gdf is not None and not gdf.empty:
            geom_types = set(gdf.geometry.geom_type.unique())
            fig = go.Figure()

            if geom_types == {"Point"}:
                fig = px.scatter_mapbox(gdf, lat=gdf.geometry.y, lon=gdf.geometry.x, hover_name=gdf.get("nome"), zoom=11, center={"lat": -25.429, "lon": -49.271})
                fig.update_layout(mapbox_style="carto-positron", autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
                return fig

            for _, row in gdf.iterrows():
                geom = row.geometry
                if geom.geom_type == "LineString":
                    x, y = geom.xy
                    fig.add_trace(go.Scattermapbox(lon=list(x), lat=list(y), mode="lines", line=dict(width=2, color="#007bff"), showlegend=False))
                elif geom.geom_type == "MultiLineString":
                    for line in geom.geoms:
                        x, y = line.xy
                        fig.add_trace(go.Scattermapbox(lon=list(x), lat=list(y), mode="lines", line=dict(width=2, color="#007bff"), showlegend=False))
                elif geom.geom_type == "Polygon":
                    x, y = geom.exterior.xy
                    lon = list(x) + [x[0]]
                    lat = list(y) + [y[0]]
                    fig.add_trace(go.Scattermapbox(lon=lon, lat=lat, mode="lines", fill="toself", fillcolor="rgba(0,123,255,0.15)", line=dict(width=1, color="#007bff"), showlegend=False))
                elif geom.geom_type == "MultiPolygon":
                    for poly in geom.geoms:
                        x, y = poly.exterior.xy
                        lon = list(x) + [x[0]]
                        lat = list(y) + [y[0]]
                        fig.add_trace(go.Scattermapbox(lon=lon, lat=lat, mode="lines", fill="toself", fillcolor="rgba(0,123,255,0.1)", line=dict(width=1, color="#007bff"), showlegend=False))

            fig.update_layout(mapbox_style="carto-positron", autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, mapbox_center={"lat": -25.429, "lon": -49.271}, mapbox_zoom=11, showlegend=False)
            return fig

        df = Recursos.carregar_dados_recurso(recurso, usar_reestruturado=usar_reestruturado)
        if df is not None:
            if "latitude" in df.columns and "longitude" in df.columns:
                df_use = df
                if "nome" in df.columns and unidade_dropdown:
                    df_use = df[df["nome"] == unidade_dropdown]
                fig = px.scatter_mapbox(df_use, lat="latitude", lon="longitude", hover_name=df_use.get("nome"), zoom=11, center={"lat": -25.429, "lon": -49.271})
                fig.update_layout(mapbox_style="carto-positron", autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
                return fig

            if "geometry" in df.columns:
                df["geometry"] = df["geometry"].apply(wkt.loads)
                gdf = gpd.GeoDataFrame(df, geometry="geometry")
                fig = go.Figure()
                for _, row in gdf.iterrows():
                    geom = row.geometry
                    if geom.geom_type == "Point":
                        fig.add_trace(go.Scattermapbox(lon=[geom.x], lat=[geom.y], mode="markers", marker={"size":8, "color":"#007bff"}, showlegend=False))
                    elif geom.geom_type == "LineString":
                        x, y = geom.xy
                        fig.add_trace(go.Scattermapbox(lon=list(x), lat=list(y), mode="lines", line=dict(width=2, color="#007bff"), showlegend=False))
                    elif geom.geom_type == "Polygon":
                        x, y = geom.exterior.xy
                        lon = list(x) + [x[0]]
                        lat = list(y) + [y[0]]
                        fig.add_trace(go.Scattermapbox(lon=lon, lat=lat, mode="lines", fill="toself", fillcolor="rgba(0,123,255,0.15)", line=dict(width=1, color="#007bff"), showlegend=False))
                fig.update_layout(mapbox_style="carto-positron", autosize=True, margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
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
        import glob
        base_path = os.path.join("shapefiles", "gerenciamento_recursos", recurso)
        pasta = "reestruturada" if usar_reestruturado else "atual"
        dir_path = os.path.join(base_path, pasta)
        if not os.path.exists(dir_path):
            return None
        arquivos_csv = glob.glob(os.path.join(dir_path, "*.csv"))
        if arquivos_csv:
            return pd.read_csv(arquivos_csv[0])
        return None

    def selecionar_recurso(self, nome):
        return self.df_ativo[self.df_ativo["nome"] == nome]

    def obter_reestruturacao_proposta(self, acatar):
        if acatar:
            self.df_ativo = self.df_reestruturado.copy()
        else:
            self.df_ativo = self.df_original.copy()
        return self.listar_recursos()

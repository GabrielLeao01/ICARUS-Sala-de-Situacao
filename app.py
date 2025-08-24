import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime
import plotly.express as px

from icarus.situacao import Situacao
from icarus.alerta import Alerta
from icarus.recursos import Recursos
from icarus.graficos import Graficos

import pandas as pd

CSV_PATH = "shapefiles/unidades-saude.csv"
SHAPE_PATH = "shapefiles/area_prioritaria.shp"
CSV_REESTRUTURADO_PATH = "shapefiles/unidades_de_saude_reestruturadas.csv"

df_saude = pd.read_csv(CSV_PATH)
df_saude_reestruturado = pd.read_csv(CSV_REESTRUTURADO_PATH)

situacao = Situacao(SHAPE_PATH)
recursos = Recursos(df_saude, df_saude_reestruturado)

def layout_situacao_atual():
	return html.Div([
		html.Div([
			html.H3("Situação Atual"),
			html.A(
				"Acessar Gerenciamento de Recursos",
				href="/gerenciamento",
				className="btn-gerenciamento"
			),
		], className="sidebar"),

		html.Div([
			dcc.Graph(id="mapa-situacao", className="mapa-graph"),
			html.Div(id="texto-atualizacao", className="texto-atualizacao"),
			dcc.Interval(id="interval-situacao", interval=60*1000, n_intervals=0)
		], className="mapa"),

		html.Div([
			html.H4("Alertas existentes"),
			html.Div(id="alerta-poligonos", className="alerta-poligonos"),
		], className="alertas"),

	], className="container")

def layout_gerenciamento_recursos():
	return html.Div([
		dcc.Store(id="controle-mapa", data={"atualizar": 0}),

		html.Div([
			html.H3("Gerenciamento de Recursos"),
			html.A(
				"↩ Voltar para Situação Atual",
				href="/",
				className="btn-gerenciamento"
			),

			dcc.Dropdown(
				id="dropdown-unidades",
				options=[{"label": nome, "value": nome} for nome in sorted(recursos.listar_recursos())],
				placeholder="Escolha uma unidade",
				style={"marginTop": "20px"}
			),

			html.Div([
				html.Div("Alterações foram feitas na alocação de unidades de saúde, deseja acatar?", style={
					"marginTop": "20px",
					"marginBottom": "10px"
				}),
				html.Button("Sim", id="btn-acatar", n_clicks=0, className="btn-sim"),
				html.Button("Não", id="btn-rejeitar", n_clicks=0, className="btn-nao"),
			])
		], className="sidebar"),

		html.Div([
			dcc.Graph(id="mapa-gerenciamento", style={"height": "100%", "width": "100%"})
		], className="mapa"),
	], className="container")



app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Interface ICARUS"

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

@app.callback(
	Output("mapa-situacao", "figure"),
	Output("texto-atualizacao", "children"),
	Input("interval-situacao", "n_intervals")
)
def atualizar_mapa_situacao(n):
	fig = situacao.obter_mapa_base(px)
	fig = situacao.obter_regioes_afetadas(fig, px)
	hora_atual = datetime.now().strftime("Última atualização: %H:%M:%S")
	return fig, hora_atual

@app.callback(
	Output("alerta-poligonos", "children"),
	Input("interval-situacao", "n_intervals")
)
def exibir_alertas_callback(n):
	return Alerta.exibir_alertas(situacao.gdf)

@app.callback(
	Output("dropdown-unidades", "options"),
	Output("controle-mapa", "data"),
	Input("btn-acatar", "n_clicks"),
	Input("btn-rejeitar", "n_clicks"),
	prevent_initial_call=True
)
def obter_reestruturacao_proposta(n_acatar, n_rejeitar):
	ctx = dash.callback_context
	if not ctx.triggered:
		raise dash.exceptions.PreventUpdate
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "btn-acatar":
		recursos.obter_reestruturacao_proposta(True)
	elif trigger_id == "btn-rejeitar":
		recursos.obter_reestruturacao_proposta(False)
	opcoes = [{"label": nome, "value": nome} for nome in sorted(recursos.listar_recursos())]
	return opcoes, {"atualizar": datetime.now().timestamp()}

@app.callback(
	Output("mapa-gerenciamento", "figure"),
	Input("dropdown-unidades", "value"),
	Input("controle-mapa", "data")
)
def atualizar_mapa_gerenciamento(unidade_dropdown, controle):
	return recursos.obter_mapa_recurso(unidade_dropdown)

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def exibir_pagina(pathname):
	if pathname == '/gerenciamento':
		return layout_gerenciamento_recursos()
	else:
		return layout_situacao_atual()

if __name__ == "__main__":
	app.run_server(debug=True, host="192.168.15.49", port=8050)

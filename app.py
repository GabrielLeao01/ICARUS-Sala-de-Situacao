import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
from datetime import datetime
import plotly.express as px
import dash_bootstrap_components as dbc
from icarus.situacao import Situacao
from icarus.alerta import Alerta
from icarus.recursos import Recursos
from icarus.graficos import Graficos

import pandas as pd
import os

SHAPE_PATH = "shapefiles/area_prioritaria.shp"
situacao = Situacao(SHAPE_PATH)


def layout_situacao_atual():
    return dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H2("Sala de Situação", className="mb-4"),
                    ], className="text-center"),
                    dbc.Button([
                        html.I(className="bi bi-building me-2"), "Gerenciamento de Recursos"
                    ], href="/gerenciamento", color="primary", className="mb-3 w-100 fs-5"),
                    dbc.Button([
                        html.I(className="bi bi-bar-chart-line me-2"), "Gráficos"
                    ], href="/graficos", color="secondary", className="w-100 fs-5"),
                ])
            ], className="bg-dark bg-opacity-75 text-light shadow-lg rounded-4 border-0 p-2"),
            width=2, className="sidebar p-0"
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        id="mapa-situacao",
                        className="mapa-graph",
                        style={"height": "65vh", "width": "100%"}
                    ),
                    html.Div(id="texto-atualizacao", className="texto-atualizacao text-end mt-2"),
                    dcc.Interval(id="interval-situacao", interval=60*1000, n_intervals=0)
                ])  
            ], className="bg-dark bg-opacity-75 text-light shadow-lg rounded-4 border-0 p-2"),
            width={"xs": 12, "md": 8}, className="mapa p-0"
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"), "Alertas"
                    ], className="mb-3"),
                    html.Div(id="alerta-poligonos", className="alerta-poligonos"),
                ])
            ], className="bg-dark bg-opacity-75 text-light shadow-lg rounded-4 border-0 p-2"),
            width=2, className="alertas p-0"
        ),
    ], className="g-3 align-items-stretch", style={"height": "100vh"})



def layout_graficos():
	graficos_disponiveis = Graficos.listar_graficos()
	return dbc.Row([
			dbc.Col(
				dbc.Card([
					dbc.CardBody([
						html.H3("Gráficos", className="mb-4"),
						dbc.Button("↩ Voltar para Situação Atual", href="/", color="secondary", className="mb-3 w-100"),
						dcc.Dropdown(
							id="dropdown-graficos",
							options=[{"label": nome, "value": nome} for nome in graficos_disponiveis],
							placeholder="Escolha um gráfico",
							style={"marginTop": "10px"}
						),
					])
				], className="mb-4"), width=3, className="sidebar"
			),
			dbc.Col(
				dbc.Card([
					dbc.CardBody([
						dcc.Graph(id="grafico-visualizacao", style={"height": "100%", "width": "100%"})
					])
				], className="mb-4"), width=9, className="mapa"
			),
		], className="g-2 align-items-stretch")

def layout_gerenciamento_recursos():
	recursos_disponiveis = Recursos.listar_recursos()
	return dbc.Row([
		dcc.Store(id="controle-mapa", data={"atualizar": 0}),
		dbc.Col(
			dbc.Card([
				dbc.CardBody([
					html.H3("Gerenciamento de Recursos", className="mb-4", style={"fontSize": "18px"}),
					dbc.Button("↩ Voltar para Situação Atual", href="/", color="secondary", className="mb-3 w-100"),
					dbc.Label("Escolha o recurso", style={"marginTop": "10px"}),
					dcc.Dropdown(
						id="dropdown-recurso",
						options=[{"label": nome.capitalize(), "value": nome} for nome in recursos_disponiveis],
						placeholder="Selecione o recurso",
						className="mb-3"
					),
					dcc.Dropdown(id="dropdown-unidades", options=[], placeholder="Selecione a unidade", style={"display": "none"}),
					html.Div(id="popup-reestruturacao"),
				])
			], className="mb-4"), width=3, className="sidebar"
		),
		dbc.Col(
			dbc.Card([
				dbc.CardBody([
					dcc.Graph(id="mapa-gerenciamento", style={"height": "100%", "width": "100%"})
				])
			], className="mb-4"), width=9, className="mapa"
		),
	], className="g-2 align-items-stretch")



app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.CYBORG,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
    ]
)
app.title = "Interface ICARUS"

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], fluid=True, className="bg-gradient bg-dark min-vh-100")

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
	Output("popup-reestruturacao", "children"),
	Output("controle-mapa", "data"),
	Input("dropdown-recurso", "value"),
	Input({'type': 'btn-acatar', 'index': ALL}, 'n_clicks'),
	Input({'type': 'btn-rejeitar', 'index': ALL}, 'n_clicks'),
	prevent_initial_call=True
)
def atualizar_unidades_popup_controle(recurso, n_acatar_list, n_rejeitar_list):
	return Recursos.atualizar_unidades_popup_controle(recurso, n_acatar_list, n_rejeitar_list)


@app.callback(
	Output("mapa-gerenciamento", "figure"),
	Input("dropdown-unidades", "value"),
	Input("controle-mapa", "data")
)
def obter_mapa_recurso_callback(unidade_dropdown, controle):
	return Recursos.obter_mapa_recurso(unidade_dropdown, controle)

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def exibir_pagina(pathname):
	if pathname == '/gerenciamento':
		return layout_gerenciamento_recursos()
	elif pathname == '/graficos':
		return layout_graficos()
	else:
		return layout_situacao_atual()
	
@app.callback(
	Output("grafico-visualizacao", "figure"),
	Input("dropdown-graficos", "value"),
	prevent_initial_call=True
)
def exibir_grafico_callback(grafico_id):
	import plotly.graph_objs as go
	if not grafico_id:
		return go.Figure()
	data = Graficos.obter_grafico(grafico_id)

	if data and 'data' in data and 'layout' in data:
		return go.Figure(data=data['data'], layout=data['layout'])
	elif data:
		return go.Figure(data=data)
	return go.Figure()

if __name__ == "__main__":
	app.run(debug=True, host="192.168.15.49", port=8050)

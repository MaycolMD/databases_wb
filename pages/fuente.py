from dash import Dash, html, dcc
import dash
import pyodbc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/dssource')

first_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.CardImg(src=dash.get_asset_url('ins.png'), top=True, style={'marginBottom': 30}),
                html.H1(children='Para acceder al repositorio donde se encuentra el Dataset',
                        style = {'textAlign' : 'center'}
                ),
                html.P("""El Instituto Nacional de Salud de Colombia es una Institución Pública adscrita al Ministerio de Salud de Colombia, con independencia administrativa y presupuesto propio.""", style={'textAlign': 'center'}),
                dbc.Button("Dataset", href="https://www.ins.gov.co/Paginas/Boletines-casos-COVID-19-Colombia.aspx", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
            ]
        )
    ]
, color = 'primary', outline = True, style={'marginBottom': 10})

second_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.CardImg(src=dash.get_asset_url('git.png'), top=True, style={'marginBottom': 30}),
                html.H1(children='Para acceder al repositorio donde se encuentra alojado el código de esta web',
                        style = {'textAlign' : 'center'}
                ),
                html.P("""GitHub es una forja para alojar proyectos utilizando el sistema de control de versiones Git. \n
                Presione para acceder al repositorio.""", style={'textAlign': 'center'}),
                dbc.Button("Github", href="https://github.com/MaycolMD/databases_wb.git", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
            ]
        )
    ]
, color = 'primary', outline = True)


layout = html.Div(children=[
    dbc.Row(dbc.Col(html.Div([
            html.H1(children='Covid Analytics',
                    style = {'textAlign' : 'center'}
            )],
            style = {'padding-top' : '1%'}
        ),
        )),
    dbc.Card(
    [
        dbc.CardHeader("Datos de Covid-19 en el año 2020"),
        dbc.CardBody(
            [
                html.H4("Proyecto Universitario", className="card-title"),
                html.P("""Nuestro dataset fue sacado de la plataforma INS. \n
                Este dataset consta de +300k registros, con más de 15 columnas cada registro
""", className="card-text"),
            ]
        ),
        dbc.CardFooter("Todos los derechos reservados. Copyright©."),
    ],
    style={"width": "36rem", 'textAlign':'center', 'margin':'auto', 'marginBottom':20},color="primary",
),
dbc.Row(
    [
        dbc.Col(first_card, width=6),
        dbc.Col(second_card, width=6),
    ]
),
])

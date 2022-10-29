from dash import Dash, html, dcc
import dash
import pyodbc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')
first_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.CardImg(src=dash.get_asset_url('g1.png'), top=True, style={'marginBottom': 30}),
                html.H5("Diagnosticados por intervalo de tiempo", className="card-title", style={'fontSize': 20, 'marginBottom': 20, 'textAlign': 'center'}),
                html.P("""En esta gráfica, podremos ver el comportamiento por fecha, mes
                y día de la semana específico de la fecha en que los pacientes del estudio
                fueron diagnosticados de Covid-19. \n
                Ingresa para más detalles.""", style={'textAlign': 'center'}),
                dbc.Button("Ingresar", href="/g1", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
            ]
        )
    ]
, color = 'primary', outline = True, style={"height": "68rem"},)

second_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.CardImg(src=dash.get_asset_url('g2.png'), top=True, style={'marginBottom': 30}),
                html.H5("Muertes en Colombia", className="card-title", style={'fontSize': 20, 'marginBottom': 20, 'textAlign': 'center'}),
                html.P("""En esta mapa de Colombia, podremos ver la concentración de muertes por departamento
                en Colombia a causa del Covid-19. \n
                Ingresa para más detalles.""", style={'textAlign': 'center'}),
                dbc.Button("Ingresar", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
            ]
        )
    ]
, color = 'primary', outline = True, style={"height": "68rem", 'marginBottom': 40})

third_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.CardImg(src=dash.get_asset_url('g3.png'), top=True, style={'marginBottom': 30}),
                html.H5("Diagnosticados por rango de edad", className="card-title", style={'fontSize': 20, 'marginBottom': 20, 'textAlign': 'center'}),
                html.P("""En esta gráfica, podremos ver el comportamiento por rango de edad y género
                de las personas diagnosticadas con Covid19. \n
                Ingresa para más detalles.""", style={'textAlign': 'center'}),
                dbc.Button("Ingresar", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
            ]
        )
    ]
, color = 'primary', outline = True)

fourth_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.CardImg(src=dash.get_asset_url('g3.png'), top=True, style={'marginBottom': 30}),
                html.H5("Diagnosticados por departamentos", className="card-title", style={'fontSize': 20, 'marginBottom': 20, 'textAlign': 'center'}),
                html.P("""En esta gráfica, podremos ver el comportamiento por departamento en Colombia
                de las personas diagnosticadas con Covid19. \n
                Ingresa para más detalles.""", style={'textAlign': 'center'}),
                dbc.Button("Ingresar", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
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
    dbc.Row(
        [
            dbc.Col(first_card, width=6),
            dbc.Col(second_card, width=6),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(third_card, width=6),
            dbc.Col(fourth_card, width=6),
        ]
    )
])

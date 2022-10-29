from dash import Dash, html, dcc
import dash
import pyodbc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/dssource')
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
                html.P("""Nuestro dataset fue sacado de la plataforma Kaggle
                Este dataset consta de +300k registros, con más de 15 columnas cada registro
""", className="card-text"),
            ]
        ),
        dbc.CardFooter("Todos los derechos reservados. Copyright©."),
    ],
    style={"width": "36rem", 'textAlign':'center', 'margin':'auto'},color="primary",
),
dbc.Row(dbc.Col(html.Div([
        html.H1(children='Para acceder al repositorio donde se encuentra el Dataset, presione aquí',
                style = {'textAlign' : 'center'}
        )],
        style = {'padding-top' : '1%'}
    ),
    )),
dbc.Button("Dataset", href="/g1", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15, 'width':"30rem",'fontSize':20}),
dbc.Row(dbc.Col(html.Div([
        html.H1(children='Para acceder al repositorio donde se encuentra alojado el código de esta web, presione aquí',
                style = {'textAlign' : 'center'}
        )],
        style = {'padding-top' : '1%'}
    ),
    )),
dbc.Button("Github", href="https://github.com/MaycolMD/databases_wb.git", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15, 'width':"30rem",'fontSize':20}),

])

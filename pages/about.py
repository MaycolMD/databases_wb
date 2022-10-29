from dash import Dash, html, dcc
import dash
import pyodbc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/about')


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
                html.P("""Proyecto académico realizado por estudiantes de la Universidad del Norte del programa de Ingeniería de Sistemas, en el curso de Bases de Datos.
                El presente proyecto utiliza un dataset relacionado con la situación de pandemia del covid19 y con este interpreta y representa información de este dataset en diferentes gráficos y formatos.
""", className="card-text"),
            ]
        ),
        dbc.CardFooter("Todos los derechos reservados. Copyright©."),
    ],
    style={"width": "36rem", 'textAlign':'center', 'margin':'auto'},color="primary",
),
dbc.Row(dbc.Col(html.Div([
        html.H1(children='Desarrollado por',
                style = {'textAlign' : 'center'}
        )],
        style = {'padding-top' : '1%'}
    ),
    )),
dbc.Row(
        [
            dbc.Col(dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/static/images/portrait-placeholder.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Maycol Moreno", className="card-title"),
                            html.P(
                                "Ingeniería de Sistemas",
                                className="card-text",
                            ),
                            html.Small(
                                "Última actualización 29/10/2022",
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )),
            dbc.Col(dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/static/images/portrait-placeholder.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("José Rueda", className="card-title"),
                            html.P(
                                "Ingeniería de Sistemas",
                                className="card-text",
                            ),
                            html.Small(
                                "Última actualización 29/10/2022",
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8"
                ),
            ],
            className="g-0 d-flex align-items-center"
            )),
            dbc.Col(dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/static/images/portrait-placeholder.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Natalia Mendoza", className="card-title"),
                            html.P(
                                "Ingeniería de Sistemas",
                                className="card-text",
                            ),
                            html.Small(
                                "Última actualización 29/10/2022",
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )),
        ],
        className="mb-4",
    )
])

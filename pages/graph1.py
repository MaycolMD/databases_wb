import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pyodbc
import pandas as pd
from pandas.api.types import CategoricalDtype
import dash_bootstrap_components as dbc
import pymssql
import os

server_name = 'paba.database.windows.net' # Nombre del server
database_name='covid19'
username = 'maycolsa@paba'
password1 = 'sa123456.'
cnx = pymssql.connect(
    server=server_name,
    user=username,
    password=password1,
    database=database_name
)

cursor=cnx.cursor()

dash.register_page(__name__, path='/g1')

SIDEBAR_STYLE = {
    "width": "16rem",
    "padding": "2rem 1rem",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}



layout = html.Div(children=[
    dbc.Row(dbc.Col(html.Div([
            html.H1(children='Diagnosticados por intervalo de tiempo',
                    style = {'textAlign' : 'center'}
            )],
            style = {'padding-top' : '1%'}
        ),
        )),

     dbc.Row(
            [
                dbc.Col(html.Div(
                    [
                        html.H2("Gráficas", className="display-4"),
                        html.Hr(),
                        dbc.Nav(
                            [
                                dbc.NavLink("Diagnosticados por tiempo", href="/g1", active="exact", style={'fontSize': 13, 'textAlign':'center'}),
                                dbc.NavLink("Diagnosticados por rango de edad", href="/g3", active="exact", style={'fontSize': 13, 'textAlign':'center'}),
                                dbc.NavLink("Diagnosticados por departamento", href="/g4", active="exact", style={'fontSize': 13, 'textAlign':'center'}),
                                dbc.NavLink("Muertes geográficamente en Colombia", href="/g2", active="exact", style={'fontSize': 13, 'textAlign':'center'})
                            ],
                            vertical=True,
                            pills=True,
                        ),
                    ],
                    style=SIDEBAR_STYLE,
                ), width=2),
                dbc.Col(html.Div(
                dcc.Graph(
                    id='barchart',
                ),), width=6),
                dbc.Col(
                html.Div([
                dcc.Dropdown(['Fecha', 'Mes', 'Día de la semana'], 'Mes', id='demo-dropdown', style={'marginBottom': 30, 'color': 'black'}),
                dcc.RadioItems(['Barras','Circular'], 'Barras', id='analytics-inputt3', style = {'textAlign':'center'}, labelStyle = {'marginRight':15}),
                dbc.Row(dbc.Col(html.Div(id = 'dd-output-container',
                        style = {'padding-top' : '1%', 'fontSize': 25}
                    ),
                    )),
                html.P("""En esta gráfica, podremos ver un análisis de los contagios por fecha específica, mes
                y día de la semana en Colombia durante el año 2020. Para ajustar la medida de tiempo por la cual se desea
                ver el gráfico ajuste la ventana desplegable con la que desee. \n
                Para más detalles sobre nuestra fuente de datos, ingrese aquí""", style={'textAlign': 'center'}),
                dbc.Button("Ver fuente de datos", href="/fuente", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
                ],

                ), width=2, style={'marginLeft': 30}),
            ]
        ),
])

content = html.Div(id="page-content", style=CONTENT_STYLE)

layout = html.Div([dcc.Location(id="url"), layout, content])

@callback(
    [Output('dd-output-container', 'children'),
    Output('barchart', 'figure')],
    [Input('demo-dropdown', 'value'),
    Input('analytics-inputt3', 'value'),
    Input("url", "pathname")
    ]
)
def update_output(value, valuee, pathname):

    df = pd.read_sql_query(
    """
    select d.FechaDiagnostico
    from dbo.Dataset d
    where d.FechaDiagnostico != 'NO APLICA'
    """
    , cnx)

    if value == 'Día de la semana':
        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['dates'] = pd.to_datetime(df['FechaDiagnostico'])
        df['day_of_week'] = df['dates'].dt.day_name()
        cat_type = CategoricalDtype(categories=cats, ordered=True)
        df['day_of_week'] = df['day_of_week'].astype(cat_type)
        values = df['day_of_week'].value_counts(sort=False).keys().tolist()
        counts = df['day_of_week'].value_counts(sort=False).tolist()
        title = 'Día de la semana'
    elif value == 'Fecha':
        values = df['FechaDiagnostico'].value_counts(sort=False).keys().tolist()
        counts = df['FechaDiagnostico'].value_counts(sort=False).tolist()
        title = 'Fecha'
    else:
        df['month'] = pd.to_datetime(df['FechaDiagnostico']).apply(lambda x: x.month_name())
        df = df.sort_values(by="FechaDiagnostico")
        values = df['month'].value_counts(sort=False).keys().tolist()
        counts = df['month'].value_counts(sort=False).tolist()
        title = 'Mes'

    ndf = pd.DataFrame()
    ndf[title] = values
    ndf['Diagnosticados']=counts

    if value == 'Fecha':
        barch = px.bar(ndf, x=title, y='Diagnosticados',text_auto=True)
    else:
        if valuee == 'Circular':
            barch = px.pie(ndf,values='Diagnosticados', names=title)
        else:
            barch = px.bar(ndf, x=title, y='Diagnosticados',text_auto=True,color=title)
    if pathname == "/g1":
        return html.P(children="Diagnosticados por tiempo", style = {'textAlign' : 'center'}), barch
    elif pathname == "/g2":
        return html.P(children="Muertes en Colombia", style = {'textAlign' : 'center'}), barch
    elif pathname == "/g3":
        return html.P(children="Covid por género", style = {'textAlign' : 'center'}), barch
    elif pathname == "/g4":
        return html.P(children="Covid por departamento", style = {'textAlign' : 'center'}), barch
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    ), barch

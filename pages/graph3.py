import dash
from dash import html, dcc, callback, Input, Output
import pyodbc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import pymssql

dash.register_page(__name__, path='/g3')
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
print('succesfull conection')

cursor=cnx.cursor()

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
            html.H1(children='Diagnosticados por rango de edad',
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
                    id='h-barchart',
                ),), width=6),
                dbc.Col(
                html.Div([
                dcc.RadioItems(['Todos', 'Hombres','Mujeres'], 'Todos', id='analytics-input3', style = {'textAlign':'center'}, labelStyle = {'marginRight':15}),
                html.Div(id='analytics-output3'),
                dbc.Row(dbc.Col(html.Div(id = 'analytics-output3',
                        style = {'padding-top' : '1%', 'fontSize': 25}
                    ),
                    )),
                html.P("""En esta gráfica, podremos ver un análisis de los contagios por rangos de edades en Colombia durante el 2020.
                Esta gráfica puede filtrarse para obtener solo datos por género, presionando en el filtro que se desee en la parte superior. Por defecto muestra ambos géneros. \n
                Para más detalles sobre nuestra fuente de datos, ingrese aquí""", style={'textAlign': 'center'}),
                dbc.Button("Ver fuente de datos", href="/dssource", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
                ],

                ), width=2, style={'marginLeft': 30}),
            ]
        ),
])

content = html.Div(id="page-content", style=CONTENT_STYLE)

layout = html.Div([dcc.Location(id="url"), layout, content])


@callback(
    [
    Output('analytics-output3', 'children'),
    Output('h-barchart', 'figure')],
    [
    Input('analytics-input3', 'value'),
    Input("url", "pathname")
    ]

)

def update_output(value, pathname):

    if value == 'Hombres':
        df = pd.read_sql_query(
        """
        SELECT SUM(CASE WHEN d.Edad < 18 and d.Sexo = 'F' THEN 1 ELSE 0 END) AS [Under 18],
           SUM(CASE WHEN d.Edad BETWEEN 18 AND 24 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [18-24],
           SUM(CASE WHEN d.Edad BETWEEN 25 AND 34 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [25-34],
    	   SUM(CASE WHEN d.Edad BETWEEN 35 AND 44 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [35-44],
    	   SUM(CASE WHEN d.Edad BETWEEN 45 AND 54 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [45-54],
    	   SUM(CASE WHEN d.Edad BETWEEN 55 AND 64 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [55-64],
    	   SUM(CASE WHEN d.Edad BETWEEN 65 AND 74 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [65-74],
    	   SUM(CASE WHEN d.Edad BETWEEN 75 AND 84 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [75-84],
    	   SUM(CASE WHEN d.Edad BETWEEN 85 AND 94 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [85-94],
    	   SUM(CASE WHEN d.Edad BETWEEN 95 AND 104 and d.Sexo != 'F' THEN 1 ELSE 0 END) AS [95-104]
           from Dataset d
        """
        , cnx)
    elif value == 'Mujeres':
        df = pd.read_sql_query(
        """
        SELECT SUM(CASE WHEN d.Edad < 18 and d.Sexo = 'F' THEN 1 ELSE 0 END) AS [Under 18],
           SUM(CASE WHEN d.Edad BETWEEN 18 AND 24 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [18-24],
           SUM(CASE WHEN d.Edad BETWEEN 25 AND 34 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [25-34],
    	   SUM(CASE WHEN d.Edad BETWEEN 35 AND 44 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [35-44],
    	   SUM(CASE WHEN d.Edad BETWEEN 45 AND 54 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [45-54],
    	   SUM(CASE WHEN d.Edad BETWEEN 55 AND 64 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [55-64],
    	   SUM(CASE WHEN d.Edad BETWEEN 65 AND 74 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [65-74],
    	   SUM(CASE WHEN d.Edad BETWEEN 75 AND 84 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [75-84],
    	   SUM(CASE WHEN d.Edad BETWEEN 85 AND 94 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [85-94],
    	   SUM(CASE WHEN d.Edad BETWEEN 95 AND 104 and d.Sexo != 'M' THEN 1 ELSE 0 END) AS [95-104]
           from Dataset d
        """
        , cnx)
    else:
        df = pd.read_sql_query(
        """
        SELECT SUM(CASE WHEN d.Edad < 18 and d.Sexo = 'F' THEN 1 ELSE 0 END) AS [Under 18],
           SUM(CASE WHEN d.Edad BETWEEN 18 AND 24 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [18-24],
           SUM(CASE WHEN d.Edad BETWEEN 25 AND 34 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [25-34],
    	   SUM(CASE WHEN d.Edad BETWEEN 35 AND 44 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [35-44],
    	   SUM(CASE WHEN d.Edad BETWEEN 45 AND 54 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [45-54],
    	   SUM(CASE WHEN d.Edad BETWEEN 55 AND 64 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [55-64],
    	   SUM(CASE WHEN d.Edad BETWEEN 65 AND 74 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [65-74],
    	   SUM(CASE WHEN d.Edad BETWEEN 75 AND 84 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [75-84],
    	   SUM(CASE WHEN d.Edad BETWEEN 85 AND 94 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [85-94],
    	   SUM(CASE WHEN d.Edad BETWEEN 95 AND 104 and d.Sexo != 'W' THEN 1 ELSE 0 END) AS [95-104]
           from Dataset d
        """
        , cnx)


    values = df.columns
    counts = df.iloc[0]
    print(counts)
    ndf = pd.DataFrame()
    ndf['Diagnosticados']=counts
    ndf['Rango'] = values
    print(ndf)
    barch = px.bar(ndf, x='Diagnosticados', y='Rango', text_auto=True, orientation = 'h', color = 'Diagnosticados',color_continuous_scale = "matter", title = value)
    if pathname == "/g1":
        return html.P(children="Diagnosticados por tiempo", style = {'textAlign' : 'center'}), barch
    elif pathname == "/g2":
        return html.P(children="Muertes en Colombia", style = {'textAlign' : 'center'}), barch
    elif pathname == "/g3":
        return html.P(children="Covid por rango de edad", style = {'textAlign' : 'center'}), barch
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

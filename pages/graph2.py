import dash
from dash import html, dcc, callback, Input, Output
import pyodbc
import pymssql
import pandas as pd
import requests
import plotly.express as px
import dash_bootstrap_components as dbc


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

df = pd.read_sql_query(
"""
select d.CodigoDepartamento, d.NombreDepartamento, count(*) as Cantidad
from Dataset d
where d.EstadoActual = 'Fallecido'
group by d.CodigoDepartamento, d.NombreDepartamento

"""
, cnx)

dash.register_page(__name__, path='/g2')

repo_url = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
co_regions = requests.get(repo_url).json()

fig = px.choropleth(
    data_frame = df,
    geojson = co_regions,
    locations='CodigoDepartamento',
    featureidkey = 'properties.DPTO',
    color='Cantidad',
    color_continuous_scale = "rainbow",
    hover_name =df['NombreDepartamento']
)

fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds='locations')

fig.update_layout(
    title_text = 'Muertos por departamento en Colombia en 2020',
    font = dict(
        family = "Ubuntu",
        size = 18
    ),
)

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
            html.H1(children='Muertes geográficamente en Colombia por CoVid',
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
                   figure=fig
               ),
               ), width=6),
                dbc.Col(
                html.Div([
                dbc.Row(dbc.Col(html.Div(html.P(children="Muertes en Colombia", style = {'textAlign' : 'center'}),
                        style = {'padding-top' : '1%', 'fontSize': 25}
                    ),
                    )),
                html.P("""En este mapa, podremos ver la concentración de muertes por Covid-19 en Colombia durante
                el año 2020. Si coloca su ratón sobre algún departamento, tendrá más información sobre este,
                como su Nombre, Código y cantidad de muertos allí. Puede acercarse en el gráfico con la rueda del ratón. \n
                Para más detalles sobre nuestra fuente de datos, ingrese aquí""", style={'textAlign': 'center'}),
                dbc.Button("Ver fuente de datos", href="/fuente", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
                html.P("Para obtener información sobre el GeoJson utilizado, ingrese aquí""", style={'textAlign': 'center'}),
                dbc.Button("GeoJson Colombia", href="https://gist.github.com/john-guerra/43c7656821069d00dcbc", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),

                ],

                ), width=2, style={'marginLeft': 30}),
            ]
        ),
])

content = html.Div(id="page-content", style=CONTENT_STYLE)

layout = html.Div([dcc.Location(id="url2"), layout, content])

@callback(
    [
    Output('dd-output-container2', 'children')
    ],
    [
    Input("url2", "pathname")
    ]
)
def update_output(pathname):
    if pathname == "/g1":
        return html.P(children="Diagnosticados por tiempo", style = {'textAlign' : 'center'})
    elif pathname == "/g2":
        return html.P(children="Muertes en Colombia", style = {'textAlign' : 'center'})
    elif pathname == "/g3":
        return html.P(children="Covid por género", style = {'textAlign' : 'center'})
    elif pathname == "/g4":
        return html.P(children="Covid por departamento", style = {'textAlign' : 'center'})
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

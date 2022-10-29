import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pyodbc
import pandas as pd
from pandas.api.types import CategoricalDtype
import dash_bootstrap_components as dbc

server = 'DESKTOP-61S4LKS\SQLEXPRESS' # Nombre del server
database_name='covid19'
cnx=pyodbc.connect(driver='{SQL server}', host=server, database=database_name)
print('succesfull conection')

# Creación de la tabla y obtención de valores
cursor=cnx.cursor()
if cursor.tables(table='Dataset', tableType='TABLE').fetchone():
    print("exists")
else:
    cursor.execute("""

        CREATE TABLE Dataset(IdCaso INT PRIMARY KEY, FechaNotificacion DATE, CodigoDepartamento INT, NombreDepartamento VARCHAR(255) , CodigoMunicipio INT, NombreMunicipio VARCHAR(255), Edad INT, Sexo VARCHAR(2), TipoContagio VARCHAR(50), UbicacionCaso VARCHAR(255), EstadoActual VARCHAR(255) NOT NULL, CodigoPaisDeViaje VARCHAR(50), NombrePaisDeViaje VARCHAR(255), FechaInicioSintomas VARCHAR(255), FechaMuerte VARCHAR(255), FechaDiagnostico VARCHAR(255), FechaRecuperacion VARCHAR(50), FechaCargueWeb DATE, TipoRecuperacion VARCHAR(255), PertenenciaEtnica VARCHAR(255), NombreGrupoEtnico VARCHAR(255))

        """)

    cursor.executemany("INSERT INTO Dataset VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values_list_data)
cursor.commit()
cursor.close()
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
                        html.P(
                            "Selecciona la gráfica que deseas ver", className="lead", style={'textAlign': 'center'}
                        ),
                        dbc.Nav(
                            [
                                dbc.NavLink("Diagnosticados por tiempo", href="/g1", active="exact"),
                                dbc.NavLink("Diagnosticados por rango de edad", href="/g3", active="exact"),
                                dbc.NavLink("Diagnosticados por departamento", href="/g4", active="exact"),
                                dbc.NavLink("Muertes geográficamente en Colombia", href="/g2", active="exact")
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
    Input("url", "pathname")
    ]
)
def update_output(value, pathname):

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

    barch = px.bar(ndf, x=title, y='Diagnosticados')
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

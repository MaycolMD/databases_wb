import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pyodbc
import pandas as pd
import dash_bootstrap_components as dbc

server = 'LAPTOP-51FAGA1L' # Nombre del server
database_name='covid19'
cnx=pyodbc.connect(driver='{SQL server}', host=server, database=database_name)
print('succesfull conection')

cursor=cnx.cursor()
cursor.tables(table='Dataset', tableType='TABLE').fetchone()

dash.register_page(__name__, path='/g4')

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
            html.H1(children='Diagnosticados por Departamento',
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
                    id='nbarchart',
                ),), width=6),
                dbc.Col(
                html.Div([
                dcc.Dropdown(['Departamento', 'Amazonas', 'Antioquia', 'Arauca', 'Archipiélago de San Andrés Providencia y Santa Catalina', 'Atlántico', 'Barranquilla D.E.', 'Bogotá D.C.', 'Bolívar', 'Boyacá', 'Buenaventura D.E.', 'Caldas', 'Caquetá','Cartagena D.T. y C.', 'Casanare', 'Cauca', 'Cesar', 'Chocó', 'Córdoba', 'Cundinamarca', 'Guainía', 'Guaviare', 'Huila', 'La Guajira', 'Magdalena', 'Meta', 'Nariño', 'Norte de Santander', 'Putumayo', 'Quindío', 'Risaralda', 'Santa Marta D.T. y C.', 'Santander', 'Sucre', 'Tolima', 'Valle del Cauca', 'Vaupés', 'Vichada' ], 'Departamento', id='demo-dropdown-n', style={'marginBottom': 50, 'color': 'black'}),
                dbc.Row(dbc.Col(html.Div(id = 'dd-output-container-n',
                        style = {'padding-top' : '1%', 'fontSize': 25}
                    ),
                    )),
                html.P("""En esta gráfica, podremos ver un análisis de los contagios en Colombia por departamento.
                Si desea, puede acceder a la información general de todos los departamentos, o filtrar por departamento y conocer los casos registrados \n
                Para más detalles sobre nuestra fuente de datos, ingrese aquí""", style={'textAlign': 'center'}),
                dbc.Button("Ver fuente de datos", href="/fuente", color="primary", size="lg", className="d-grid gap-2 col-6 mx-auto", style={'margin': 15}),
                ],

                ), width=2, style={'marginLeft': 30}),
            ]
        ),
])

content = html.Div(id="page-content", style=CONTENT_STYLE)

layout = html.Div([dcc.Location(id="url_n2"), layout, content])

@callback(
    [Output('dd-output-container-n', 'children'),
    Output('nbarchart', 'figure')],
    [Input('demo-dropdown-n', 'value'),
    Input("url_n2", "pathname")
    ]
)

def update_output_n(value, pathname):

    if value == 'Departamento':
        df = pd.read_sql_query(
            """
            SELECT d.NombreDepartamento, COUNT(*) AS TotalCasosPorDept
            FROM dbo.Dataset d
            WHERE d.NombreDepartamento NOT LIKE 'No Aplica' and d.FechaDiagnostico NOT LIKE 'No Aplica'
            GROUP BY d.NombreDepartamento
            ORDER BY d.NombreDepartamento

            """, cnx)
        values = df['NombreDepartamento'].value_counts(sort=False).keys().tolist()
        counts = df['TotalCasosPorDept'].value_counts(sort=False).tolist()
        title = 'Departamentos'

    else:

        dept = str('%'+value+'%')
        df = pd.read_sql_query(
        """
        SELECT d.FechaDiagnostico, d.NombreDepartamento, COUNT(*) AS CasosPorFecha 
        FROM covid19.dbo.Dataset d 
        WHERE d.FechaDiagnostico NOT LIKE 'No Aplica' AND d.NombreDepartamento LIKE '%s'
        GROUP BY d.FechaDiagnostico, d.NombreDepartamento 
        ORDER BY d.FechaDiagnostico ASC
        """ %dept
        , cnx)

        df['month'] = pd.to_datetime(df['FechaDiagnostico']).apply(lambda x: x.month_name())
        df = df.sort_values(by="FechaDiagnostico")
        values = df['month'].value_counts(sort=False).keys().tolist()
        countsDept = df['month'].value_counts(sort=False).tolist()

        counts = []
        sumIndex=0
        for index in range (len(countsDept)):
            sum = 0

            if index == 0:
                index2=0
            else: 
                index2=sumIndex
                print(index2)
                
            tope=countsDept[index]+index2
            print(tope)

            while index2<tope:
                sum = sum + df['CasosPorFecha'][index2]
                sumIndex=sumIndex+1
                index2=index2+1
                print(index2)
            counts.append(sum)
                
        print(counts)

        title = 'Mes'


    ndf = pd.DataFrame()
    ndf[title] = values
    ndf['Diagnosticados']=counts

    barch = px.bar(ndf, x=title, y='Diagnosticados')
    if pathname == "/g1":
        return html.P(children="Diagnosticados Covid por tiempo", style = {'textAlign' : 'center'}), barch
    elif pathname == "/g2":
        return html.P(children="Muertes en Colombia", style = {'textAlign' : 'center'}), barch
    elif pathname == "/g3":
        return html.P(children="Diagnosticados Covid por rango de edad", style = {'textAlign' : 'center'}), barch
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

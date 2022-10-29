import dash
from dash import html, dcc, callback, Input, Output
import pyodbc

import pandas as pd
import requests
import plotly.express as px

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
    color_continuous_scale = "burg",
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


layout = html.Div(children=[
    html.H1(children='This is our Analytics page'),
	html.Div([
        "Select a city: ",
        dcc.RadioItems(['New York City', 'Montreal','San Francisco'],
        'Montreal',
        id='analytics-input')
    ]),
	html.Br(),
    html.Div(id='analytics-output'),
    dcc.Graph(
       figure=fig
   ),
])


@callback(
    Output(component_id='analytics-output', component_property='children'),
    Input(component_id='analytics-input', component_property='value')
)
def update_city_selected(input_value):
    return f'You selected: {input_value}'

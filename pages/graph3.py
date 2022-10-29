import dash
from dash import html, dcc, callback, Input, Output
import pyodbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/g3')
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

layout = html.Div(children=[
    html.H1(children='This is our 3 Analytics page'),
	html.Div([
        "Select a city: ",
        dcc.RadioItems(['Todos  ', 'Hombres  ','Mujeres  '],
        'Todos  ',
        id='analytics-input3')
    ]),
	html.Br(),
    html.Div(id='analytics-output3'),
    dcc.Graph(
       id='h-barchart'
    )
])


@callback(
    [Output('analytics-output3', 'children'),
    Output('h-barchart', 'figure')],
    Input('analytics-input3', 'value')
)

def update_output(value):

    if value == 'Hombres  ':
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
    elif value == 'Mujeres  ':
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
    barch = px.bar(ndf, x='Diagnosticados', y='Rango', orientation = 'h')
    return f'You have selected {value}', barch

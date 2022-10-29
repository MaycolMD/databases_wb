import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pyodbc
import pandas as pd
from pandas.api.types import CategoricalDtype

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





layout = html.Div(children=[
    html.H1(children='This is our Home page'),

    html.Div(children='''
        This is our Home page content.
    '''),

    dcc.Dropdown(['Date', 'Month', 'Dayweek'], id='demo-dropdown'),
    html.Div(id='dd-output-container'),

     dcc.Graph(
        id='barchart'
    )
])

@callback(
    [Output('dd-output-container', 'children'),
    Output('barchart', 'figure')],
    Input('demo-dropdown', 'value')
)
def update_output(value):

    df = pd.read_sql_query(
    """
    select d.FechaDiagnostico
    from dbo.Dataset d
    where d.FechaDiagnostico != 'NO APLICA'
    """
    , cnx)

    if value == 'Dayweek':
        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['dates'] = pd.to_datetime(df['FechaDiagnostico'])
        df['day_of_week'] = df['dates'].dt.day_name()
        cat_type = CategoricalDtype(categories=cats, ordered=True)
        df['day_of_week'] = df['day_of_week'].astype(cat_type)
        values = df['day_of_week'].value_counts(sort=False).keys().tolist()
        counts = df['day_of_week'].value_counts(sort=False).tolist()
        title = 'Día de la semana'
    elif value == 'Date':
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
    return f'You have selected {value}', barch

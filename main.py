from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import pyodbc

import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask
import numpy as np

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
web = Flask(__name__)

report_data=pd.read_csv('./csv/dataset20220808.csv', encoding='latin-1')
values_list_data=report_data.values.tolist()

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

@web.after_request
def after_request(response):
    print('Después de la petición')
    return response

@web.route('/')
def principal():

    return render_template('home.html')

@web.route('/image')
def visualize():
    df = pd.read_sql_query(
    """
    select d.FechaDiagnostico
    from dbo.Dataset d
    where d.FechaDiagnostico != 'NO APLICA'
    """
    , cnx)
    df['month'] = pd.to_datetime(df['FechaDiagnostico']).apply(lambda x: x.month_name())
    print(df)
    values = df['month'].value_counts(sort=False).keys().tolist()
    counts = df['month'].value_counts(sort=False).tolist()
    print(values)
    print(counts)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = values
    ys = counts
    axis.plot(xs, ys)
    for index in range(len(xs)):
        axis.text(xs[index], ys[index], ys[index], size=10)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@web.route('/about')
def about():
    return render_template('about.html')

def not_found(error):
    return render_template('error.html'), 404
    #return redirect(url_for('principal'))

if __name__ == '__main__':
    web.register_error_handler(404, not_found)
    web.run(debug=True)


cnx.close()

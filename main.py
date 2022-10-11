from flask import Flask, render_template
import pandas as p
import pyodbc

web = Flask(__name__)

report_data=p.read_csv('C:/Users/natyp/OneDrive/Escritorio/BASES DE DATOS/dataset20220808.csv', encoding='latin-1')
values_list_data=report_data.values.tolist()

server = 'LAPTOP-51FAGA1L'
database_name='covid19'
cnx=pyodbc.connect(driver='{SQL server}', host=server, database=database_name)
print('succesfull conection')

@web.after_request
def after_request(response):
    print('Después de la petición')
    return response

@web.route('/')
def principal():
    
    cursor=cnx.cursor()
    cursor.execute("CREATE TABLE Dataset(IdCaso INT PRIMARY KEY, FechaNotificacion DATE, CodigoDepartamento INT, NombreDepartamento VARCHAR(255) , CodigoMunicipio INT, NombreMunicipio VARCHAR(255), Edad INT, Sexo VARCHAR(2), TipoContagio VARCHAR(50), UbicacionCaso VARCHAR(255), EstadoActual VARCHAR(255) NOT NULL, CodigoPaisDeViaje VARCHAR(50), NombrePaisDeViaje VARCHAR(255), FechaInicioSintomas VARCHAR(255), FechaMuerte VARCHAR(255), FechaDiagnostico VARCHAR(255), FechaRecuperacion VARCHAR(50), FechaCargueWeb DATE, TipoRecuperacion VARCHAR(255), PertenenciaEtnica VARCHAR(255), NombreGrupoEtnico VARCHAR(255))")

    cursor.executemany("INSERT INTO Dataset VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values_list_data)

    cursor.commit()

    print("The process is alredy finished.")

    return render_template('home.html')

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
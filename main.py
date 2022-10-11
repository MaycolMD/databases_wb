from flask import Flask, render_template
from flask_mysqldb import MySQL

web = Flask(__name__)

web.config['MYSQL_HOST'] = 'localhost'
web.config['MYSQL_USER'] = 'sa'
web.config['MYSQL_PASSWORD'] = '123456'
web.config['MYSQL_DB'] = 'AdventureWorks2012_CS'
sql = MySQL(web)

@web.after_request
def after_request(response):
    print('Después de la petición')
    return response

@web.route('/')
def principal():
    search = sql.connection.cursor()
    search.execute("""
    with SumaT (IDTerr, suma) as (
	select sale.TerritoryID, sum(sale.SubTotal) Suma
	from Sales.SalesOrderHeader sale
	group by sale.TerritoryID
    )
    select top 1 *
    from Sales.SalesTerritory s join SumaT suma
    on s.TerritoryID = suma.IDTerr
    order by suma.suma desc
    """)
    user = search.fetchone()
    print(user)
    search.close()
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

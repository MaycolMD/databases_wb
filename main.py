from dash import Dash, html, dcc
import dash
import pyodbc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import pymssql

report_data=pd.read_csv('csv/dataset20200808.csv', encoding='latin-1')
values_list_data=report_data.values.tolist()

#DESKTOP-61S4LKS\SQLEXPRESS -- maycol server
#LAPTOP-51FAGA1L -- natalia server

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

# Creación de la tabla y obtención de valores
cursor=cnx.cursor()

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.QUARTZ, dbc.icons.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

app.title = "CoVid Analytics"

app.layout = html.Div(
    [
		dbc.Navbar(
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col([
                            html.Img(src=dash.get_asset_url('coronavirus.png'), height="40px", style={'marginRight': 50}),
                            dbc.NavbarBrand("Covid Analytics", className="ms-2", style={'fontSize': 20})
                        ],
                        width={"size":"auto"})
                    ],
                    align="center",
                    className="g-0"),

                    dbc.Row([
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink("Inicio", href="/")),
                                #dbc.NavItem(dbc.NavLink("Fundamentals", href="/fundamentals")),
                                dbc.NavItem(dbc.DropdownMenu(
                                        children=[
                                            dbc.DropdownMenuItem("Diagnosticados por tiempo", href="/g1", style={'fontSize': 11}),
											dbc.DropdownMenuItem("Diagnosticados por rango de edad", href="/g3", style={'fontSize': 11}),
											dbc.DropdownMenuItem("Diagnosticados por departamento", href="/g4", style={'fontSize': 11}),
                                            dbc.DropdownMenuItem("Muertos geográficamente en Colombia", href="/g2", style={'fontSize': 11})
                                        ],
                                        nav=True,
                                        in_navbar=True,
                                        label="Gráficas",
                                )),
                                dbc.NavItem(dbc.DropdownMenu(
                                        children=[
                                            dbc.DropdownMenuItem("¿Quiénes somos?", href="/about", style={'fontSize': 15}),
                                            dbc.DropdownMenuItem("Fuente de datos", href="/dssource", style={'fontSize': 15})
                                        ],
                                        nav=True,
                                        in_navbar=True,
                                        label="Más opciones",
                                ))
                            ],
                            navbar=True
                            )
                        ],
                        width={"size":"auto"})
                    ],
                    align="center"),
                    dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),

                    dbc.Row([
                        dbc.Col(
                             dbc.Collapse(
                                dbc.Nav([
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi-github"), href="https://github.com/MaycolMD/databases_wb.git",external_link=True) ),
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi bi-twitter"), href="https://twitter.com/INSColombia",external_link=True) ),
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi-facebook"), href="https://www.facebook.com/INSColombia",external_link=True) ),
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi-youtube"), href="https://www.youtube.com/user/INSColombia",external_link=True) ),
                                ]
                                ),
                                id="navbar-collapse",
                                is_open=False,
                                navbar=True
                             )
                        )
                    ],
                    align="center")
                ],
            fluid=True
            ),
		    color="primary",
		    dark=True
		),

		dash.page_container
    ]
)

@dash.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
cursor.close()
cnx.close()

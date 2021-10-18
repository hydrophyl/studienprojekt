import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from backend import get_df_today, get_df_week, get_df_month, get_df_all, get_df_lastmonth, plotting

df1 = get_df_today()
df2 = get_df_week()
df3 = get_df_month()
df4 = get_df_lastmonth()
df5 = get_df_all()
#plotting todays data    
fig1 = plotting(df1)
fig2 = plotting(df2)
fig3 = plotting(df3)
fig4 = plotting(df4)
fig5 = plotting(df5)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Studienprojekt Feinstaub Messung mit Module SDS011", href="/")),
    ],
    brand="HAW-Hamburg",
    brand_href="/",
    color="#023A9D",
    dark=True,
)

app.layout = dbc.Container([
    html.Div([dcc.Location(id="url"), navbar ]),
    html.H4('Aktuelle Daten von letztem Tag'), 
    dcc.Graph(
        id='graph1',
        figure=fig1
    ),
    html.H4('Aktuelle Daten für eine Woche'), 
    dcc.Graph(
        id='graph2',
        figure=fig2
    ),
    html.H4('Aktuelle Daten für einem Monat'), 
    dcc.Graph(
        id='graph3',
        figure=fig3
    ),
    html.H4('Daten von letztem Monat'), 
    dcc.Graph(
        id='graph4',
        figure=fig4
    ),
    html.H4('Alle Daten'), 
    dcc.Graph(
        id='graph5',
        figure=fig5
    )
])

if __name__ == "__main__":
    app.run_server()
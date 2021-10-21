import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from backend import (
    get_df_today,
    get_df_week,
    get_df_month,
    get_df_all,
    get_df_lastmonth,
    plotting,
    plotting_temperature_humidity,
)

df1 = get_df_today()
df2 = get_df_week()
df3 = get_df_month()
df4 = get_df_lastmonth()
df5 = get_df_all()
# plotting todays data
fig1 = plotting(df1)
fig2 = plotting(df2)
fig3 = plotting(df3)
fig4 = plotting(df4)
fig5 = plotting(df5)
fig11 = plotting_temperature_humidity(df1)
fig21 = plotting_temperature_humidity(df2)
fig31 = plotting_temperature_humidity(df3)
fig41 = plotting_temperature_humidity(df4)
fig51 = plotting_temperature_humidity(df5)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink("Studienprojekt Feinstaub Messung mit Module SDS011", href="/")
        ),
    ],
    brand="HAW-Hamburg",
    brand_href="/",
    color="#023A9D",
    dark=True,
)

app.layout = dbc.Container(
    [
        html.Div([dcc.Location(id="url"), navbar]),
        html.Div(
            [
                html.H4("Aktuelle Daten von letztem Tag"),
                dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig11),
            ]
        ),
        html.Div(
            [
                html.H4("Aktuelle Daten für eine Woche"),
                dcc.Graph(figure=fig2),
                dcc.Graph(figure=fig21),
            ]
        ),
        html.Div(
            [
                html.H4("Aktuelle Daten für einem Monat"),
                dcc.Graph(figure=fig3),
                dcc.Graph(figure=fig31),
            ]
        ),
        html.Div(
            [
                html.H4("Daten von letztem Monat"),
                dcc.Graph(figure=fig4),
                dcc.Graph(figure=fig41),
            ]
        ),
        html.Div(
            [html.H4("Alle Daten"), dcc.Graph(figure=fig5), dcc.Graph(figure=fig51),]
        ),
    ]
)

if __name__ == "__main__":
    app.run_server()

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
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

app.layout = dbc.Container([
    dcc.Graph(
        id='graph1',
        figure=fig1
    ),
    dcc.Graph(
        id='graph2',
        figure=fig2
    ),
    dcc.Graph(
        id='graph3',
        figure=fig3
    ),
    dcc.Graph(
        id='graph4',
        figure=fig4
    ),
    dcc.Graph(
        id='graph5',
        figure=fig5
    )
])

if __name__ == "__main__":
    app.run_server()
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port


# import individual components from files
from track import track
from leaderboard import leaderboard
from navbar import navbar
from telemetry import telemetry
from controls import menubox

#### intialize app structure
#### layout needs to be defined first so that callbacks will work
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "OmniSci Grand Prix | GTC 2019"

body = dbc.Container([
        dbc.Row([track, leaderboard]),
        dbc.Row([telemetry, menubox])
    ],
    className="mt-4",
    fluid=True
)

app.layout = html.Div([navbar, body])



#### reactive leaderboard component
@app.callback(Output('leaderboard-tbl', 'figure'),
              [Input('leaderboard-interval', 'n_intervals')])
def create_leaderboard(notused):

    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)

    #where clause of >= 60 just to ensure a full lap, even though view definition
    #tries to calculate full lap. could also add a date clause if want to limit
    #leaderboard to drivers at current event
    df = pd.read_sql("""select
                        sessionuid,
                        lapnumber,
                        lapstarttime,
                        laptime,
                        weather
                        from v_leaderboard_melbourne
                        where laptime >= 60
                        order by laptime
                        limit 10
                    """, conn)

    #formatting for session column to make table display width smaller
    df["session"] = [f"""S{x[-4:]}""" for x in df["sessionuid"]]

    #create table with top 10 fastest laps
    #### TODO: evaluate replacing this with native dash table
    #### due to blinking that happens on first load because of using Graph()
    #### shows axis before settling on displaying table
    figure = ff.create_table(df[["session","lapnumber","lapstarttime", "laptime", "weather"]],
                             height_constant=30)

    figure.layout.width = 625

    return figure


#### run app
#### TODO: disable debug when finished
if __name__ == "__main__":
    app.run_server(debug=True)

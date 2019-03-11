import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import pymapd
import pandas as pd
from credentials import host, user, password, dbname


#### helper functions
def get_leaderboard():
    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=6274)

    #query columns intentionally left vague, can optimize later
    df = pd.read_sql("""select
                        sessionuid,
                        lapnumber,
                        playercarindex,
                        lapstarttime,
                        lapendtime,
                        laptime,
                        lapdistance,
                        era,
                        weather,
                        airtemp,
                        tracklength,
                        tracktemp
                        from v_leaderboard_melbourne
                        where laptime >= 60
                        order by laptime
                        limit 50
                    """, conn)

    return df


#### create leaderboard
#### leaderboard_df also used to populate reference lap dropdown
#### TODO: How do we update this every 30 seconds or so? Doesn't need to be fast, laps avg 90s
#### TODO: What happens to dropdown if this table does update in the middle, does reference lap change?
leaderboard_df = get_leaderboard()

#formatting for session column to make table width smaller
leaderboard_df["session"] = [f"""S{x[-4:]}""" for x in leaderboard_df["sessionuid"]]

#create table with top 10 fastest laps
figure = ff.create_table(leaderboard_df[["session","lapnumber","lapstarttime", "laptime", "weather"]].head(10))
figure.layout.width = 625

tbl = html.Div([
    dcc.Graph(id='my-table',
              figure=figure,
              config={
                  'displayModeBar': False
              })
])

leaderboard = dbc.Col([html.H4("Leaderboard - Melbourne"), tbl], md=4, width=6)

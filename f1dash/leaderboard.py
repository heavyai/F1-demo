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
    #possible to use this same df to select reference lap, and have one fewer query?
    df = pd.read_sql("""select *
                        from v_leaderboard_melbourne
                        where laptime >= 60
                        order by laptime
                        limit 50
                    """, conn)

    return df


#### create leaderboard

leaderboard = get_leaderboard()
figure = ff.create_table(leaderboard[["sessionuid","lapnumber","lapstarttime", "laptime", "weather"]].head(10),
                         )
figure.layout.width = 750

tbl = html.Div([
    dcc.Graph(id='my-table',
              figure=figure,
              config={
                  'displayModeBar': False
              })
])

leaderboard = dbc.Col([
                      html.H4("Leaderboard - Melbourne"),
                      tbl
                      ],
                      md=4,
                      width=6)

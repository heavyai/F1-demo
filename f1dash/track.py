import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port

#### helper functions
#### TODO: after choosing value to color track, remove unneeded columns
def get_lapdata(sessionuid, lapstarttime, lapendtime):

    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user = user, password = password, dbname = dbname, port = port)

    cm = f"""select
    gforcelateral,
    gforcelongitudinal,
    gforcevertical,
    worldpositionx,
    worldpositionz,
    worldvelocityx,
    worldvelocityy,
    worldvelocityz
    from
    gtc_carmotion_v2
    where sessionuid = '{sessionuid}' and
    packettime between '{lapstarttime}' and '{lapendtime}' and
    playerscar = true
    """

    carmotion = pd.read_sql(cm, conn)

    return carmotion

#gets current lap loaded into database, used to populate track and telemetry
def get_current_lap():

    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)
    data = pd.read_sql("select * from v_most_recent_lap_melbourne", conn)

    data["lapstarttime"] = [x.strftime("%Y-%m-%d %H:%M:%S") for x in data["lapstarttime"]]
    data["lapstarttime"] = [x.strftime("%Y-%m-%d %H:%M:%S") for x in data["lapendtime"]]

    return data

#display in dash
trackgraph = html.Div([
                        dcc.Graph(id='track-graph',
                            config={
                                'displayModeBar': True
                            }
                        ),
                        #controls when track and telemetry updates
                        dcc.Interval(
                                id='track-interval',
                                interval=7*1000, # in milliseconds
                                n_intervals=0
                            )
                      ])

#controls bootstrap positioning
track = dbc.Col([trackgraph], width=6)

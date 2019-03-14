import plotly.figure_factory as ff
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port

#### helper functions
def get_lapdata(sessionuid, lapstarttime, lapendtime):
    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)

    cm = f"""select
    gforcelateral,
    gforcelongitudinal,
    gforcevertical,
    packettime,
    pitch,
    roll,
    sessiontime,
    worldpositionx,
    worldpositiony,
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


#TODO: make reference lap chooseable from interface
ref_lap_data = get_lapdata(1270608935058109592, "2019-03-08 23:11:06", "2019-03-08 23:12:34")

#TODO: get most recent lap programmatically
ref_current_data = get_lapdata(1270608935058109592, "2019-03-08 23:09:37", "2019-03-08 23:11:06")

#graph properties changed here
trace_reference = go.Scattergl(x=ref_lap_data["worldpositionx"],
                             y=ref_lap_data["worldpositionz"],
                             mode="markers",
                             marker = dict(size = 2, color = "#404040"),
                             name="Reference Lap"
                            )

#TODO: set color based on another pandas series
trace_current = go.Scattergl(x=ref_current_data["worldpositionx"],
                           y=ref_current_data["worldpositionz"],
                           mode="markers",
                           marker = dict(size = 4, color = "#1A84C7"),
                           name="Current Lap"
                           )

#display in dash
trackgraph = dcc.Graph(
                    figure={
                        "data": [trace_reference, trace_current],
                        "layout": go.Layout(legend=dict(orientation="h", y=1),
                                            title='Racing Line: Current vs. Reference Lap',
                                            height=410,
                                            xaxis=dict(title='worldpositionx'),
                                            yaxis=dict(title='worldpositionz')
                                            )
                    },
                    config={
                        'displayModeBar': True
                    }
)

#controls bootstrap positioning
track = dbc.Col([trackgraph], width=6)

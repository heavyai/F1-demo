import dash_core_components as dcc
import dash_bootstrap_components as dbc

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port

#### helper functions
#### TODO: after choosing value to color track, remove unneeded columns
def get_lapdata(sessionuid, lapstarttime, lapendtime):

    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)

    cm = f"""select
    gforcelateral,
    gforcelongitudinal,
    gforcevertical,
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

#display in dash
trackgraph = dcc.Graph(id='track-graph',
                       config={
                            'displayModeBar': True
                       }
                      )

#controls bootstrap positioning
track = dbc.Col([trackgraph], width=6)

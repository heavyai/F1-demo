import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port

def get_telemetry_data(sessionuid, lapstarttime, lapendtime, playercarindex, metric):

    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)

    ## get telemetry data
    ## by specifying the timestamps and sessionuid, it implies a single track
    tele = f"""select
    packettime,
    max({metric}) as {metric}
    from gtc_cartelemetry_v2
    where sessionuid = '{sessionuid}' and
    packettime between '{lapstarttime}' and '{lapendtime}' and
    playercarindex = {playercarindex}
    group by 1
    order by 1
    """

    telemetry_ref = pd.read_sql(tele, conn)

    return telemetry_ref


telgraph = dcc.Graph(id='telemetry-graph',
                    config={
                        'displayModeBar': True
                    }
                )

#controls bootstrap positioning
telemetry = dbc.Col([telgraph], width=9)

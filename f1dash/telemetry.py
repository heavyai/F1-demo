import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go

#### telemetry: line plot of metrics

import pymapd
import pandas as pd
from credentials import host, user, password, dbname

conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=6274)

playercarindex = 0
sessionuid = 10206713599870479199
lapstarttime = "2018-12-20 00:58:36"
lapendtime =  "2018-12-20 01:00:18"

## get telemetry data
## by specifying the timestamps and sessionuid, it implies a single track
## > 0 a weird hack...unclear if data coming in from other cars or what
tele = f"""select
brake,
enginerpm,
frameidentifier,
gear,
packettime,
sessiontime,
speed,
steer,
throttle
from gtc_cartelemetry_v2
where sessionuid = '{sessionuid}' and
packettime between '{lapstarttime}' and '{lapendtime}' and
playercarindex = {playercarindex} and speed > 0
order by frameidentifier
"""

telemetry_ref = pd.read_sql(tele, conn)

# iloc statements a crude downsample of data coming at 60hz to improve visual clarity
# alternatives could be a boxplot, smoothing of some sort
telemetry_trace_reference = go.Scatter(x=telemetry_ref["frameidentifier"].iloc[::30],
                             y=telemetry_ref["speed"].iloc[::30],
                            )



telgraph = dcc.Graph(
                    figure={
                        "data": [telemetry_trace_reference],
                        "layout": go.Layout(legend=dict(orientation="h"),
                                            title='Telemetry'
                                            )
                    },
                    config={
                        'displayModeBar': True
                    }
                )

#controls bootstrap positioning
telemetry = dbc.Col([telgraph], width=9)

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port

def get_telemetry_data(sessionuid, lapstarttime, lapendtime, playercarindex):

    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)

    ## get telemetry data
    ## by specifying the timestamps and sessionuid, it implies a single track
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
    playercarindex = {playercarindex}
    order by frameidentifier
    """

    telemetry_ref = pd.read_sql(tele, conn)

    return telemetry_ref

#### TODO: make this get values from dropdown
telemetry_ref = get_telemetry_data(1270608935058109592, "2019-03-08 23:11:06", "2019-03-08 23:12:34", 19)
telemetry_ref_lim = telemetry_ref.iloc[::480]
#telemetry_ref_lim["normalized_frame"] = (telemetry_ref_lim["frameidentifier"] - telemetry_ref_lim["frameidentifier"].min())/(telemetry_ref_lim["frameidentifier"].max() - telemetry_ref_lim["frameidentifier"].min())


#### TODO: get current lap values here
telemetry_rt = get_telemetry_data(1270608935058109592, "2019-03-08 23:09:37", "2019-03-08 23:11:06", 19)
telemetry_rt_lim = telemetry_rt.iloc[::480]
#telemetry_rt_lim["normalized_frame"] = (telemetry_rt_lim["frameidentifier"] - telemetry_rt_lim["frameidentifier"].min())/(telemetry_rt_lim["frameidentifier"].max() - telemetry_rt_lim["frameidentifier"].min())

# iloc statements a crude downsample of data coming at 60hz to improve visual clarity
# alternatives could be a boxplot, smoothing of some sort
telemetry_trace_reference = go.Scatter(x=telemetry_ref_lim.index,
                                       y=telemetry_ref_lim["speed"],
                                       name="Reference Lap",
                                       marker = dict(size = 2, color = "#404040")
                            )

telemetry_trace_rt = go.Scatter(x=telemetry_rt_lim.index,
                                y=telemetry_rt_lim["speed"],
                                name="Current Lap",
                                marker = dict(size = 4, color = "#1A84C7")
                            )


telgraph = dcc.Graph(
                    figure={
                        "data": [telemetry_trace_reference, telemetry_trace_rt],
                        "layout": go.Layout(legend=dict(orientation="h",y=1.2),
                                            title='Vehicle Telemetry',
                                            xaxis=dict(title='Normalized Lap Time'),
                                            yaxis=dict(title='Value')
                                            )
                    },
                    config={
                        'displayModeBar': True
                    }
                )

#controls bootstrap positioning
telemetry = dbc.Col([telgraph], width=9)

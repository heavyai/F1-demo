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

    return telemetry_ref

#### TODO: make this get values from dropdown
telemetry_ref = get_telemetry_data(10206713599870479199, "2018-12-20 00:58:36", "2018-12-20 01:00:18", 0)
telemetry_ref_lim = telemetry_ref.iloc[::30]
telemetry_ref_lim["normalized_frame"] = (telemetry_ref_lim["frameidentifier"] - telemetry_ref_lim["frameidentifier"].min())/(telemetry_ref_lim["frameidentifier"].max() - telemetry_ref_lim["frameidentifier"].min())


#### TODO: get current lap values here
telemetry_rt = get_telemetry_data(1804599106752478952, "2018-12-19 20:40:27", "2018-12-19 20:48:58", 0)
telemetry_rt_lim = telemetry_rt.iloc[::30]
telemetry_rt_lim["normalized_frame"] = (telemetry_rt_lim["frameidentifier"] - telemetry_rt_lim["frameidentifier"].min())/(telemetry_rt_lim["frameidentifier"].max() - telemetry_rt_lim["frameidentifier"].min())

# iloc statements a crude downsample of data coming at 60hz to improve visual clarity
# alternatives could be a boxplot, smoothing of some sort
telemetry_trace_reference = go.Scatter(x=telemetry_ref_lim["normalized_frame"],
                                       y=telemetry_ref_lim["speed"],
                                       name="Reference Lap",
                                       marker = dict(size = 2, color = "#404040")
                            )

telemetry_trace_rt = go.Scatter(x=telemetry_rt_lim["normalized_frame"],
                                y=telemetry_rt_lim["speed"],
                                name="Current Lap",
                                marker = dict(size = 4, color = "#1A84C7")
                            )


telgraph = dcc.Graph(
                    figure={
                        "data": [telemetry_trace_reference, telemetry_trace_rt],
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

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port

# import individual components from files
from track import track, get_lapdata
from leaderboard import leaderboard
from navbar import navbar
from telemetry import telemetry, get_telemetry_data
from controls import menubox


#### intialize app structure
#### layout needs to be defined first so that callbacks will work without complaining
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "OmniSci Grand Prix | GTC 2019"
#app.config['suppress_callback_exceptions']=True

body = dbc.Container([
        dbc.Row([track, leaderboard]),
        dbc.Row([telemetry, menubox])
    ],
    className="mt-4",
    fluid=True
)

app.layout = html.Div([navbar, body])


#### reactive leaderboard component
@app.callback([Output('leaderboard-tbl', 'columns'), Output('leaderboard-tbl', 'data')],
              [Input('leaderboard-interval', 'n_intervals')])
def create_leaderboard(notused):

    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)

    #where clause of >= 60 just to ensure a full lap, even though view definition
    #tries to calculate full lap. lapstarttime limit can be used to limit
    #leaderboard to drivers at current event
    df = pd.read_sql("""select
                        sessionuid,
                        lapnumber,
                        lapstarttime,
                        laptime,
                        weather
                        from v_leaderboard_melbourne
                        where laptime >= 60 and lapstarttime >= '2019-03-02 00:00:00'
                        order by laptime
                        limit 10
                    """, conn)

    #formatting for session column to make table display width smaller
    df["session"] = [f"""S{x[-4:]}""" for x in df["sessionuid"]]
    df["rank"] = [x+1 for x in df.index]

    #Limit columns in df,
    df_ = df[["rank", "session","lapnumber","lapstarttime", "laptime", "weather"]]
    columns=[{"name": i, "id": i} for i in df_.columns]

    print("Leaderboard updated from database")
    return columns, df_.to_dict("rows")

#### populate/update reference lap dropdown dynamically
#### https://community.plot.ly/t/want-to-update-dropdown-options-but-not-selected-value/20820/2?u=randyzwitch
@app.callback(
    [Output("reflapmenu", "options"), Output("reflapmenu", "value")],
    [Input('leaderboard-interval', "n_intervals")],
    [State("reflapmenu", "value"), State("metricmenu", "value")]
)
def make_reflap_options(notused, value, values):

    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)

    df = pd.read_sql("""select
                        sessionuid,
                        lapnumber,
                        laptime,
                        lapstarttime,
                        lapendtime,
                        playercarindex
                        from v_leaderboard_melbourne
                        where laptime >= 60 and lapstarttime >= '2019-03-02 00:00:00'
                        order by laptime
                        limit 50
                    """, conn)

    #formatting for session column to make table width smaller
    df["session"] = [f"""S{x[-4:]}""" for x in df["sessionuid"]]

    options = [{'label': f"""{uid} - Lap {lnum} - {lapt}""",
                'value': f"""{sessionuid},{lstart},{lend},{pci}"""}
                for uid, sessionuid, lnum, lapt, lstart, lend, pci
                in zip(df["session"], df["sessionuid"], df["lapnumber"], df["laptime"], df["lapstarttime"], df["lapendtime"], df["playercarindex"])
              ]

    if value not in [o["value"] for o in options]:
        # if the value is not in the new options list, we choose a different value
        if options:
            value = options[0]["value"]
        else:
            value = None

    print("Dropdown updated from database")

    return options, value

#### Update track
#### TODO: currently tied to leaderboard-interval update, consider second timer for more frequent updates
@app.callback(Output('track-graph', 'figure'),
              [Input('leaderboard-interval', 'n_intervals'), Input('reflapmenu', 'value')])
def build_track_chart(notused, reflapvalue):

    #unpack reflapvalue into parameters to use for reference lap
    sessionuid, lapstarttime, lapendtime, _ = reflapvalue.split(',')
    ref_lap_data = get_lapdata(sessionuid, lapstarttime, lapendtime)

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

    figure={
        "data": [trace_reference, trace_current],
        "layout": go.Layout(legend=dict(orientation="h", y=1.2),
                            title='Racing Line: Current vs. Reference Lap',
                            height=410,
                            xaxis=dict(title='worldpositionx'),
                            yaxis=dict(title='worldpositionz'),
                            uirevision='never'
                            )
    }

    print("build_track_chart fired: " + reflapvalue)

    return figure

#### telemetry
@app.callback(Output('telemetry-graph', 'figure'),
              [Input('leaderboard-interval', 'n_intervals'), Input('reflapmenu', 'value'), Input('metricmenu', 'value')])
def build_telemetry_chart(notused, reflapvalue, metric):

    #unpack reflapvalue into parameters to use for reference lap
    sessionuid, lapstarttime, lapendtime, playercarindex = reflapvalue.split(',')
    telemetry_ref = get_telemetry_data(sessionuid, lapstarttime, lapendtime, playercarindex)
    telemetry_ref_lim = telemetry_ref.iloc[::480]


    #### TODO: get current lap values here
    telemetry_rt = get_telemetry_data(1270608935058109592, "2019-03-08 23:09:37", "2019-03-08 23:11:06", 19)
    telemetry_rt_lim = telemetry_rt.iloc[::480]

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
    figure={
        "data": [telemetry_trace_reference, telemetry_trace_rt],
        "layout": go.Layout(legend=dict(orientation="h",y=1.2),
                            title='Vehicle Telemetry',
                            xaxis=dict(title='Normalized Lap Time'),
                            yaxis=dict(title=metric),
                            uirevision='never'
                            )
    }

    print("build_telemetry_chart fired: " + metric)

    return figure

#### run app
#### TODO: disable debug when finished
if __name__ == "__main__":
    app.run_server(debug=True)

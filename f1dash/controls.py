import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port

#### helper functions
def get_sessions():
    #placing connection inside to avoid having stale connection
    conn = pymapd.connect(host = host, user= user, password= password, dbname= dbname, port=port)

    #query columns intentionally left vague, can optimize later
    df = pd.read_sql("""select
                        sessionuid,
                        lapnumber,
                        laptime,
                        playercarindex
                        from v_leaderboard_melbourne
                        where laptime >= 60
                        order by laptime
                        limit 50
                    """, conn)

    return df

### create leaderboard
### leaderboard_df also used to populate reference lap dropdown
### TODO: What happens to dropdown if this table does update in the middle, does reference lap change?
leaderboard_df = get_sessions()

#formatting for session column to make table width smaller
leaderboard_df["session"] = [f"""S{x[-4:]}""" for x in leaderboard_df["sessionuid"]]

#### reference lap: build list dynamically from leaderboard_df defined in leaderboard.py
reflapmenu = dcc.Dropdown(
    id='reflapmenu',
    options = [{'label': f"""{uid} - Lap {lnum} - {lapt}""", 'value': uid} for uid, lnum, lapt in
                zip(leaderboard_df["session"], leaderboard_df["lapnumber"], leaderboard_df["laptime"])],
    value=leaderboard_df["session"][0],
    searchable=False,
    clearable=False,
    style=dict(width = '275px')
)

#### telemetry metrics: these are the reasonable values from the table
metricmenu = dcc.Dropdown(
    id='metricmenu',
    options=[
        {'label': 'speed', 'value': 'speed'},
        {'label': 'enginerpm', 'value': 'enginerpm'},
        {'label': 'brake', 'value': 'brake'},
        {'label': 'gear', 'value': 'gear'},
        {'label': 'steer', 'value': 'steer'},
        {'label': 'throttle', 'value': 'throttle'}
    ],
    value="speed",
    searchable=False,
    clearable=False,
    style=dict(width = '275px')
)

#### this builds the stacked controls div
#### TODO: understand if this is stable or whether to use rows
menubox = dbc.Col([html.H5("Reference Lap"),
                   reflapmenu,
                   html.H5("Metric", style={'padding-top': 50}),
                   metricmenu
                   ],
                   width=3)

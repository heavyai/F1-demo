import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from leaderboard import leaderboard_df


reflapmenu = dcc.Dropdown(
    options=[{'label': f"""{uid} - Lap {lnum} - {lapt}""", 'value': uid} for uid, lnum, lapt in
                zip(leaderboard_df["session"], leaderboard_df["lapnumber"], leaderboard_df["laptime"])
            ],
    value=leaderboard_df["session"][0],
    searchable=False,
    clearable=False,
    style=dict(width = '275px')
)


metricmenu = dcc.Dropdown(
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

menubox = dbc.Col([html.H5("Reference Lap"),
                   reflapmenu,
                   html.H5("Metric", style={'padding-top': 50}),
                   metricmenu
                   ],
                   width=3)

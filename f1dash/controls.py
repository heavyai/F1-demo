import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import pymapd
import pandas as pd
from credentials import host, user, password, dbname, port

#### reference lap: build list dynamically with callback
reflapmenu = dcc.Dropdown(
    id='reflapmenu',
    searchable=False,
    clearable=False,
    style=dict(minWidth = '250px', paddingRight = '15px', borderRadius = 0)
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
    style=dict(minWidth = '250px', paddingRight = '15px', borderRadius = 0)
)

#### this builds the stacked controls div
menubox = dbc.Col([html.H5("Reference Lap"),
                   reflapmenu,
                   html.H5("Metric", style={'padding-top': 50}),
                   metricmenu
                   ],
                   width=3)

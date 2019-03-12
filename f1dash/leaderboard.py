import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


tbl = html.Div([
    dcc.Graph(id='leaderboard-tbl',
              config={
                  'displayModeBar': False
              }
              ),
    #controls when create_leaderboard() runs
    dcc.Interval(
            id='leaderboard-interval',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
])

leaderboard = dbc.Col([html.H4("Leaderboard - Melbourne"), tbl], md=4, width=6)

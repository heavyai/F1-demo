import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table


tbldiv = html.Div([
    dash_table.DataTable(
        id='leaderboard-tbl',
        style_cell_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': '#1A84C7',
            'color': 'white',
            'fontFamily': '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"'
        },
        style_table={
            'height': '330'
        },
        style_cell={
            'fontFamily': '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"'
        }
    ),
    #controls when create_leaderboard() and make_reflap_options runs
    dcc.Interval(
            id='leaderboard-interval',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
])

leaderboard = dbc.Col([html.H4("Leaderboard - Melbourne"), tbldiv], md=4, width=6)

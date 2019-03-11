import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

# import individual components from files
from track import track
from leaderboard import leaderboard
from navbar import navbar
from telemetry import telemetry

#### intialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "OmniSci Grand Prix | GTC 2019"

#### mockup body
body = dbc.Container([
        dbc.Row([track, leaderboard]),
        dbc.Row([telemetry])
    ],
    className="mt-4",
    fluid=True
)

app.layout = html.Div([navbar, body])

#### run app
#### TODO: disable debug when finished
if __name__ == "__main__":
    app.run_server(debug=True)

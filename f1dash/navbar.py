import dash_bootstrap_components as dbc
import dash_html_components as html


logo = html.Div([
    html.Img(src='/assets/omnisci_secondary_horizontalbox.svg',
             style={'width': '60%', 'float': 'right'},
             className="logo-img")
])

navbar = dbc.NavbarSimple(
    children=[logo],
    brand="OmniSci Grand Prix - NVIDIA GTC 2019",
    # sticky="top",
    fluid=True
)

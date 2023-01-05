import dash_bootstrap_components as dbc
from dash import html



error_page = dbc.Container([
    html.H3(
        "Looks like something went wrong..."
    ),
])
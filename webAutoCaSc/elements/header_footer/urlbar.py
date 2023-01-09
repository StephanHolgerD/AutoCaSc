import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dcc import Download



from elements.header_footer import footer as footertxt
from elements.header_footer import navbar as navbartxt
from elements.header_footer import urlbar as urlbartxt

footer = footertxt.footer
navbar = navbartxt.navbar

stores = ["query_memory",
          "variant_queue_input",
          "variant_queue_url",
          "variant_memory",
          "results_memory",
          "transcripts_to_use_memory"]

url_bar_and_content_div = html.Div(
    [
        dcc.Store(id=_store) for _store in stores] + [
        dcc.Location(id='url', refresh=False),
        Download(id="download"),
        navbar,
        dbc.Toast(
            "You have selected X-linked inheritance, but the variant is not located on the X-chromosome.",
            id="warning-toast",
            header="CAVE!",
            is_open=False,
            dismissable=True,
            icon="danger",
            style={
                "position": "fixed",
                "top": 66,
                "right": 10,
                "width": 350,
                "zIndex": 2
            },
        ),
        dbc.Container(
            dbc.Row(
                id='page-content',
                style={
                    "marginTop": "70px",
                    "marginBottom": "63px",
                    "height": "calc(100vh - 133px)",
                    "overflowY": "auto",
                    "justifyContent": "start",
                    "width": "100%",
                },
                align="start",
                className="hide_scrollbar"
            ),
            style={
                "zIndex": 1
            }
        ),
        footer
    ],
    style={"width": "100%"})
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dcc import Download



from elements.frontend.static_pages.header_footer import footer as footertxt
from elements.frontend.static_pages.header_footer import navbar as navbartxt
from elements.frontend.static_pages.header_footer import urlbar as urlbartxt

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
        Download(id="frontend_staticpages_header_footer_urlbar_download"),
        navbar,
        dbc.Toast(
            "You have selected X-linked inheritance, but the variant is not located on the X-chromosome.",
            id="frontend_staticpages_header_footer_urlbar_warning-toast",
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
                id='frontend_staticpages_impressum_impressum_page-content',
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
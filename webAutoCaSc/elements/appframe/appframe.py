from elements.header_footer import footer as footertxt
from elements.header_footer import urlbar as urlbartxt
from elements.about import about as abouttxt
from elements.faq import faq as faqtxt
from elements.impressum import impressum as impressumtxt
from elements.news import news as newstxt
from elements.instructions import instructions as instructionstxt
from elements.landingpage import landingpage as landingpagetxt
from elements.error import error 
from elements.loading import loading
from statistics import mean
from flask import Flask
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from urllib.parse import unquote, quote



url_bar_and_content_div = urlbartxt.url_bar_and_content_div
about_page = abouttxt.about_page
landing_page = landingpagetxt.landing_page
search_page = loading.search_page
error_page = error.error_page
impressum_page = impressumtxt.impressum_page
faq_page = faqtxt.faq_page
news_page = newstxt.news_page
tutorial_page = instructionstxt.tutorial_page
footer = footertxt.footer
about_ger = abouttxt.about_ger

server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                server=server,
                suppress_callback_exceptions=True)
app.title = "webAutoCaSc"




# index layout
app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    about_page,
    landing_page,
    search_page,
    error_page,
    dbc.Button(id="download_button"),
    html.Div([
        dbc.Container([
            dbc.Card([
                dbc.CardHeader(
                    dbc.Tabs(
                        id="card_tabs",
                    )
                ),
                dbc.CardBody(
                    html.P(id="card_content", className="card_text")
                )
            ])
        ])
    ]),
    html.Div(id="loading_output"),
    dcc.Dropdown(id="transcript_dropdown"),
    impressum_page,
    faq_page,
    news_page,
    tutorial_page,
    footer,
    dbc.Button(id="collapse_button_transcripts"),
    dbc.Collapse(id="collapse_transcripts")
])
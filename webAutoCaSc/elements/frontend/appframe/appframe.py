from elements.frontend.static_pages.header_footer import footer as footertxt
from elements.frontend.static_pages.header_footer import urlbar as urlbartxt
from elements.frontend.static_pages.about import about as abouttxt
from elements.frontend.static_pages.faq import faq as faqtxt
from elements.frontend.static_pages.impressum import impressum as impressumtxt
from elements.frontend.static_pages.news import news as newstxt
from elements.frontend.static_pages.instructions import instructions as instructionstxt
from elements.frontend.landingpage import landingpage as landingpagetxt
from elements.frontend.static_pages.error import error 
from elements.frontend.static_pages.loading import loading
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
    impressum_page,
    faq_page,
    news_page,
    tutorial_page,
    footer
])
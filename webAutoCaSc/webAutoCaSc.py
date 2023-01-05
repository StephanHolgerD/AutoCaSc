from elements.frontend import frontend
from elements.backend import backend
from elements.about import about as abouttxt
from elements.faq import faq as faqtxt
from elements.impressum import impressum as impressumtxt
from elements.news import news as newstxt
from elements.instructions import instructions as instructionstxt
from elements.callbacks import ResultCard
from elements.callbacks import download
from elements.landingpage import landingpage as landingpagetxt
from elements.loading import loading
from elements.appframe import appframe
from statistics import mean

import dash
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import unquote, quote
import os, sys
from AutoCaSc_core.AutoCaSc import AutoCaSc, VERSION
from refseq_transcripts_converter import convert_variant


landing_page = landingpagetxt.landing_page
search_page = loading.search_page
about_eng = abouttxt.about_eng
about_ger = abouttxt.about_ger
about_page = abouttxt.about_page
faq_ger = faqtxt.faq_ger 
faq_eng = faqtxt.faq_eng
tutorial_page = instructionstxt.tutorial_page
faq_page = faqtxt.faq_page
news_page = newstxt.news_page
impressum_ger = impressumtxt.impressum_ger
impressum_eng = impressumtxt.impressum_eng
impressum_page = impressumtxt.impressum_page


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


app = appframe.app

########## FRONTEND ##########
parse_input = frontend.parse_input
get_results_page = frontend.get_results_page
input_ok = frontend.input_ok


for _item in ["navbar", "footer"]:
    @app.callback(
        Output(f"{_item}-collapse", "is_open"),
        [Input(f"{_item}-toggler", "n_clicks")],
        [State(f"{_item}-collapse", "is_open")])
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

@app.callback(
    Output("collapse_transcripts", "is_open"),
    Output("collapse_transcripts", "children"),
    Input("collapse_button_transcripts", "n_clicks"),
    State("collapse_transcripts", "is_open"),
    State("active_variant_tab", "data")
)
def load_all_hgvsc_notations(n, is_open, active_variant):
    # this calls convert_variant() from "refseq_transcripts_converter.py" to get RefSeq transcripts via VEP REST API
    if n:
        if not is_open:
            notations = convert_variant(active_variant.get("active_variant"))
            notations_styled_children = []
            if notations:
                for _notation in notations:
                    notations_styled_children.append(_notation)
                    notations_styled_children.append(html.Br())
                notations_styled = html.Div(notations_styled_children)
            else:
                notations_styled = "Sorry, none found."
        else:
            notations_styled = None
        return not is_open, notations_styled
    return is_open, ""


@app.callback(
    Output("warning-toast", "is_open"),
    Input("page-content", "children"),
    State("results_memory", "data")
)
def check_x_linkedness(_, results_memory):
    if results_memory is not None:
        for _variant, _instance_attributes in results_memory.get("instances").items():
            if _instance_attributes.get("inheritance") == "x_linked":
                if not _instance_attributes.get("vcf_string")[0] == "X":
                    return True
    return False

@app.callback([Output('page-content', 'children'),
              Output("query_memory", "clear_data"),
              Output("variant_queue_input", "clear_data"),
              Output("variant_queue_url", "clear_data"),
              Output("results_memory", "clear_data"),
              Output("transcripts_to_use_memory", "clear_data"),
              Output("page-content", "align")],
              [Input('url', 'pathname'),
               Input("results_memory", "data")])
def display_page(pathname, results_memory):
    ctx = dash.callback_context
    print(dir(ctx))
    if "results_memory" in ctx.triggered[0]['prop_id'] and results_memory is not None:
        print("results page")
        return [get_results_page(results_memory)] + [False for _store in range(5)] + ["center"]
    elif "url" in ctx.triggered[0]['prop_id']:
        if pathname == "/about":
            return [about_page] + [False for _store in range(5)] + ["start"]
        if pathname == "/impressum":
            return [impressum_page] + [False for _store in range(5)] + ["start"]
        if pathname == "/faq":
            return [faq_page] + [False for _store in range(5)] + ["start"]
        if pathname == "/tutorial":
            return [tutorial_page] + [False for _store in range(5)] + ["start"]
        if pathname == "/news":
            return [news_page] + [False for _store in range(5)] + ["start"]
        if "/search" in pathname:
            if results_memory is None:
                print("search page")
                return [search_page] + [False for _store in range(5)] + ["center"]
            else:
                print("results page")
                return [get_results_page(results_memory)] + [False for _store in range(5)] + ["center"]
        else:
            print("landing page")
            return [landing_page] + [True for _store in range(5)] + ["center"]
    else:
        raise PreventUpdate


@app.callback(
    Output("variant_input", "valid"),
    Output("variant_input", "invalid"),
    Output("variant_queue_input", "data"),
    [Input("variant_input", "n_blur"),
     Input("inheritance_input", "value")],
    [State("variant_input", "value")]
)
def check_user_input(trigger_1, trigger_2, user_input):
    # checks if variants entered fit either HGVS or VCF notation,
    # if so: stores them in dcc.Store "variant_queue_input", initiating VEP API requests
    if user_input is not None:
        variants = parse_input(user_input)
        variant_instances = [AutoCaSc(_variant, mode="web") for _variant in variants]
        if input_ok(variant_instances):
            variant_queue = {"instances": {_instance.__dict__.get("variant"): _instance.__dict__ for _instance in
                                           variant_instances}}
            return True, False, variant_queue
        else:
            return False, True, None
    raise PreventUpdate


@app.callback(
    Output("url", "pathname"),
    Input("search_button", "n_clicks"),
    State("variant_queue_input", "data"),
    State("variant_queue_url", "data"),
    State("inheritance_input", "value")
)
def search_button_click(n_clicks, variant_queue_input, variant_queue_url, inheritance):
    # by clicking the "Search" button on the landing page, the URL is updated, triggering the calculation and display
    # of the results page
    variant_queue = variant_queue_input or variant_queue_url
    if n_clicks is not None and not variant_queue is None and not inheritance is None:
        variants = [variant_queue.get("instances").get(_key).get("variant") for _key in
                    variant_queue.get("instances").keys()]
        url_suffix = quote(f"/search/inheritance={inheritance}/variants={'%'.join(variants)}")
        return url_suffix
    else:
        raise PreventUpdate


@app.callback(
    Output("query_memory", "data"),
    Input("url", "pathname"),
    State("query_memory", "data")
)
def interpret_url_inheritance(pathname, query_memory):
    # this extracts inheritance from URL in case the site is not accessed via landing page e.g. if results are refreshed
    if "search" in pathname and query_memory is None:
        inheritance = unquote(pathname).split("inheritance=")[-1].split("/")[0]
        query_data = {"inheritance": inheritance}
        return query_data
    raise PreventUpdate


@app.callback(
    Output("variant_queue_url", "data"),
    Input("url", "pathname"),
    State("variant_memory", "data")
)
def interpret_url_variants(pathname, variant_memory):
    # this extracts variants from URL in case the site is not accessed via landing page e.g. if results are refreshed
    if "search" in pathname and variant_memory is None:
        variants = unquote(pathname).split("variants=")[-1].split("%")
        variant_instances = [AutoCaSc(_variant, mode="web") for _variant in variants]
        variant_queue = {"instances": {_instance.__dict__.get("variant"): _instance.__dict__ for _instance in
                                       variant_instances}}
        return variant_queue
    elif "search" in pathname:
        variants = unquote(pathname).split("variants=")[-1].split("%")
        if any([_variant not in variant_memory.get("instances").keys() for _variant in variants]):
            variant_instances = [AutoCaSc(_variant, mode="web") for _variant in variants]
            variant_queue = {"instances": {_instance.__dict__.get("variant"): _instance.__dict__ for _instance in
                                           variant_instances}}
            return variant_queue
    raise PreventUpdate


def show_other_variant_column(results_memory):
    if any([results_memory.get("instances").get(_variant).get("inheritance") == "comphet"
            for _variant in results_memory.get("instances").keys()]):
        return True
    else:
        return False


@app.callback(
    Output("transcripts_to_use_memory", "data"),
    Input("transcript_dropdown", "value"),
    State("transcripts_to_use_memory", "data"),
    State("card_tabs", "active_tab"),
    State("results_memory", "data")
)
def update_transcripts_to_use(selected_transcript,
                              transcript_dict,
                              active_tab,
                              results_memory):
    # manually selecting a transcript of the dropdown menu, this choice is stored in dcc.Store
    # "transcripts_to_use_memory", so that for corresponding comphet variants the same transcript is used
    if not transcript_dict:
        transcript_dict = {}
    tab_num = int(active_tab.split("_")[-1])
    _variant = list(results_memory.get("instances").keys())[tab_num]
    transcript_dict[_variant] = selected_transcript

    if results_memory.get("instances").get(_variant).get("inheritance") == "comphet":
        _other_variant = results_memory.get("instances").get(_variant).get("other_variant")
        transcript_dict[_other_variant] = selected_transcript
    return transcript_dict


@app.callback(
    Output("card_content", "children"),
    Output("active_variant_tab", "data"),
    Input("card_tabs", "active_tab"),  # todo: check out pattern-matching callbacks to avoid callback error
    Input("transcripts_to_use_memory", "data"),
    State("results_memory", "data"),
)
def get_tab_card(active_tab,transcripts_to_use,results_memory):
    x =  ResultCard.ResultCard(active_tab,transcripts_to_use,results_memory)
    return x

@app.callback(
    Output("about_text", "children"),
    Output("about_language_button", "children"),
    Input("about_language_button", "n_clicks"),
    State("about_language_button", "children")
)
def get_about_text(n_clicks, language):
    # changes about page text between English and German
    if not n_clicks:
        raise PreventUpdate
    if language == "DE":
        return about_ger, "EN"
    else:
        return about_eng, "DE"


@app.callback(
    Output("impressum_text", "children"),
    Output("impressum_language_button", "children"),
    Input("impressum_language_button", "n_clicks"),
    State("impressum_language_button", "children")
)
def get_impressum_text(n_clicks, language):
    # changes impressum content between English and German
    if not n_clicks:
        raise PreventUpdate
    if language == "DE":
        return impressum_ger, "EN"
    else:
        return impressum_eng, "DE"


@app.callback(
    Output("faq_text", "children"),
    Output("faq_language_button", "children"),
    Input("faq_language_button", "n_clicks"),
    State("faq_language_button", "children")
)
def get_faq_text(n_clicks, language):
    # changes FAQ text between English and German
    if not n_clicks:
        raise PreventUpdate
    if language == "DE":
        return faq_ger, "EN"
    else:
        return faq_eng, "DE"

########## BACKEND ##########
score_variants = backend.score_variants
dict_to_instances = backend.dict_to_instances
instances_to_dict = backend.instances_to_dict
store_instances = backend.store_instances


@app.callback(
    Output("variant_memory", "data"),
    Input("variant_queue_input", "data"),
    Input("variant_queue_url", "data"),
    [State("variant_memory", "data")]
)
def retrieve_variant_data(variant_queue_input, variant_queue_url, variant_memory):
    # triggered by adding variants to dcc.Store "variant_queue_input" (input form) or "variant_queue_url" (url access)
    variant_queue = variant_queue_input or variant_queue_url
    if variant_queue:
        if variant_memory is not None:
            if variant_queue.get("instances").keys() == variant_memory.get("instances").keys():
                return store_instances(dict_to_instances(variant_memory))
        instances = dict_to_instances(variant_queue)
        for _instance in instances:
            if not _instance.data_retrieved:
                _instance.retrieve_data()  # this initiates API calls
        return store_instances(instances)
    else:
        raise PreventUpdate


@app.callback(
    Output("results_memory", "data"),
    Input("variant_memory", "data"),
    Input("query_memory", "data")
)
def calculate_results(variant_memory, query_memory):
    # triggered by storing new variant instances or change of query parameters like inheritance
    inheritance = None
    if query_memory:
        inheritance = query_memory.get("inheritance")
    if variant_memory is not None and inheritance is not None:
        instances = dict_to_instances(variant_memory)
        instances = score_variants(instances, inheritance)
        return store_instances(instances)
    raise PreventUpdate


@app.callback(
    Output("download", "data"),
    Input("download_button", "n_clicks"),
    State("results_memory", "data"),
    State("transcripts_to_use_memory", "data")
)
def download_button_click(n_cklicks, results_memory, transcripts_to_use):
    # this compiles and provides the summary table
    # todo check comphet behavior
    if not n_cklicks:
        raise PreventUpdate
    
    x = download.download(results_memory, transcripts_to_use)
    return x

if __name__ == '__main__':
    app.run_server(debug=True,
                   dev_tools_hot_reload=True,
                   host='0.0.0.0',
                   port=5000
                   )

from elements.frontend import frontend
from elements.backend import backend
from elements.frontend.static_pages.about import about as abouttxt
from elements.frontend.static_pages.faq import faq as faqtxt
from elements.frontend.static_pages.impressum import impressum as impressumtxt
from elements.frontend.static_pages.news import news as newstxt
from elements.frontend.static_pages.instructions import instructions as instructionstxt
from elements.frontend.callbacks import ResultCard
from elements.frontend.callbacks import download
from elements.frontend.landingpage import landingpage as landingpagetxt
from elements.frontend.static_pages.loading import loading
from elements.frontend.appframe import appframe
from statistics import mean

import dash
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import unquote, quote
import os, sys
from AutoCaSc_core.AutoCaSc import AutoCaSc, VERSION

from refseq_transcripts_converter import convert_variant
from elements import ids

ids = ids.ids

frontend_frontend_overview_tab = ids["frontend_frontend_overview_tab"]
frontend_frontend_active_variant_tab =ids["frontend_frontend_active_variant_tab"]
frontend_frontend_card_tabs = ids["frontend_frontend_card_tabs"]
frontend_frontend_card_content = ids["frontend_frontend_card_content"]
frontend_frontend_sysid_badge = ids["frontend_frontend_sysid_badge"]
frontend_frontend_gene_badge = ids["frontend_frontend_gene_badge"]
frontend_callbacks_resultcard_download_button = ids["frontend_callbacks_resultcard_download_button"]
frontend_callbacks_resultcard_percentile_target = ids["frontend_callbacks_resultcard_percentile_target"]
frontend_callbacks_resultcard_hover_target = ids["frontend_callbacks_resultcard_hover-target"]
frontend_callbacks_resultcard_transcript_dropdown = ids["frontend_callbacks_resultcard_transcript_dropdown"]
frontend_callbacks_resultcard_collapse_button_transcripts = ids["frontend_callbacks_resultcard_collapse_button_transcripts"]
frontend_callbacks_resultcard_collapse_transcripts = ids["frontend_callbacks_resultcard_collapse_transcripts"]
frontend_input_input_variant_input = ids["frontend_input_input_variant_input"]
frontend_input_input_inheritance_input = ids["frontend_input_input_inheritance_input"]
frontend_input_input_genomeversion_input = ids["frontend_input_input_genomeversion_input"]
frontend_landingpage_landingpage_search_button = ids["frontend_landingpage_landingpage_search_button"]
frontend_staticpages_about_about_about_language_button = ids["frontend_staticpages_about_about_about_language_button"]
frontend_staticpages_about_about_about_text = ids["frontend_staticpages_about_about_about_text"]
frontend_staticpages_faq_faq_faq_language_button = ids["frontend_staticpages_faq_faq_faq_language_button"]
frontend_staticpages_faq_faq_faq_text = ids["frontend_staticpages_faq_faq_faq_text"]
frontend_staticpages_header_footer_footer_footer_toggler = ids["frontend_staticpages_header_footer_footer_footer-toggler"]
frontend_staticpages_header_footer_footer_footer_collapse = ids["frontend_staticpages_header_footer_footer_footer-collapse"]
frontend_staticpages_header_footer_navbar_navbar_toggler = ids["frontend_staticpages_header_footer_navbar_navbar-toggler"]
frontend_staticpages_header_footer_navbar_navbar_collapse = ids["frontend_staticpages_header_footer_navbar_navbar-collapse"]
url = ids["url"]
frontend_staticpages_header_footer_urlbar_download = ids["frontend_staticpages_header_footer_urlbar_download"]
frontend_staticpages_header_footer_urlbar_warning_toast = ids["frontend_staticpages_header_footer_urlbar_warning-toast"]
frontend_staticpages_impressum_impressum_page_content = ids["frontend_staticpages_impressum_impressum_page-content"]
frontend_staticpages_impressum_impressum_impressum_language_button = ids["frontend_staticpages_impressum_impressum_impressum_language_button"]
frontend_staticpages_impressum_impressum_impressum_text = ids["frontend_staticpages_impressum_impressum_impressum_text"]
frontend_staticpages_news_news_faq_text = ids["frontend_staticpages_news_news_faq_text"]



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





#URL checker
##checks the selected inheritance in the URL
@app.callback(
    Output("query_memory", "data"),
    Input(url, "pathname"),
    State("query_memory", "data")
)
def interpret_url_inheritance(pathname, query_memory):
    # this extracts inheritance from URL in case the site is not accessed via landing page e.g. if results are refreshed
    if "search" in pathname and query_memory is None:
        inheritance = unquote(pathname).split("inheritance=")[-1].split("/")[0]
        query_data = {"inheritance": inheritance}
        return query_data
    raise PreventUpdate


##checks the variant in the URL
@app.callback(
    Output("variant_queue_url", "data"),
    Input(url, "pathname"),
    State("variant_memory", "data")
)
def interpret_url_variants(pathname, variant_memory):
    # this extracts variants from URL in case the site is not accessed via landing page e.g. if results are refreshed
    if "search" in pathname and variant_memory is None:
        variants = unquote(pathname).split("variants=")[-1].split("%")
        genomeversion = unquote(pathname).split("genomeversion=")[-1].split("/")[0]
        variant_instances = [AutoCaSc(_variant, mode="web", assembly=genomeversion) for _variant in variants]
        variant_queue = {"instances": {_instance.__dict__.get("variant"): _instance.__dict__ for _instance in
                                       variant_instances}}
        return variant_queue
    elif "search" in pathname:
        variants = unquote(pathname).split("variants=")[-1].split("%")
        genomeversion = unquote(pathname).split("genomeversion=")[-1].split("/")[0]

        if any([_variant not in variant_memory.get("instances").keys() for _variant in variants]):
            variant_instances = [AutoCaSc(_variant, mode="web", assembly=genomeversion) for _variant in variants]
            variant_queue = {"instances": {_instance.__dict__.get("variant"): _instance.__dict__ for _instance in
                                           variant_instances}}
            return variant_queue
    raise PreventUpdate




#ContextChecker

@app.callback([Output(frontend_staticpages_impressum_impressum_page_content, 'children'),
              Output("query_memory", "clear_data"),
              Output("variant_queue_input", "clear_data"),
              Output("variant_queue_url", "clear_data"),
              Output("results_memory", "clear_data"),
              Output("transcripts_to_use_memory", "clear_data"),
              Output(frontend_staticpages_impressum_impressum_page_content, "align")],
              [Input(url, 'pathname'),
               Input("results_memory", "data")])
def display_page(pathname, results_memory):
    ctx = dash.callback_context
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





#NavigationBar
@app.callback(
        Output("navbar-collapse", "is_open"),
        [Input(frontend_staticpages_header_footer_navbar_navbar_toggler, "n_clicks")],
        [State("navbar-collapse", "is_open")])
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open













#InputPage
##Input Validation

#frontend_input_input_genomeversion_input


@app.callback(
    Output(frontend_input_input_variant_input, "valid"),
    Output(frontend_input_input_variant_input, "invalid"),
    Output("variant_queue_input", "data"),
    [Input(frontend_input_input_variant_input, "n_blur"),
     Input(frontend_input_input_inheritance_input, "value"),
     Input(frontend_input_input_genomeversion_input, "value")],
    [State(frontend_input_input_variant_input, "value")]
)
def check_user_input(trigger_1, trigger_2,genomeversion, user_input):
    # checks if variants entered fit either HGVS or VCF notation,
    # if so: stores them in dcc.Store "variant_queue_input", initiating VEP API requests
    if user_input is not None:
        #genomeversion=backend.clean_genomeversion(genomeversion)

        variants = parse_input(user_input)
        variant_instances = [AutoCaSc(_variant, mode="web",assembly=genomeversion) for _variant in variants]
        if input_ok(variant_instances):
            variant_queue = {"instances": {_instance.__dict__.get("variant"): _instance.__dict__ for _instance in
                                           variant_instances}}
            return True, False, variant_queue
        else:
            return False, True, None
    raise PreventUpdate


#InputPage
##URLstring
@app.callback(
    Output(url, "pathname"),
    Input(frontend_landingpage_landingpage_search_button, "n_clicks"),
    State("variant_queue_input", "data"),
    State("variant_queue_url", "data"),
    State(frontend_input_input_inheritance_input, "value"),
    State(frontend_input_input_genomeversion_input, "value")
    
)
def search_button_click(n_clicks, variant_queue_input, variant_queue_url, inheritance,genomeversion):

    # by clicking the "Search" button on the landing page, the URL is updated, triggering the calculation and display
    # of the results page
    variant_queue = variant_queue_input or variant_queue_url
    if n_clicks is not None and not variant_queue is None and not inheritance is None:
        #genomeversion=backend.clean_genomeversion(genomeversion)

        variants = [variant_queue.get("instances").get(_key).get("variant") for _key in
                    variant_queue.get("instances").keys()]
        url_suffix = quote(f"/search/genomeversion={genomeversion}/inheritance={inheritance}/variants={'%'.join(variants)}")
        return url_suffix
    else:
        raise PreventUpdate






#ResultPage
## Xlinked Warning - Cave
@app.callback(
    Output(frontend_staticpages_header_footer_urlbar_warning_toast, "is_open"),
    Input(frontend_staticpages_impressum_impressum_page_content, "children"),
    State("results_memory", "data")
)
def check_x_linkedness(_, results_memory):
    if results_memory is not None:
        for _variant, _instance_attributes in results_memory.get("instances").items():
            if _instance_attributes.get("inheritance") == "x_linked":
                if not _instance_attributes.get("vcf_string")[0] == "X":
                    return True
    return False





#ResultPage
## ResultCard




@app.callback(
    Output(frontend_frontend_card_content, "children"),
    Output(frontend_frontend_active_variant_tab, "data"),
    Input(frontend_frontend_card_tabs, "active_tab"),  # todo: check out pattern-matching callbacks to avoid callback error
    Input("transcripts_to_use_memory", "data"),
    State("results_memory", "data"),
)
def get_tab_card(active_tab,transcripts_to_use,results_memory):
    x =  ResultCard.ResultCard(active_tab,transcripts_to_use,results_memory)
    return x





#ResultPage
##AltTransscripts Collapsing
@app.callback(
    Output(frontend_callbacks_resultcard_collapse_transcripts, "is_open"),
    Output(frontend_callbacks_resultcard_collapse_transcripts, "children"),
    Input(frontend_callbacks_resultcard_collapse_button_transcripts, "n_clicks"),
    State(frontend_callbacks_resultcard_collapse_transcripts, "is_open"),
    State(frontend_frontend_active_variant_tab, "data")
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






#ResultPage
##LoadAll HGVSC Annotations
@app.callback(
    Output("transcripts_to_use_memory", "data"),
    Input(frontend_callbacks_resultcard_transcript_dropdown, "value"),
    State("transcripts_to_use_memory", "data"),
    State(frontend_frontend_card_tabs, "active_tab"),
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
            print(variant_memory)
            if variant_queue.get("instances").keys() == variant_memory.get("instances").keys():
                queue_assembly = [variant_queue['instances'][x].get('assembly') for x in variant_queue.get("instances").keys()]
                memory_assembly = [variant_memory['instances'][x].get('assembly') for x in variant_memory.get("instances").keys()]
                if queue_assembly ==memory_assembly:
                    return store_instances(dict_to_instances(variant_memory))
        instances = dict_to_instances(variant_queue)
        for _instance in instances:
            print(_instance.assembly)
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
    Output(frontend_staticpages_header_footer_urlbar_download, "data"),
    Input(frontend_callbacks_resultcard_download_button, "n_clicks"),
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







#AboutPage
##Language
@app.callback(
    Output(frontend_staticpages_about_about_about_text, "children"),
    Output(frontend_staticpages_about_about_about_language_button, "children"),
    Input(frontend_staticpages_about_about_about_language_button, "n_clicks"),
    State(frontend_staticpages_about_about_about_language_button, "children")
)
def get_about_text(n_clicks, language):
    # changes about page text between English and German
    if not n_clicks:
        raise PreventUpdate
    if language == "DE":
        return about_ger, "EN"
    else:
        return about_eng, "DE"


#ImpressumPage
##Language
@app.callback(
    Output(frontend_staticpages_impressum_impressum_impressum_text, "children"),
    Output(frontend_staticpages_impressum_impressum_impressum_language_button, "children"),
    Input(frontend_staticpages_impressum_impressum_impressum_language_button, "n_clicks"),
    State(frontend_staticpages_impressum_impressum_impressum_language_button, "children")
)
def get_impressum_text(n_clicks, language):
    # changes impressum content between English and German
    if not n_clicks:
        raise PreventUpdate
    if language == "DE":
        return impressum_ger, "EN"
    else:
        return impressum_eng, "DE"

#FAQPage
##Language
@app.callback(
    Output(frontend_staticpages_faq_faq_faq_text, "children"),
    Output(frontend_staticpages_faq_faq_faq_language_button, "children"),
    Input(frontend_staticpages_faq_faq_faq_language_button, "n_clicks"),
    State(frontend_staticpages_faq_faq_faq_language_button, "children")
)
def get_faq_text(n_clicks, language):
    # changes FAQ text between English and German
    if not n_clicks:
        raise PreventUpdate
    if language == "DE":
        return faq_ger, "EN"
    else:
        return faq_eng, "DE"


@app.callback(
        Output(frontend_staticpages_header_footer_footer_footer_collapse, "is_open"),
        [Input(frontend_staticpages_header_footer_footer_footer_toggler, "n_clicks")],
        [State(frontend_staticpages_header_footer_footer_footer_collapse, "is_open")])
def toggle_footer_collapse(n, is_open):
    if n:
        return not is_open
    return is_open







if __name__ == '__main__':
    app.run_server(debug=True,
                   dev_tools_hot_reload=True,
                   host='0.0.0.0',
                   port=5000
                   )





########### TabCard wird zusammen mit den backend memory storage initialisiert --> callback wird ausgefuert auch wenn es den input noch nicht gibt --> Fehler ; loesung Tabcard output gibt es erst wenn resultpage gealaden wurde
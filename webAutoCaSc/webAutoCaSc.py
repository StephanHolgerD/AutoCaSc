from elements.header_footer import footer as footertxt
from elements.header_footer import navbar as navbartxt
from elements.header_footer import urlbar as urlbartxt
from elements.frontend import frontend
from elements.backend import backend
from elements.about import about as abouttxt
from elements.faq import faq as faqtxt
from elements.impressum import impressum as impressumtxt
from elements.news import news as newstxt
from elements.instructions import instructions as instructionstxt


from elements.input import input as inputtxt

from elements.landingpage import landingpage as landingpagetxt
import copy
import io
from statistics import mean
from flask import Flask
import dash
from dash import dcc
from dash.dcc import Download
from dash import html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from urllib.parse import unquote, quote
import pandas as pd
from numpy import array
import re
import os, sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from AutoCaSc_core.AutoCaSc import AutoCaSc, VERSION
#from dash_extensions import Download
from refseq_transcripts_converter import convert_variant

server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                server=server,
                suppress_callback_exceptions=True)
app.title = "webAutoCaSc"
footer = footertxt.footer
navbar = navbartxt.navbar
url_bar_and_content_div = urlbartxt.url_bar_and_content_div
variant_input_card = inputtxt.variant_input_card 
misc_input_card = inputtxt.misc_input_card
landing_page = landingpagetxt.landing_page

search_page = dbc.Container([
    dbc.Spinner(fullscreen=True)
])

error_page = dbc.Container([
    html.H3(
        "Looks like something went wrong..."
    ),
])

about_eng = abouttxt.about_eng
about_ger = abouttxt.about_ger
about_page = abouttxt.about_page
browser_compatibility_header = faqtxt.browser_compatibility_header
browser_compatibility_row1 = faqtxt.browser_compatibility_row1
browser_compatibility_row2 = faqtxt.browser_compatibility_row2
browser_compatibility_row3 = faqtxt.browser_compatibility_row3
browser_compatibility_body = faqtxt.browser_compatibility_body
faq_ger = faqtxt.faq_ger 
faq_eng = faqtxt.faq_eng
tutorial_page = instructionstxt.tutorial_page
faq_page = faqtxt.faq_page
news_page = newstxt.news_page
impressum_ger = impressumtxt.impressum_ger
impressum_eng = impressumtxt.impressum_eng
impressum_page = impressumtxt.impressum_page


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


########## FRONTEND ##########
parse_input = frontend.parse_input
get_display_variant = frontend.get_display_variant
get_results_page = frontend.get_results_page
input_ok = frontend.input_ok
get_error = frontend.get_error
get_status_badge = frontend.get_status_badge
get_gene_badge = frontend.get_gene_badge
get_percentile = frontend.get_percentile
get_casc_color = frontend.get_casc_color

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
def get_tab_card(active_tab,
                 transcripts_to_use,
                 results_memory):
    # this updates the content of the currently displayed results card
    cell_style = {
        "padding": "5px",
        "padding-left": "12px"
    }
    if active_tab == "overview_tab":
        if show_other_variant_column(results_memory):
            other_variant_column_header = html.Th("Corresponding Variant")
        else:
            other_variant_column_header = None

        overview_table_header = html.Thead(
            html.Tr(
                [
                    html.Th("Variant"),
                    html.Th("Candidate Score"),
                    html.Th("HGVS"),
                    other_variant_column_header
                ],
            )
        )
        overview_table_rows = []
        tooltips = []

        for i, _variant in enumerate(results_memory.get("instances").keys()):

            if results_memory.get("instances").get(_variant).get("status_code") == 200:
                try:
                    if _variant in transcripts_to_use.keys():
                        _transcript = transcripts_to_use.get(_variant)
                    else:
                        _transcript = results_memory.get("instances").get(_variant).get("affected_transcripts")[0]
                except AttributeError:
                    _transcript = results_memory.get("instances").get(_variant).get("affected_transcripts")[0]
                _instance_attributes = results_memory.get("instances").get(_variant).get("transcript_instances").get(
                    _transcript)
            else:
                _instance_attributes = results_memory.get("instances").get(_variant)

            if _instance_attributes.get("gene_symbol"):
                _hgvs = _instance_attributes.get("gene_symbol")
                if _instance_attributes.get("hgvsc_change") is not None:
                    _hgvs += ":" + _instance_attributes.get("hgvsc_change")
                if _instance_attributes.get("hgvsp_change") is not None:
                    if ":" not in _hgvs:
                        _hgvs += ":"
                    else:
                        _hgvs += " "
                    _hgvs += _instance_attributes.get("hgvsp_change")
            else:
                _hgvs = None

            if show_other_variant_column(results_memory):
                other_variant_column = html.Th(
                    html.P(_instance_attributes.get("other_variant"),
                           id=f"other_variant_target_{i}"),
                    style=cell_style)
                tooltips.append(dbc.Tooltip(f"The corresponding compound heterozygous variant.",
                                            target=f"other_variant_target_{i}"))
            else:
                other_variant_column = None

            overview_table_rows.append(
                html.Tr(
                    [
                        html.Th(dbc.Row([dbc.Col(_variant,
                                                 width="auto"),
                                         dbc.Col(get_status_badge(_instance_attributes.get("status_code"), i),
                                                 width="auto")],
                                        justify="start",
                                        className="g-0"),
                                style=cell_style),
                        html.Th(_instance_attributes.get("candidate_score"),
                                style=cell_style),
                        html.Th(html.P(_hgvs,
                                       id=f"hgvs_target_{i}"),
                                style=cell_style),
                        other_variant_column
                    ]
                )
            )
            tooltips.append(dbc.Tooltip(f"Transcript: {_instance_attributes.get('transcript')}",
                                        target=f"hgvs_target_{i}"))

        overview_table = dbc.Table(
            [
                overview_table_header,
                html.Tbody(
                    overview_table_rows
                ),
            ],
            responsive=True,
            hover=True,
            striped=True,
        )
        tab_card_content = [
            html.Div(tooltips),
            dbc.Row(
                [
                    dbc.Col(html.H3("Overview on variants")),
                    dbc.Col(dbc.Button("Download",
                                       id="download_button",
                                       style={
                                           # "margin-bottom": "10px",
                                           "marginTop": "0",
                                           "padding": "10px"
                                       },
                                       size="large",
                                       color="secondary"),
                            width="auto"
                            )
                ],
                justify="between",
            ),
            overview_table
        ]
        return tab_card_content, None
    else:
        tab_num = int(active_tab.split("_")[-1])
        _variant = list(results_memory.get("instances").keys())[tab_num]

        if results_memory.get("instances").get(_variant).get("status_code") == 200:
            try:
                if _variant in transcripts_to_use.keys():
                    _transcript = transcripts_to_use.get(_variant)
                else:
                    _transcript = results_memory.get("instances").get(_variant).get("affected_transcripts")[0]
            except AttributeError:
                _transcript = results_memory.get("instances").get(_variant).get("affected_transcripts")[0]
            _instance_attributes = results_memory.get("instances").get(_variant).get("transcript_instances").get(
                _transcript)
        else:
            _instance_attributes = results_memory.get("instances").get(_variant)

        status_code = _instance_attributes.get("status_code")

        if len(results_memory.get("instances")) == 1:
            download_button = dbc.Col(dbc.Button("Download",
                                                       id="download_button",
                                                       color="secondary",
                                                       style={
                                                           "marginBottom": "10px",
                                                           "padding": "10px",
                                                           "marginTop": "0"
                                                       }
                                                       ),
                                            width="auto")
        else:
            download_button = None
        card_header = dbc.Row(
            [
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H3(
                                    f"Variant: {get_display_variant(_variant)}"),
                                width="auto"
                            ),
                            get_gene_badge(_instance_attributes)
                        ],
                    justify="start",
                    className="g-0"
                    ),
                    md=6
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(

                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.H3(
                                                        f"Candidate Score:",
                                                        id="percentile_target"),
                                                    width="auto"
                                                ),
                                                dbc.Col(
                                                    html.H3(_instance_attributes.get('candidate_score'),
                                                            id="hover-target",
                                                            style={
                                                                "border": "3px",
                                                                "borderStyle": "solid",
                                                                "borderColor": get_casc_color(_instance_attributes.get('candidate_score'), 'border'),
                                                                "borderRadius": "5px",
                                                                "padding": "7px",
                                                                "backgroundColor": get_casc_color(_instance_attributes.get('candidate_score'), 'background')
                                                            }
                                                        ),
                                                    width="auto"
                                                ),
                                                dbc.Popover(
                                                    f"About {get_percentile(_instance_attributes.get('candidate_score'))} of the variants scored "
                                                    f"at the Institute for Human Genetics Leipzig had a lower score than this.",
                                                    target="hover-target",
                                                    body=True,
                                                    trigger="hover",
                                                )
                                            ],
                                            class_name="flex-nowrap",
                                            align="center"
                                        )



                                    ],
                                    md=8
                                ),
                                download_button
                            ],
                            justify="between",
                            align="center"
                        ),

                    ],
                    md=6
                ),
            ],
            style={"marginBottom": "0",
                   "paddingBottom": "0"},
            align="center"
        )
        if status_code == 200:
            scoring_results = {
                "inheritance_score": "Inheritance",
                "gene_constraint_score": "Gene Constraint",
                "variant_score": "Variant Attributes",
                "gene_plausibility": "Literature Plausibility",
            }

            parameters = {
                "impact": "Impact",
                "cadd_phred": "CADD phred",
                "oe_lof_interval": "o/e LoF",
                "oe_mis_interval": "o/e mis",
                "gerp_rs_rankscore": "GERP++ RS",
                "allele_count": "gnomAD allele count"
            }
            if _instance_attributes.get("vcf_string")[0] == "X":
                parameters["n_hemi"] = "gnomAD hemizygous count"
            if _instance_attributes.get("inheritance") not in ["ad_inherited", "de_novo"]:
                parameters["ac_hom"] = "gnomAD homozygous count"

            casc_table_header = html.Thead(
                html.Tr(
                    [
                        html.Th("Subscore"),
                        html.Th("")
                    ]
                )
            )
            casc_table_rows = []
            for _subscore in scoring_results.keys():
                casc_table_rows.append(
                    html.Tr(
                        [
                            html.Th(scoring_results.get(_subscore),
                                    id=f"{_subscore}_description",
                                    scope="row",
                                    style=cell_style),
                            html.Td(_instance_attributes.get(_subscore),
                                    id=f"{_subscore}_explanation",
                                    style=cell_style)
                        ],
                    )
                )

            explanation_tooltips = [
                dbc.Tooltip(f"{_instance_attributes.get('explanation_dict').get('pli_z')}",
                            target="gene_constraint_score_explanation"),
                dbc.Tooltip(f"impact: {_instance_attributes.get('impact_score')}, "
                            f"insilico: {_instance_attributes.get('in_silico_score')}, "
                            f"conservation: {_instance_attributes.get('conservation_score')}, "
                            f"frequency: {_instance_attributes.get('frequency_score')}",
                            target="variant_score_explanation"),
                dbc.Tooltip(f"{_instance_attributes.get('explanation_dict').get('inheritance')}",
                            target="inheritance_score_explanation"),
                dbc.Tooltip(f"weighted sum from PubTator: {round(float(_instance_attributes.get('pubtator_score')) * 1.19, 2)} [max 1.19], "
                            f"GTEx: {round(float(_instance_attributes.get('gtex_score')) * 0.6, 2)} [max 0.6], "
                            f"PsyMuKB: {round(float(_instance_attributes.get('denovo_rank_score')) * 0.65, 2)} [max 0.65], "
                            f"DisGeNET: {round(float(_instance_attributes.get('disgenet_score')) * 1.66, 2)} [max 1.66], "
                            f"MGI: {round(float(_instance_attributes.get('mgi_score')) * 0.97, 2)} [max 0.97], "
                            f"STRING: {round(float(_instance_attributes.get('string_score')) * 0.98, 2)} [max 0.98]",
                            target="gene_plausibility_explanation")
            ]
            description_tooltips = [
                dbc.Tooltip("Points attributed for inheritance & segregation",
                            target="inheritance_score_description"),
                dbc.Tooltip("Points attributed for gene constraint parameters.",
                            target="gene_constraint_score_description"),
                dbc.Tooltip("Points attributed for insilico predictions, conservation and allele frequency",
                            target="variant_score_description"),
                dbc.Tooltip("Points attributed for data in literature databases, animal models, expression pattern, "
                            "interaction networks",
                            target="gene_plausibility_description")
            ]

            parameter_table_header = html.Thead(
                html.Tr(
                    [
                        html.Th("Parameter"),
                        html.Th("")
                    ],
                )
            )
            parameter_table_rows = []
            for _parameter in parameters.keys():
                parameter_table_rows.append(
                    html.Tr(
                        [
                            html.Th(parameters.get(_parameter),
                                    scope="row",
                                    style=cell_style),
                            html.Td(_instance_attributes.get(_parameter),
                                    style=cell_style,
                                    id=f"cell_{_parameter}")
                        ],
                    )
                )

            if _instance_attributes.get('explanation_dict').get("impact_splice_site"):
                impact_splice_site_tooltip = dbc.Tooltip(
                    _instance_attributes.get('explanation_dict').get("impact_splice_site"),
                    target="cell_impact"
                    )
            else:
                impact_splice_site_tooltip = html.Div()

            tab_card_content = [
                html.Div(description_tooltips + explanation_tooltips),
                impact_splice_site_tooltip,
                card_header,
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown(f"**Gene symbol:** {_instance_attributes.get('gene_symbol')}"),
                                className="col-12 col-md-6"),
                        dbc.Col(dbc.Row(
                            [
                                dbc.Col(dcc.Markdown("**Transcript:**"),
                                     width="auto",
                                     style={"marginTop": "6px"}
                                     ),
                                dbc.Col(dcc.Dropdown(
                                 options=[{"label": f"{_transcript}", "value": f"{_transcript}"} for _transcript in
                                          results_memory.get("instances").get(_variant).get(
                                              "transcript_instances").keys()],
                                 value=_transcript,
                                 clearable=False,
                                 style={
                                     "paddingLeft": "5px",
                                     "marginTop": "1px",
                                     "paddingTop": "0px"
                                 },
                                 id="transcript_dropdown"
                                 ))
                            ],
                            className="g-0",
                            align="start"
                        ),
                            className="col-12 col-md-6")
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown(f"**HGVS:** {_instance_attributes.get('hgvsc_change')} "
                                             f"{_instance_attributes.get('hgvsp_change') or ''}"),
                                className="col-12 col-md-6"),
                        dbc.Col(dcc.Markdown(f"**VCF:** {_instance_attributes.get('vcf_string')}"),
                                className="col-12 col-md-6")
                    ],
                ),
                # html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Table(
                                [
                                    casc_table_header,
                                    html.Tbody(
                                        casc_table_rows
                                    ),
                                ],
                                responsive=True,
                                hover=True,
                                striped=True,
                                style={"marginBottom": 0}
                            ),
                            className="col-12 col-md-6"
                        ),
                        dbc.Col(
                            dbc.Table(
                                [
                                    parameter_table_header,
                                    html.Tbody(
                                        parameter_table_rows
                                    ),
                                ],
                                responsive=True,
                                hover=True,
                                striped=True,
                                style={"marginBottom": 0}
                            ),
                            className="col-12 col-md-6"
                        )
                    ]
                ),
                # html.Br(),
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            [
                                "Load all HGVSC notations (coding only)"
                            ],
                            id="collapse_button_transcripts",
                            className="mb-3",
                            n_clicks=0,
                            color="secondary"
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Collapse(
                            dbc.Card(dbc.CardBody("This content is hidden")),
                            id="collapse_transcripts",
                            is_open=False
                    )
                    )
                )
            ]
            return tab_card_content, {"active_variant": f"{_transcript}:{_instance_attributes.get('hgvsc_change')}"}
        else:
            error_message, error_color = get_error(status_code)
            return dbc.Alert(error_message, color=error_color), None


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
    df = pd.DataFrame()
    for i, _variant in enumerate(results_memory.get("instances").keys()):
        try:
            if _variant in transcripts_to_use.keys():
                _transcript = transcripts_to_use.get(_variant)
            else:
                _transcript = \
                    list(results_memory.get("instances").get(_variant).get("transcript_instances").keys())[0]
        except AttributeError:
            _transcript = list(results_memory.get("instances").get(_variant).get("transcript_instances").keys())[0]

        _instance_attributes = \
            results_memory.get("instances").get(_variant).get("transcript_instances").get(_transcript)

        try:
            if _instance_attributes.get("vcf_string") in df["vcf_format_2"].to_list():
                continue
        except KeyError:
            pass
        if _instance_attributes.get("inheritance") == "comphet":
            comphet = True
            _other_variant = _instance_attributes.get("other_variant")
            _other_instance_attributes = results_memory.get("instances").get(_other_variant).get(
                "transcript_instances").get(_transcript)
        else:
            comphet = False
            _other_instance_attributes = {}
        df.loc[i, "hgnc_symbol"] = _instance_attributes.get("gene_symbol")
        df.loc[i, "transcript"] = _transcript
        df.loc[i, "vcf_format_1"] = _instance_attributes.get("vcf_string")
        df.loc[i, "vcf_format_2"] = _other_instance_attributes.get("vcf_string")
        df.loc[i, "cDNA_1"] = _instance_attributes.get("hgvsc_change")
        df.loc[i, "cDNA_2"] = _other_instance_attributes.get("hgvsc_change")
        df.loc[i, "amino_acid_1"] = _instance_attributes.get("hgvsp_change")
        df.loc[i, "amino_acid_2"] = _other_instance_attributes.get("hgvsp_change")
        df.loc[
            i, "var_1_full_name"] = f"{_instance_attributes.get('transcript')}:" \
                                    f"{_instance_attributes.get('hgvsc_change')} " \
                                    f"{_instance_attributes.get('hgvsp_change')}"
        if comphet:
            df.loc[
                i, "var_2_full_name"] = f"{_other_instance_attributes.get('transcript')}:" \
                                        f"{_other_instance_attributes.get('hgvsc_change')} " \
                                        f"{_other_instance_attributes.get('hgvsp_change')}"
        else:
            df.loc[i, "var_2_full_name"] = ""
        df.loc[i, "inheritance"] = _instance_attributes.get("inheritance")
        df.loc[i, "candidate_score"] = _instance_attributes.get("candidate_score")
        df.loc[i, "literature_plausibility"] = _instance_attributes.get("gene_plausibility")
        df.loc[i, "inheritance_score"] = _instance_attributes.get("inheritance_score")
        if comphet:
            df.loc[i, "variant_attribute_score"] = round(mean([_instance_attributes.get("variant_score"),
                                                               _other_instance_attributes.get("variant_score")]), 2)
        else:
            df.loc[i, "variant_attribute_score"] = _instance_attributes.get("variant_score")
        df.loc[i, "gene_constraint_score"] = _instance_attributes.get("gene_constraint_score")
        df["version"] = str(VERSION)

    data = io.StringIO()
    df.to_csv(data, sep="\t", decimal=",")
    data.seek(0)
    return dict(content=data.getvalue(), filename="AutoCaSc_results.tsv")


if __name__ == '__main__':
    app.run_server(debug=True,
                   dev_tools_hot_reload=True,
                   host='0.0.0.0',
                   port=5000
                   )

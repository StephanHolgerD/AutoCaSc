import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from elements.frontend import frontend

get_display_variant = frontend.get_display_variant
get_gene_badge = frontend.get_gene_badge
get_casc_color = frontend.get_casc_color
get_percentile = frontend.get_percentile
get_status_badge =  frontend.get_status_badge
def show_other_variant_column(results_memory):
    if any([results_memory.get("instances").get(_variant).get("inheritance") == "comphet"
            for _variant in results_memory.get("instances").keys()]):
        return True
    else:
        return False

def ResultCard(active_tab,transcripts_to_use,results_memory):
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
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

image_column_width = 8
text_column_width = 12 - image_column_width

tutorial_page = html.Div(
    [
        html.Br(),
        html.H2("Instructions"),
        html.Br(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='../../assets/faq_images/input.png',
                                         style={"maxWidth": "100%"}),
                                width=image_column_width),
                        dbc.Col(html.P("""Enter the variant (hg19!) to be analyzed in the input field. The formatting of the variant is checked and if it is ok a green frame appears. In case there is a problem, the frame is red and scoring cannot be started. Then select one of the available heritages for the entered variants and click on "Start search". For a more detailed explanation of the choices, please see above ("What do the inheritance options stand for?")."""),
                                width=text_column_width)
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/results.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """Scoring may take a moment, then the results overview will open. At the top left you will see the variant you entered. Two flags may appear here: if the gene is associated with a phenotype in OMIM and if the gene is listed as a candidate gene or known NDD gene in SysID. On the upper right side you will find the result highlighted in color. The bluer, the lower, the redder, the higher the result.
                                   Below this you will find general information: which gene is affected, what are the HGVS and VCF notations and which transcript was used for the evaluation. In the lower part there are two tables. The left table contains the scores achieved by the candidate variant in the four categories. For more detailed scoring information, please see "What do the 4 subscores stand for?" above. The right table contains detailed information about the corresponding variant: the VEP-predicted impact on protein function, the phred-scaled CADD score, gnomAD gene constraint metrics o/e LoF and o/e missense, GERP++ rank score and allele count in gnomAD."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/percentile.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """Hovering over the result will display what percentage of candidates evaluated at the Institute of Human Genetics in Leipzig achieved a lower score."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/subscores.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """If you hover over the result of a subscore, a short explanation of how the score is composed is displayed."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/transcripts.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """For many variants there are several transcripts for which the variant achieves an equally high CaSc. You can select all ENSEMBL transcripts with an equally high CaSc from the drop down menu to the right of "Transcript:"."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/all_notations.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """For an overview of even more (including RefSeq) transcripts, click on "Load all HGVSC notations (coding only)". After a short moment a list of all possible affected transcripts will be displayed."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/hgvsc_input.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """It is also possible to enter variants in HGVSC notation, but we strongly recommend to use VCF notation. Problems can occur especially when RefSeq transcripts are used. Since the annotation is done with VEP (Ensembl), it may not be possible to identify a corresponding Ensembl transcript."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/multiple_variants_input.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """It is also possible to enter multiple variants, these should be separated with a comma."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/multiple_variants_overview.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """The results are then presented in a tabular overview."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/multiple_variants_detailed.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """A click on one of the tabs labeled with the variants will lead you to the corresponding results of a variant."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='../../assets/faq_images/downloaded.png',
                                style={"maxWidth":"100%"}
                            ),
                            width=image_column_width),
                        dbc.Col(
                            html.P(
                                """Clicking on "Download" will download the results in tab-separated form."""
                            ),
                            width=text_column_width
                        )
                    ],
                    align="center"
                )
            ]
        )
    ]
)

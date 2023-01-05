import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from elements.input import input as inputtxt


variant_input_card = inputtxt.variant_input_card 
misc_input_card = inputtxt.misc_input_card
landing_page = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    dcc.Markdown("""# Welcome to **webAutoCaSc**,\n #### a webinterface for the automatic CaSc \
                    classification of research candidate variants in neurodevelopmental disorders."""),
                    dcc.Markdown("Enter your variant (hg19) of interest and presumed inheritance mode here:"),
                    variant_input_card,
                    misc_input_card
                ]
            ),
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Start search",
                        color="primary",
                        id="search_button"
                    ),
                    style={"paddingBottom": "10px"}
                )
            ]
        ),

        html.Br(),
        dbc.Row(
            dcc.Markdown(
                """**Reference**:  
                J. Lieberwirth, B. Büttner, C. Klöckner, K. Platzer, B. Popp, R. Abou Jamra. (2022). [AutoCaSc: Prioritizing candidate genes for neurodevelopmental disorders](https://onlinelibrary.wiley.com/doi/10.1002/humu.24451)"""
            )
        )
    ]
)
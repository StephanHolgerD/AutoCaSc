import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


news_page = dbc.Container(
    [
        html.Br(),
        dbc.Row([
            dbc.Col(html.H2("News"),
                    width="auto")
        ]),
        html.Br(),
        html.Div(
            [
                dcc.Markdown(
                    """**29.08.2022**  
                    Our paper has been published and can be found here: [AutoCaSc: Prioritizing candidate genes for neurodevelopmental disorders](https://onlinelibrary.wiley.com/doi/10.1002/humu.24451).
                    """
                ),
                html.Hr(),
                dcc.Markdown(
                    """**20.06.2022**  
                    Our manuscript is available as a preprint at [Authorea](https://www.authorea.com/users/479253/articles/567112-autocasc-prioritizing-candidate-genes-for-neurodevelopmental-disorders).
                    """
                )
            ],
            id="faq_text")
    ],
    style={"height": "calc(100vh - 150px)"}
)
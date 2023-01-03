import dash_bootstrap_components as dbc
from dash import html


footer = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                html.Img(src='../../assets/by-nc-sa.eu.svg',
                         height="30px"
                         ),
                href="https://creativecommons.org/licenses/by-nc-sa/4.0/",
                target="_blank"),
            dbc.NavbarToggler(id="footer-toggler"),
            dbc.Collapse(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavLink("Github",
                                        href='https://github.com/JohannKaspar/AutoCaSc',
                                        target="_blank",
                                        style={"color": "#ffffff"}),
                            align="center",
                            width="auto"),
                        dbc.Col(dbc.NavLink("Human Genetics Leipzig",
                                            href='https://www.uniklinikum-leipzig.de/einrichtungen/humangenetik',
                                            target="_blank",
                                            style={"color": "#ffffff"}),
                                align="center",
                                width="auto"),
                        dbc.Col(dbc.NavLink("Our Paper",
                                            href="https://onlinelibrary.wiley.com/doi/10.1002/humu.24451",
                                            target="_blank",
                                            style={"color": "#ffffff"}),
                                align="center",
                                width="auto"
                                )
                    ],
                    className="ms-auto flex-nowrap mt-3 mt-md-0 g-0",
                    align="center",
                ),
                id="footer-collapse",
                navbar=True,
            )
        ]
    ),
    color="dark",
    dark=True,
    fixed="bottom"
)
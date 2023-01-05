import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


variant_input_card = html.Div(
    [
        dbc.Input(
            type="text",
            id="variant_input",
            placeholder="e.g. chrX-12345-T-C",
            autoFocus=True
        ),
        dcc.Markdown('''Although HGVS might work in some cases, we recommend using VCF format. 
                     Examples: [chr12-121987483-AT-A](/search/inheritance%3Dad_inherited/variants%3D12%3A121987483%3AAT%3AA), 
                     [11:94730916:A:C](/search/inheritance%3Dde_novo/variants%3D11%3A94730916%3AA%3AC), 
                     [X-101409056-A-C](/search/inheritance%3Dx_linked/variants%3DX%3A101409056%3AA%3AC),
                     [NC_000005.9:g.65466513_65466516del](/search/inheritance%3Dde_novo/variants%3DNC_000005.9%3Ag.65466513_65466516del), 
                     [ENST00000378402.5:c.4966G>A](/search/inheritance%3Dhomo/variants%3DENST00000378402.5%3Ac.4966G%3EA),
                     [NM_012285.3:c.2946C>A](/search/inheritance%3Dunknown/variants%3DNM_012285.3%3Ac.2946C>A)
                     ''',
                     style={"fontSize": "12px",
                            "marginTop": "10px"})
    ]
)

misc_input_card = html.Div(
    [
        dbc.RadioItems(
            id="inheritance_input",
            options=[
                {"label": "De novo", "value": "de_novo"},
                {"label": "Inherited dominant", "value": "ad_inherited"},
                {"label": "Homozygous recessive", "value": "homo"},
                {"label": "X-linked", "value": "x_linked"},
                {"label": "Compound heterozygous", "value": "comphet"},
                {"label": "Unknown", "value": "unknown"}
            ],
            inline=True
        ),
    ]
)
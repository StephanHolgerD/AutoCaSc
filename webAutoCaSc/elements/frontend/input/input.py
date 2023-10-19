import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


variant_input_card = html.Div(
    [
        dbc.Input(
            type="text",
            id="frontend_input_input_variant_input",
            placeholder="e.g. chrX-12345-T-C",
            autoFocus=True
        ),
        dcc.Markdown('''**HG19 Examples**: [chr12-121987483-AT-A](/search/genomeversion%3DGRCh37/inheritance%3Dad_inherited/variants%3D12%3A121987483%3AAT%3AA), 
                     [11:94730916:A:C](/search/genomeversion%3DGRCh37/inheritance%3Dde_novo/variants%3D11%3A94730916%3AA%3AC), 
                     [X-101409056-A-C](/search/genomeversion%3DGRCh37/inheritance%3Dx_linked/variants%3DX%3A101409056%3AA%3AC),
                     [NC_000005:g.65466513_65466516del](/search/genomeversion%3DGRCh37/inheritance%3Dde_novo/variants%3DNC_000005%3Ag.65466513_65466516del), 
                     [ENST00000378402.5:c.4966G>A](/search/genomeversion%3DGRCh37/inheritance%3Dhomo/variants%3DENST00000378402.5%3Ac.4966G%3EA),
                     [NM_012285.3:c.2946C>A](/search/genomeversion%3DGRCh37/inheritance%3Dunknown/variants%3DNM_012285.3%3Ac.2946C>A)
                     ''',
                     style={"fontSize": "12px",
                            "marginTop": "10px"}),
		dcc.Markdown('''**HG38 Examples**: [chr12-121549578-AT-A](/search/genomeversion%3DGRCh38/inheritance%3Dad_inherited/variants%3D12%3A121549578%3AAT%3AA), 
                     [11:94997752:A:C](/search/genomeversion%3DGRCh38/inheritance%3Dde_novo/variants%3D11%3A94997752%3AA%3AC), 
                     [X-102154084-A-C](/search/genomeversion%3DGRCh38/inheritance%3Dx_linked/variants%3DX%3A102154084%3AA%3AC),
                     [NC_000005:g.66170685_66170688del](/search/genomeversion%3DGRCh38/inheritance%3Dde_novo/variants%3DNC_000005%3Ag.66170685_66170688del), 
                     [ENST00000378402.5:c.4966G>A](/search/genomeversion%3DGRCh38/inheritance%3Dhomo/variants%3DENST00000378402.5%3Ac.4966G%3EA),
                     [NM_012285.3:c.2946C>A](/search/genomeversion%3DGRCh38/inheritance%3Dunknown/variants%3DNM_012285.3%3Ac.2946C>A)
                     ''',
                     style={"fontSize": "12px",
                            "marginTop": "10px"})
    ]
)




misc_input_card = html.Div(
    [
        dbc.RadioItems(
            id="frontend_input_input_inheritance_input",
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

genomeversion_input_card = html.Div(
    [
        dbc.RadioItems(
            id="frontend_input_input_genomeversion_input",
            options=[
                {"label": "HG19", "value": "GRCh37"},
                {"label": "HG38", "value": "GRCh38"}
            ],
            inline=True,
			value='GRCh37'
        ),
    ]
)
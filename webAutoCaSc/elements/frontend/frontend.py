import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dcc import Download

########## FRONTEND ##########
def parse_input(input):
    # basic string_formatting and initiating AutoCaSc intsances in order to check if input is ok
    return [input.split(",")[i].strip() for i in range(len(input.split(",")))]


def get_display_variant(_variant, n_chars=25):
    if len(_variant) < (n_chars + 5):
        return _variant
    else:
        return _variant[:n_chars] + "..."


def get_results_page(results_memory):
    if not results_memory:
        return error_page
    else:
        tab_list = []
        initial_tab = "tab_0"
        tab_num = 0
        if len(results_memory.get("instances").items()) > 1:
            tab_list.append(dbc.Tab(
                label="Overview",
                tab_id="overview_tab"
            ))
            initial_tab = "overview_tab"
        for _variant, _instance_attributes in results_memory.get("instances").items():
            tab_list.append(dbc.Tab(label=get_display_variant(_variant), tab_id=f"tab_{tab_num}"))
            tab_num += 1

        results_page = dbc.Container(
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Row(
                            [
                                dbc.Tabs(
                                    tab_list,
                                    id="card_tabs",
                                    active_tab=initial_tab,
                                ),

                            ],
                            className="align-items-baseline",
                            style={
                                "paddingBottom": "0 !important",
                                "marginBottom": "0 !important",
                                "paddingLeft": "10px",
                                "paddingRight": "10px",
                            },
                            justify="between",
                        ),
                    ),
                    dbc.CardBody(
                        html.P(id="card_content"),
                        style={"paddingBottom": "0"}
                    )
                ]
            ),
            style={"width": "100%",
                   # "minHeight": "calc(100vh - 150px)"
                   }
        )
        return results_page


def input_ok(instances):
    for instance in instances:
        if instance.variant_format == "incorrect":
            return False
    return True


def get_error(error_code):
    error_dict = {
        201: ("Error: The reference sequence does not match GRCh37!", "warning"),
        301: ("Error: Could not identify the corresponding compound heterozygous variant!", "danger"),
        400: ("Error: Could not process variant. Please try VCF annotation or HGVS annotation using HGNC gene symbol!",
              "danger"),
        496: ("Error: The alternative sequence matches the GRCh37 reference sequence!", "danger"),
        498: ("Error: You have entered an intergenic variant.", "danger")
    }
    return error_dict.get(error_code) or (f"Some error occurred. Code {error_code}", "warning")


def get_status_badge(status_code, i=None):
    if status_code == 200:
        return None
    else:
        error_message, error_color = get_error(status_code)
        return_badge = html.Div(
            [
                dbc.Badge(status_code, color=error_color, className="mx-2", id=f"return_badge_{i}"),
                dbc.Tooltip(error_message, target=f"return_badge_{i}")
            ]
        )
    return return_badge

def get_gene_badge(_instance_attributes):
    sysid = _instance_attributes.get("sysid")
    if sysid == "known NDD":
        sysid_color = "success"
    elif sysid == "candidate":
        sysid_color = "warning"
    else:
        sysid_color = None
        sysid_badge = None
        omim_color = "danger"
        omim_comment = "Gene has associated phenotypes in OMIM, but is not listed in SysID: "

    if sysid_color:
        sysid_badge = html.Div(
                [
                    dbc.Badge("SysID", color=sysid_color, className="mx-2", id="sysid_badge"),
                    dbc.Tooltip(sysid, target="sysid_badge")
                ]
            )
        omim_color = "warning"
        omim_comment = ""

    omim_ids = _instance_attributes.get("mim_number")
    if omim_ids is not None:
        omim_ids = omim_ids.split(",")
        omim_badge = html.Div(
                [
                    dbc.Badge("OMIM", color=omim_color, className="mx-2", id="gene_badge"),
                    dbc.Tooltip(omim_comment + str(omim_ids), target="gene_badge")
                ]
            )
    else:
        omim_badge = None

    return dbc.Col(
        dbc.Row(
            [dbc.Col(omim_badge,
                     width="auto"),
             dbc.Col(sysid_badge,
                     width="auto")],
            justify="start",
            className="g-0"
        ),
           width="auto")
    # if status_code == 200:
    #     return None
    # else:
    #     error_message, error_color = get_error(status_code)
    #     return_badge = html.Div(
    #         [
    #             dbc.Badge(status_code, color=error_color, className="mx-2", id=f"return_badge_{i}"),
    #             dbc.Tooltip(error_message, target=f"return_badge_{i}")
    #         ]
    #     )
    # return return_badge

def get_percentile(candidate_score):
    try:
        int(candidate_score)
        internal_scores = [10.46, 9.24, 9.86, 9.51, 11.81, 9.24, 10.5, 8.42, 8.03, 9.56, 0.0, 10.52, 8.04, 9.29, 9.66,
                           9.02, 7.22, 8.33, 10.37, 9.97, 0.0, 9.06, 6.87, 10.2, 9.06, 9.35, 8.01, 8.63, 8.94, 7.58,
                           8.47, 8.12, 8.9, 8.45, 9.19, 8.34, 5.85, 5.02, 7.96, 6.69, 8.14, 0.0, 7.63, 7.81, 8.06, 7.62,
                           6.28, 8.81, 8.41, 10.34, 9.64, 0.0, 8.23, 5.99, 0.0, 8.09, 8.78, 9.57, 6.61, 0.0, 8.43, 9.35,
                           5.74, 6.84, 6.39, 7.54, 9.04, 9.23, 9.31, 6.35, 10.0, 4.82, 7.9, 5.08, 8.5, 6.6, 8.05, 5.95,
                           6.2, 8.77, 6.49, 7.53, 0.0, 6.75, 0.0, 6.46, 5.0, 8.05, 7.76, 5.5, 5.79, 4.36, 8.76, 6.31,
                           5.86, 5.07, 7.53, 0.0, 6.79, 0.0, 9.53, 8.09, 6.63, 6.11, 7.24, 10.86, 5.57, 5.55, 6.73, 7.9,
                           7.34, 6.81, 7.66, 5.56, 6.1, 7.47, 6.03, 8.32, 3.85, 7.21, 5.46, 0.0, 8.32, 7.79, 9.16, 5.83,
                           5.05, 5.18, 5.41, 7.51, 6.28, 5.71, 5.99, 5.12, 6.41, 0.0, 5.88, 5.31, 6.46, 4.95, 0.0, 6.04,
                           5.12, 6.44, 4.74, 3.95, 4.37, 6.21, 4.66, 5.52, 5.76, 4.66, 6.24, 8.1, 5.15, 4.89, 4.94,
                           8.04, 0.0, 7.23, 5.02, 6.66, 4.94, 5.04, 7.97, 4.71, 5.84, 6.77, 5.67, 6.04, 4.6, 6.24, 5.85,
                           6.68, 5.07, 5.55, 7.57, 5.98, 7.99, 4.21, 6.89, 8.4, 6.89, 5.55, 5.18, 5.93, 6.88, 6.83,
                           6.22, 7.68, 5.95, 6.62, 4.05, 3.7, 6.09, 8.1, 0.0, 6.42, 4.19, 5.26, 0.0, 0.0, 4.03, 5.23,
                           3.96, 6.4, 5.53, 8.32, 5.92, 8.25, 0.0, 0.0, 5.7, 5.36, 4.99, 0.0, 0.0, 5.04, 6.28, 4.96,
                           0.0, 0.0, 5.94, 4.73, 6.16, 4.85, 7.14, 0.0, 5.05, 5.44, 0.0, 5.12, 5.84, 5.0, 6.46, 4.45,
                           6.75, 4.7, 0.0, 0.0, 3.45, 5.44, 6.22, 5.24, 0.0, 4.94, 5.83, 0.0, 5.13, 6.45, 4.65, 5.64,
                           6.02, 6.34, 5.94, 5.33, 5.04, 4.89, 6.21, 4.36, 0.0, 0.0, 6.23, 0.0, 6.22, 5.12, 5.94, 4.18,
                           6.03, 5.18, 5.51, 5.04, 5.49, 6.15, 3.83, 7.9, 4.88, 8.07, 6.67, 5.28, 5.26, 5.19, 4.95, 5.0,
                           4.26, 7.82, 5.8, 5.89, 5.98, 5.02, 5.39, 6.69, 0.0, 0.0, 6.98, 8.03, 4.63, 5.75, 6.43, 6.5,
                           6.6, 6.22, 4.41, 6.32, 4.57, 5.41, 5.73, 0.0, 4.82, 5.53, 0.0, 5.26, 0.0, 6.77, 4.72, 4.46,
                           4.66, 5.24, 4.31, 0.0, 4.6, 6.11, 4.74, 4.23, 4.75, 4.91, 4.96, 4.73, 4.58, 3.41, 4.92, 0.0,
                           5.45, 7.24, 4.08, 5.79, 0.0, 4.76, 5.1, 6.11, 0.0, 4.27, 4.98, 0.0, 4.17, 5.05, 4.88, 6.78,
                           4.73, 5.03, 5.6, 5.94, 0.0, 6.22, 4.38, 5.76, 4.35, 5.15, 5.91, 4.54, 0.0, 5.17, 0.0, 4.84,
                           4.8, 4.23, 5.09, 4.38, 4.62, 4.65, 4.5, 6.74, 5.51, 4.26, 5.19, 4.88, 6.01, 4.38, 5.63, 4.84,
                           0.0, 0.0, 5.1, 5.7, 4.98, 4.84, 6.35, 5.54, 4.09, 5.0, 0.0, 0.0, 4.01, 5.54, 3.91, 0.0, 4.64,
                           8.49, 3.56, 6.4, 0.0, 4.59, 4.15, 7.2, 4.79, 4.85, 0.0, 0.0, 3.7, 3.84, 4.8, 4.04, 5.14,
                           6.07, 5.81, 4.81, 0.0, 4.07, 4.73, 4.78, 4.32, 5.2, 4.93, 0.0, 2.28, 3.25, 3.5, 4.28, 4.78,
                           4.15, 4.29, 6.32, 7.4, 5.54, 4.19, 0.0, 4.84, 0.0, 5.21, 5.36, 3.71, 0.0, 4.92, 3.68, 6.24,
                           4.39, 5.22, 0.0, 4.3, 3.71, 3.94, 2.86, 5.36, 2.53, 0.0, 7.04, 0.0, 4.55, 5.1, 4.16, 4.53,
                           4.91, 5.29, 6.18, 0.0, 4.61, 6.32, 3.57, 4.85, 0.0, 3.2, 2.29, 0.0, 0.0, 0.0, 4.39, 4.01,
                           5.66, 5.46, 0.0, 4.37, 4.96, 3.67, 5.89, 5.01, 2.46, 3.56, 0.0, 3.83, 4.61, 5.31, 0.0, 4.58,
                           3.5, 6.04, 5.21, 0.0, 1.26, 2.17, 0.0, 0.0, 3.16, 4.38, 3.08, 2.33, 4.61, 4.57, 4.84, 3.14,
                           0.0, 3.32, 4.03, 4.8, 4.92, 4.73, 5.81, 3.12, 0.0, 5.58, 6.04, 3.55, 3.59, 0.0, 0.0, 3.77,
                           5.69, 3.68, 0.0, 3.4, 3.13, 0.0, 3.99, 5.45, 4.66, 4.67, 3.68, 3.77, 0.0, 0.0, 4.71, 0.0,
                           4.01, 3.48, 2.39, 3.73, 3.29, 5.18, 0.0, 0.0, 0.0, 3.32, 2.86, 0.0, 0.0, 5.02, 4.25, 6.38,
                           0.0, 0.0, 2.83, 0.0, 4.19, 0.0, 3.28, 3.45, 4.72, 3.54, 4.96, 3.12, 0.0, 4.54, 4.61, 3.44,
                           3.08, 1.93, 4.63, 3.1, 0.0, 3.96, 4.59, 3.26, 5.0, 5.17, 4.85, 0.0, 2.89, 3.89, 4.92, 3.32,
                           3.37, 0.0, 3.38, 5.64, 2.66, 3.5, 4.78, 0.0, 0.0, 4.1, 3.42, 0.0, 2.74, 0.0, 3.55, 2.08,
                           5.14, 0.0, 1.04, 0.0, 3.68, 2.72, 2.35, 1.69, 3.37, 0.0, 9.13, 6.9, 6.69, 2.8, 4.33, 7.13,
                           9.79, 5.45, 5.02, 7.67, 4.32, 4.3, 9.23, 4.52, 5.54, 7.13, 5.8, 4.15, 3.93, 4.35, 4.43, 2.95,
                           1.62, 4.24, 5.29, 4.82, 5.25, 5.0, 5.7, 3.18, 5.17, 3.36, 8.17, 4.94, 5.9, 4.24, 5.77, 7.12,
                           4.66, 2.73, 5.03, 0.0, 4.5, 4.75, 3.31, 0.0, 4.27, 3.4, 5.37, 2.59, 4.14, 4.85, 4.66, 7.03,
                           5.0, 5.96, 5.27, 5.44, 5.36, 6.1]
        a = array(internal_scores)
        percentile = 100. * len(a[a < candidate_score]) / len(internal_scores)
        return str(round(percentile)) + "%"
    except (TypeError, ValueError):
        return "-"

def get_casc_color(casc, layer="border"):
    border_colors = ['#213ECC', '#353ABE', '#4A36AF', '#5E32A1', '#732E92', '#872B84', '#9B2775', '#B02366', '#C41F58', '#D91B4A', '#ED173B']
    background_colors = ['#B2BEF8', '#B9B9EF', '#C1B3E5', '#C8AEDC', '#D0A8D2', '#D7A3C9', '#DE9DC0', '#E698B6', '#ED92AD', '#F58DA3', '#FC879A']
    if round(casc) <= 5:
        i = 0
    else:
        i = round(casc) - 5
    if layer == "border":
        return border_colors[i]
    if layer == "background":
        return background_colors[i]
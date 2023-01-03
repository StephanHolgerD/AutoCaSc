
import dash_bootstrap_components as dbc
from dash import html


citations = html.Div([
    html.Hr(),
    dbc.Container([
        html.P([
            "1. ",
            html.A(html.B("VEP"), href="https://grch37.ensembl.org/info/docs/tools/vep/index.html", target="_blank"),
            ": McLaren, W. et al. The Ensembl Variant Effect Predictor. Genome Biol 17, 122 (2016)."
        ]),
        html.P([
            "2. ", html.A(html.B("gnomAD"), href="https://gnomad.broadinstitute.org", target="_blank"),
            ": Karczewski, K. J. et al. The mutational constraint spectrum quantified from variation in 141,"
            "456 humans. Nature 581, 434–443 (2020)."
        ]),
        html.P([
            "3. ", html.A(html.B("GTEx"), href="http://www.gtexportal.org/home/index.html", target="_blank"),
            ": Consortium, T. Gte. The GTEx Consortium atlas of genetic regulatory effects across human tissues. "
            "Science 369, 1318–1330 (2020). "
        ]),
        html.P([
            "4. ", html.A(html.B("STRING"), href="https://string-db.org", target="_blank"),
            ": Szklarczyk, D. et al. STRING v11: protein-protein association networks with increased coverage, "
            "supporting functional discovery in genome-wide experimental datasets. Nucleic Acids Res 47, D607–D613 ("
            "2019). "
        ]),
        html.P([
            "5. ", html.A(html.B("MGI"), href="http://www.informatics.jax.org", target="_blank"),
            ": Bult, C. J. et al. Mouse Genome Database (MGD) 2019. Nucleic Acids Res 47, D801–D806 (2019)."
        ]),
        html.P([
            "6. ", html.A(html.B("PubTator"), href="https://www.ncbi.nlm.nih.gov/research/pubtator/", target="_blank"),
            ": Wei, C.-H., Allot, A., Leaman, R. & Lu, Z. PubTator central: automated concept annotation for "
            "biomedical full text articles. Nucleic Acids Res 47, W587–W593 (2019). "
        ]),
        html.P([
            "7. ", html.A(html.B("PsyMuKB"), href="http://www.psymukb.net", target="_blank"),
            ": Lin, G. N. et al. PsyMuKB: An Integrative De Novo Variant Knowledge Base for Developmental Disorders. "
            "Genomics Proteomics Bioinformatics 17, 453–464 (2019). "
        ]),
        html.P([
            "8. ", html.A(html.B("DisGeNET"), href="https://www.disgenet.org", target="_blank"),
            ": Piñero, J. et al. DisGeNET: a comprehensive platform integrating information on human "
            "disease-associated genes and variants. Nucleic Acids Res 45, D833–D839 (2017). "
        ])
    ]),
    html.Hr()
])


about_eng = [html.P(
    "AutoCaSc is a tool for quantifying the plausibility of candidate variants for Neurodevelopmental Disorders ("
    "NDD). AutoCaSc is intended to be used on impactful rare variants in a research setting. In its current version, "
    "12 parameters are counted in, achieving a maximum of 15 points. User inputs are the identified variant in a "
    "standard HGVS/VCF format together with segregation aspects (de novo, recessive, dominant and X-chromosomal). We "
    "use the Ensembl VEP REST API (1) to annotate variant attributes (e.g. variant consequence, allele frequency from "
    "gnomAD, in silico predictions) and gene based scores dependent on inheritance mode (e.g. high Z-score is of "
    "relevant for de novo missense) from dbNSFP. Other attributes were previously labor intensive and predisposed to "
    "variability. These included important categories like expression in the nervous system, neuronal functions, "
    "co-expression and protein interactions, search for relevant literature, model organisms and observations in "
    "screening studies. As an objective approach we now searched a defined set of databases (gnomAD (2), GTEx (3), "
    "STRING (4), MGI (5), PubTator (6), PsyMuKB (7), DisGeNET (8)) and generated empirical cut-offs for each category "
    "by comparing the respective readout between a manually curated list of known NDD genes from the SysID database ("
    "9) and a list of genes not involved in NDD.",
    style={"textAlign": "justify"}),
             html.Br(),
             html.P(
                 "Feel free to contact johann.lieberwirth@medizin.uni-leipzig.de or "
                 "rami.aboujamra@medizin.uni-leipzig.de in case you have further questions or in case you have found "
                 "a bug.",
                 style={"textAlign": "justify"})]

about_ger = [html.P(
    "AutoCaSc ist ein Skript zum automatisierten Bewerten von Kandidatenvarianten in Fällen neuronaler "
    "Entwicklungsverzögerung. Es ist ausschließlich für Forschungszwecke zu benutzen. Die Annotation der Varianten "
    "erfolgt mit der REST API von VEP (ensembl, (1)). Zur Berechnung der Kandidatenpunktzahl (Candidate score, "
    "CaSc) werden 12 verschiedene Parameter einbezogen. Dies sind die Art der Vererbung (z.B. de novo), Genattribute "
    "wie pLI & Z-Score (gnomAD (2)), Expressionsmuster (GTEx (3)), in silico Analysen, Proteininteratkionsdatnebanken "
    "(StringDB (4)), Tierdatenbanken (MGI (5)), Literaturdatenbanken (Pubtator Central (6)),  sowie weitere (PsymuKB "
    "(7), DisGeNET (8)). Die maximal erreichbare Punktzahl sind 15 Punkte. Je höher der erreichte Punktwert, "
    "desto plausibler scheint die aus den zugrundeliegenden Daten errechnete Pathogenität der Variante mit Blick auf "
    "neuronale Entwicklungsverzögerung.",
    style={"textAlign": "justify"}),
             html.Br(),
             html.P(
                 "Bei Fragen und Anmerkungen kontaktieren Sie bitte johann.lieberwirth@medizin.uni-leipzig.de oder "
                 "rami.aboujamra@medizin.uni-leipzig.de.",
                 style={"textAlign": "justify"})]

about_page = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col(html.H2("About"),
                width="auto"),
        dbc.Col(dbc.Button("DE",
                           id="about_language_button",
                           color="secondary"),
                width="auto")
    ]),
    html.Br(),
    html.Div(about_eng,
             id="about_text"),
    html.Br(),
    citations
])
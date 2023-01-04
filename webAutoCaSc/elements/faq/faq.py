import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


browser_compatibility_header = [
    html.Thead(html.Tr([html.Th("OS"),
                        html.Th("Version"),
                        html.Th("Chrome"),
                        html.Th("Firefox"),
                        html.Th("Microsoft Edge"),
                        html.Th("Safari")]))
]
browser_compatibility_row1 = html.Tr([html.Td("MacOS"),
                html.Td("12.0.1"),
                html.Td("96.0.4664.110"),
                html.Td("94.0.2"),
                html.Td("n/a"),
                html.Td("15.1")])
browser_compatibility_row2 = html.Tr([html.Td("Linux"),
                html.Td("20.04.3 LTS"),
                html.Td("93.0.4577.82"),
                html.Td("n/a"),
                html.Td("n/a"),
                html.Td("n/a")])
browser_compatibility_row3 = html.Tr([html.Td("Windows 10"),
                html.Td("1809"),
                html.Td("94.0.4606.71"),
                html.Td("92.0.1"),
                html.Td("96.0.1504.53"),
                html.Td("n/a")])

browser_compatibility_body = [html.Tbody([browser_compatibility_row1,
                                          browser_compatibility_row2,
                                          browser_compatibility_row3])]


faq_ger = html.Div(
    [
        dcc.Markdown("""
            __Was ist AutoCaSc?__  
            AutoCaSc ist ein Werkzeug zur systematischen Evaluierung der Plausibilität von Varianten in Genen, welche 
            bislang nicht mit Erkrankungen in Verbindung gebracht wurden ("Kandidatengene"), in Fällen neurologischer 
            Entwicklungsverzögerung (neurodevelopmental disorder, NDD). Solche Varianten werden üblicherweise durch 
            genomweites Screeningmethoden bei Individuen mit NDD, aber ohne eindeutige diagnostische Variante 
            identifiziert. AutoCaSc berücksichtigt variantenspezifische Parameter (Konservierung, 
            "in silico"-Vorhersagen), genspezifische Parameter ("gene constraint", Expressionsmuster, 
            Proteininteraktionen), die Segregation der Variante und das Gesamtzusammenspiel zwischen diesen Parametern.

            __Wofür stehen die 4 Unterscores?__  
            - __Variant Attributes (6 Punkte max):__ Dazu gehören Konservierung (GERP++), "in silico"-Vorhersagen 
            (MutationAssessor, MutationTaster, Sift), Spleißstellenvorhersagen (MaxEntScan, AdaBoost, RandomForest) 
            und erwartete Auswirkungen (VEP).
            - __Gene Constraints (1 Punkte max):__ Es handelt sich dabei um gene-constraint Parameter aus gnomAD; LOUEF 
            für Loss-of-Function-Varianten, Z für Missense-Varianten.
            - __Inheritance (2 Punkte max):__ Diese Punkte hängen von der Vererbung und der Segregation der Variante in 
            der Familie ab.
            - __Gene Plausibility (6 Punkte max):__ Diese Punkte werden auf der Grundlage des Expressionsmusters des 
            Gens, der Protein-Protein-Interaktionen, der Phänotypen in Tiermodellen, der in PubMed veröffentlichten 
            Artikel zum Gen, de novo-Varianten im Gen die mit NDD in Verbindung gebacht wurden, und anderer Quellen 
            berechnet.
            
            __Wie annotiert AutoCaSc?__  
            AutoCaSc verwendet VEP hg19 Endpunkte. Zurzeit ist hg38 nicht unterstützt. Verschiedene Tools wie 
            VariantValidator (https://variantvalidator.org/) stehen zur Verfügung, um hg38 Variant zu hg19 zu 
            übersetzen. Alle wichtigen genomischen Eingabeformate wie die Notation im VCF-Format und die HGVS 
            g.-Notation werden unterstützt. Bei Verwendung anderer Transkript-Systemen (außer ensembl), wie z.B. 
            RefSeq kann es zu vereinzelten Inkompatibilitäten mit entsprechender Fehlermedlung kommen.

            __Wie kann AutoCaSc zitiert werden?__  
            J. Lieberwirth, B. Büttner, C. Klöckner, K. Platzer, B. Popp, R. Abou Jamra. (2022). [AutoCaSc: Prioritizing candidate genes for neurodevelopmental disorders](https://onlinelibrary.wiley.com/doi/10.1002/humu.24451)  
            
            __Wie kann man mehrere (compound heterozygote) Variaten eingeben?__  
            Mehrere Varianten können eingegeben werden, indem sie durch ein Komma getrennt werden. Wenn "compound 
            heterozygous" ausgewählt ist, findet webAutoCaSc automatisch Varianten im gleichen Gen und verarbeitet diese
             als entsprechende compound heterozygote Varianten.

            __Wofür stehen die Vererbungsoptionen?__  
            - __De novo:__ De novo-Varianten werden nur im Index identifiziert und sind nicht von den Eltern vererbt 
            worden.
            - __Inherited dominant:__ Im Falle einer vererbten dominanten Variante wurde die Variante von einem 
            ebenfalls betroffenen Elternteil vererbt.
            - __Homozygous recessive:__ Die Variante wird homozygot im Index und in heterozygot in beiden gesunden 
            Elternteilen identifiziert.
            - __X-linked:__ X-chromosomale Varianten werden von der heterozygoten Trägermutter vererbt und verursachen 
            bei einem männlichen Nachkommen einen Phänotyp, da er nur ein betroffenes Allel und kein gesundes zweites 
            Allel zum Ausgleich hat. De-novo-Varianten auf dem X-Chromosom, sowohl bei weiblichen als auch bei 
            männlichen Index-Individuen, werden in der Option De-novo-Vererbung berücksichtigt.
            - __Compound heterozygous:__ Compound heterozygote Varianten sind zwei verschiedene Varianten im selben Gen,
             aber auf verschiedenen Allelen. Jede wird von nur einem heterozygoten Trägerelternteil vererbt.
            - __Unknown:__ Die Option "unbekannt" kann verwendet werden, wenn Informationen zu den Eltern und damit zur 
            Segregation fehlen.
            
            __Ab wann ist ein Score hoch?__
            Die maximale Punktzahl sind 15. Um ein besseres Gefühl zu geben, ob ein candidate score hoch ist, wurde ein 
            Tooltip implementiert, welcher angezeigt wird wenn der Mauszeiger über dem Ergebnis schwebt. Der Tooltip 
            zeigt an, wie viel Prozent der Kandidaten, welche am Institut für Humangenetik in Leipzig evaluiert wurden, 
            ein gleich hohes oder niedrigeres Ergebnis erreichten.

            __Wofür steht _webAutoCaSc_?__  
            _AutoCaSc_ steht für __Auto__mated __Ca__ndidate __Sc__ore. Wir benutzen den __web__ Präfix, um das command 
            line interface (CLI) von der Webapp zu unterscheiden, welche auf dem AutoCaSc script basiert. Das 
            __Ca__ndidate __Sc__ore Prinzip wurde bereits von _Büttner et al. bioRxiv. 2019_ beschrieben. 

            __Kann webAutoCaSc für andere Phänotypen genutzt werden?__  
            AutoCaSc wurde für die Arbeit mit NDDs entwickelt. Wir empfehlen nicht, es für andere Phänotypen zu 
            verwenden. Für zukünftige Updates planen wir ein verallgemeinertes, phänotyp-unabhängiges Framework.
            
            __Auf welchen Browsern läuft webAutoCaSc?__
            Wir haben webAutoCaSc auf folgenden Betriebssystemen und Browsern getestet:
            """),
        dbc.Table(browser_compatibility_header + browser_compatibility_body, bordered=True)
    ]
)

faq_eng = html.Div(
    [
        dcc.Markdown("""
            __What is AutoCaSc?__  
            The AutoCaSc tool systematically evaluates the plausibility of variants in genes not yet associated with 
            human disease ("candidate genes") to be associated with neurodevelopmental disorders (NDDs). Such variants 
            are typically identified through genome wide screening approaches in individuals NDDs but without a clear 
            diagnostic variant. AutoCaSc accounts for variant-specific parameters (conservation, "in silico" 
            predictions), gene specific parameters (gene constraint, expression pattern, protein interactions), 
            segregation of the variant and the overall interplay between these parameters.
            
            __What do the 4 subscores stand for?__  
            - __Variant Attributes (6 points max):__ These include conservation (GERP++), "in silico" predictions 
            (MutationAssessor, MutationTaster, Sift), splice site predictions (MaxEntScan, AdaBoost, RandomForest) and 
            expected impact (VEP).
            - __Gene Constraints (1 point max):__ These are gene constraint parameters from gnomAD; LOUEF for loss of 
            function variants, Z for missense variants.
            - __Inheritance (2 points max):__ These points depend on inheritance of the variant of interest and 
            segregation of the variant in the family.
            - __Gene Plausibility (6 points max):__ These points are calculated based on the gene's expression pattern, 
            protein-protein interactions, animal model phenotypes, published articles on PubMed, de novo variants in the
             gene linked to NDD and other sources.
            
            __How does AutoCaSc annotate?__  
            AutoCaSc uses the VEP API for hg19, as currently this seems to be the most commonly used reference genome. 
            By now, hg38 is not supported. You can use tools like VariantValidator (https://variantvalidator.org/) to 
            translate your hg38 variants to hg19. All major genomic input formats like VCF format style notation and 
            HGVS g.-style notation are supported for hg19. In some cases incompatibility can occur when using 
            RefSeq transcripts, which is then displayed as an error. We recommend using the VCF format.
            
            __How can AutoCaSc be cited?__  
            If you like to cite AutoCaSc, please refer to our paper:  
            J. Lieberwirth, B. Büttner, C. Klöckner, K. Platzer, B. Popp, R. Abou Jamra. (2022). [AutoCaSc: Prioritizing candidate genes for neurodevelopmental disorders](https://onlinelibrary.wiley.com/doi/10.1002/humu.24451)  
            
            __How can I enter multiple (compound heterogyous) variants?__  
            Just enter all your variants of interest by separating them by a comma. If "compound heterozygous" is 
            selected, webAutoCaSc will automatically match variants in the same gene and process them as corresponding 
            compound heterozygous variants.

            __What do the inheritance options stand for?__  
            - __De novo:__ De novo variants are identified only in the index and have not been inherited from the 
            parents.
            - __Inherited dominant:__ In case of an inherited dominant variant, the variant of interested has been 
            inherited by an equally affected parent.
            - __Homozygous recessive:__ Variant is identified in homozygous state in the index and in heterozygous 
            state in both healthy parents.
            - __X-linked:__ X-linked variants are being inherited from the heterozygous carrier mother and cause a 
            phenotype in a male descendant as he has only one affected allele and no healthy second allele to 
            compensate. De novo variants on the X-chromosome, for both female and male index individuals, are account 
            for in the de novo inheritance option.
            - __Compound heterozygous:__ Compound heterozygous variants are two different variants in the same gene but 
            on different alleles. Each is inherited from only one heterozygous carrier parent.
            - __Unknown:__ The "unknown" option can be used if information on the parents and thus on segregation is 
            missing.
            
            __When is a score high?__  
            The maximum score is 15. To give a better feeling if a candidate score is high, a tooltip has been 
            implemented, which is displayed when the mouse pointer hovers over the result. The tooltip shows what 
            percentage of candidates evaluated at the Institute of Human Genetics in Leipzig achieved an equal or lower 
            score.
            
            __What does _webAutoCaSc_ stand for?__  
            _AutoCaSc_ stands for __Auto__mated __Ca__ndidate __Sc__ore. We use the __web__ prefix to distinguish the 
            command line interface (CLI) from the webapplication running the AutoCaSc script. The __Ca__ndidate 
            __Sc__ore principle has been previously described (Büttner et al. bioRxiv. 2019). 
            
            __Can webAutoCaSc be used for other phenotypes as well?__  
            AutoCaSc has been developed to work for NDDs. We don't recommend using it for other phenotypes. We are 
            planning a generalized phenotype agnostic framework for future updates.
            
            __What browsers can run webAutoCaSc?__
            We tested webAutoCaSc on different operating systems and browsers. You can find a table below.
            """),
        dbc.Table(browser_compatibility_header + browser_compatibility_body, bordered=True)
        ]
)


faq_page = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col(html.H2("FAQ"),
                width="auto"),
        dbc.Col(dbc.Button("DE",
                           id="faq_language_button",
                           color="secondary"),
                width="auto")
    ]),
    html.Br(),
    html.Div(faq_eng,
             id="faq_text",
             style={"textAlign": "justify"})
])
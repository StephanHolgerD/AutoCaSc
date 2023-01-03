import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

impressum_ger = dcc.Markdown("""
                            Gemäß § 28 BDSG widersprechen wir jeder kommerziellen Verwendung und Weitergabe der Daten.\n
                            __Verantwortunsbereich__:  
                            Das Impressum gilt nur für die Internetpräsenz unter der Adresse: 
                            https://autocasc.uni-leipzig.de\n
                            __Abgrenzung__:  
                            Die Web-Präsenz ist Teil des WWW und dementsprechend mit fremden, sich jederzeit wandeln 
                            könnenden Web-Sites verknüpft, die folglich auch nicht diesem Verantwortungsbereich 
                            unterliegen und für die nachfolgende Informationen nicht gelten. Dass die Links weder gegen 
                            Sitten noch Gesetze verstoßen, wurde genau ein Mal geprüft (bevor sie hier aufgenommen 
                            wurden).\n
                            __Diensteanbieter__:  
                            Johann Lieberwirth und Rami Abou Jamra\n
                            __Ansprechpartner für die Webseite__:\n
                            Johann Lieberwirth (johann.lieberwirth@medizin.uni-leipzig.de)\n
                            __Verantwortlicher__:  
                            Rami Abou Jamra (rami.aboujamra@medizin.uni-leipzig.de)\n
                            __Anschrift__:  
                            Sekretariat  
                            Philipp-Rosenthal-Str. 55  
                            04103 Leipzig  
                            Telefon: 0341 - 97 23800\n
                            __Urheberschutz und Nutzung__:  
                            Der Urheber räumt Ihnen ganz konkret das Nutzungsrecht ein, sich eine private Kopie für 
                            persönliche Zwecke anzufertigen. Nicht berechtigt sind Sie dagegen, die Materialien zu 
                            verändern und/oder weiter zu geben oder gar selbst zu veröffentlichen.
                            Wenn nicht ausdrücklich anders vermerkt, liegen die Urheberrechte bei Johann Lieberwirth
                            Datenschutz Personenbezogene Daten werden nur mit Ihrem Wissen und Ihrer Einwilligung 
                            erhoben. Auf Antrag erhalten Sie unentgeltlich Auskunft zu den über Sie gespeicherten 
                            personenbezogenen Daten. Wenden Sie sich dazu bitte an den Administrator.\n
                            __Keine Haftung__:  
                            Die Inhalte dieses Webprojektes wurden sorgfältig geprüft und nach bestem Wissen erstellt. 
                            Aber für die hier dargebotenen Informationen wird kein Anspruch auf Vollständigkeit, 
                            Aktualität, Qualität und Richtigkeit erhoben. Es kann keine Verantwortung für Schäden 
                            übernommen werden, die durch das Vertrauen auf die Inhalte dieser Website oder deren 
                            Gebrauch entstehen.\n
                            __Schutzrechtsverletzung__:  
                            Falls Sie vermuten, dass von dieser Website aus eines Ihrer Schutzrechte verletzt wird, 
                            teilen Sie das bitte umgehend per elektronischer Post mit, damit zügig Abhilfe geschafft 
                            werden kann. Bitte nehmen Sie zur Kenntnis: Die zeitaufwändigere Einschaltung eines 
                            Anwaltes zur für den Diensteanbieter kostenpflichtigen Abmahnung entspricht nicht dessen 
                            wirklichen oder mutmaßlichen Willen.\n
                            \n
                            lt. Urteil vom 12. Mai 1998 - 312 O 85/98 - "Haftung für Links" hat das Landgericht Hamburg 
                            entschieden, dass man durch die Anbringung eines Links, die Inhalte der gelinkten Seite ggf.
                             mit zu verantworten hat. Dies kann nur dadurch verhindert werden, dass man sich 
                             ausdrücklich von diesen Inhalten distanziert.
                            'Hiermit distanzieren wir uns ausdrücklich von allen Inhalten aller gelinkten Seiten auf 
                            unserer Website und machen uns diese Inhalte nicht zu eigen. Diese Erklärung gilt für alle 
                            auf unsere Website angebrachten Links.'
                            \n
                            © Copyright 2021
                """)

impressum_eng = [
        dcc.Markdown("""
            The Institute for Human Genetics (University Medical Center Leipzig) makes no representation about the 
            suitability or accuracy of this software or data for any purpose, and makes no warranties, including fitness 
            for a particular purpose or that the use of this software will not infringe any third party patents, 
            copyrights, trademarks or other rights.\n
            __Responsible for this website__:  
            Johann Lieberwirth (johann.lieberwirth@medizin.uni-leipzig.de)\n
            __Responsible for this project__:  
            Rami Abou Jamra (rami.aboujamra@medizin.uni-leipzig.de)\n
            __Address__:  
            Sekretariat  
            Philipp-Rosenthal-Str. 55  
            04103 Leipzig  
            GERMANY  
            Telefon: 0341 - 97 23800""")
]

impressum_page = dbc.Container(
    [
        html.Br(),
        dbc.Row([
            dbc.Col(html.H2("Impressum"),
                    width="auto"),
            dbc.Col(dbc.Button("EN",
                               id="impressum_language_button",
                               color="secondary"),
                    width="auto")
        ]),
        html.Br(),
        html.Div(impressum_ger,
                 id="impressum_text"
                 )
    ],
    style={
        "textAlign": "justify",
        "verticalAlign": "top!",
        "minHeight": "100%!"
    },
)
import streamlit as st

st.set_page_config(page_title="Projektzusammenfassung",layout="wide",initial_sidebar_state="expanded")

# Tabs erstellen
tab_summary, tab_challenges = st.tabs(["📘 Summary", "⚠️ Herausforderungen, Learnings & Fazit"])



# # -------------------------
# # TAB 2: HERAUSFORDERUNGEN
# # -------------------------
# with tab_challenges:
#     st.markdown("""
#     ### Herausforderungen & Learnings

#     Während der Entwicklung des Projekts traten verschiedene fachliche und technische
#     Herausforderungen auf, die den Analyseprozess geprägt haben:

#     **1. Heterogene Datenqualität**  
#     Die ASHRAE‑Daten stammen aus vielen Ländern und Studien. Unterschiedliche Messmethoden,
#     fehlende Werte und uneinheitliche Skalen machten eine gründliche Bereinigung notwendig.

#     **2. Unterschiedliche Skalen der Komfortvariablen**  
#     TSV, TP, TC und TA besitzen jeweils eigene ASHRAE‑Skalen. Dies erschwerte die
#     Interpretation von Zusammenhängen und die Erstellung konsistenter Visualisierungen.

#     **3. Große Datenmengen**  
#     Mit über 100.000 Datensätzen war eine effiziente Datenverarbeitung entscheidend.
#     Caching, Filterlogik und performante Diagramme waren zentrale technische Aufgaben.

#     **4. Machine‑Learning‑Modellierung**  
#     Thermischer Komfort ist ein subjektives, multifaktorielles Phänomen. Die Auswahl und
#     Validierung geeigneter Modelle war anspruchsvoll, da Komfort nicht rein physikalisch
#     vorhersagbar ist.

#     **5. Gestaltung einer klaren Benutzeroberfläche**  
#     Die Herausforderung bestand darin, komplexe wissenschaftliche Inhalte verständlich,
#     visuell ansprechend und interaktiv aufzubereiten.

#     **Fazit:**  
#     Das Projekt vermittelte wertvolle praktische Erfahrungen in Datenanalyse, wissenschaftlicher
#     Interpretation und der Entwicklung datengetriebener Webanwendungen. Die gewonnenen
#     Erkenntnisse stärken sowohl analytische als auch technische Kompetenzen.
#     """)


# -------------------------
# TAB 1: SUMMARY
# -------------------------
with tab_summary:
    st.markdown("""
    ## 📘 Zusammenfassung des Abschlussprojekts
    """
    )

    # st.markdown("""
    #     - **Abschlussprojekt** im Rahmen der Weiterbildung zu Data Analyst bzw. Data Scientist des Data Science Institute DSI Education GmbH
    #     - **cloudnative, prädiktive Webanwendung**, die modernste Machine‑Learning‑Algorithmen nutzt
    #     - Ziel des Projekts: Brücke zwischen **Analyse von thermodynamischen Big Data** und **Machine Learning** schlagen, um thermischen Komfort in Gebäuden nicht nur zu analysieren, sondern proaktiv vorherzusagen
    # """
    # )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""  
    Dieses Projekt wurde im Rahmen der beruflichen Weiterbildung Weiterbildung zu Data Analyst bzw. Data Scientist des Data Science Institute DSI Education GmbH entwickelt und von einem
    interdisziplinären Team durchgeführt:

    - Sabrina | Data Analyst
    - Dianela | Data Analyst  
    - Mirtha  | Data Scientist  
    - Daniel  | Data Scientist

    Gemeinsam haben wir die *ASHRAE Global Thermal Comfort Database II* analysiert, eine der
    umfangreichsten internationalen Datenquellen zum thermischen Komfort. 
    
    ### 🔍 Inhalt des Projekts
    - **Datenbereinigung und Harmonisierung** der ASHRAE‑Messdaten  
    - **Globale Analyse** von thermischen Komfortvariablen (Thermischen Komfort, thermisches Empfinden, thermische Präferenz und thermsiche Akzeptanz)  
    - **Untersuchung relevanter Einflussfaktoren** (Physikalische Parameter, Klima, Kühltechnik etc.)  
    - **Visualisierung thermischer Zusammenhänge**, z. B. Korrelationen 
    - **Machine‑Learning‑Modelle**

    ### 🎯 Ziel
    Das Projekt zeigt, wie subjektive thermische Wahrnehmung und physikalische Parameterzusammenwirken
    und welche globalen Muster sich in großen Datensätzen erkennen lassen. Die Streamlit‑App
    dient als interaktive Plattform, um diese Erkenntnisse verständlich und zugänglich zu machen.
    """)

    #st.write("Gebäudekonzepte müssen an lokale Klimabedingungen und kulturelle Gewohnheiten angepasst werden.")

    # Ziel des Projekts war es, 
    # weltweit erhobene Daten zum thermischen Komfort wissenschaftlich aufzubereiten, zu visualisieren, 
    # zu analysieren und mithilfe von Modellierungsverfahren zu untersuchen. Dabei sollten zentrale 
    # Muster und Einflussfaktoren sichtbar gemacht und die Ergebnisse in einer interaktiven Streamlit‑Anwendung 
    # verständlich dargestellt werden.

# -------------------------
# TAB 2: HERAUSFORDERUNGEN
# -------------------------
with tab_challenges:

    # -------------------------
    # Herausforderungen und Learnings
    # -------------------------
    st.markdown("""
    ## ⚠️ Herausforderungen & Learnings
                

    Während der Entwicklung des Projekts traten verschiedene fachliche und technische
    Herausforderungen auf, die unser Team geprägt und weiterentwickelt haben.
                
    1️⃣ **Große Datenmengen**
                
    - Effiziente Datenverarbeitung war wichtig ➝ Caching, Filterlogik und performante Diagramme waren zentrale technische Aufgaben
    - Gute Einarbeitung in die Daten und Fokussierung auf Fragestellungen waren wichtig
                
    2️⃣ **Heterogene Datenqualität**
    
    - ASHRAE‑Daten stammen aus vielen Ländern und Studien ➝ Unterschiedliche Messmethoden, fehlende Werte und uneinheitliche Skalen
    - Gemeinsame Entscheidungsfindung im Umgang hiermit war wichtig
                
    3️⃣ **Machine‑Learning‑Modellierung**
                
    - Thermischer Komfort ist ein subjektives, multifaktorielles Phänomen
    - Auswahl und Validierung geeigneter Modelle war anspruchsvoll, da Komfort nicht rein physikalisch vorhersagbar ist       
    """
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------
    # Fazit
    # -------------------------
    st.markdown("""
    ## 🎓 Fazit
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    # Inhaltliches Fazit
    st.markdown("""
    ##### 🎯 Inhaltlich:
    """)

    st.markdown("""
    - Unsere Ergebnisse liefern **wichtige Erkenntnisse für die Entwicklung von Gebäudesystemen**, die den Komfort der Nutzer*innen erhöhen und gleichzeitig energieeffizient sind 
    - **Weitere Analysen** zu anderen Einflussfaktoren auf die subjektive thermische Wahrnehmung und **konkreter Umsetzungsmöglichkeiten der Erkenntnisse** wären sinnvolle nächste Schritte
    """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Allgemeines Fazit
    st.markdown("""
    ##### 💡 Projektfazit:
    """)

    st.markdown("""     
    - Das Projekt vermittelte **wertvolle praktische Erfahrung** in Datenanalyse, wissenschaftlicher Interpretation und der Entwicklung datengetriebener Webanwendungen
    - Die **interdisziplinäre Zusammenarbeit** stärkte sowohl analytische als auch technische Kompetenzen
    """
    )
    # Mit über 100.000 Einträgen im Datensatz war eine effiziente Datenverarbeitung entscheidend.
    # Caching, Filterlogik und performante Diagramme waren zentrale technische Aufgaben.

    # ### 2️⃣ Heterogene Datenqualität
    # Die ASHRAE‑Daten stammen aus vielen Ländern und Studien. Unterschiedliche Messmethoden,
    # fehlende Werte und uneinheitliche Skalen machten eine gründliche Bereinigung notwendig.

    # ### 3️⃣ Unterschiedliche Skalen der Komfortvariablen
    # TSV, TP, TC und TA besitzen jeweils eigene ASHRAE‑Skalen. Dies erschwerte die
    # Interpretation von Zusammenhängen und die Erstellung konsistenter Visualisierungen.

    # ### 4️⃣ Machine‑Learning‑Modellierung
    # Thermischer Komfort ist ein subjektives, multifaktorielles Phänomen. Die Auswahl und
    # Validierung geeigneter Modelle war anspruchsvoll, da Komfort nicht rein physikalisch
    # vorhersagbar ist.

    # ### 5️⃣ Teamarbeit in einem interdisziplinären Umfeld
    # Die Zusammenarbeit zwischen Psychologie, Informatik, Physik und Bauingenieurwesen
    # brachte unterschiedliche Perspektiven zusammen – eine Stärke, aber auch eine
    # kommunikative Herausforderung.

    # ### 🎓 Fazit
    # Das Projekt vermittelte wertvolle praktische Erfahrungen in Datenanalyse,
    # wissenschaftlicher Interpretation und der Entwicklung datengetriebener Webanwendungen.
    # Die interdisziplinäre Zusammenarbeit stärkte sowohl analytische als auch technische
    # Kompetenzen und führte zu einem umfassenden Verständnis thermischen Komforts.
    # """)


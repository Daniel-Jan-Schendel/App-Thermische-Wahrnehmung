import streamlit as st

st.set_page_config(page_title="Projektzusammenfassung",layout="wide",initial_sidebar_state="expanded")

# Tabs erstellen
tab_summary, tab_challenges = st.tabs(["📘 Summary", "⚠️ Herausforderungen & Learnings"])

# -------------------------
# TAB 1: SUMMARY
# -------------------------
# with tab_summary:
#     st.markdown("""
#     ### Zusammenfassung des Abschlussprojekts

#     Dieses Projekt wurde im Rahmen einer beruflichen Weiterbildung entwickelt und beschäftigt sich
#     mit der Analyse der *ASHRAE Global Thermal Comfort Database II*. Ziel war es, weltweit gesammelte 
#     Komfortdaten zu verarbeiten, zu visualisieren und zu analysieren..

#     Die Anwendung umfasst:
#     - **Datenbereinigung und Harmonisierung** der ASHRAE‑Messdaten  
#     - **Globale Analyse** zentraler Komfortvariablen wie operative Temperatur, TSV, TP, TC und TA  
#     - **Untersuchung von Einflussfaktoren** wie Alter, Gebäudetyp, Klimazone und Kühltechnik  
#     - **Visualisierung thermischer Zusammenhänge**, z. B. Korrelationen, T_neutral, MTS vs. Indoor Temperature  
#     - **Machine‑Learning‑Modelle**, die thermische Empfindung und Komfort vorhersagen

#     Das Projekt zeigt, wie subjektive Wahrnehmung und physikalische Parameter zusammenwirken und
#     welche Muster sich in globalen Datensätzen erkennen lassen. Die Streamlit‑App dient als
#     interaktive Plattform, um diese Erkenntnisse verständlich und zugänglich darzustellen.
#     """)

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

    Dieses Projekt wurde im Rahmen einer beruflichen Weiterbildung entwickelt und von einem
    interdisziplinären Team durchgeführt:

    **👩‍⚕️ Sabrina – Psychologin | Data Analyst**  
    **👩‍💻 Dianela – Informatikingenieurin | Data Analyst**  
    **👩‍🔬 Mirtha – Physikerin | Data Scientist**  
    **👷‍♂️ Daniel – Bauingenieur | Data Scientist**

    Gemeinsam analysierten wir die *ASHRAE Global Thermal Comfort Database II*, eine der
    umfangreichsten internationalen Datenquellen zum thermischen Komfort. 
    
    ### 🔍 Inhalt des Projekts
    - **Datenbereinigung und Harmonisierung** der ASHRAE‑Messdaten  
    - **Globale Analyse** von Komfortvariablen wie operative Temperatur, TSV, TP, TC und TA  
    - **Untersuchung relevanter Einflussfaktoren** (Alter, Gebäudetyp, Klimazone, Kühltechnik)  
    - **Visualisierung thermischer Zusammenhänge**, z. B. Korrelationen, T_neutral, MTS vs. Indoor Temperature  
    - **Machine‑Learning‑Modelle**, die thermische Empfindung und Komfort vorhersagen

    ### 🎯 Ziel
    Das Projekt zeigt, wie subjektive Wahrnehmung und physikalische Parameter zusammenwirken
    und welche globalen Muster sich in großen Datensätzen erkennen lassen. Die Streamlit‑App
    dient als interaktive Plattform, um diese Erkenntnisse verständlich und zugänglich zu machen.
    """)


    # Ziel des Projekts war es, 
    # weltweit erhobene Daten zum thermischen Komfort wissenschaftlich aufzubereiten, zu visualisieren, 
    # zu analysieren und mithilfe von Modellierungsverfahren zu untersuchen. Dabei sollten zentrale 
    # Muster und Einflussfaktoren sichtbar gemacht und die Ergebnisse in einer interaktiven Streamlit‑Anwendung 
    # verständlich dargestellt werden.

# -------------------------
# TAB 2: HERAUSFORDERUNGEN
# -------------------------
with tab_challenges:
    st.markdown("""
    ## ⚠️ Herausforderungen & Learnings
                

    Während der Entwicklung des Projekts traten verschiedene fachliche und technische
    Herausforderungen auf, die unser Team geprägt und weiterentwickelt haben.
                
    ### 1️⃣ Große Datenmengen
    Mit über 100.000 Datensätzen war eine effiziente Datenverarbeitung entscheidend.
    Caching, Filterlogik und performante Diagramme waren zentrale technische Aufgaben.

    ### 2️⃣ Heterogene Datenqualität
    Die ASHRAE‑Daten stammen aus vielen Ländern und Studien. Unterschiedliche Messmethoden,
    fehlende Werte und uneinheitliche Skalen machten eine gründliche Bereinigung notwendig.

    ### 3️⃣ Unterschiedliche Skalen der Komfortvariablen
    TSV, TP, TC und TA besitzen jeweils eigene ASHRAE‑Skalen. Dies erschwerte die
    Interpretation von Zusammenhängen und die Erstellung konsistenter Visualisierungen.

    ### 4️⃣ Machine‑Learning‑Modellierung
    Thermischer Komfort ist ein subjektives, multifaktorielles Phänomen. Die Auswahl und
    Validierung geeigneter Modelle war anspruchsvoll, da Komfort nicht rein physikalisch
    vorhersagbar ist.

    ### 5️⃣ Teamarbeit in einem interdisziplinären Umfeld
    Die Zusammenarbeit zwischen Psychologie, Informatik, Physik und Bauingenieurwesen
    brachte unterschiedliche Perspektiven zusammen – eine Stärke, aber auch eine
    kommunikative Herausforderung.

    ### 🎓 Fazit
    Das Projekt vermittelte wertvolle praktische Erfahrungen in Datenanalyse,
    wissenschaftlicher Interpretation und der Entwicklung datengetriebener Webanwendungen.
    Die interdisziplinäre Zusammenarbeit stärkte sowohl analytische als auch technische
    Kompetenzen und führte zu einem umfassenden Verständnis thermischen Komforts.
    """)


import streamlit as st

# ---------------------------------------------------------
# Seitenkonfigurationen
# --------------------------------------------------------- 
st.set_page_config(page_title="Projektzusammenfassung",layout="wide",initial_sidebar_state="expanded")

# ---------------------------------------------------------
# Seitentitel
# ---------------------------------------------------------
st.title("📘 Zusammenfassung und Fazit")

# ---------------------------------------------------------
# Tabs definieren
# ---------------------------------------------------------
tab_summary, tab_challenges = st.tabs([
    "Zusammenfassung", 
    "⚠️ Herausforderungen, Learnings & Fazit"
])

#########################################################################################################
#########################################################################################################

# -------------------------
# TAB 1: SUMMARY
# -------------------------
with tab_summary:
    # --- Überschrift ---
    st.markdown("""
    ## Zusammenfassung des Abschlussprojekts
    """
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Text ---
    st.markdown("""  
    Dieses Projekt wurde im Rahmen der beruflichen Weiterbildung zu Data Analyst bzw. Data Scientist des Data Science Institute DSI Education GmbH entwickelt und von einem
    interdisziplinären Team durchgeführt:

    - Sabrina | Data Analyst
    - Dianela | Data Analyst  
    - Mirtha  | Data Scientist  
    - Daniel  | Data Scientist

    Gemeinsam haben wir die *ASHRAE Global Thermal Comfort Database II* analysiert, eine der
    umfangreichsten internationalen Datenquellen zum thermischen Komfort. 
    
    ### 🔍 Inhalt des Projekts
    - **Datenbereinigung und Harmonisierung** der ASHRAE‑Messdaten  
    - **Globale Analyse** von thermischen Komfortvariablen (Thermischen Komfort, thermisches Empfinden, thermische Präferenz und thermische Akzeptanz)  
    - **Untersuchung relevanter Einflussfaktoren** (Physikalische Parameter, Klima, Kühltechnik etc.)  
    - **Visualisierung thermischer Zusammenhänge**, z. B. Korrelationen 
    - **Machine‑Learning‑Modelle**

    ### 🎯 Ziel
    Das Projekt zeigt, wie subjektive thermische Wahrnehmung und physikalische Parameterzusammenwirken
    und welche globalen Muster sich in großen Datensätzen erkennen lassen. Die Streamlit‑App
    dient als interaktive Plattform, um diese Erkenntnisse verständlich und zugänglich zu machen.
    """)

#########################################################################################################
#########################################################################################################

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

    ➝ Durch unterschiedliche Anzahlen in den einzelnen untersuchten Gruppen und viele fehlende Werte, sollten die Ergebnisse vorsichtig interpretiert werden
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
    # --- Überschrift ---
    st.markdown("""
    ## 🎓 Fazit
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Inhaltliches Fazit ---
    st.markdown("""
    ##### 🎯 Inhaltlich:
    """)
    st.markdown("""
    - Unsere Ergebnisse liefern **wichtige Erkenntnisse für die Entwicklung von Gebäudesystemen**, die den Komfort der Nutzer*innen erhöhen und gleichzeitig energieeffizient sind 
    - **Weitere Analysen** zu anderen Einflussfaktoren auf die subjektive thermische Wahrnehmung und **konkreter Umsetzungsmöglichkeiten der Erkenntnisse** wären sinnvolle nächste Schritte
    """
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Projektfazit ---
    st.markdown("""
    ##### 💡 Projektfazit:
    """)
    st.markdown("""     
    - Das Projekt vermittelte **wertvolle praktische Erfahrung** in Datenanalyse, wissenschaftlicher Interpretation und der Entwicklung datengetriebener Webanwendungen
    - Die **interdisziplinäre Zusammenarbeit** stärkte sowohl analytische als auch technische Kompetenzen
    """
    )
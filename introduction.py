import streamlit as st

st.set_page_config(
    page_title="Introduction – Smart Building Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏢 🌱  Smart Building  Comfort Analytics – Einführung")

# -------------------------
#       TABS
# -------------------------
tab1, tab2, tab3, tab4,tab5 = st.tabs([
    "👥 Über uns",
    "1️⃣ Projekt Einführung",
    "2️⃣ Grund – Warum?",
    "3️⃣ Machine Learning Integration",
    "🧰 Tools"
])

# -------------------------
# TAB 1 – EINLEITUNG
# -------------------------
with tab1:


    st.markdown("## 👥 Über uns")
    st.markdown("""
    Wir sind vier Personen mit unterschiedlichen beruflichen Hintergründen.  
    Unsere Gruppe besteht aus zwei Data Analysts und zwei Data Scientists.
    """)

    # ---- CARD STYLE ----
    card_style = """
    <style>
    .team-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        transition: 0.3s;
        font-size: 1.9em;
        font-weight: 700;
    }
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
    }
    .team-role {
        font-size: 1.5em;
        font-weight: 600;
        text-align: center;
    }
    .team-role2 {
        font-size: 1.1em;
        font-weight: 600;
        color: #1E88E5;
        text-align: center;
    }
        .team-role3 {
        font-size: 1.1em;
        font-weight: 600;
        color: #ff7f0e;
        text-align: center;
    }
    .team-task {
        font-size: 0.95em;
        opacity: 0.85;
    }
    </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # ---- SABRINA ----
    with col1:
        st.markdown('<div class="team-card">Sabrina</div>', unsafe_allow_html=True)
        st.image("psychology.png", width=180)
        # st.markdown("### **Sabrina**")
        st.markdown('<p class="team-role">Psychologin</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-role2">Data Analyst</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Datenbereinigung <br> Datenvorverarbeitung <br> Globale Datenanalyse</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- DIANELA ----
    with col2:
        st.markdown('<div class="team-card">Dianela</div>', unsafe_allow_html=True)
        st.image("informatic_engineering.png", width=180)
        # st.markdown("### **Dianela**")
        st.markdown('<p class="team-role">Informatikingenieurin</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-role2">Data Analyst</p>', unsafe_allow_html=True)
        #st.markdown('<p class="team-role">Informatikingenieurin<br>Data Analyst</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Datenbank <br> Datenvorverarbeitung <br> Globale Datenanalyse</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- MIRTHA ----
    with col3:
        st.markdown('<div class="team-card">Mirtha</div>', unsafe_allow_html=True)
        st.image("physicist.png", width=180)
        # st.markdown("### **Mirtha**")
        st.markdown('<p class="team-role">Physikerin</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-role3">Data Scientist</p>', unsafe_allow_html=True)
        # st.markdown('<p class="team-role">Physikerin<br>Data Scientist</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Statistische Analize <br> Entwicklung interaktiver Dashboards</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- DANIEL ----
    with col4:
        st.markdown('<div class="team-card">Daniel</div>', unsafe_allow_html=True)
        st.image("civil_engineering.png", width=180)
        # st.markdown("### **Daniel**")
        st.markdown('<p class="team-role">Bauingenieur</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-role3">Data Scientist</p>', unsafe_allow_html=True)
        # st.markdown('<p class="team-role">Bauingenieur<br>Data Scientist</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe:  <br>  Feature‑Engineering <br>  Entwicklung prädiktiver Modelle </p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:

    st.subheader("Ein datengetriebener Ansatz für Komfort & Energieeffizienz")

    # ---------------------------------------------------------
    # THREE COLUMNS
    # ---------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    # ---------------------------------------------------------
    # CARD STYLE (Streamlit-safe)
    # ---------------------------------------------------------

    card_style_blue = """
        <div style="
            background-color:#E3F2FD;
            padding:20px;
            border-radius:12px;
            text-align:center;
            border:1px solid #90CAF9;">
    """
    card_style_green = """
        <div style="
            background-color:#E8F5E9;
            padding:20px;
            border-radius:12px;
            text-align:center;
            border:1px solid #A5D6A7;">
    """
    card_style_orange = """
        <div style="
            background-color:#FFF3E0;
            padding:20px;
            border-radius:12px;
            text-align:center;
            border:1px solid #FFCC80;">
    """

    # ---------------------------------------------------------
    # COLUMN 1 – Unser Auftrag
    # ---------------------------------------------------------
    with col1:
        st.markdown(card_style_blue, unsafe_allow_html=True)
        #st.image("https://cdn-icons-png.flaticon.com/512/1040/1040230.png", width=70)
        st.markdown("""
        ### 🏢 Unser Auftrag  
        Ein führendes Unternehmen möchte prüfen,  
        ob auf Basis von Daten ein intelligentes  
        Gebäudesystem entwickelt werden kann,  
        das den Komfort der Nutzer erhöht und  
        gleichzeitig energieeffizient ist.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # COLUMN 2 – Unser Ansatz
    # ---------------------------------------------------------
    with col2:
        st.markdown(card_style_green, unsafe_allow_html=True)
        #st.image("https://cdn-icons-png.flaticon.com/512/4144/4144784.png", width=70)
        st.markdown("""
        ### 🔍 Unser Ansatz  
        Wir analysieren die **ASHRAE Global  
        Thermal Comfort Database II**, eine der  
        weltweit größten Datenquellen zu  
        thermischer Behaglichkeit in  
        verschiedenen Umgebungen.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # COLUMN 3 – Unser Ziel
    # ---------------------------------------------------------
    with col3:
        st.markdown(card_style_orange, unsafe_allow_html=True)
       #st.image("https://cdn-icons-png.flaticon.com/512/992/992700.png", width=70)
        st.markdown("""
        ### 🎯 Unser Ziel  
        Datenbasierte Erkenntnisse liefern, die  
        als Grundlage für die Entwicklung eines  
        **intelligenten, adaptiven und nachhaltigen  
        Gebäudesystems** dienen.
        """)
        st.markdown("</div>", unsafe_allow_html=True)


   
    # ---------------------------------------------------------
    # OPTIONAL: VISUAL STRUCTURE
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🔗 Komfort + Energieeffizienz = Smart Building")
    st.markdown("""
    Dieses Projekt zeigt, wie reale Komfortdaten genutzt werden können,  
    um Gebäude intelligenter, nachhaltiger und nutzerfreundlicher zu machen.
    """)

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------
    st.markdown("---")
    st.caption("Smart Building Comfort Analytics – Streamlit Prototype")


    st.markdown("""
    ## 🎯 Beratungsziel

    Unsere Aufgabe ist es, bestehende **Daten zur thermischen Behaglichkeit** aus der  
    **ASHRAE Global Thermal Comfort Database II** zu analysieren, um die wichtigsten 
    Einflussfaktoren auf die **thermische Wahrnehmung und den Komfort von Personen** 
    zu identifizieren.

    Die gewonnenen Erkenntnisse unterstützen Unternehmen dabei, fundierte Entscheidungen 
    für die Entwicklung moderner und intelligenter Gebäude zu treffen.

    ---

    ### 🔍 Anwendungsfelder der Ergebnisse

    🏢 **Gebäudeautomatisierung**  
    - Entwicklung intelligenter Regelstrategien  
    - Anpassung von Gebäudesystemen an Nutzerbedürfnisse  

    🌡️ **Heizung, Lüftung und Klimatisierung (HLK/HVAC)**  
    - Optimierung von Heiz- und Kühlsystemen  
    - Verbesserung der Raumklimaregelung  

    📡 **Sensorplatzierung und Datenerfassung**  
    - Identifikation wichtiger Messgrößen  
    - Auswahl relevanter Sensorparameter für Smart Buildings  

    👤 **Personalisierte Komfortlösungen**  
    - Berücksichtigung individueller Unterschiede  
    - Entwicklung nutzerorientierter Klimastrategien  

    ⚡ **Energieeffizienter Gebäudebetrieb**  
    - Balance zwischen Komfort und Energieverbrauch  
    - Optimierung des Gebäudemanagements  

    🏠 **Arbeitsplatzgestaltung**  
    - Verbesserung der Innenraumqualität  
    - Unterstützung eines angenehmen Arbeitsumfelds  

    ---

    ### 🌱 Übergeordnetes Ziel

    Entwicklung von datenbasierten Empfehlungen für ein **Smart-Building-Konzept**,  
    das eine optimale Balance zwischen:

    - ✅ Nutzerkomfort  
    - ✅ gesundem Raumklima  
    - ✅ Energieeffizienz  

    ermöglicht.
    """)


    st.markdown(
    """
    <div style="
        background-color: #f7f7f7;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #4B9CD3;
        font-size: 20px;
        line-height: 1.5;
        margin-top: 20px;
    ">
        Dieses Projekt analysiert Gebäudedaten, um Energieeffizienz,
        Komfort und Nachhaltigkeit in klimatisierten Infrastrukturen zu verbessern.
        Hier findest du Dashboards, Datenpipelines und Machine-Learning-Modelle,
        die unser Smart-Building-Konzept unterstützen.
    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    ## 1️⃣ Einführung

    **Smart Building Analytics** ist unser Abschlussprojekt im Rahmen der beruflichen Weiterbildung.
    Es handelt sich nicht um ein statisches Dashboard, sondern um eine **cloudnative, prädiktive
    Webanwendung**, die modernste Machine‑Learning‑Algorithmen nutzt.

    Ziel des Projekts ist es, die Brücke zwischen **thermodynamischen Big Data** und **künstlicher
    Intelligenz** zu schlagen, um thermischen Komfort in Gebäuden nicht nur zu analysieren,
    sondern **proaktiv vorherzusagen**.

    ### 🔧 Systemüberblick
    - Entwicklung einer cloudnativen, prädiktiven Webanwendung zur intelligenten Visualisierung
      und Prognose globaler Mikroklimadaten.
    - Technologie‑Stack: **Python + Streamlit** im Frontend, **Neon PostgreSQL** als Cloud‑Datenbank.
    - Integration von Machine Learning zur Vorhersage thermischer Komfortparameter.
    - Fokus auf den vier Hauptvariablen:
        - **Thermal Comfort (TC)**
        - **Thermal Sensation (TSV)**
        - **Thermal Preference (TP)**
        - **Thermal Acceptability (TA)**

    ### 🎯 Projektziele – Datengetriebener Pipeline‑Ansatz
    - **Datenbereinigung:** Strukturierung und systematische Behandlung unvollständiger Rohdaten.
    - **Datenkonsistenz:** Aufbau einer robusten relationalen Cloud‑Datenbank (Neon PostgreSQL).
    - **Prädiktive Analytik:** KI‑Modelle zur automatischen Vorhersage von TSV, TC, TP und TA.
    - **Deployment:** Bereitstellung aller Datenströme, Filter und Modelle über eine interaktive
      Streamlit‑Webanwendung.
    """)

# -------------------------
# TAB 2 – WARUM?
# -------------------------
with tab3:


    st.subheader("Hauptziel der Analyse")

    st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                Untersuchung von möglichen Einflussfaktoren auf das thermische Empfinden
                -> Ziel: Unterstützung für Firmen bei der Erschaffung eines guten Arbeitsumfelds
            </div>
            """,
            unsafe_allow_html=True
        )
    


    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1 ,1 ,1])
   
    #######################################################################################################################################################
    #######################################################################################################################################################

    # - Fragestellung 1 -
    with col1:
        st.markdown(
            """
            <h3 style="text-align: center;">
                Fragestellung 1
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                <b>Klima</b><br>
                Beeinflussen Klimazonen das thermische Empfinden?
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # - Fragestellung 2 -
    with col2:
        st.markdown(
            """
            <h3 style="text-align: center;">
                Fragestellung 2
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                <b>Belüftungsart</b><br>
                Beeinflusst die Belüftungsart das thermische Empfinden?
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # - Fragestellung 3 -
    with col3:
        st.markdown(
            """
            <h3 style="text-align: center;">
                Fragestellung 3
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                <b>Raumklima</b><br>
                Beeinflusst das Klima des Innenraums das thermische Empfinden?
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    st.text("Ein datenbasiertes Gleichgewicht zwischen wirtschaftlicher Effizienz und menschlichem Wohlbefinden.")

    st.text("Kopie von Notitzen")

    

    st.markdown("""
    ## 2️⃣ Grund – Warum Smart Building Analytics?

    ### 🌍 Big‑Data‑Herausforderung
    Klassische Werkzeuge versagen bei der Analyse von über **100.000 Messreihen** und führen zu
    Systemabstürzen. Smart Building Analytics löst dieses Problem durch Cloud‑Computing und
    optimierte Datenpipelines.

    ### ⚡ Energieeffizienz
    Gebäude verursachen weltweit rund **40 % des Energieverbrauchs**.  
    KI‑gestützte Steuerung kann den CO₂‑Ausstoß drastisch reduzieren.

    ### 🙂 Nutzer‑Wohlbefinden
    Raumklima beeinflusst Produktivität und Gesundheit.  
    Unser System erkennt kritische Diskomfort‑Zustände im Sekundenbruchteil, indem es die vier
    Komfortparameter mit **Alter** und **Geschlecht** verknüpft, um präzise Komfortzonen zu bestimmen.
    """)

# -------------------------
# TAB 3 – MACHINE LEARNING
# -------------------------
with tab4:
    st.markdown("""
    ## 3️⃣ Machine Learning Integration

    Der wichtigste Meilenstein unseres Projekts ist die **Machine‑Learning‑Integration**.
    Wir nutzen die **109.000 historischen Datensätze** nicht nur für Grafiken, sondern als
    Trainingsdaten für KI‑Modelle.

    Das System lernt Muster der menschlichen Wahrnehmung und kann dadurch zukünftige
    Komfortstufen autonom prognostizieren – bevor Energie verschwendet wird.

    ### 🤖 Prädiktive Analytik via Machine Learning
    - Übergang von deskriptiver Statistik zu **Predictive Analytics**.
    - Klassifikationsmodelle wie **Random Forest** und **Gradient Boosting**.
    - Ziel: KI‑gestützte Prognose von **Thermal Acceptability** und **Thermal Sensation**.
    - Grundlage: Live‑Sensordaten (Temperatur, Feuchtigkeit, Luftgeschwindigkeit).
    """)

# -------------------------
# TAB 4 – ASHRAE DATENSATZ
# -------------------------
with tab5:

    st.subheader("🛠️ Data Science & Analytics Tools")
        #st.header("🧰 Data Science & Analytics Tools")

    # st.text("Tools für Datenanalyse, Machine Learning und interaktive Dashboards")
    st.write("Moderne Tools für Datenanalyse, Machine Learning und interaktive Dashboards")

    st.code("Datenerfassung → Datenaufbereitung → Analyse → Maschinelles Lernen → Visualisierung → Bereitstellung")
    # st.markdown("""
    # ### <span style="font-size:32px; font-weight:800;">
    # **Datenerfassung → Datenaufbereitung → Analyse → Maschinelles Lernen → Visualisierung → Bereitstellung**
    # </span>
    # """, unsafe_allow_html=True)


    # --- STYLE ---
    style = """
    <style>
    .tech-card {
        background-color: #ff7f0e;
        padding: 22px;
        font-size: 1.2em;
        font-weight: 700;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.12);
        transition: 0.3s ease;
        color: #0A2540;
        border: 1px solid #e6e6e6;
        margin-bottom: 20px;
    }
    .tech-card:hover {
        transform: translateY(-6px);
        box-shadow: 0px 8px 22px rgba(0,0,0,0.18);
    }
    .tech-icon {
        width: 55px;
        height: 55px;
        object-fit: contain;
        margin-bottom: 10px;
    }
    .tech-title {
        font-size: 1.2em;
        font-weight: 700;
        color: #0A2540;
        margin-bottom: 6px;
    }
    .tech-desc {
        font-size: 0.95em;
        color: #333333;
        opacity: 0.85;
    }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

    # --- GRID 3 COLUMNS ---
    col1, col2, col3 = st.columns(3)

    # COLUMN 1
    with col1:
        st.markdown('<div  class="tech-card">Python</div>', unsafe_allow_html=True)
        #st.markdown('<img src="tools/python.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">Python</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Programmiersprache für Datenanalyse, Automatisierung und maschinelles Lernen.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">Explorative Datenanalyse (EDA)</div>', unsafe_allow_html=True)
        # st.markdown('<img src="tools/eda.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">Explorative Datenanalyse (EDA)</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Untersuchung und Visualisierung von Datensätzen zur Erkennung von Mustern und Anomalien.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">PostgreSQL Neon</div>', unsafe_allow_html=True)
        # st.markdown('<img src="tools/neon.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">PostgreSQL Neon</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Cloud‑Datenbank für effiziente Speicherung und Abfrage großer Datenmengen.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # COLUMN 2
    with col2:
        st.markdown('<div class="tech-card">Power BI</div>', unsafe_allow_html=True)
        # st.markdown('<img src="tools/powerbi.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">Power BI</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Business‑Intelligence‑Tool zur Erstellung interaktiver Visualisierungen und Berichte.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">Jupyter Notebook</div>', unsafe_allow_html=True)
        # st.markdown('<img src="tools/jupyter.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">Jupyter Notebook</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Interaktive Umgebung für Datenanalyse, Dokumentation und Präsentation von Code.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">NumPy</div>', unsafe_allow_html=True)
        # st.markdown('<img src="tools/numpy.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">NumPy</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Bibliothek für numerische Berechnungen und effiziente Verarbeitung großer Arrays.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # COLUMN 3
    with col3:
        st.markdown('<div class="tech-card">Pandas</div>', unsafe_allow_html=True)
        # st.markdown('<img src="tools/pandas.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">Pandas</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Datenmanipulation und ‑analyse mit leistungsstarken DataFrames.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">Machine Learning</div>', unsafe_allow_html=True)
        # st.markdown('<img src="tools/ml.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">Machine Learning</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Erstellung prädiktiver Modelle zur Analyse und Vorhersage von Mustern.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">Streamlit</div>', unsafe_allow_html=True)
        # st.markdown('<img src="tools/streamlit.png" class="tech-icon">', unsafe_allow_html=True)
        # st.markdown('<div class="tech-title">Streamlit</div>', unsafe_allow_html=True)
        # st.markdown('<div class="tech-desc">Framework zur Entwicklung interaktiver Web‑Apps für Datenvisualisierung.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)








    st.markdown("""
    ## 4️⃣ ASHRAE Datensatz – Die wissenschaftliche Basis

    ### 📊 ASHRAE Global Thermal Comfort Database v2.1
    - Erstellt von der *American Society of Heating, Refrigerating and Air‑Conditioning Engineers*.
    - Wir verwenden die frei verfügbaren Datensätze von **Kaggle**.
    - Umfang: **109.033 empirische Datensätze** mit **59 physikalischen und demografischen Variablen**.
    - Wissenschaftlicher Wert: Globaler Goldstandard zur Validierung adaptiver Komfortmodelle
      wie der **ASHRAE‑Norm 55**.

    Die Daten bilden die Grundlage für alle Analysen, Visualisierungen und Machine‑Learning‑Modelle
    in unserer Anwendung.
    """)



    # st.text("Ein datenbasiertes Gleichgewicht zwischen wirtschaftlicher Effizienz und menschlichem Wohlbefinden.")

    # st.text("Kopie von Notitzen")

    # st.title("Introduction to the Global Thermal Comfort Database")

    # st.write("""
    # The Global Thermal Comfort Database is an international collection of field studies 
    # that document how people experience thermal conditions in real buildings across 
    # different climates, seasons, and building types. The database integrates thousands 
    # of observations that include environmental measurements, occupant surveys, and 
    # contextual metadata. 

    # Its purpose is to support research on human thermal comfort, adaptive behavior, 
    # and indoor environmental quality by providing a unified and standardized dataset 
    # that researchers can analyze and compare across regions.
    # """)

    # st.subheader("Why the Data Collection Method Matters")

    # st.write("""
    # Understanding how the data was collected is essential for interpreting the results 
    # correctly. Each study in the database may differ in terms of measurement equipment, 
    # survey methods, building characteristics, and climatic context. These differences 
    # influence how occupants perceive their environment and how comfort models should 
    # be applied.

    # Documenting the data collection process ensures:

    # - **Transparency**: Researchers can evaluate the reliability and limitations of each dataset.
    # - **Reproducibility**: Other analysts can replicate or extend the study using the same methods.
    # - **Comparability**: Differences between studies can be understood rather than mistaken for 
    #     behavioral or climatic effects.
    # - **Correct interpretation**: Comfort responses depend on context—building type, season, 
    #     climate, and occupant expectations all matter.

    # For these reasons, the metadata describing how each study was conducted is just as 
    # important as the measurements themselves.
    # """)

    # st.subheader("Structure of the Database")

    # st.write("""
    # The database is organized into two main components:

    # - **Metadata**: Information about the study, building, climate, and measurement methods.
    # - **Measurements**: Individual observations including temperatures, humidity, air speed, 
    #     clothing levels, metabolic rates, and subjective comfort votes.

    # This structure allows users to link each measurement to its environmental and contextual 
    # background, enabling multi‑scale analysis and robust interpretation.
    # """)




    # st.subheader("Why is it important to study this topic today?")

    # st.write("""
    # 🌍 **1. Climate change and more frequent heatwaves**  
    # Due to climate change, extreme temperatures are becoming more common. Buildings must 
    # protect people under these conditions and maintain comfort. Understanding thermal 
    # comfort helps us design better and more resilient buildings.
    # """)

    # st.write("""
    # ⚡ **2. Energy crisis and the need for efficiency**  
    # Heating, cooling, and ventilation account for **30–50%** of a building’s total energy use.  
    # If we can better predict how people perceive thermal conditions, we can:
    # - Save energy  
    # - Reduce operational costs  
    # - Avoid overheating or overcooling  

    # Thermal comfort models (e.g., based on ASHRAE data) are essential for this.
    # """)

    # st.write("""
    # 🧠 **3. Artificial intelligence in buildings**  
    # Modern buildings are becoming *smart*. Data such as those from the ASHRAE Global Thermal 
    # Comfort Database enable:
    # - AI models that predict comfort  
    # - Automatic adjustment of HVAC systems  
    # - Personalized indoor climate control  

    # This makes the topic highly relevant today.
    # """)

    # st.write("""
    # 🏢 **4. Health, wellbeing, and productivity**  
    # Thermal comfort influences:
    # - Concentration  
    # - Performance  
    # - Health  
    # - User satisfaction  

    # Companies and public institutions increasingly focus on indoor wellbeing.
    # """)

    # st.write("""
    # 🌐 **5. Sustainable building and international standards**  
    # ASHRAE standards such as **55**, **62.1**, and **90.1** are globally important.  
    # Anyone working in architecture, building engineering, or research will encounter them.

    # This topic matters today because it connects people, energy, climate, technology, 
    # and health. It is a research field with direct impact on the future of our buildings 
    # and cities.
    # """)
    
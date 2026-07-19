import streamlit as st

st.set_page_config(
    page_title="Introduction",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏢 Thermischer Komfort in Innenräumen - Datenanalyse und Machine Learning Modellierung")

# -------------------------
#       TABS
# -------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1️⃣ Einführung und Team",
    "2️⃣ Wahl des Themas",
    "3️⃣ Datenquelle",
    "4️⃣ Machine Learning Integration",
    "5️⃣ Tools und Prozess",
    "6️⃣ Projektziele"
])

# -------------------------
# TAB 1 – Einführung
# -------------------------
with tab1:
    st.subheader("1️⃣ Einführung")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
    """
    <div style="
        background-color: #f7f7f7;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #4B9CD3;
        font-size: 18px;
        line-height: 1.5;
        margin-top: 20px;
    ">
        Dieses Projekt analysiert weltweite Gebäudedaten, um Komfort, Energieeffizienz und Nachhaltigkeit in klimatisierten Infrastrukturen zu verbessern
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
        #### ℹ️ Wichtige Informationen zum Projekt
    """
    )

    st.markdown("""
        - **Abschlussprojekt** im Rahmen der Weiterbildung zu Data Analyst bzw. Data Scientist des Data Science Institute DSI Education GmbH
        - **cloudnative, prädiktive Webanwendung**, die modernste Machine‑Learning‑Algorithmen nutzt
        - Ziel des Projekts: Brücke zwischen **Analyse von thermodynamischen Big Data** und **Machine Learning** schlagen, um thermischen Komfort in Gebäuden nicht nur zu analysieren, sondern proaktiv vorherzusagen
    """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        #### 👥 Team
    """
    )

    st.markdown("""
        - Wir sind vier Personen mit **unterschiedlichen beruflichen Hintergründen**  
        - Unsere Gruppe besteht aus **zwei Data Analysts und zwei Data Scientists**
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
            font-size: 1.5em;
            font-weight: 500;
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

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # ---- SABRINA ----
    with col1:
        st.markdown('<div class="team-card">Sabrina</div>', unsafe_allow_html=True)
        st.image("psychology.png", width=180)
        # st.markdown("### **Sabrina**")
        st.markdown('<p class="team-role">B. Sc. Psychologie</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-role2">Data Analyst</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Datenbereinigung <br> Datenvorverarbeitung <br> Klima Analyse</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- DIANELA ----
    with col2:
        st.markdown('<div class="team-card">Dianela</div>', unsafe_allow_html=True)
        st.image("informatic_engineering.png", width=180)
        # st.markdown("### **Dianela**")
        st.markdown('<p class="team-role">Informatikingenieurin</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-role2">Data Analyst</p>', unsafe_allow_html=True)
        #st.markdown('<p class="team-role">Informatikingenieurin<br>Data Analyst</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Datenbank <br> Datenvorverarbeitung <br> Cooling Typ Analyse</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- MIRTHA ----
    with col3:
        st.markdown('<div class="team-card">Mirtha</div>', unsafe_allow_html=True)
        st.image("physicist.png", width=180)
        # st.markdown("### **Mirtha**")
        st.markdown('<p class="team-role">Physikerin</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-role3">Data Scientist</p>', unsafe_allow_html=True)
        # st.markdown('<p class="team-role">Physikerin<br>Data Scientist</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Thermal Comofort Analyse <br> Entwicklung der GitHub-Architektur <br> Entwicklung der Streamlit-Architektur</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- DANIEL ----
    with col4:
        st.markdown('<div class="team-card">Daniel</div>', unsafe_allow_html=True)
        st.image("civil_engineering.png", width=180)
        # st.markdown("### **Daniel**")
        st.markdown('<p class="team-role">Bauingenieur</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-role3">Data Scientist</p>', unsafe_allow_html=True)
        # st.markdown('<p class="team-role">Bauingenieur<br>Data Scientist</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe:  <br> Machine Learning  <br> Feature‑Engineering <br>  Entwicklung prädiktiver Modelle </p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # **Smart Building Analytics** ist unser Abschlussprojekt im Rahmen der beruflichen Weiterbildung.
    # Es handelt sich nicht um ein statisches Dashboard, sondern um eine **cloudnative, prädiktive
    # Webanwendung**, die modernste Machine‑Learning‑Algorithmen nutzt.

    # Ziel des Projekts ist es, die Brücke zwischen **thermodynamischen Big Data** und **künstlicher
    # Intelligenz** zu schlagen, um thermischen Komfort in Gebäuden nicht nur zu analysieren,
    # sondern **proaktiv vorherzusagen**.

    

    # ### 🎯 Projektziele – Datengetriebener Pipeline‑Ansatz
    # - **Datenbereinigung:** Strukturierung und systematische Behandlung unvollständiger Rohdaten.
    # - **Datenkonsistenz:** Aufbau einer robusten relationalen Cloud‑Datenbank (Neon PostgreSQL).
    # - **Prädiktive Analytik:** KI‑Modelle zur automatischen Vorhersage von TSV, TC, TP und TA.
    # - **Deployment:** Bereitstellung aller Datenströme, Filter und Modelle über eine interaktive
    #   Streamlit‑Webanwendung.
    

# -------------------------
# TAB 2 – Wahl des Themas
# -------------------------
with tab2:
    st.subheader("2️⃣ Warum Untersuchung des Thermischen Komforts in Innenräumen?")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1.5])
    
    with col1: 
        st.info("""
        ℹ️ **Thermischer Komfort in Innenräumen ist ein wichtiges Thema** 
        
        
        ➝ Es verbindet:
                

        - Menschen
        - Klima
        - Technologie
        - Energie
        - Gesundheit 
        """
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    #### 🙂 Nutzer*innen‑Wohlbefinden
    - Raumklima beeinflusst Produktivität und Gesundheit
    - Durch Klimawandel nehmen extreme Temperaturen zu ➝ Gebäude sollten auch unter diesen Bedingungen den Komfort der Menschen erhalten 
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    #### ⚡ Energieeffizienz und Nachhaltigkeit
    - Gebäude verursachen weltweit rund 40 % des Energieverbrauchs **-> Quelle?**  
    - Internationale Standards für Gebäude wie die von ASHRAE sind für nachhaltige Gebäude sehr wichtig
    - Bessere Vorhersage der optimalen thermischen Bedingungen kann z.B. Enegerie sparen und CO₂‑Ausstoß drastisch reduzieren
    """)      
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    #### 🧠 Künstliche Intelligenz in Gebäuden
    - Daten können helfen, KI-Modelle zu generieren, die z.B.:
        
                
        - thermischen Komfort vorhersagen 
        - personalisierte Kontrolle des Innenraumklimas ermöglichen   
    """)

    

    

    
    # ### 🌍 Big‑Data‑Herausforderung
    # Klassische Werkzeuge versagen bei der Analyse von über **100.000 Messreihen** und führen zu
    # Systemabstürzen. Smart Building Analytics löst dieses Problem durch Cloud‑Computing und
    # optimierte Datenpipelines.

    # Unser System erkennt kritische Diskomfort‑Zustände im Sekundenbruchteil, indem es die vier
    # Komfortparameter mit **Alter** und **Geschlecht** verknüpft, um präzise Komfortzonen zu bestimmen.

# -------------------------
# TAB 3 – Datenquelle
# -------------------------
with tab3:
    st.subheader("3️⃣ Datenquelle: ASHRAE Global Thermal Comfort Database v2.1")

    st.markdown("<br>", unsafe_allow_html=True)


    st.write(
        "Umfassende Datenbank zur **Untersuchung des thermischen Komforts in Gebäuden weltweit**"
    )

    st.markdown(
        """
        - Zusammenstellung von Feldstudien aus dem Zeitraum **1995–2016**
        - Erstellt von der *American Society of Heating, Refrigerating and Air‑Conditioning Engineers*
        - Besteht aus zwei verschiedenen Datenbanken db 1.0 und db 2.0
        - Update der Datenbank mit neuen Einträgen -> db 2.1
        - Ein finaler, zusammengeführter Datensatz mit insgesamt **109.033** Einträgen
        - Wissenschaftlicher Wert: Globaler Goldstandard zur Validierung adaptiver Komfortmodelle wie der **ASHRAE‑Norm 55**
    """
    )
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
    """
    #### **🔗 Dataset Source:**

    [ASHRAE Global Thermal Comfort Database II](https://datadryad.org/dataset/doi:10.6078/D1F671)

    - Datensatz findet sich in verschiedenen Versionen z.B. bei kaggle 
    - Für dieses Projekt wurde der **originale Datensatz von ASHRAE** genutzt
    """
    )

    st.markdown("<br>", unsafe_allow_html=True)


# -------------------------
# TAB 4 – MACHINE LEARNING
# -------------------------
with tab4:
    st.markdown("""
    ## 4️⃣  Machine Learning Integration

    Ein wichtiger Teil unseres Projekts ist die **Machine‑Learning‑Integration**.
    Wir nutzen die **109.000 Datensätze** nicht nur für Grafiken, sondern als
    Trainingsdaten für Vorhersage-Modelle.

    Das System lernt Muster der menschlichen thermischen Bewertung und kann dadurch zukünftige
    thermische Parameter autonom prognostizieren – bevor Energie verschwendet wird.

    ### 🤖 Prädiktive Analytik via Machine Learning
    - Übergang von deskriptiver Statistik zu **Predictive Analytics**.
    - Klassifikationsmodelle wie **Random Forest** und **Gradient Boosting**.
    - Ziel: Prognose von **Thermal Acceptability** und **Thermal Sensation**.
    - Grundlage: Live‑Sensordaten (Temperatur, Feuchtigkeit, Luftgeschwindigkeit).
    """)

# -------------------------
# TAB 5 – Tools und Prozess
# -------------------------
with tab5:
    st.subheader("5️⃣ Data Science & Analytics Tools und Prozess")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tools
    st.markdown("""
        #### 🛠️ Tools
    """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- STYLE ---
    style = """
    <style>
    .tech-card {
        background-color: #f7f7f7;
        padding: 10px;
        font-size: 1em;
        font-weight: 700;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.12);
        transition: 0.3s ease;
        color: #0A2540;
        border: 1px solid #e6e6e6;
        margin-bottom: 20px;
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
        st.markdown('<div class="tech-card">Power BI ??????????</div>', unsafe_allow_html=True)
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

        st.markdown('<div  class="tech-card">GitHub</div>', unsafe_allow_html=True)

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


    st.markdown("<br>", unsafe_allow_html=True)

    # Prozess
    st.markdown("""
        #### 🔁 Prozess des Projekts
    """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1, 0.2, 1, 0.2, 1])
    col6, col7, col8, col9, col10 = st.columns([1, 0.2, 1, 0.2, 1])
    col11, col12, col13, col14, col15 = st.columns([1, 0.2, 1, 0.2, 1])

    with col1:
        st.markdown('<div  class="tech-card">Themenfindung und Datenrecherche</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col2:
        st.markdown(
                    "<span style='font-size:30px;'>➡️</span>",
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div  class="tech-card">Datenaufbereitung</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col4:
        st.markdown(
                    "<span style='font-size:30px;'>➡️</span>",
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


    with col5:
        st.markdown('<div  class="tech-card">Datenbank</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col10:
        st.markdown(
            """
            <div style="text-align: center;">
                <span style='font-size:30px;'>⬇️</span>
            """,
            unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col15:
        st.markdown('<div  class="tech-card">Datenanalyse und Visualisierungen</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col14:
        st.markdown(
                    "<span style='font-size:30px;'>⬅️</span>",
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col13:
        st.markdown('<div  class="tech-card">Machine Learning </div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col12:
        st.markdown(
                    "<span style='font-size:30px;'>⬅️</span>",
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col11:
        st.markdown('<div  class="tech-card">Streamlit-App</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    
    
# ### 🔧 Systemüberblick
    # - Entwicklung einer cloudnativen, prädiktiven Webanwendung zur intelligenten Visualisierung
    #   und Prognose globaler Mikroklimadaten.
    # - Technologie‑Stack: **Python + Streamlit** im Frontend, **Neon PostgreSQL** als Cloud‑Datenbank.
    # - Integration von Machine Learning zur Vorhersage thermischer Komfortparameter.
    # - Fokus auf den vier Hauptvariablen:
    #     - **Thermal Comfort (TC)**
    #     - **Thermal Sensation (TSV)**
    #     - **Thermal Preference (TP)**
    #     - **Thermal Acceptability (TA)**
# with tab5:
#     st.text("Ein datenbasiertes Gleichgewicht zwischen wirtschaftlicher Effizienz und menschlichem Wohlbefinden.")


#     st.write("""
#     The Global Thermal Comfort Database is an international collection of field studies 
#     that document how people experience thermal conditions in real buildings across 
#     different climates, seasons, and building types. The database integrates thousands 
#     of observations that include environmental measurements, occupant surveys, and 
#     contextual metadata. 

#     Its purpose is to support research on human thermal comfort, adaptive behavior, 
#     and indoor environmental quality by providing a unified and standardized dataset 
#     that researchers can analyze and compare across regions.
#     """)

#     st.subheader("Why the Data Collection Method Matters")

#     st.write("""
#     Understanding how the data was collected is essential for interpreting the results 
#     correctly. Each study in the database may differ in terms of measurement equipment, 
#     survey methods, building characteristics, and climatic context. These differences 
#     influence how occupants perceive their environment and how comfort models should 
#     be applied.

#     Documenting the data collection process ensures:

#     - **Transparency**: Researchers can evaluate the reliability and limitations of each dataset.
#     - **Reproducibility**: Other analysts can replicate or extend the study using the same methods.
#     - **Comparability**: Differences between studies can be understood rather than mistaken for 
#         behavioral or climatic effects.
#     - **Correct interpretation**: Comfort responses depend on context—building type, season, 
#         climate, and occupant expectations all matter.

#     For these reasons, the metadata describing how each study was conducted is just as 
#     important as the measurements themselves.
#     """)

#     st.subheader("Structure of the Database")

#     st.write("""
#     The database is organized into two main components:

#     - **Metadata**: Information about the study, building, climate, and measurement methods.
#     - **Measurements**: Individual observations including temperatures, humidity, air speed, 
#         clothing levels, metabolic rates, and subjective comfort votes.

#     This structure allows users to link each measurement to its environmental and contextual 
#     background, enabling multi‑scale analysis and robust interpretation.
#     """)




#     st.subheader("Why is it important to study this topic today?")

#     st.write("""
#     🌍 **1. Climate change and more frequent heatwaves**  
#     Due to climate change, extreme temperatures are becoming more common. Buildings must 
#     protect people under these conditions and maintain comfort. Understanding thermal 
#     comfort helps us design better and more resilient buildings.
#     """)

#     st.write("""
#     ⚡ **2. Energy crisis and the need for efficiency**  
#     Heating, cooling, and ventilation account for **30–50%** of a building’s total energy use.  
#     If we can better predict how people perceive thermal conditions, we can:
#     - Save energy  
#     - Reduce operational costs  
#     - Avoid overheating or overcooling  

#     Thermal comfort models (e.g., based on ASHRAE data) are essential for this.
#     """)

#     st.write("""
#     🧠 **3. Artificial intelligence in buildings**  
#     Modern buildings are becoming *smart*. Data such as those from the ASHRAE Global Thermal 
#     Comfort Database enable:
#     - AI models that predict comfort  
#     - Automatic adjustment of HVAC systems  
#     - Personalized indoor climate control  

#     This makes the topic highly relevant today.
#     """)

#     st.write("""
#     🏢 **4. Health, wellbeing, and productivity**  
#     Thermal comfort influences:
#     - Concentration  
#     - Performance  
#     - Health  
#     - User satisfaction  

#     Companies and public institutions increasingly focus on indoor wellbeing.
#     """)

#     st.write("""
#     🌐 **5. Sustainable building and international standards**  
#     ASHRAE standards such as **55**, **62.1**, and **90.1** are globally important.  
#     Anyone working in architecture, building engineering, or research will encounter them.

#     This topic matters today because it connects people, energy, climate, technology, 
#     and health. It is a research field with direct impact on the future of our buildings 
#     and cities.
#     """)

# -------------------------
# TAB 6 – Projektziele
# -------------------------
with tab6:
    st.subheader("6️⃣ Ziele des Projekts")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 0.5, 1])

    with col1:
        st.markdown("""
            #### 🔧 Systemüberblick und Ziele
        """
        )
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
            - Entwicklung einer **cloudnativen, prädiktiven Webanwendung zur Visualisierung und Prognose von thermischer Bewertung**
                    

                ➝ Technologie‑Stack: **Python + Streamlit** im Frontend, **Neon PostgreSQL** als Cloud‑Datenbank
                    

            - Untersuchung von möglichen **Einflussfaktoren** auf die thermische Bewertung
            - Integration von Machine Learning zur **Vorhersage thermischer Komfortparameter**
        """
        )

        st.markdown("<br><br><br>", unsafe_allow_html=True)

    with col2:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("""
                <div style="text-align: center;">
                        <span style='font-size:30px;'>➡️</span>""",
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("""
            #### 🎯 Zielvariablen des Projekts
        """
        )
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
            - **Thermal Comfort**
            - **Thermal Sensation**
            - **Thermal Preference**
            - **Thermal Acceptability**
        """
        )
        #     - **Thermal Comfort (TC)**
        #     - **Thermal Sensation (TSV)**
        #     - **Thermal Preference (TP)**
        #     - **Thermal Acceptability (TA)**
        st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown("""
        #### ❓ Fragestellungen der Datenanalyse
    """
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, spacer, col2, spacer, col3 = st.columns([1, 0.2, 1, 0.2, 1])
   
    
    # - Fragestellung 1 -
    with col1:
        st.markdown(
            """
            <h5 style="text-align: center;">
               🌍 Klimatische/geografische Variablen Analyse
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                Gibt es einen Zusammenhang zwischen klimatischen/geografischen Variablen und thermischer Bewertung?
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # - Fragestellung 2 -
    with col2:
        st.markdown(
            """
            <h5 style="text-align: center;">
                🌀 Cooling Type und Gender Analyse
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                - Gibt es einen Zusammenhang zwischen Cooling Type und thermischer Bewertung?
                <br>
                - Gibt es einen Zusammenhang zwischen Gender und thermischer Bewertung?
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # - Fragestellung 3 -
    with col3:
        st.markdown(
            """
            <h5 style="text-align: center;">
                🌡️ Thermische Bewertung und Innen-
                raumklima Analyse
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                - Wie hängen verschiedene Faktoren der thermischen Bewertung miteinander zusammen?
                <br>
                - Gibt es einen Zusammenhang zwischen Innenraumklima und thermischer Bewertung?
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

 
    st.markdown("""
        #### 🎯Ziele des Machine Learning
    """
    )
    
    
import streamlit as st

st.set_page_config(
    page_title="Introduction – Smart Building Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏢 Smart Building Analytics – Einführung")

# -------------------------
#       TABS
# -------------------------
tab1, tab2, tab3, tab4,tab5 = st.tabs([
    "1️⃣ Einführung",
    "2️⃣ Grund – Warum?",
    "3️⃣ Machine Learning Integration",
    "4️⃣ ASHRAE Datensatz",
    "example"
])

# -------------------------
# TAB 1 – EINLEITUNG
# -------------------------
with tab1:

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
with tab2:
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
with tab3:
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
with tab4:
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


with tab5:
    st.text("Ein datenbasiertes Gleichgewicht zwischen wirtschaftlicher Effizienz und menschlichem Wohlbefinden.")

    st.text("Kopie von Notitzen")

    st.title("Introduction to the Global Thermal Comfort Database")

    st.write("""
    The Global Thermal Comfort Database is an international collection of field studies 
    that document how people experience thermal conditions in real buildings across 
    different climates, seasons, and building types. The database integrates thousands 
    of observations that include environmental measurements, occupant surveys, and 
    contextual metadata. 

    Its purpose is to support research on human thermal comfort, adaptive behavior, 
    and indoor environmental quality by providing a unified and standardized dataset 
    that researchers can analyze and compare across regions.
    """)

    st.subheader("Why the Data Collection Method Matters")

    st.write("""
    Understanding how the data was collected is essential for interpreting the results 
    correctly. Each study in the database may differ in terms of measurement equipment, 
    survey methods, building characteristics, and climatic context. These differences 
    influence how occupants perceive their environment and how comfort models should 
    be applied.

    Documenting the data collection process ensures:

    - **Transparency**: Researchers can evaluate the reliability and limitations of each dataset.
    - **Reproducibility**: Other analysts can replicate or extend the study using the same methods.
    - **Comparability**: Differences between studies can be understood rather than mistaken for 
        behavioral or climatic effects.
    - **Correct interpretation**: Comfort responses depend on context—building type, season, 
        climate, and occupant expectations all matter.

    For these reasons, the metadata describing how each study was conducted is just as 
    important as the measurements themselves.
    """)

    st.subheader("Structure of the Database")

    st.write("""
    The database is organized into two main components:

    - **Metadata**: Information about the study, building, climate, and measurement methods.
    - **Measurements**: Individual observations including temperatures, humidity, air speed, 
        clothing levels, metabolic rates, and subjective comfort votes.

    This structure allows users to link each measurement to its environmental and contextual 
    background, enabling multi‑scale analysis and robust interpretation.
    """)




    st.subheader("Why is it important to study this topic today?")

    st.write("""
    🌍 **1. Climate change and more frequent heatwaves**  
    Due to climate change, extreme temperatures are becoming more common. Buildings must 
    protect people under these conditions and maintain comfort. Understanding thermal 
    comfort helps us design better and more resilient buildings.
    """)

    st.write("""
    ⚡ **2. Energy crisis and the need for efficiency**  
    Heating, cooling, and ventilation account for **30–50%** of a building’s total energy use.  
    If we can better predict how people perceive thermal conditions, we can:
    - Save energy  
    - Reduce operational costs  
    - Avoid overheating or overcooling  

    Thermal comfort models (e.g., based on ASHRAE data) are essential for this.
    """)

    st.write("""
    🧠 **3. Artificial intelligence in buildings**  
    Modern buildings are becoming *smart*. Data such as those from the ASHRAE Global Thermal 
    Comfort Database enable:
    - AI models that predict comfort  
    - Automatic adjustment of HVAC systems  
    - Personalized indoor climate control  

    This makes the topic highly relevant today.
    """)

    st.write("""
    🏢 **4. Health, wellbeing, and productivity**  
    Thermal comfort influences:
    - Concentration  
    - Performance  
    - Health  
    - User satisfaction  

    Companies and public institutions increasingly focus on indoor wellbeing.
    """)

    st.write("""
    🌐 **5. Sustainable building and international standards**  
    ASHRAE standards such as **55**, **62.1**, and **90.1** are globally important.  
    Anyone working in architecture, building engineering, or research will encounter them.

    This topic matters today because it connects people, energy, climate, technology, 
    and health. It is a research field with direct impact on the future of our buildings 
    and cities.
    """)


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

    
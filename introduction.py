import streamlit as st

st.set_page_config(
    page_title="Introduction",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏢 Thermisches Befinden in Innenräumen")

# -------------------------
#       TABS
# -------------------------
tab1, tab2, tab3 = st.tabs([
    "1️⃣ Über uns",
    "2️⃣ Wahl des Themas und Datenquelle",
    "3️⃣ Tools"
])

# -------------------------
# TAB 1 – Einführung
# -------------------------
with tab1:
    st.subheader("1️⃣ Einführung")

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
        st.markdown('<p class="team-role2">Data Analyst</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Datenbereinigung <br> Klima-Analyse</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- DIANELA ----
    with col2:
        st.markdown('<div class="team-card">Dianela</div>', unsafe_allow_html=True)
        st.image("informatic_engineering.png", width=180)
        st.markdown('<p class="team-role2">Data Analyst</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Datenbank <br> Cooling Type-Analyse</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- MIRTHA ----
    with col3:
        st.markdown('<div class="team-card">Mirtha</div>', unsafe_allow_html=True)
        st.image("physicist.png", width=180)
        st.markdown('<p class="team-role3">Data Scientist</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe: <br> Thermischer Komfort-Analyse <br> Entwicklung der GitHub- und Streamlit-Architektur</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- DANIEL ----
    with col4:
        st.markdown('<div class="team-card">Daniel</div>', unsafe_allow_html=True)
        st.image("civil_engineering.png", width=180)
        st.markdown('<p class="team-role3">Data Scientist</p>', unsafe_allow_html=True)
        st.markdown('<p class="team-task">Aufgabe:  <br> Machine Learning  <br>  Entwicklung prädiktiver Modelle </p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# TAB 2 – Wahl des Themas
# -------------------------
with tab2:

    st.subheader("2️⃣ Ein datengetriebener Ansatz für Komfort & Energieeffizienz")

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
        thermischem Befinden in Innenräumen in 
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
        Gebäudesystems** dienen können.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🧾 Datenquelle: ASHRAE Global Thermal Comfort Database v2.1")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
    """
    #### **🔗 Dataset Source:**

    [ASHRAE Global Thermal Comfort Database II](https://datadryad.org/dataset/doi:10.6078/D1F671) 
    """
    )

    with st.expander("Weitere Informationen zur Datenquelle"):
        st.markdown(
            """
            - Umfassende Datenbank zur **Untersuchung des thermischen Komforts in Gebäuden weltweit**
            - Zusammenstellung von Feldstudien aus dem Zeitraum **1995–2016**
            - Erstellt von der *American Society of Heating, Refrigerating and Air‑Conditioning Engineers*
            - Datensatz findet sich in verschiedenen Versionen z.B. bei kaggle 
            - Für dieses Projekt wurde der **originale Datensatz von ASHRAE** genutzt
        """
        )
    st.markdown("<br><br>", unsafe_allow_html=True)

#    - Besteht aus zwei verschiedenen Datenbanken db 1.0 und db 2.0 ➝ Update der Datenbank mit neuen Einträgen -> db 2.1
#    - Ein finaler, zusammengeführter Datensatz mit insgesamt **109.033** Einträgen

    st.markdown("""
        ℹ️ **Thermisches Befinden in Innenräumen ist ein wichtiges Thema** ➝ Es verbindet:
                
        - Menschen (Produktivität, Gesundheit)
        - Klima
        - Technologie
        - Energie (Effizienz, Nachhaltigkeit)
        """
        )
    

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
        #### 🎯 Wichtige Variablen für Untersuchung des thermischen Befindens
    """
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col1, spacer, col2 = st.columns([2, 0.5, 2])
    col3, spacer, col4 = st.columns([2, 0.5, 2])

    with col1:
        st.markdown("""
            ##### 1. Thermischer Komfort 
        **Sehr unkomfortabel ◄────────────────► Sehr komfortabel**  
                `  1             2            3           4           5            6   `
        """)
        st.markdown("<br>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        ##### 2. Thermisches Empfinden
        **Kalt  ◄────── Neutral ──────►  Heiß**  
        `-3    -2    -1    0    +1    +2    +3 `
        """)
        st.markdown("<br>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        ##### 3. Thermische Akzeptanz
        ○ Nicht akzeptabel  
        ○ Akzeptabel  
        """)
        st.markdown("<br>", unsafe_allow_html=True)

    with col4:
        st.markdown("""
        ##### 4. Thermische Präferenz 
        **Kühler ◄──────── Keine Änderung ────────► Wärmer**  
        `  -1                         0                         +1     `
        """)
        st.markdown("<br><br>", unsafe_allow_html=True)

    
    st.markdown("""
        #### ❓ Fragestellungen von Datenanalyse und Machine Learning
    """
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, spacer, col2, spacer, col3, spacer, col4 = st.columns([1, 0.2, 1, 0.2, 1, 0.2, 1])
   
    
    # - Fragestellung 1 -
    with col1:
        st.markdown(
            """
            <h5 style="text-align: center;">
               🌍 Klima-Analyse
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.html("<div style='height: 10px;'></div>")   
        
        st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                Gibt es einen Zusammenhang zwischen Klima und thermischem Befinden?
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        #st.markdown("<br><br><br>", unsafe_allow_html=True)
    
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
        #st.markdown("<br>", unsafe_allow_html=True)
        st.html("<div style='height: 10px;'></div>")   

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

    with col4:

 
        st.markdown("""
            #### 🎯Machine Learning
        """
        )
        
        #st.markdown("<br>", unsafe_allow_html=True)
        st.html("<div style='height: 27px;'></div>")    

        st.markdown(
            """
            <div style="
                background-color: #f7f7f7;
                padding: 15px;
                border-radius: 8px;
            ">
                - Lässt sich thermisches Empfinden mit Hilfe von Machine Learning bestimmen?
                <br>
                - Gibt es andere Kenngrößen die das Wohlbefinden beeinflussen die sich vorhersagen lassen?
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------
# TAB 5 – Tools und Prozess
# -------------------------
with tab3:
    st.subheader("5️⃣ Data Science & Analytics Tools")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tools
    st.markdown("""
        #### 🛠️ Tools
    """
    )

    st.write("Moderne Tools für Datenanalyse, Machine Learning und interaktive Dashboards")

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
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">Explorative Datenanalyse (EDA)</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">PostgreSQL Neon</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # COLUMN 2
    with col2:
        st.markdown('<div class="tech-card">Power BI</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">Jupyter Notebook</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">NumPy</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div  class="tech-card">GitHub</div>', unsafe_allow_html=True)

    # COLUMN 3
    with col3:
        st.markdown('<div class="tech-card">Pandas</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">Machine Learning</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tech-card">Streamlit</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)

#     # Prozess
#     st.markdown("""
#         #### 🔁 Prozess des Projekts
#     """
#     )

#     st.markdown("<br>", unsafe_allow_html=True)

#     col1, col2, col3, col4, col5 = st.columns([1, 0.2, 1, 0.2, 1])
#     col6, col7, col8, col9, col10 = st.columns([1, 0.2, 1, 0.2, 1])
#     col11, col12, col13, col14, col15 = st.columns([1, 0.2, 1, 0.2, 1])

#     with col1:
#         st.markdown('<div  class="tech-card">Themenfindung und Datenrecherche</div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col2:
#         st.markdown(
#                     "<span style='font-size:30px;'>➡️</span>",
#                     unsafe_allow_html=True
#                 )
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col3:
#         st.markdown('<div  class="tech-card">Datenaufbereitung</div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col4:
#         st.markdown(
#                     "<span style='font-size:30px;'>➡️</span>",
#                     unsafe_allow_html=True
#                 )
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)


#     with col5:
#         st.markdown('<div  class="tech-card">Datenbank</div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col10:
# #         st.markdown(
# # with tab3:

#         st.markdown(
#                 """
#                 <div style="text-align: center;">
#                     <span style='font-size:30px;'>⬇️</span>
#                 """,
#                 unsafe_allow_html=True
#                 )
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col15:
#         st.markdown('<div  class="tech-card">Datenanalyse und Visualisierungen</div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col14:
#         st.markdown(
#                     "<span style='font-size:30px;'>⬅️</span>",
#                     unsafe_allow_html=True
#                 )
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col13:
#         st.markdown('<div  class="tech-card">Machine Learning </div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col12:
#         st.markdown(
#                     "<span style='font-size:30px;'>⬅️</span>",
#                     unsafe_allow_html=True
#                 )
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col11:
#         st.markdown('<div  class="tech-card">Streamlit-App</div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)
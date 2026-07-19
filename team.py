import streamlit as st
import base64
import os


st.set_page_config(page_title="Team", layout="wide",initial_sidebar_state="expanded")

st.title("Technologien & Werkzeuge unseres Projekts")
# -------------------------
#       TABS
# -------------------------
tab1, tab2 = st.tabs(["👥 Über uns", "🧰 Tools"])

# -------------------------
#       TAB 1 – ÜBER UNS
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



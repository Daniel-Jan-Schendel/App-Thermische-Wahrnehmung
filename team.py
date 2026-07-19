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


# -------------------------
#       TAB 2 – TOOLS
# -------------------------



    # st.write("""
    # - **Python**  
    # - **EDA (Explorative Datenanalyse)**  
    # - **Postgre SQL Neon** 
    # - **Power BI**  
    # - **Jupyter**
    # - **Numpy**
    # - **Pandas**
    # - **Machine Learning**
    # - **Streamlit**
    # """)


    # st.markdown("## 🛠️ Technologien")

    # # --- FLAT MINIMALIST STYLE ---
    # style = """
    # <style>
    # .tool-icon {
    #     width: 42px;
    #     height: 42px;
    #     object-fit: contain;
    #     margin-bottom: 6px;
    # }
    # .tool-title {
    #     font-size: 1.1em;
    #     font-weight: 700;
    #     color: #0A2540;
    #     margin-bottom: 0px;
    # }
    # .tool-desc {
    #     font-size: 0.9em;
    #     color: #444444;
    #     opacity: 0.85;
    #     margin-bottom: 20px;
    # }
    # </style>
    # """
    # st.markdown(style, unsafe_allow_html=True)

    # # --- GRID 3 COLUMNS ---
    # col1, col2, col3 = st.columns(3)

    #     # COLUMN 1
    # with col1:
    #     st.markdown('<img src="tools/python.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">Python</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Python Programming</div>', unsafe_allow_html=True)

    #     st.markdown('<img src="tools/eda.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">EDA</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Explorative Datenanalyse</div>', unsafe_allow_html=True)

    #     st.markdown('<img src="tools/neon.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">PostgreSQL Neon</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Cloud Database</div>', unsafe_allow_html=True)

    # # COLUMN 2
    # with col2:
    #     st.markdown('<img src="tools/powerbi.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">Power BI</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Business Intelligence</div>', unsafe_allow_html=True)

    #     st.markdown('<img src="tools/jupyter.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">Jupyter</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Interactive Notebooks</div>', unsafe_allow_html=True)

    #     st.markdown('<img src="tools/numpy.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">NumPy</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Numerical Computing</div>', unsafe_allow_html=True)

    # # COLUMN 3
    # with col3:
    #     st.markdown('<img src="tools/pandas.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">Pandas</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Data Manipulation</div>', unsafe_allow_html=True)

    #     st.markdown('<img src="tools/ml.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">Machine Learning</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Predictive Models</div>', unsafe_allow_html=True)

    #     st.markdown('<img src="tools/streamlit.png" class="tool-icon">', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-title">Streamlit</div>', unsafe_allow_html=True)
    #     st.markdown('<div class="tool-desc">Interactive Web Apps</div>', unsafe_allow_html=True)


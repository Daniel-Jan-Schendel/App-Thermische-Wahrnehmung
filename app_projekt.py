import warnings 
import streamlit as st
from styles import apply_styles
import base64

# -- Set page config
apptitle = 'ASHRAE Data Analysis'
#st.sidebar.image("logo.png", width=500)


st.set_page_config(page_title="ASHRAE", layout="wide", initial_sidebar_state="expanded")

#st.title("ASHRAE")

#apply_styles()


pg = st.navigation(
    [
        st.Page("welcome.py", title="Startseite", icon=":material/home:"),
        #st.Page("team.py", title="Team & Tools", icon=":material/group:"),
        st.Page("introduction.py", title="Einführung", icon=":material/info:"),
        st.Page("datenbereinigung.py", title="Datenbereinigung", icon=":material/menu_book:"),
        st.Page("database.py", title="Datenbank", icon=":material/dashboard:"),
        st.Page("analytics.py", title="Globale Datenanalyse", icon=":material/analytics:"),
        st.Page("analytics_clima.py", title="Klima-Analyse", icon=":material/analytics:"),
        st.Page("analytics_dianela.py", title="Cooling Type-Analyse", icon=":material/analytics:"),
        st.Page("thermal_comfort_analysis.py", title="Thermischer Komfort-Analyse", icon=":material/analytics:"),
        #st.Page("machine_learning.py", title="Machine Learning", icon=":material/smart_toy:"),
        #st.Page("ML_test_iris.py", title="Machine Learning Test", icon=":material/smart_toy:"),
        #st.Page("ML_test_ASHRAE.py", title="Machine Learning Test 2", icon=":material/smart_toy:"),
        st.Page("ml_ashrae.py", title="Machine Learning Modelling", icon=":material/smart_toy:"),
        #st.Page("./ML/ml_streamlit.py", title="Machine Learning Modelling - Klassifikation", icon=":material/smart_toy:"),
        #st.Page("./ML/ml_streamlit_cooling_type.py", title="Machine Learning - Klassifikation", icon=":material/smart_toy:"),
        #st.Page("./ML/ml_streamlit_clo.py", title="Machine Learning - Regression", icon=":material/smart_toy:"),
        st.Page("zusammenfassung.py", title="Zusammenfassung", icon=":material/menu_book:"),
        st.Page("dashboard.py", title="Dashboard", icon=":material/menu_book:")
    ]
)

pg.run()
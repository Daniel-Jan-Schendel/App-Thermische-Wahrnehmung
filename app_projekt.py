import warnings 
import streamlit as st
from styles import apply_styles
import base64

# -- Set page config
apptitle = 'ASHRAE Data Analysis'
#st.sidebar.image("logo.png", width=500)


st.set_page_config(page_title="ASHRAE", layout="wide", initial_sidebar_state="expanded")


pg = st.navigation(
    [
        st.Page("welcome.py", title="Startseite", icon=":material/home:"),
        st.Page("introduction.py", title="Einführung", icon=":material/info:"),
        st.Page("datenbereinigung.py", title="Datenbereinigung", icon=":material/menu_book:"),
        st.Page("database.py", title="Datenbank", icon=":material/dashboard:"),
        st.Page("analytics_clima.py", title="Klima-Analyse", icon=":material/analytics:"),
        st.Page("analytics_dianela.py", title="Belüftungsart-Analyse", icon=":material/analytics:"),
        st.Page("thermal_comfort_analysis.py", title="Physikalische Parameter-Analyse", icon=":material/analytics:"),
        st.Page("ML/ml_ashrae.py", title="Machine Learning Modelling", icon=":material/smart_toy:"),
        st.Page("dashboard_neu.py", title="Dashboard", icon=":material/analytics:"),
        st.Page("zusammenfassung.py", title="Zusammenfassung", icon=":material/menu_book:")
    ]
)

pg.run()
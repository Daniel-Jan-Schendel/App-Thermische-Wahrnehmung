import warnings 
import streamlit as st
from styles import apply_styles
import base64

# ---------------------------------------------------------
# Titel der App
# --------------------------------------------------------- 
apptitle = 'ASHRAE Data Analysis'

# ---------------------------------------------------------
# Seitenkonfigurationen
# --------------------------------------------------------- 
st.set_page_config(page_title="ASHRAE", layout="wide", initial_sidebar_state="expanded")

# ---------------------------------------------------------
# Seitennavigation
# --------------------------------------------------------- 
pg = st.navigation(
    [
        st.Page("Startseite.py", title="Startseite", icon=":material/home:"),
        st.Page("Einführung/introduction_app.py", title="Einführung", icon=":material/info:"),
        st.Page("Datenbereinigung/datenbereinigung_app.py", title="Datenbereinigung", icon=":material/menu_book:"),
        st.Page("database.py", title="Datenbank", icon=":material/dashboard:"),
        st.Page("analytics_clima:_app.py", title="Klima-Analyse", icon=":material/analytics:"),
        st.Page("analytics_dianela.py", title="Belüftungsart-Analyse", icon=":material/analytics:"),
        st.Page("thermal_comfort_analysis.py", title="Physikalische Parameter-Analyse", icon=":material/analytics:"),
        st.Page("ml_ashrae.py", title="Machine Learning Modelling", icon=":material/smart_toy:"),
        st.Page("Dashboard/dashboard_neu.py", title="Dashboard", icon=":material/analytics:"),
        st.Page("Zusammenfassung und Fazit/zusammenfassung_app.py", title="Zusammenfassung", icon=":material/menu_book:")
    ]
)

pg.run()
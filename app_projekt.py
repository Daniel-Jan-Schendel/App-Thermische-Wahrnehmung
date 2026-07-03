import warnings 
import streamlit as st
from styles import apply_styles
import base64

st.set_page_config(page_title="ASHRAE", layout="wide", initial_sidebar_state="expanded")

apply_styles()

#st.sidebar.image("logo.png", width=500)

pg = st.navigation(
    [
        st.Page("welcome.py", title="Startsite", icon=":material/home:"),
        st.Page("introduction.py", title="Einführung", icon=":material/info:"),
        st.Page("database.py", title="Datenbank", icon=":material/dashboard:"),
        st.Page("datenbereinigung.py", title="Datenbereinigung", icon=":material/menu_book:"),
        st.Page("analytics.py", title="Globale Datenanalyse", icon=":material/analytics:"),
        st.Page("machine_learning.py", title="Machine Learning", icon=":material/smart_toy:"),
        st.Page("ML_test_iris.py", title="Machine Learning Test", icon=":material/smart_toy:"),
        st.Page("ML_test_ASHRAE.py", title="Machine Learning Test 2", icon=":material/smart_toy:"),
        st.Page("ml_ashrae.py", title="Machine Learning Modelling", icon=":material/smart_toy:"),
        st.Page("dashboard.py", title="Dashboard", icon=":material/menu_book:")
    ]
)

pg.run()
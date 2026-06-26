import warnings 
import streamlit as st
from styles import apply_styles
import base64

st.set_page_config(page_title="ASHRAE", layout="wide", initial_sidebar_state="expanded")

apply_styles()

#st.sidebar.image("logo.png", width=500)

pg = st.navigation(
    [
        st.Page("welcome.py", title="Willkommen", icon=":material/groups:"),
        st.Page("introduction.py", title="Main Menu", icon=":material/home:"),
        st.Page("dashboard.py", title="Dashboard", icon=":material/menu_book:"),
        st.Page("database.py", title="Database", icon=":material/dashboard:"),
        st.Page("datenbereinigung.py", title="Datenbereinigung", icon=":material/menu_book:"),
        st.Page("analytics.py", title="Analytics", icon=":material/analytics:"),
        st.Page("machine_learning.py", title="Machine Learning", icon=":material/smart_toy:")
    ]
)

pg.run()
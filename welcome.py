import streamlit as st

st.set_page_config(page_title="Welcome", layout="wide",initial_sidebar_state="expanded")
import streamlit as st

st.title("SmartBuilding-Analytics")
st.header("Datenarchitektur zur Optimierung klimatisierter Gebäudeinfrastrukturen")
st.image("introduction_ashrae.png", width=700)


st.header("👥 Über uns")
#st.write("""
# We are a multidisciplinary group with backgrounds in:
# **• Mirtha – Physicist**  
# **• Daniel – Mechanical Engineer**  
# **• Sabrina – Expert in Psychology / Art / Tourism**  
# **• Dianela – Computer Engineer**
# Our diverse academic profiles allow us to approach thermal comfort analysis 
# from scientific, technical, and human-centered perspectives.
# """)'

# --- Teammitglieder ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader("Sabrina")
    st.image("psychology.png", width=250)
    st.write("**Psychologe**")
    st.write("Data Analyst")

with col2:
    st.subheader("Dianela")
    st.image("informatic_engineering.png", width=250)
    st.write("**Informatikingenieurin**")
    st.write("Data Analyst")

with col3:
    st.subheader("Mirtha")
    st.image("physicist.png", width=250)
    st.write("**Physikerin**")
    st.write("Data Scientist")

with col4:
    st.subheader("Daniel")
    st.image("civil_engineering.png", width=250)
    st.write("**Bauingenieur**")
    st.write("Data Scientist")


# st.subheader("📫 Contact")
# st.write("""
# For questions or collaboration inquiries, please reach out through the project repository.
# """)


st.sidebar.subheader("Tools")

st.header("🧰 Data Science & Analytics Werkzeuge")

st.write("""
- Excel 
- **Python**  
- SQL  
- **EDA (Explorative Datenanalyse)**  
- **Power BI**  
- AWS Cloud 
- Scrum
- **Machine Learning**
""")


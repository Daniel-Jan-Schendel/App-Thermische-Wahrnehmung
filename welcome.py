import streamlit as st

st.set_page_config(page_title="Willkommen", layout="wide",initial_sidebar_state="expanded")
import streamlit as st

st.title("SmartBuilding-Analytics")
st.header("Datenarchitektur zur Optimierung klimatisierter Gebäudeinfrastrukturen")
#st.image("introduction_ashrae.png", width=700)

col1, col2 = st.columns([1, 1])

with col1:
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
        """,
        unsafe_allow_html=True
    )

with col2:
    st.image("introduction_ashrae.png", width=900)


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
st.text("test")

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
- Jupyter
- Numpy
- Streamlit
- Pandas
""")


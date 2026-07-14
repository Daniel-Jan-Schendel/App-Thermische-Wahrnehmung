import streamlit as st
#
st.set_page_config(page_title="Welcome", layout="wide",initial_sidebar_state="expanded")

st.title("SmartBuilding-Analytics")
st.header("Datenarchitektur zur Optimierung klimatisierter Gebäudeinfrastrukturen")
#st.image("introduction_ashrae.png", width=700)


# -------------------------
#       TABS
# -------------------------
tab1, tab2, tab3 = st.tabs(["📘 Projekt", "👥 Über uns", "🧰 Tools"])

# -------------------------
#       TAB 1 – PROJEKT
# -------------------------
with tab1:
    st.header("📘 Projekt")

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
        st.caption("Hinweis: Dieses Bild wurde mit KI generiert.")


# -------------------------
#       TAB 2 – ÜBER UNS
# -------------------------
with tab2:
    st.header("👥 Über uns")
    st.text(" Wir sind vier Personen mit unterschliedichen berufliche Hintergrund. Unsere Grupe bestehlt aus zwei Dataanalyst und zwei Datascientist.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("Sabrina")
        st.image("psychology.png", width=250)
        st.write("**Psychologe?**")
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
        st.write("**Experimental Semiconductor**")
        st.write("Data Scientist")

    with col4:
        st.subheader("Daniel")
        st.image("civil_engineering.png", width=250)
        st.write("**Bauingenieur**")
        st.write("Data Scientist")


# -------------------------
#       TAB 3 – TOOLS
# -------------------------
with tab3:
    st.header("🧰 Data Science & Analytics Tools")

    st.write("""
    - **Python**  
    - **EDA (Explorative Datenanalyse)**  
    - **Postgre SQL Neon** 
    - **Power BI**  
    - **Jupyter**
    - **Numpy**
    - **Pandas**
    - **Machine Learning**
    - **Streamlit**
    """)
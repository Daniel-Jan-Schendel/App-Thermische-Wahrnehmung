import streamlit as st
import base64
import os


st.set_page_config(page_title="Welcome", layout="wide",initial_sidebar_state="expanded")


def load_image_as_base64(path):
    if not os.path.exists(path):
        st.error(f"❌ Imagen no encontrada: {path}")
        return None
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


image_path = "introduction_ashrae.png"  
image_base64 = load_image_as_base64(image_path)

if image_base64:
    ext = image_path.split(".")[-1].lower()
    mime = "image/png" if ext == "png" else "image/jpeg"

    hero_html = f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, #0A2540 0%, #1E88E5 100%);
        padding: 20px 40px;
        border-radius: 25px;
        color: white;
        min-height: 800px;
    ">
    <!-- Texto a la izquierda -->
        <div style="flex: 1.2; padding-right: 10px;">
        <p style="font-size: 1.1em; opacity: 0.85; margin-bottom: 1px;">
            Abschlussprojekt in Data Science & Data Analytics</p>

    <h1 style="font-size: 3em; font-weight: 500; margin-bottom: 10px;">
        Thermisches Befinden in Innenräumen:
    </h1>

    <h1 style="font-size: 3em; font-weight: 500; margin-bottom: 10px;">
        Datenanalyse und Machine Learning Modellierung
    </h1>

    <p style="font-size: 1.15em; margin-top: 25px;">
        <strong>Team:</strong><br>
        Sabrina · Dianela · Mirtha · Daniel
    </p>
    </div>

    <!-- Imagen a la derecha (tamaño fijo) -->
    <div style="flex: 1; text-align: right;">
            <img src="data:{mime};base64,{image_base64}"
            style="
                width: 950px;              /* TAMAÑO FIJO */
                height: auto;
                border-radius: 20px;
                box-shadow: 0px 6px 20px rgba(0,0,0,0.45);
            " />
        </div>
    </div>
        """
    st.markdown(hero_html, unsafe_allow_html=True)


# with st.expander("👥 Team & Tools"):
#     st.subheader("Team Members")
#     st.write("""
#     - Sabrina  
#     - Dianela  
#     - Mirtha  
#     - Daniel  
#     """)

#     st.subheader("Tools Used")
#     st.write("""
#     - Python  
#     - Streamlit  
#     - Pandas  
#     - Scikit‑Learn  
#     - Neon PostgreSQL  
#     - ASHRAE Global Thermal Comfort Database II  
#     """)

  


# 'st.title("SmartBuilding-Analytics")
# st.header("Datenarchitektur zur Optimierung klimatisierter Gebäudeinfrastrukturen")
# #st.image("introduction_ashrae.png", width=700)


# # -------------------------
# #       TABS
# # -------------------------
# tab1, tab2, tab3 = st.tabs(["📘 Projekt", "👥 Über uns", "🧰 Tools"])

# # -------------------------
# #       TAB 1 – PROJEKT
# # -------------------------
# with tab1:
#     st.header("📘 Projekt")

#     col1, col2 = st.columns([1, 1])

#     with col1:
#         st.markdown(
#             """
#             <div style="
#                 background-color: #f7f7f7;
#                 padding: 15px;
#                 border-radius: 12px;
#                 border-left: 5px solid #4B9CD3;
#                 font-size: 20px;
#                 line-height: 1.5;
#                 margin-top: 20px;
#             ">
#                 Dieses Projekt analysiert Gebäudedaten, um Energieeffizienz,
#                 Komfort und Nachhaltigkeit in klimatisierten Infrastrukturen zu verbessern.
#                 Hier findest du Dashboards, Datenpipelines und Machine-Learning-Modelle,
#                 die unser Smart-Building-Konzept unterstützen.
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     with col2:
#         st.image("introduction_ashrae.png", width=900)
#         st.caption("Hinweis: Dieses Bild wurde mit KI generiert.")


# # -------------------------
# #       TAB 2 – ÜBER UNS
# # -------------------------
# with tab2:
#     st.header("👥 Über uns")
#     st.text(" Wir sind vier Personen mit unterschliedichen berufliche Hintergrund. Unsere Grupe bestehlt aus zwei Dataanalyst und zwei Datascientist.")

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.subheader("Sabrina")
#         st.image("psychology.png", width=250)
#         st.write("**Psychologe?**")
#         st.write("Data Analyst")

#     with col2:
#         st.subheader("Dianela")
#         st.image("informatic_engineering.png", width=250)
#         st.write("**Informatikingenieurin**")
#         st.write("Data Analyst")

#     with col3:
#         st.subheader("Mirtha")
#         st.image("physicist.png", width=250)
#         st.write("**Physikerin**")
#         st.write("Data Scientist")

#     with col4:
#         st.subheader("Daniel")
#         st.image("civil_engineering.png", width=250)
#         st.write("**Bauingenieur**")
#         st.write("Data Scientist")


# # -------------------------
# #       TAB 3 – TOOLS
# # -------------------------
# with tab3:
#     st.header("🧰 Data Science & Analytics Tools")

#     st.write("""
#     - **Python**  
#     - **EDA (Explorative Datenanalyse)**  
#     - **Postgre SQL Neon** 
#     - **Power BI**  
#     - **Jupyter**
#     - **Numpy**
#     - **Pandas**
#     - **Machine Learning**
#     - **Streamlit**
#     """)'
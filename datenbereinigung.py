import streamlit as st
import pandas as pd
import io
from streamlit_echarts import st_echarts
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Datenbereinigung - ASHRAE", layout="wide",initial_sidebar_state="expanded")

st.header("🔍 Inspektion und Bereinigung des Datensatzes")

# Datensätze laden

metadata = pd.read_csv("db_metadata.csv")
measurements = pd.read_csv("db_measurements_v210.csv")
df = measurements.merge(metadata, on="building_id", how="inner")

df_bereinigt = pd.read_csv("db_bereinigt_final.csv")
df = pd.read_csv("db_bereinigt.csv")

tab1, tab2, tab3 = st.tabs([
    "ℹ️ Datensatz",
    "⚠️ Prozess und Herausforderungen",
    "🧹 Bereinigter Datensatz"
#    "🔢 Standardisierung von Kategorien"
])

###############################################################################################################################################
###############################################################################################################################################

with tab1:   
    # - Datensatz Aufbau -
    st.subheader("ℹ️ Datensatz")

    st.write("Der Datensatz ist in **zwei Haupttabellen** gegliedert: ")

    col1, spacer, col2 = st.columns([2, 0.2, 2])

    with col1:
        st.info("""
        **`metadata` Tabelle**

        - Enthält allgemeine **Gebäude- und Studieninformationen**
        - Bereitgestellt als Standard-CSV file
        """)
        

    with col2:
        st.info("""
        **`measurements` Tabelle**

        - Enthält die **Messdaten** (z.B.)
            - Fragebogenantworten → zentral für Untersuchung der thermischen Bewertung
            - Physikalische Messdaten

        - Bereitstellung:
            - Als komprimierte CSV-Datei (.csv.gz) in UTF-8-Kodierung
        """)
        

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- Einteilung der Variablen ---
    st.subheader("📋 Übersicht über Variablen")

    data = {
        "Gruppe": [
            "🏢 Gebäude- und Studiendaten",
            "👤 Personenbezogene Variablen",
            "🌡️ Umgebungsvariablen",
            "🧍 Subjektive Komfortbewertungen",
            "📊 Komfort-Indizes"
        ],
        "Beschreibung": [
            "Informationen zum Messkontext",
            "Eigenschaften der Personen",
            "Physikalische Bedingungen",
            "Komfortangaben der Personen",
            "Berechnete thermische Kennwerte"
        ],
        "Variablen (Bsp.)": [
            "building_type, cooling_type, country, climate, season",
            "age, gender, met, clo",
            "air_temperature, humidity, air_velocity",
            "thermal_sensation, thermal_comfort, thermal_preference, thermal_acceptability",
            "PMV, PPD, SET"
        ]
    }

    df_groups = pd.DataFrame(data)

    st.dataframe(
    df_groups,
    use_container_width=True,
    hide_index=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    with st.expander("ℹ️ Hinweis zu den Variablen"):
        st.markdown("""
        Der Datensatz enthält sehr viele Parameter ➝ nicht alle wurden für die Analyse und das Machine Learning genutzt
        """
        )

###############################################################################################################################################
###############################################################################################################################################


with tab2:

    st.subheader("🧹 Prozess und Herausforderungen der Datenbereinigung")

    st.markdown("<br>", unsafe_allow_html=True)


    # 1. Zusammenführen der Datensätze
    st.info("""
    1. **Zusammenführen** der beiden Datensätze für Analysen in Python
    """) 
    col1, col2, col3 = st.columns([1.5, 0.2, 2])
    
    with col1:
        st.markdown("⚠️ **Herausforderung**: ")

        st.markdown("""
        - Sehr großer Datensatz mit **vielen erhobenen Werten**
        """
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown("🛠️ **Umgang mit Herausforderung:**")
        st.markdown(
            """
            - **Überblick verschaffen**

                - Welche Werte sind für uns relevant? 
                - Welche Fragestellungen wollen wir untersuchen?
            """
        )


        st.markdown("<br>", unsafe_allow_html=True)

    # 2. Bereinigung Datentypen
    st.info("""
    2. **Bereinigung von Datentypen** 
    """)  


    # 3. Fehlende Werte
    st.info("""
    3. 🔍 Übersichten zur Verteilung des Datensatzes und **Untersuchung der fehlenden Werte** 
    """)  

    col4, col5, col6 = st.columns([1.5, 0.2, 2])
    
    with col4:
        st.markdown("⚠️ **Herausforderung**: ")

        st.markdown("""
        - Sehr viele **fehlende Werte**
        """
        )

        with st.expander("Weitere Informationen"):
            st.markdown("""
            Spalten variieren stark bezüglich Anzahl der fehlenden Werte (z.B.):
                        
            - age ➝ 55% (60039 Einträge)
            - thermal_sensation ➝ 3% (2862 Einträge)
            - thermal_comfort ➝ 65% (70998 Einträge)
        """
        )
                        
    with col5:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    with col6:
        st.markdown("🛠️ **Umgang mit Herausforderung:**")
        st.markdown(
        """
        - Untersuchung der fehlenden Werte auf Muster
        - **Gemeinsame Überlegungen, welche Voraussetzungen wir benötigen** für Datenanalyse und Machine Learning
        

        - **Entscheidung:**

            - kategoriale Spalten: mit "Unknown" auffüllen
            - numerische Spalten: fehlende Werte nicht bearbeiten, um Analysen nicht zu verzerren
            - für Machine Learning: Entfernen der Zeilen mit fehlenden Werten in relevanten Variablen
        """
        )

        st.markdown("<br>", unsafe_allow_html=True)


    # 4. Bearbeitung von Spalten
    st.info("""
    4. Bearbeitung der Spalten: 
    - **Umbenennung von Spalten** für besseres Verständnis
    - **Entfernen** von nicht benötigten Spalten 
    - Erstellen einer neuen **Spalte mit vier Hauptklimazonen** 
    """)  

    col7, col8, col9 = st.columns([1.5, 0.2, 2])
    
    with col7:
        st.markdown("⚠️ **Herausforderung**: ")
        st.markdown("""
        - 31 verschiedene **Klimata** ➜ unübersichtlich für Analysen
        """
        )
                        
    with col8:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    with col9:
        st.markdown("🛠️ **Umgang mit Herausforderung:**")
        st.markdown(
        """
        - Neue Spalte mit **4 Hauptklimazonen**:
        
            - Erstellen eines Mapping, um Klimata den Hauptklimazonen zuzuweisen
            - Hierdurch bei Analyse auch eine generellere Betrachtung möglich
        """
        )
        st.markdown("<br>", unsafe_allow_html=True)

    # 5. Standardisierung
    st.info("""
    5. **Standardisierung**: Runden der Werte von thermal_comfort und thermal_sensation für klare Kategorien 
    
    ➝ wichtig für Machine Learning 
    """)  

    col10, col11, col12 = st.columns([1.5, 0.2, 2])
    
    with col10:
        st.markdown("⚠️ **Herausforderung**: ")

        st.markdown("""
        - Werte in den Spalten **thermal_comfort** und **thermal_sensation** enthalten Dezimalwerte
        """
        )
        with st.expander("Weitere Informationen"):
            st.markdown("""
            **Worin liegt die Schwierigkeit?**
                        
            - ASHRAE Global Thermal Comfort Database II sammelt Daten aus vielen verschiedenen Studien, Ländern, Klimazonen und Gebäudetypen
            - Dadurch entstehen **unterschiedliche Werte, Skalen und Formate** für dieselben Komfortparameter
            - Zudem werden in manchen Studien **Aggregationen** vorgenommen und in anderen nicht
        """)
                      
    with col11:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    with col12:
        st.markdown("🛠️ **Umgang mit Herausforderung:**")
        st.markdown(
        """
        - **Standardisierung** durch Runden der Dezimalwerte ➜ Für bessere Vergleichbarkeit und Auswertung der Daten
        """)

        with st.expander("Weitere Informationen"):
            st.markdown("""
            Durch Standardisierung werden alle Werte auf die **ASHRAE‑Skala** (z.B. 1–6) abgebildet
            """
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("🔢 **Runden der thermischen Komfortparameter:**")

            st.markdown(
            """
            **1. Thermischer Komfort**
            """)
            
            col1, spacer, col2 = st.columns([0.5, 0.1, 0.5])

            # ---------------------------------------------------------
            # 🟦 Spalte 1: Originalwerte
            # ---------------------------------------------------------
            with col1:
                
                # Grafik für thermal_comfort
                fig, ax = plt.subplots(figsize=(6,4))
                ax.hist(df["thermal_comfort"].dropna(), bins=20, color="#4C72B0", edgecolor="white")
                ax.set_title("Originale Thermal Comfort Werte")
                ax.set_xlabel("Wert")
                ax.set_ylabel("Häufigkeit")
                st.pyplot(fig)

                st.markdown("<br>", unsafe_allow_html=True)

            # ---------------------------------------------------------
            # 🟩 Spalte 2: Standardisierte / gerundete Werte
            # ---------------------------------------------------------
            with col2:
                # Grafik für thermal_comfort
                fig, ax = plt.subplots(figsize=(6,4))
                ax.hist(df_bereinigt["thermal_comfort"].dropna(), bins=20, color="#4C72B0", edgecolor="white")
                ax.set_title("Standardisierte Thermal Comfort Werte")
                ax.set_xlabel("Wert")
                ax.set_ylabel("Häufigkeit")
                st.pyplot(fig)

                st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
            """
            **2. Thermisches Empfinden**
            """)

            col3, spacer, col4 = st.columns([0.5, 0.1, 0.5])

            with col3:
                # Grafik für thermal_sensation
                fig, ax = plt.subplots(figsize=(6,4))
                ax.hist(df["thermal_sensation"].dropna(), bins=20, color="#4C72B0", edgecolor="white")
                ax.set_title("Originale Thermal Sensation Werte")
                ax.set_xlabel("Wert")
                ax.set_ylabel("Häufigkeit")
                st.pyplot(fig)

            

            with col4:
                # Grafik für thermal_sensation
                fig, ax = plt.subplots(figsize=(6,4))
                ax.hist(df_bereinigt["thermal_sensation"].dropna(), bins=20, color="#4C72B0", edgecolor="white")
                ax.set_title("Standardisierte Thermal Sensation Werte")
                ax.set_xlabel("Wert")
                ax.set_ylabel("Häufigkeit")
                st.pyplot(fig)



        st.markdown("<br><br><br>", unsafe_allow_html=True)

   
with tab3:
    col1, col2, col3, spacer = st.columns([1,0.2, 1, 0.3])

    # Übersicht Dimensionen vor und nach Bereinigung
    with col1:
        # Dimensionen vor der Bereinigung 
        st.write("### 📏 Dimensionen vor Bereinigung")
        st.write(f"**Zeilen:** {df.shape[0]}")
        st.write(f"**Spalten:** {df.shape[1]}")

    with col2:
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    with col3:   
        # Dimensionen nach der Bereinigung 
        st.write("### 📏 Dimensionen nach Bereinigung")
        st.write(f"**Zeilen:** {df_bereinigt.shape[0]}")
        st.write(f"**Spalten:** {df_bereinigt.shape[1]}")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Tabelle Datensatz nach Bereinigung
    st.subheader("🧾 Datensatz nach der Bereinigung")

    tab1, tab2 = st.tabs([
        "Übersicht Datensatz",
        "Übersicht fehlende Werte"
    ])

    with tab1:
        st.dataframe(df_bereinigt)

    #with tab2:
        # Dataframe fehlende Werte erstellen
        #st.dataframe(df_nans)
  


###############################################################################################################################################
###############################################################################################################################################

# with tab3:

#     st.subheader("Worin liegt die Schwierigkeit?")

#     st.markdown(
#         """
#         - ASHRAE Global Thermal Comfort Database II sammelt Daten aus vielen verschiedenen Studien, Ländern, Klimazonen und Gebäudetypen
#         - Dadurch entstehen **unterschiedliche Werte, Skalen und Formate** für dieselben Komfortparameter
#         - Zudem werden in manchen Studien **Aggregationen** vorgenommen und in anderen nicht
        
#         ➜ Für bessere Vergleichbarkeit und Auswertung der Daten: **Standardisierung**

#         ➜ Durch Standardisierung werden alle Werte auf die **ASHRAE‑Skala** (z.B. 1–6) abgebildet
#     """
#     )
    
#     st.markdown("<br>", unsafe_allow_html=True)

#     st.subheader("Standardisierte thermische Komfortparameter (TSV, TP, TC)")

#     image = Image.open("thermal_parameters_code_numbers.png")

#     # Bild anzeigen mit definierter Breite
#     st.image(image, caption="Thermische Komfortparameter (TSV, TP, TC) – Standardisierte Codes", width=700)

#     st.markdown("<br>", unsafe_allow_html=True)

#     # ---------------------------------------------------------
#     # 📍 Layout: Zwei Spalten
#     # ---------------------------------------------------------
#     st.subheader("🔢 Runden der thermischen Komfortparameter")
    
#     st.info(
#             """
#             - Thermischer Komfort
#         """
#         )
    
#     col1, spacer, col2 = st.columns([0.5, 0.1, 0.5])

#     # ---------------------------------------------------------
#     # 🟦 Spalte 1: Originalwerte
#     # ---------------------------------------------------------
#     with col1:
        
#         # Grafik für thermal_comfort
#         fig, ax = plt.subplots(figsize=(6,4))
#         ax.hist(df["thermal_comfort"].dropna(), bins=20, color="#4C72B0", edgecolor="white")
#         ax.set_title("Originale Thermal Comfort Werte")
#         ax.set_xlabel("Wert")
#         ax.set_ylabel("Häufigkeit")
#         st.pyplot(fig)

#         st.markdown("<br>", unsafe_allow_html=True)

#     # ---------------------------------------------------------
#     # 🟩 Spalte 2: Standardisierte / gerundete Werte
#     # ---------------------------------------------------------
#     with col2:
#         # Grafik für thermal_comfort
#         fig, ax = plt.subplots(figsize=(6,4))
#         ax.hist(df_bereinigt["thermal_comfort"].dropna(), bins=20, color="#4C72B0", edgecolor="white")
#         ax.set_title("Standardisierte Thermal Comfort Werte")
#         ax.set_xlabel("Wert")
#         ax.set_ylabel("Häufigkeit")
#         st.pyplot(fig)

#         st.markdown("<br>", unsafe_allow_html=True)

#     st.info(
#         """
#         - Thermisches Empfinden
#     """
#     )

#     col3, spacer, col4 = st.columns([0.5, 0.1, 0.5])

#     with col3:
#         # Grafik für thermal_sensation
#         fig, ax = plt.subplots(figsize=(6,4))
#         ax.hist(df["thermal_sensation"].dropna(), bins=20, color="#4C72B0", edgecolor="white")
#         ax.set_title("Originale Thermal Sensation Werte")
#         ax.set_xlabel("Wert")
#         ax.set_ylabel("Häufigkeit")
#         st.pyplot(fig)

    

#     with col4:
#         # Grafik für thermal_sensation
#         fig, ax = plt.subplots(figsize=(6,4))
#         ax.hist(df_bereinigt["thermal_sensation"].dropna(), bins=20, color="#4C72B0", edgecolor="white")
#         ax.set_title("Standardisierte Thermal Sensation Werte")
#         ax.set_xlabel("Wert")
#         ax.set_ylabel("Häufigkeit")
#         st.pyplot(fig)


    

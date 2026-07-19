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

tab1, tab2, tab3, tab4 = st.tabs([
    "ℹ️ Datensatz",
    "🧹 Prozess Datenbereinigung",
    "⚠️ Herausforderungen bei Datenbereinigung",
    "🔢 Standardisierung von Kategorien"
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

        - Enthält allgemeine Gebäude- und Studieninformationen
        - Bereitgestellt als Standard-**CSV file**
        """)
        

    with col2:
        st.info("""
        **`measurements` Tabelle**

        - Enthält die Messdaten (z.B.)
            - Fragebogenantworten → zentral für Untersuchung der thermischen Bewertung
            - Physikalische Messdaten

        - Bereitstellung:
            - Als **komprimierte CSV-Datei (.csv.gz)** in UTF-8-Kodierung
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


###############################################################################################################################################
###############################################################################################################################################


with tab2:

    st.subheader("🧹 Prozess der Datenbereinigung")

    st.markdown("<br>", unsafe_allow_html=True)

    
    
    col1, spacer, col2 = st.columns([1.5,0.2, 1])

    with col1:
        st.info("""
        1. **Zusammenführen** der beiden Datensätze für Analysen in Python
        """)  
    
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>⬇️</h1>",
            unsafe_allow_html=True,
        )
        
        st.info("""
        2. **Bereinigung von Datentypen** 
        """)  

        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>⬇️</h1>",
            unsafe_allow_html=True,
        )

        st.info("""
        3. **Umbenennung von Spalten** für besseres Verständnis (z.B. ta ➝ air_temperature)
        """)  

        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>⬇️</h1>",
            unsafe_allow_html=True,
        )

        st.info("""
        4. 🔍 Übersichten zur Verteilung des Datensatzes und **Untersuchung der fehlenden Werte** 
                
        ➝ Gibt es Muster wie z.B. bestimmte Länder mit vielen fehlenden Werten?
        """)  

        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>⬇️</h1>",
            unsafe_allow_html=True,
        )

        st.info("""
        5. **Entfernen** von nicht benötigten Spalten 
        """)  

        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>⬇️</h1>",
            unsafe_allow_html=True,
        )

        st.info("""
        6. Bei kategorialen Spalten: **Auffüllen** der fehlenden Werte mit der Kategorie "Unknown"
        """)  
        
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>⬇️</h1>",
            unsafe_allow_html=True,
        )

        st.info("""
        7. **Standardisierung**: Runden der Werte von thermal_comfort und thermal_sensation für klare Kategorien 
        
        ➝ wichtig für Machine Learning 
        """)  
        
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>⬇️</h1>",
            unsafe_allow_html=True,
        )

        st.info("""
        8. Erstellen einer neuen **Spalte mit vier Hauptklimazonen** 
        
        ➝ Zuordnung der Klimata zu diesen Hauptklimazonen
        """)  

        st.markdown("<br><br>", unsafe_allow_html=True)

    # Übersicht Dimensionen vor und nach Bereinigung
    with col2:
        # Dimensionen vor der Bereinigung 
        st.write("### 📏 Dimensionen vor Bereinigung")
        st.write(f"**Zeilen:** {df.shape[0]}")
        st.write(f"**Spalten:** {df.shape[1]}")
        
        # Dimensionen nach der Bereinigung 
        st.write("### 📏 Dimensionen nach Bereinigung")
        st.write(f"**Zeilen:** {df_bereinigt.shape[0]}")
        st.write(f"**Spalten:** {df_bereinigt.shape[1]}")

    # Tabelle Datensatz nach Bereinigung
    st.subheader("🧾 Datensatz nach der Bereinigung")
    st.dataframe(df_bereinigt)


###############################################################################################################################################
###############################################################################################################################################

with tab3:

    st.subheader("Herausforderungen bei der Datenbereinigung")

    col1, col2, col3 = st.columns([1.5, 0.2, 2])
    col4, col5, col6 = st.columns([1.5, 0.2, 2])
    col7, col8, col9 = st.columns([1.5, 0.2, 2])
    col10, col11, col12 = st.columns([1.5, 0.2, 2])

    # ---------------------------------------------------------
    # Linke Spalte: Herausforderungen
    # ---------------------------------------------------------
    with col1:
        st.markdown("#### ⚠️ Herausforderung")
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            """
            1. Sehr großer Datensatz mit **vielen erhobenen Werten**
        """
        )

        st.markdown(
            """
            - Viele verschiedene Messdaten
            
            ➝ z.B. bei air_temperature 4 verschiedene Werte: allgemein, 10cm über Boden, 60cm über Boden, 110cm über Boden
                
            """
        ) 

        st.markdown("<br>", unsafe_allow_html=True)

    with col4:
        st.info(
            """
            2. Sehr viele **fehlende Werte**
        """
        )

        st.markdown(
            """
            - Spalten variieren stark bezüglich Anzahl der fehlenden Werte (z.B.):
                - age ➝ 55% (60039 Einträge)
                - thermal_sensation ➝ 3% (2862 Einträge)
                - thermal_comfort ➝ 65% (70998 Einträge)
            """
        ) 

        st.markdown("<br>", unsafe_allow_html=True)

    with col7:
        st.info(
            """
            3. Werte in den Spalten **thermal_comfort** und **thermal_sensation** enthalten Dezimalwerte
        """
        )

        st.markdown(
            """
            - thermal_comfort und thermal_sensation haben eigentlich Kategorien (z.B. -3: sehr kalt bis 3: sehr heiß)
            - Dezimalwerte in den Daten entstehen durch Aggregationen und Verwendung von unterschiedlichen Skalen
            """
        )      

        st.markdown("<br>", unsafe_allow_html=True)

    with col10:
        st.info(
            """
            4. 31 verschiedene **Klimata**
        """
        )

        st.markdown(
            """
            - unübersichtlich für Analysen
            """
        ) 

        st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Mittlere Spalte: Pfeile
    # ---------------------------------------------------------

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    with col8:
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    with col11:
        st.markdown(
            "<h1 style='text-align: center; margin: 0; font-size: 20px;'>➡️</h1>",
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------------
    # Rechte Spalte: Lösungen
    # ---------------------------------------------------------

    with col3:
        st.markdown("#### 🛠️ Umgang mit Herausforderung")
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            """
            1. Überblick verschaffen  
        """
        )

        st.markdown(
            """
            - Welche Werte sind für uns relevant? 
            - Welche Fragestellungen wollen wir untersuchen?
        """
        )

        st.markdown("<br>", unsafe_allow_html=True)

    with col6:
        st.info(
            """
            2. Gemeinsame Überlegungen, welche Voraussetzungen wir benötigen für:
        """
        )

        st.markdown(
            """
        - Datenanalyse
        - Machine Learning

        **➜ Untersuchung der fehlenden Werte auf Muster**

        **➜ Entscheidung:**

        - kategoriale Spalten: mit "Unknown" auffüllen
        - numerische Spalten: fehlende Werte nicht bearbeiten, um Analysen nicht zu verzerren
        - für Machine Learning: Entfernen der Zeilen mit fehlenden Werten in relevanten Variablen
        """
        )
        
        st.markdown("<br>", unsafe_allow_html=True)

    with col9:
        st.info(
            """
            3. Standardisierung durch Runden der Dezimalwerte  
        """
        )

        st.markdown(
            """
            ➝ ausführlichere Informationen auf nächster Seite
        """
        )

        st.markdown("<br>", unsafe_allow_html=True)

        with col12:
            st.info(
                """
                4. Neue Spalte mit 4 Hauptklimazonen  
            """
            )

            st.markdown(
                """
                - Erstellen eines Mapping, um Klimata den Hauptklimazonen zuzuweisen
                - Hierdurch bei Analyse auch eine generellere Betrachtung möglich
            """
            )

            st.markdown("<br>", unsafe_allow_html=True)



###############################################################################################################################################
###############################################################################################################################################

with tab4:

    st.subheader("Worin liegt die Schwierigkeit?")

    st.markdown(
        """
        - ASHRAE Global Thermal Comfort Database II sammelt Daten aus vielen verschiedenen Studien, Ländern, Klimazonen und Gebäudetypen
        - Dadurch entstehen **unterschiedliche Werte, Skalen und Formate** für dieselben Komfortparameter
        - Zudem werden in manchen Studien **Aggregationen** vorgenommen und in anderen nicht
        
        ➜ Für bessere Vergleichbarkeit und Auswertung der Daten: **Standardisierung**

        ➜ Durch Standardisierung werden alle Werte auf die **ASHRAE‑Skala** (z.B. 1–6) abgebildet
    """
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Standardisierte thermische Komfortparameter (TSV, TP, TC)")

    image = Image.open("thermal_parameters_code_numbers.png")

    # Bild anzeigen mit definierter Breite
    st.image(image, caption="Thermische Komfortparameter (TSV, TP, TC) – Standardisierte Codes", width=700)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 📍 Layout: Zwei Spalten
    # ---------------------------------------------------------
    st.subheader("🔢 Runden der thermischen Komfortparameter")
    
    st.info(
            """
            - Thermischer Komfort
        """
        )
    
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

    st.info(
        """
        - Thermisches Empfinden
    """
    )

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


    

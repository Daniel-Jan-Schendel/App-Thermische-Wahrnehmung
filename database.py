import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import matplotlib.pyplot as plt
import pydeck as pdk    
import numpy as np

import json

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(page_title="Database", layout="wide", initial_sidebar_state="expanded")

st.title("Die Datenwolke hinter Smart Building Analytics")

# st.title("Neon PostgreSQL: Unsere cloudnative Datenbasis")
# st.title("Datenbank Überblick")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
# @st.cache_data
# def load_data():
#     return pd.read_csv("db_bereinigt.csv")
# df = load_data()


# ---------------------------------------------------------
# TABS (ONLY ON MAIN PAGE)
# ---------------------------------------------------------
tab_1, tab_2, tab_3, tab_4 = st.tabs(["📘 Neon PostgreSQL – Datenbank", "🧱 Datenbank-Architektur & Optimierung", "📊 Power BI-Integration", "Verfahren"])

# ---------------------------------------------------------
# SOURCE TAB
# ---------------------------------------------------------
with tab_1:
    # Title
    st.markdown("## **Cloud-native Infrastruktur & Datenmodellierung**")
   
    col_center, col_right = st.columns([5, 3])
    
    with col_center:
        # Einleitende Infobox zur Neon-Plattform
        st.info(
            "**Neon** ist eine cloudnative, serverlose PostgreSQL-Datenbank, "
            "die speziell für moderne Entwickler konzipiert wurde.\n\n"
            "Sie bietet sofortiges Branching (Datenbank-Klonen) sowie eine vollständig automatische "
            "Skalierung der Rechenleistung."
        )
    
    st.markdown("---")
    
    # Symmetrisches Zwei-Spalten-Layout für die technische Dokumentation
    col_doc1, col_doc2 = st.columns(2)
    
    with col_doc1:
        st.markdown("### 📊 **Ausgangssituation & Herausforderung**")
        st.markdown(
            "**Datensatz:** ASHRAE v2.1-Datenbank mit über **109.033 Messungen** und **59 structured Spalten**.\n\n"
            "**Zielstellung:** Aufbau einer hochverfügbaren, performanten Cloud-Infrastruktur, um Echtzeit-Analysen "
            "für das gesamte Projektteam plattformunabhängig bereitzustellen."
        )
        
        # st.markdown("### ⚡ **Systemvorteile der Cloud**")
        # st.markdown(
        #     "* **Skalierbarkeit:** Automatische Anpassung an große Abfragemengen bei minimaler Latenz.\n"
        #     "* **Ressourcen-Trennung:** Unabhängige Verwaltung von Cloud-Speicher und Rechenleistung.\n"
        #     "* **Sicherheit:** Verschlüsselte Ende-zu-Ende-Verbindung über sichere SSL-Kanäle."
        # )


with tab_2:
    st.markdown("---")
    
    col_doc1, col_doc2 = st.columns(2)
    
    with col_doc1:
        st.markdown("### 🧱 **Datenbank-Architektur & Optimierung**")
        st.markdown(
            "**Modellierung:** Erfolgreiche Überführung einer flachen Tabelle in eine **optimierte, relationale Datenbankstruktur**.\n\n"
            "Durch diese gezielte Normalisierung wurde die Performance der Abfragen in Python signifikant optimiert."
        )
        
        st.info("**dim_buildings:** Stammdaten-Katalog für die einzigartigen Gebäudestrukturen (9 Spalten).")
        st.info("**fact_thermal_records:** Zentrale Faktentabelle mit 50 Metrik- und Sensor-Spalten (Sensation, Comfort, Preference, Acceptability).")
        
with tab_3:
    col_doc1, col_doc2 = st.columns(2)
    
    with col_doc1:
        # 2. Saubere Power BI Erklärung (Sección ejecutiva limpia)
        st.markdown("### 📊 **Power BI-Integration**")
        st.markdown(
            "**Daten-Schnittstelle:** Die normalisierte relationale Struktur ermöglicht eine direkte, "
            "native Anbindung an **Microsoft Power BI** über standardisierte PostgreSQL-Connectors."
        )

    # # Texto final corregido sin barras invertidas innecesarias
    # st.text("Technologische und moderne Ansätze:")
    # st.text("     1. Neon ist die serverlose Zukunft von PostgreSQL.")
    # st.text("     2. Mit Neon skaliert die Datenbank automatisch auf Null.")
    # st.text("     3. Neon trennt Speicher und Berechnung für maximale Effizienz.")

# ==============================================================================
# 🏗️ PROJEKT-ARCHITEKTUR: DATENBANK-PIPELINE & NEON CLOUD INFRASTRUKTUR
# ==============================================================================
import os 
with tab_4:
    st.header("🏗️ Datenbasis & Cloud-Infrastruktur-Prozess")
    st.caption(
        "Der folgende Abschnitt dokumentiert das vollständige Backend-Engineering des Projekts. "
        "Die Pipeline erstreckt sich von der Bereitstellung der Cloud-Datenbank über das relationale "
        "Mapping bis hin zur finalen Integration in das Business-Intelligence-Infrastruktur-System."
    )

    st.markdown("---")

    # Helper-Funktion, um Abstürze bei fehlenden oder falsch geschriebenen Bildern komplett zu verhindern
    def safe_st_image(file_path, caption_text):
        if os.path.exists(file_path):
            st.image(file_path, caption=caption_text, use_container_width=True)
        else:
            # Versucht automatisch eine korrigierte Großbuchstaben-Erweiterung zu finden (.PNG)
            alt_path = file_path.replace(".png", ".PNG")
            if os.path.exists(alt_path):
                st.image(alt_path, caption=caption_text, use_container_width=True)
            else:
                st.warning(f"⚠️ Bild nicht gefunden: '{file_path}'. Bitte überprüfen Sie den Ordner-Pfad.")

    # ------------------------------------------------------------------------------
    # ABSCHNITT 1: NEON CLOUD INITIALISIERUNG
    # ------------------------------------------------------------------------------
    st.subheader("1. Bereitstellung der Serverlosen PostgreSQL-Datenbank in Neon")
    c1, c2 = st.columns(2)

    with c1:
        safe_st_image("neon/neon_01.jpg", "Abbildung 1: Initialisierung des Cloud-Projekts auf AWS Frankfurt.")
        st.markdown(
            "**Cloud-Provisionierung:** Einrichtung des serverlosen PostgreSQL-Clusters in der Region "
            "AWS Europe Central 1 (Frankfurt) zur Gewährleistung minimaler Latenzzeiten bei Abfragen."
        )

    with c2:
        safe_st_image("neon/neon_02.jpg", "Abbildung 2: Architektur-Übersicht der Compute-Ressourcen im Neon-Dashboard.")
        st.markdown(
            "**Infrastruktur-Monitoring:** Überwachung von Speicher (Storage) und Rechenleistung (Compute-Units) "
            "in Echtzeit. Generierung des sicheren SSL-Verbindungsstrings für die Backend-Kopplung."
        )

    st.markdown("---")

    # ------------------------------------------------------------------------------
    # ABSCHNITT 2: DATABASE OVERVIEW & SQL OPERATIONS
    # ------------------------------------------------------------------------------
    st.subheader("2. Datenbank-Projekt-Struktur & SQL DDL-Spezifikation")
    c3, c4 = st.columns(2)

    with c3:
        safe_st_image("neon/neon_03.jpg", "Abbildung 3: Detaillierte Projekt-Übersicht und Verbindungsparameter.")
        st.markdown(
            "**Datenbank-Konfiguration:** Verwaltung der Datenbank-Instanzen und Endpunkte. Sichere Bereitstellung "
            "der Zugriffsrechte für den DB-Owner zur Datenmanipulation."
        )

    with c4:
        safe_st_image("neon/neon_04.jpg", "Abbildung 4: SQL DDL-Skript im integrierten Neon SQL Editor.")
        st.markdown(
            "**Tabellen-Strukturierung (DDL):** Generierung des relationalen Datenbankschemas. Erstellung der "
            "Dimensionstabelle (`dim_buildings`) und der zentralen Faktentabelle (`fact_thermal_records`) "
            "mit strikten Primärschlüssel-Restriktionen."
        )

    st.markdown("---")

    # ------------------------------------------------------------------------------
    # ABSCHNITT 3: PYTHON PIPELINE & VERIFIKATION
    # ------------------------------------------------------------------------------
    st.subheader("3. Automatisierte Dateninjektion & Tabellen-Verifikation")
    c5, _ = st.columns([1,1])

    with c5:
        safe_st_image("neon/neon_05.jpg", "Abbildung 5: Robustes Python-Skript zur massiven Cloud-Injektion (SQLAlchemy).")
        st.markdown(
            "**ETL-Pipeline (Injektion):** Automatisierter Datentransfer via Python. Das Skript bereinigt "
            "Metadaten der Sensoren und lädt die **109.033 Zeilen** mithilfe optimierter Blockgrößen "
            "(Chunksize = 10.000) effizient in die Cloud hoch."
        )

    st.markdown("---")

    # ------------------------------------------------------------------------------
    # ABSCHNITT 4: POWER BI INTEGRATION
    # ------------------------------------------------------------------------------
    st.subheader("4. Business-Intelligence-Anbindung (Power BI)")
    c6, c7 = st.columns(2)

    with c6:
        safe_st_image("neon/neon_06.jpg", "Abbildung 6: Strukturierte Tabellen-Ansicht innerhalb der Neon-Datenbank-Konsole.")
        st.markdown(
            "**Daten-Validierung:** Direktprüfung der hochgeladenen Datensätze in der Cloud zur Gewährleistung "
            "von Datenkonsistenz und fehlerfreien Datentypen vor der BI-Verknüpfung."
        )

    with c7:
        safe_st_image("neon/neon_07.jpg", "Abbildung 7: Konfiguration der nativen PostgreSQL-Schnittstelle in Power BI.")
        st.markdown(
            "**DirectQuery / Import-Modus:** Anbindung der Cloud-Datenbank an das analytische Frontend. "
            "Einfügen des verschlüsselten AWS-Endpunkts und Authentifizierung des DB-Owners."
        )
    
    c8, _ = st.columns([1,1])
    with c8:
        safe_st_image("neon/neon_08.jpg", "Abbildung 8: Ausführung und Laden der Datenströme in die BI-Umgebung.")
        st.markdown(
            "**Verbindungs-Aufbau:** Datenübertragung aus Neon in das relationale Modell. Die Tabellen "
            "werden ohne Informationsverlust in den Hauptspeicher der BI-Anwendung geladen."
        )

    st.markdown("---")

    # ------------------------------------------------------------------------------
    # ABSCHNITT 5: RELATIONAL MODEL & COMPONENT SCHEME
    # ------------------------------------------------================--------------
    st.subheader("5. Relationales Sternschema & Komponenten-Integrität")
    c9, c10 = st.columns(2)

    with c9:
        safe_st_image("neon/neon_09.jpg", "Abbildung 9: Komponenten-Übersicht des Datenmodells.")
        st.markdown(
            "**System-Architektur:** Validierung der einzelnen Datenkomponenten. Überprüfung der Datenintegrität "
            "und Vorbereitung der Kennzahlen-Berechnungen (Measures)."
        )

    with c10:
        safe_st_image("neon/neon_10.jpg", "Abbildung 10: Finales Sternschema mit einer mathematischen Viele-zu-Eins-Beziehung (*:1).")
        st.markdown(
            "**Datenmodellierung (Star Schema):** Verknüpfung der Faktentabelle mit der Dimensionstabelle über "
            "das gemeinsame Feld `building_id`. Dieses relationale Design sichert die referenzielle Integrität "
            "und bildet das mathematische Fundament für die Berechnungen unseres Dashboards."
        )

# ---------------------------------------------------------
# MAP TAB
# ---------------------------------------------------------
# with tab_2:

#     st.subheader("🌍 Globale Verteilung der ASHRAE‑Feldstudien")
#     st.markdown(
#         """
#         <p style="font-size:16px; line-height:1.6; color:#444;">
#             Diese Karte zeigt die weltweite Verteilung der Feldstudien aus der 
#             <strong>ASHRAE Global Thermal Comfort Database II</strong>.
#             Jeder Marker repräsentiert einen Standort, an dem Messungen durchgeführt wurden.
#         </p>
#         """,
#         unsafe_allow_html=True
#     )

#     col1, col2, col3 = st.columns([1.2,1.8,0.8])

#   #######################################################################################################################################################
#   #######################################################################################################################################################

#     with col1: 


#         anz_daten = len(df)
#         st.write(f"**Datensätze insgesamt:** {anz_daten}")

        
#         # Jahr – nur Min/Max anzeigen
#         if "year" in df.columns:
#             year_min = df["year"].dropna().min()
#             year_max = df["year"].dropna().max()
#             st.write(f"**Jahre (Range):** {year_min} – {year_max}")


#         # Daten bereinigen
#         year_data = df["year"].dropna()

#         #st.subheader("📊 Verteilung der Jahre")

#         fig, ax = plt.subplots()
#         ax.hist(year_data, bins=20, color="steelblue", edgecolor="black")
#         ax.set_xlabel("Jahre")
#         ax.set_ylabel("Anzahl")
#         ax.set_title("Histogramm der Jahresverteilung")
#         st.pyplot(fig)


#     with col2: 
#         df_map = pd.read_csv("db_bereinigt.csv")
#         df_map = df_map.dropna(subset=["latitude", "longitude"])

#         city_counts = (
#             df_map.groupby(["country", "city", "latitude", "longitude"])
#             .size()
#             .reset_index(name="count")
#         )

#         # Proportional size
#         city_counts["radius"] = np.log1p(city_counts["count"]) * 30000

#         layer = pdk.Layer(
#             "ScatterplotLayer",
#             data=city_counts,
#             get_position="[longitude, latitude]",
#             get_radius="radius",
#             get_fill_color=[46, 134, 193, 180],
#             pickable=True,
#         )

#         view_state = pdk.ViewState(
#             latitude=city_counts["latitude"].mean(),
#             longitude=city_counts["longitude"].mean(),
#             zoom=1,
#         )

#         tooltip = {
#             "html": "<b>{city}, {country}</b><br/>Studies: {count}",
#             "style": {"color": "white"}
#         }

#         st.pydeck_chart(
#             pdk.Deck(
#                 layers=[layer],
#                 initial_view_state=view_state,
#                 tooltip=tooltip,
#                 map_style=None  
#             )
#         )
#         st.text("Geografische Verteilung  in der ASHRAE Global Thermal Comfort Database II.")


#     with col3:

#         # Anzahl Regionen
#         anz_regionen = df["region"].dropna().nunique()

#         # Anzahl Länder
#         anz_laender = df["country"].dropna().nunique()

#         # Anzahl Städte
#         anz_staedte = df["city"].dropna().nunique()

#         st.write(f"**Regionen insgesamt:** {anz_regionen}")
#         st.write(f"**Länder insgesamt:** {anz_laender}")
#         st.write(f"**Städte insgesamt:** {anz_staedte}")


#         # Building Type
#         if "building_type" in df.columns:
#             anz_building_type = df["building_type"].dropna().nunique()
#             st.write(f"**Gebäudetypen insgesamt:** {anz_building_type}")

#         # Climate
#         if "climate" in df.columns:
#             anz_climate = df["climate"].dropna().nunique()
#             st.write(f"**Klimazonen insgesamt:** {anz_climate}")

#         # Season
#         if "season" in df.columns:
#             anz_season = df["season"].dropna().nunique()
#             st.write(f"**Jahreszeiten insgesamt:** {anz_season}")

#         # Cooling Type
#         if "cooling_type" in df.columns:
#             anz_cooling = df["cooling_type"].dropna().nunique()
#             st.write(f"**Kühlungsarten insgesamt:** {anz_cooling}")

#         # Fan (1 = on, 0 = off)
#         if "fan" in df.columns:
#             fan_on = (df["fan"] == 1).sum()
#             fan_off = (df["fan"] == 0).sum()
#             st.write(f"**Ventilator:** {fan_on} × an, {fan_off} × aus")

#         # Heater (1 = on, 0 = off)
#         if "heater" in df.columns:
#             heater_on = (df["heater"] == 1).sum()
#             heater_off = (df["heater"] == 0).sum()
#             st.write(f"**Heizung:** {heater_on} × an, {heater_off} × aus")

#         # Window (0 = open, 1 = closed)
#         if "window" in df.columns:
#             window_open = (df["window"] == 0).sum()
#             window_closed = (df["window"] == 1).sum()
#             st.write(f"**Fenster:** {window_open} × offen, {window_closed} × geschlossen")

#         # Door (0 = open, 1 = closed)
#         if "door" in df.columns:
#             door_open = (df["door"] == 0).sum()
#             door_closed = (df["door"] == 1).sum()
#             st.write(f"**Tür:** {door_open} × offen, {door_closed} × geschlossen")

#         # Gender
#         if "gender" in df.columns:
#             anz_gender = df["gender"].dropna().nunique()
#             st.write(f"**Geschlechter insgesamt:** {anz_gender}")

#         # Age – nur Min/Max anzeigen
#         if "age" in df.columns:
#             age_min = df["age"].dropna().min()
#             age_max = df["age"].dropna().max()
#             st.write(f"**Alter (Range):** {age_min} – {age_max}")



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

st.title("Datenbank Überblick")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("db_bereinigt.csv")
df = load_data()


# ---------------------------------------------------------
# TABS (ONLY ON MAIN PAGE)
# ---------------------------------------------------------
tab_1,  tab_2, tab_3, tab_4 = st.tabs(
    ["📘 Neon", "🗂️ ERD", "🌍 Karte",  "📊 Explorer"]
)

# ---------------------------------------------------------
# SOURCE TAB
# ---------------------------------------------------------
with tab_1:

    st.text("Technologische und moderne Ansätze Neon ist die serverlose Zukunft von PostgreSQL Mit Neon skaliert die Datenbank automatisch " \
    "auf Null. Neon trennt Speicher und Berechnung für maximale Effizienz. Entwickler-Fokus. Neon ermöglicht Datenbank-Branching wie in Git.. " \
    "Datenbanken erstellen in Sekunden Neon macht die Datenbankverwaltung für Entwickler mühelos.")
    st.text("Neon ist eine cloudnative, serverlose PostgreSQL-Datenbank, die für moderne Entwickler entwickelt wurde und sofortiges Branching sowie automatische Skalierung bietet.")
    st.text("Technologische und moderne Ansätze:")
    st.text("1. Neon ist die serverlose Zukunft von PostgreSQL. 2 . Mit Neon skaliert die Datenbank automatisch auf Null. 3. .Neon trennt Speicher und Berechnung für maximale Effizienz.")
    

# ---------------------------------------------------------
# ERD TAB
# ---------------------------------------------------------
with tab_2:

    st.subheader("Entity Relationship Diagram (ERD)")
    st.write("Visual representation of the database schema and relationships.")

# ---------------------------------------------------------
# MAP TAB
# ---------------------------------------------------------
with tab_3:

    st.subheader("🌍 Globale Verteilung der ASHRAE‑Feldstudien")
    st.markdown(
        """
        <p style="font-size:16px; line-height:1.6; color:#444;">
            Diese Karte zeigt die weltweite Verteilung der Feldstudien aus der 
            <strong>ASHRAE Global Thermal Comfort Database II</strong>.
            Jeder Marker repräsentiert einen Standort, an dem Messungen durchgeführt wurden.
        </p>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.2,1.8,0.8])

  #######################################################################################################################################################
  #######################################################################################################################################################

    with col1: 


        anz_daten = len(df)
        st.write(f"**Datensätze insgesamt:** {anz_daten}")

        
        # Jahr – nur Min/Max anzeigen
        if "year" in df.columns:
            year_min = df["year"].dropna().min()
            year_max = df["year"].dropna().max()
            st.write(f"**Jahre (Range):** {year_min} – {year_max}")


        # Daten bereinigen
        year_data = df["year"].dropna()

        #st.subheader("📊 Verteilung der Jahre")

        fig, ax = plt.subplots()
        ax.hist(year_data, bins=20, color="steelblue", edgecolor="black")
        ax.set_xlabel("Jahre")
        ax.set_ylabel("Anzahl")
        ax.set_title("Histogramm der Jahresverteilung")
        st.pyplot(fig)


    with col2: 
        df_map = pd.read_csv("db_bereinigt.csv")
        df_map = df_map.dropna(subset=["latitude", "longitude"])

        city_counts = (
            df_map.groupby(["country", "city", "latitude", "longitude"])
            .size()
            .reset_index(name="count")
        )

        # Proportional size
        city_counts["radius"] = np.log1p(city_counts["count"]) * 30000

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=city_counts,
            get_position="[longitude, latitude]",
            get_radius="radius",
            get_fill_color=[46, 134, 193, 180],
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=city_counts["latitude"].mean(),
            longitude=city_counts["longitude"].mean(),
            zoom=1,
        )

        tooltip = {
            "html": "<b>{city}, {country}</b><br/>Studies: {count}",
            "style": {"color": "white"}
        }

        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style=None  
            )
        )
        st.text("Geografische Verteilung  in der ASHRAE Global Thermal Comfort Database II.")


    with col3:

        # Anzahl Regionen
        anz_regionen = df["region"].dropna().nunique()

        # Anzahl Länder
        anz_laender = df["country"].dropna().nunique()

        # Anzahl Städte
        anz_staedte = df["city"].dropna().nunique()

        st.write(f"**Regionen insgesamt:** {anz_regionen}")
        st.write(f"**Länder insgesamt:** {anz_laender}")
        st.write(f"**Städte insgesamt:** {anz_staedte}")


        # Building Type
        if "building_type" in df.columns:
            anz_building_type = df["building_type"].dropna().nunique()
            st.write(f"**Gebäudetypen insgesamt:** {anz_building_type}")

        # Climate
        if "climate" in df.columns:
            anz_climate = df["climate"].dropna().nunique()
            st.write(f"**Klimazonen insgesamt:** {anz_climate}")

        # Season
        if "season" in df.columns:
            anz_season = df["season"].dropna().nunique()
            st.write(f"**Jahreszeiten insgesamt:** {anz_season}")

        # Cooling Type
        if "cooling_type" in df.columns:
            anz_cooling = df["cooling_type"].dropna().nunique()
            st.write(f"**Kühlungsarten insgesamt:** {anz_cooling}")

        # Fan (1 = on, 0 = off)
        if "fan" in df.columns:
            fan_on = (df["fan"] == 1).sum()
            fan_off = (df["fan"] == 0).sum()
            st.write(f"**Ventilator:** {fan_on} × an, {fan_off} × aus")

        # Heater (1 = on, 0 = off)
        if "heater" in df.columns:
            heater_on = (df["heater"] == 1).sum()
            heater_off = (df["heater"] == 0).sum()
            st.write(f"**Heizung:** {heater_on} × an, {heater_off} × aus")

        # Window (0 = open, 1 = closed)
        if "window" in df.columns:
            window_open = (df["window"] == 0).sum()
            window_closed = (df["window"] == 1).sum()
            st.write(f"**Fenster:** {window_open} × offen, {window_closed} × geschlossen")

        # Door (0 = open, 1 = closed)
        if "door" in df.columns:
            door_open = (df["door"] == 0).sum()
            door_closed = (df["door"] == 1).sum()
            st.write(f"**Tür:** {door_open} × offen, {door_closed} × geschlossen")

        # Gender
        if "gender" in df.columns:
            anz_gender = df["gender"].dropna().nunique()
            st.write(f"**Geschlechter insgesamt:** {anz_gender}")

        # Age – nur Min/Max anzeigen
        if "age" in df.columns:
            age_min = df["age"].dropna().min()
            age_max = df["age"].dropna().max()
            st.write(f"**Alter (Range):** {age_min} – {age_max}")


#########################################################################################################################################################

##########################################################################################################################################################


    

# ---------------------------------------------------------
# EXPLORER TAB
# ---------------------------------------------------------

with tab_4:
    st.subheader("Data Explorer")

    column = st.selectbox("Choose a column:", df.columns)
    st.write(df[column].describe())

    if pd.api.types.is_numeric_dtype(df[column]):
        min_val, max_val = float(df[column].min()), float(df[column].max())
        selected_range = st.slider("Select value range:", min_val, max_val, (min_val, max_val))
        filtered_df = df[(df[column] >= selected_range[0]) & (df[column] <= selected_range[1])]
        st.dataframe(filtered_df.head())
    else:
        unique_values = df[column].dropna().unique()
        selected_value = st.selectbox("Select a value:", unique_values)
        filtered_df = df[df[column] == selected_value]
        st.dataframe(filtered_df.head())



######################################################################################################################



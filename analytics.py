import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import chi2_contingency
import os

st.set_page_config(page_title="Betrachtung der Verteilungen", layout="wide", initial_sidebar_state="expanded")

df = pd.read_csv("db_bereinigt_final.csv")

def plot_column(data, colname, color="steelblue"):
    """Erzeugt automatisch den passenden Plot für eine Spalte."""
    fig, ax = plt.subplots()

    # Numerische Spalte → Histogramm
    if pd.api.types.is_numeric_dtype(data):
        ax.hist(data, bins=20, color=color, edgecolor="black")
        ax.set_xlabel(colname)
        ax.set_ylabel("Anzahl")
        ax.set_title(f"Verteilung von {colname}")

    # Binäre Spalte (0/1) → Balkendiagramm
    elif set(data.unique()).issubset({0, 1}):
        counts = data.value_counts().sort_index()
        ax.bar(["0", "1"], counts.values, color=["tomato", "seagreen"])
        ax.set_xlabel(colname)
        ax.set_ylabel("Anzahl")
        ax.set_title(f"{colname}: 0/1 Verteilung")

    # Kategorische Spalte → Balkendiagramm
    else:
        counts = data.value_counts()
        ax.bar(counts.index.astype(str), counts.values, color=color)
        ax.set_xlabel(colname)
        ax.set_ylabel("Anzahl")
        ax.set_title(f"Kategorien in {colname}")
        plt.xticks(rotation=45, ha="right")

    return fig

def map_tsv(v):
    if pd.isna(v): return None
    if v <= -2.5: return -3
    elif v <= -1.5: return -2
    elif v <= -0.5: return -1
    elif v < 0.5: return 0
    elif v < 1.5: return 1
    elif v < 2.5: return 2
    else: return 3

def map_tc(v):
    if pd.isna(v): return None
    if v < 1.5: return 1
    elif v < 2.5: return 2
    elif v < 3.5: return 3
    elif v < 4.5: return 4
    elif v < 5.5: return 5
    else: return 6

def plot_comfort_variable(series, labels, colors, title):
    series = pd.to_numeric(series, errors="coerce").dropna()
    counts = series.value_counts().sort_index()
    total = counts.sum()

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, level in enumerate(counts.index):
        count = counts[level]
        pct = count / total * 100

        ax.bar(str(level), count, color=colors[level])
        ax.text(i, count + 0.5, f"{count} ({pct:.1f}%)", ha="center")

    ax.set_title(title)
    ax.set_xlabel("Kategorie")
    ax.set_ylabel("Anzahl")

    st.pyplot(fig)
    plt.close(fig)



# Load data

#st.title("Globale Datenanalyse")
#st.line_chart(df_bereinigt["DB"])
#st.dataframe(df_bereinigt)

st.title("📊 Betrachtung der Verteilungen")

#st.header("Datenverteilung")

# Klima / Building

tab1,tab2 = st.tabs(["Globale Datenverteilung","Übersicht Datenverteilung wichtige Variablen"], on_change="rerun")


with tab1:
    col1, spacer, col2 = st.columns([2, 0.4, 1])

    # --- Grafik mit Anzahl Einträge ---
    with col1:
        
        # ---------------------------------------------------------
        # 🔎 1. Mapping-Dictionary
        # ---------------------------------------------------------
        mapping = {
            "Region": "region",
            "Land": "country",
            "Klimazone": "climate_zone",
            "Klima": "climate"
        }

        # ---------------------------------------------------------
        # 🔍 2. Filter-Widget (Kima/Klimazone)
        # ---------------------------------------------------------
        selected_variable = st.selectbox(
            "Variable auswählen",
            list(mapping.keys()),
            key="verteilung_variable"
        )

        # ---------------------------------------------------------
        # 🔍 3. Mapping anwenden
        # ---------------------------------------------------------
        column = mapping[selected_variable]

        # ---------------------------------------------------------
        # 🔍 4. Berechnungen
        # ---------------------------------------------------------
        counts = df[column].value_counts()
        percent = counts / counts.sum() * 100

        # ---------------------------------------------------------
        # 🔍 5. Darstellung
        # ---------------------------------------------------------
        selection_df = pd.DataFrame({
            selected_variable: counts.index,
            "Anzahl": counts.values,
            "Prozent": percent.values
        })

        selection_df["Prozent"] = (
            selection_df["Prozent"].round(2).astype(str) + " %"
        )

      
        # ---------------------------------------------------------
        # 🔎 6. Grafik erstellen
        # ---------------------------------------------------------
        st.subheader(f"Anzahl Einträge je {selected_variable}")

        # Sichergehen, dass in der Grafik die ausgewählte Variable verwendet wird
        category = selection_df.columns[0]

        chart = (
            alt.Chart(selection_df)
            .mark_bar()
            .encode(
                x=alt.X("Anzahl:Q", title="Anzahl Einträge"),
                y=alt.Y(f"{category}:N", sort="-x", title=category),
                tooltip=[category, "Anzahl", "Prozent"]
            )
            .properties(
                width=600,
                height=550
            )
        )

        st.altair_chart(chart, use_container_width=True)
    

    # --- Anzahl Einträge in der Kategorie ---
    with col2:
        st.markdown(f"### Übersicht Anzahl Einträge je {selected_variable}")

        st.dataframe(
            selection_df,
            use_container_width=True,
            hide_index=True
        )


#########################################################################################################
#########################################################################################################

with tab2:


    # ---------------------------------------------------------
    # ROW 2 → 3 Spalten: season, climate, cooling_type
    # ---------------------------------------------------------
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.subheader("🌦️ Season")
        fig_season = plot_column(df["season"], "season")
        st.pyplot(fig_season)
        plt.close(fig_season)

    with row2_col2:
        st.subheader("❄️ Cooling Type")
        fig_cooling = plot_column(df["cooling_type"], "cooling_type")
        st.pyplot(fig_cooling)
        plt.close(fig_cooling)

    with row2_col3:
        st.subheader("🏢 Building Type")
        fig_bt = plot_column(df["building_type"], "building_type")
        st.pyplot(fig_bt)
        plt.close(fig_bt)

    # ---------------------------------------------------------
    # NEUE ROW → 4 Spalten: fan, heater, window, door
    # ---------------------------------------------------------
    row_fan, row_heater, row_window, row_door = st.columns(4)

    with row_fan:
        st.subheader("🌀 Fan")
        fig_fan = plot_column(df["fan"], "fan")
        st.pyplot(fig_fan)
        plt.close(fig_fan)

    with row_heater:
        st.subheader("🔥 Heater")
        fig_heater = plot_column(df["heater"], "heater")
        st.pyplot(fig_heater)
        plt.close(fig_heater)

    with row_window:
        st.subheader("🪟 Window")
        fig_window = plot_column(df["window"], "window")
        st.pyplot(fig_window)
        plt.close(fig_window)

    with row_door:
        st.subheader("🚪 Door")
        fig_door = plot_column(df["door"], "door")
        st.pyplot(fig_door)
        plt.close(fig_door)

    # ---------------------------------------------------------
    # ROW 3 → 3 Spalten: leer | age | gender
    # ---------------------------------------------------------
    row3_col1, row3_col2, row3_col3 = st.columns(3)

    with row3_col1:
        st.write("")  # bewusst leer

    with row3_col2:
        st.subheader("👤 Age")
        fig_age = plot_column(df["age"], "age")
        st.pyplot(fig_age)
        plt.close(fig_age)

    with row3_col3:
        st.subheader("🚻 Gender")
        fig_gender = plot_column(df["gender"], "gender")
        st.pyplot(fig_gender)
        plt.close(fig_gender)


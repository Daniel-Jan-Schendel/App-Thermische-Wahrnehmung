import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 



st.set_page_config(page_title="Globale Datenanalyse", layout="wide", initial_sidebar_state="expanded")
  
# ---------------------------------------------------------
# Daten laden
# ---------------------------------------------------------
df_bereinigt = pd.read_csv("db_bereinigt.csv")
df = pd.read_csv("db_bereinigt_fertig.csv")

st.title("Analyse der Komfortparameter")

# ---------------------------------------------------------
# Tabs definieren
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Feature‑Korrelationen (Thermischer Komfort)",
    "Komfortparameter: Data Insights",
    "Parameter Interactions & Correlations",
    "Komfortfaktoren – Data Relationships",
    "Komfortanalyse: Multivariate Zusammenhänge"
])

with tab1:

        # ---------------------------------------------------------
    # 🎨 Labels & Farben
    # ---------------------------------------------------------

    tsv_labels = {
        -3: "–3 Sehr kalt",
        -2: "–2 Kalt",
        -1: "–1 Kühl",
        0: "0 Neutral",
        1: "+1 Warm",
        2: "+2 Heiß",
        3: "+3 Sehr heiß"
    }

    tsv_colors = {
        -3: "#4575b4",
        -2: "#74add1",
        -1: "#abd9e9",
        0: "#d9d9d9",
        1: "#fdae61",
        2: "#f46d43",
        3: "#d73027"
    }

    tp_labels = {
        -1: "–1 Kühler bevorzugt",
        0: "0 Keine Präferenz",
        1: "+1 Wärmer bevorzugt"
    }

    tp_colors = {
        -1: "#74add1",
        0: "#d9d9d9",
        1: "#f46d43"
    }

    tc_labels = {
        1: "1 Ungemütlich",
        2: "2 Leicht ungemütlich",
        3: "3 Akzeptabel / Neutral",
        4: "4 Leicht gemütlich",
        5: "5 Gemütlich",
        6: "6 Sehr gemütlich"
    }

    tc_colors = {
        1: "#fc8d59",
        2: "#fee08b",
        3: "#d9d9d9",
        4: "#a6d96a",
        5: "#1a9850",
        6: "#006837"
    }

    # ---------------------------------------------------------
    # 🔧 Mapping-Funktionen
    # ---------------------------------------------------------

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

    tp_map = {"cooler": -1, "no change": 0, "warmer": 1}

    # ---------------------------------------------------------
    # 📊 Plot-Funktion
    # ---------------------------------------------------------

    def plot_comfort_variable(df, column, labels, colors, title):

        y = df[column].dropna()

        if column == "thermal_sensation":
            y = y.apply(map_tsv)

        if column == "thermal_preference":
            y = y.map(tp_map)

        if column == "thermal_comfort":
            y = y.apply(map_tc)

        y = pd.to_numeric(y, errors="coerce").dropna()
        counts = y.value_counts().sort_index()
        total = counts.sum()

        fig, ax = plt.subplots(figsize=(8, 5))

        for i, level in enumerate(counts.index):
            count = counts[level]
            pct = count / total * 100

            ax.bar(str(level), count, color=colors[level])
            ax.text(i, count + 0.5, f"{count} ({pct:.1f}%)", ha="center")

        ax.set_title(title)
        ax.set_xlabel("Kategorie")
        ax.set_ylabel("Häufigkeit")

        st.pyplot(fig)

    # ---------------------------------------------------------
    # 📌 Streamlit UI – Botones
    # ---------------------------------------------------------

    st.header("🎨 Thermische Komfortparameter – Interaktive Buttons")

    df = pd.read_csv("db_bereinigt.csv")

    col1, col2, col3 = st.columns(3)

    with col1:
        btn_tsv = st.button("Thermal Sensation (TSV)", type="primary")

    with col2:
        btn_tp = st.button("Thermal Preference (TP)", type="primary")

    with col3:
        btn_tc = st.button("Thermal Comfort (TC)", type="primary")

    # ---------------------------------------------------------
    # 🔄 Logik: welcher Button wurde geklickt?
    # ---------------------------------------------------------

    if btn_tsv:
        plot_comfort_variable(df, "thermal_sensation", tsv_labels, tsv_colors,
                            "Thermal Sensation – Häufigkeiten")

    elif btn_tp:
        plot_comfort_variable(df, "thermal_preference", tp_labels, tp_colors,
                            "Thermal Preference – Häufigkeiten")

    elif btn_tc:
        plot_comfort_variable(df, "thermal_comfort", tc_labels, tc_colors,
                            "Thermal Comfort – Häufigkeiten")









###############################################################################################################################################
##############################################################################################################################################

# ---------------------------------------------------------
# TAB 1 – Korrelationsmatrix
# ---------------------------------------------------------

    st.header("Feature‑Korrelationen (Thermischer Komfort)")
    st.write("Analyse der statistischen Zusammenhänge zwischen numerischen Komfortparametern.")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)



    # Nur relevante numerische Komfortparameter auswählen
    relevant_cols = [
        "temp", "humidity", "pmv", "ppd", "air_speed",
        "met", "clo"
    ]

    # Nur Spalten verwenden, die wirklich existieren
    relevant_cols = [c for c in relevant_cols if c in df.columns]

    # Korrelationsmatrix berechnen
    corr = df[relevant_cols].corr()

    # Heatmap schöner darstellen
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",          # nur 2 Nachkommastellen
        cmap="coolwarm",
        linewidths=0.5,
        square=True,
        ax=ax
    )

    ax.set_title("Korrelationsmatrix der Komfortparameter", fontsize=14)
    st.pyplot(fig)

# ---------------------------------------------------------
# TAB 2 – Data Insights (Histogramme)
# ---------------------------------------------------------
with tab2:

    st.text("asaaass")

# ---------------------------------------------------------
    # 🎨 Labels & Farben für Komfortvariablen
    # ---------------------------------------------------------

    tsv_labels = {
        -3: "–3 Sehr kalt",
        -2: "–2 Kalt",
        -1: "–1 Kühl",
        0: "0 Neutral",
        1: "+1 Warm",
        2: "+2 Heiß",
        3: "+3 Sehr heiß"
    }

    tsv_colors = {
        -3: "#4575b4",
        -2: "#74add1",
        -1: "#abd9e9",
        0: "#d9d9d9",
        1: "#fdae61",
        2: "#f46d43",
        3: "#d73027"
    }

    tp_labels = {
        -1: "–1 Kühler bevorzugt",
        0: "0 Keine Präferenz",
        1: "+1 Wärmer bevorzugt"
    }

    tp_colors = {
        -1: "#74add1",
        0: "#d9d9d9",
        1: "#f46d43"
    }

    tc_labels = {
        1: "1 Ungemütlich",
        2: "2 Leicht ungemütlich",
        3: "3 Akzeptabel / Neutral",
        4: "4 Leicht gemütlich",
        5: "5 Gemütlich",
        6: "6 Sehr gemütlich"
    }

    tc_colors = {
        1: "#fc8d59",
        2: "#fee08b",
        3: "#d9d9d9",
        4: "#a6d96a",
        5: "#1a9850",
        6: "#006837"
    }

    # ---------------------------------------------------------
    # 🔧 Mapping
    # ---------------------------------------------------------

    tp_map = {"cooler": -1, "no change": 0, "warmer": 1}

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

    # ---------------------------------------------------------
    # 📊 Plot Funktion
    # ---------------------------------------------------------

    def plot_comfort_variable(series, labels, colors, title):
        series = pd.to_numeric(series, errors="coerce").dropna()
        counts = series.value_counts().sort_index()
        total = counts.sum()

        fig, ax = plt.subplots(figsize=(5, 3))  # kompakte Größe

        for i, level in enumerate(counts.index):
            count = counts[level]
            pct = count / total * 100
            ax.bar(str(level), count, color=colors[level])
            ax.text(i, count + 0.3, f"{count} ({pct:.1f}%)", ha="center", fontsize=8)

        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Kategorie")
        ax.set_ylabel("Anzahl")

        st.pyplot(fig)

    # ---------------------------------------------------------
    # 📌 Daten laden
    # ---------------------------------------------------------

    df = pd.read_csv("db_bereinigt.csv")

    df["thermal_sensation_cat"] = df["thermal_sensation"].apply(map_tsv)
    df["thermal_preference_cat"] = df["thermal_preference"].map(tp_map)
    df["thermal_comfort_cat"] = df["thermal_comfort"].apply(map_tc)

    # ---------------------------------------------------------
    # ⭐ 2×2 GRID
    # ---------------------------------------------------------

    row1_col1, row1_col2 = st.columns([1,2])
    row2_col1, row2_col2 = st.columns([1,2])

    # ---------------------------------------------------------
    # 🟩 BOX 1 — Filter + Karte (oben links)
    # ---------------------------------------------------------

    with row1_col1:

        st.header("📍 Komfort nach Region / Land / Stadt")

        column_map = {
            "Region": "region",
            "Land": "country",
            "Stadt": "city"
        }

        option = st.selectbox("Verteilung anzeigen nach:", list(column_map.keys()))
        colname = column_map[option]

        werte = df[colname].dropna()
        auswahl = st.selectbox(f"{option} auswählen:", sorted(werte.unique()))

        gefiltert = df[df[colname] == auswahl]

        st.markdown(f"### Karte – {option}: {auswahl}")

        if "latitude" in gefiltert.columns and "longitude" in gefiltert.columns:
            geo = gefiltert[["latitude", "longitude"]].dropna()
            if len(geo) > 0:
                st.map(geo)
            else:
                st.info("Keine gültigen geografischen Koordinaten verfügbar.")
        else:
            st.info("Keine geografischen Koordinaten verfügbar.")

    # ---------------------------------------------------------
    # 🟦 BOX 2 — Thermal Comfort (oben rechts)
    # ---------------------------------------------------------

    with row1_col2:

        st.subheader("Thermal Comfort")
        plot_comfort_variable(
            gefiltert["thermal_comfort_cat"],
            tc_labels,
            tc_colors,
            f"Thermal Comfort – {auswahl}"
        )

    # ---------------------------------------------------------
    # 🟧 BOX 3 — Thermal Sensation (unten links)
    # ---------------------------------------------------------

    with row2_col1:

        st.subheader("Thermal Sensation")
        plot_comfort_variable(
            gefiltert["thermal_sensation_cat"],
            tsv_labels,
            tsv_colors,
            f"Thermal Sensation – {auswahl}"
        )

    # ---------------------------------------------------------
    # 🟥 BOX 4 — Thermal Preference (unten rechts)
    # ---------------------------------------------------------

    with row2_col2:

        st.subheader("Thermal Preference")
        plot_comfort_variable(
            gefiltert["thermal_preference_cat"],
            tp_labels,
            tp_colors,
            f"Thermal Preference – {auswahl}"
        )




    st.header("Komfortparameter: Data Insights")
    st.write("Verteilungen der wichtigsten Komfortparameter.")

    cols_to_plot = ["age", "year", "temp", "humidity"]  # Beispiel
    for col in cols_to_plot:
        if col in df.columns:
            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=20, color="steelblue")
            ax.set_title(f"Verteilung von {col}")
            st.pyplot(fig)




########################################################################################################################
#########################################################################################################################
# ---------------------------------------------------------
# TAB 3 – Interaktionen (Scatterplots)
# ---------------------------------------------------------
with tab3:
    st.header("Parameter Interactions & Correlations")
    st.write("Scatterplots zur Analyse von Zusammenhängen.")

    scatter_pairs = [
        ("temp", "humidity"),
        ("temp", "pmv"),
        ("humidity", "pmv")
    ]

    for x, y in scatter_pairs:
        if x in df.columns and y in df.columns:
            fig, ax = plt.subplots()
            ax.scatter(df[x], df[y], alpha=0.4)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f"{x} vs. {y}")
            st.pyplot(fig)

# ---------------------------------------------------------
# TAB 4 – Komfortfaktoren (Kategorische Parameter)
# ---------------------------------------------------------
with tab4:
    st.header("Komfortfaktoren – Data Relationships")
    st.write("Analyse der Häufigkeiten kategorischer Komfortfaktoren.")

    cat_cols = ["season", "climate", "cooling_type", "building_type"]

    for col in cat_cols:
        if col in df.columns:
            counts = df[col].value_counts()
            fig, ax = plt.subplots()
            ax.bar(counts.index.astype(str), counts.values, color="slateblue")
            ax.set_title(f"Kategorien in {col}")
            plt.xticks(rotation=45)
            st.pyplot(fig)

# ---------------------------------------------------------
# TAB 5 – Multivariate Analyse (Pairplot)
# ---------------------------------------------------------
with tab5:
    st.header("Komfortanalyse: Multivariate Zusammenhänge")
    st.write("Multivariate Analyse der wichtigsten Komfortparameter.")

    multi_cols = ["temp", "humidity", "pmv", "age"]

    available_cols = [c for c in multi_cols if c in df.columns]

    if len(available_cols) >= 2:
        fig = sns.pairplot(df[available_cols].dropna())
        st.pyplot(fig)
    else:
        st.warning("Nicht genügend numerische Spalten für eine multivariate Analyse.")

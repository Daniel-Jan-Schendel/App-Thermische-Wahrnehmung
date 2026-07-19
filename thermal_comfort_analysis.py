import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from tabulate import tabulate
from PIL import Image
import networkx as nx
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px




st.set_page_config(page_title="Thermischekomfort Datenanalyse", layout="wide", initial_sidebar_state="expanded")

# ---------------------------------------------------------
# Daten laden
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("db_bereinigt_final.csv")
df = load_data()

def apply_sidebar_filters(df):
    # ============================================================
    # RESET BUTTON
    # ============================================================

    if st.sidebar.button("Reset filters"):
        st.query_params.clear()
        st.rerun()

    # ============================================================
    # SIDEBAR FILTERS WITH CASCADING LOGIC
    # ============================================================

    st.sidebar.header("Filters")

    # --- REGION ---
    region_list = ["All"] + sorted(df["region"].dropna().unique())
    region = st.sidebar.selectbox("Region", region_list)

    # --- COUNTRY depends on REGION ---
    if region != "All":
        country_list = ["All"] + sorted(df[df["region"] == region]["country"].dropna().unique())
    else:
        country_list = ["All"] + sorted(df["country"].dropna().unique())
    country = st.sidebar.selectbox("Country", country_list)

    # --- CITY depends on COUNTRY ---
    if country != "All":
        city_list = ["All"] + sorted(df[df["country"] == country]["city"].dropna().unique())
    else:
        city_list = ["All"] + sorted(df["city"].dropna().unique())
    city = st.sidebar.selectbox("City", city_list)

    # --- CLIMATE ---
    climate_list = ["All"] + sorted(df["climate"].dropna().unique())
    climate = st.sidebar.selectbox("Climate", climate_list)

    # --- BUILDING TYPE depends on CLIMATE ---
    if climate != "All":
        building_list = ["All"] + sorted(df[df["climate"] == climate]["building_type"].dropna().unique())
    else:
        building_list = ["All"] + sorted(df["building_type"].dropna().unique())
    building_type = st.sidebar.selectbox("Building Type", building_list)

    # --- COOLING TYPE depends on BUILDING TYPE ---
    if building_type != "All":
        cooling_list = ["All"] + sorted(df[df["building_type"] == building_type]["cooling_type"].dropna().unique())
    else:
        cooling_list = ["All"] + sorted(df["cooling_type"].dropna().unique())
    cooling_type = st.sidebar.selectbox("Cooling Type", cooling_list)

    # --- SEASON ---
    season_list = ["All"] + sorted(df["season"].dropna().unique())
    season = st.sidebar.selectbox("Season", season_list)

    # --- GENDER ---
    gender_list = ["All"] + sorted(df["gender"].dropna().unique())
    gender = st.sidebar.selectbox("Gender", gender_list)

    if season != "All":
        clo_min = float(df[df["season"] == season]["clothing_ensemble_insulation"].min())
        clo_max = float(df[df["season"] == season]["clothing_ensemble_insulation"].max())
    else:
        clo_min = float(df["clothing_ensemble_insulation"].min())
        clo_max = float(df["clothing_ensemble_insulation"].max())
    clo = st.sidebar.slider("Clothing Insulation (clo)", clo_min, clo_max, (clo_min, clo_max), step=0.01)

    # --- METABOLIC RATE SLIDER ---
    met_min = float(df["metabolic_rate"].min())
    met_max = float(df["metabolic_rate"].max())
    metabolic_rate = st.sidebar.slider("Metabolic Rate (met)", min_value=met_min,max_value=met_max,value=(met_min, met_max),step=0.01)

    # --- AGE SLIDER ---
    age_min = int(df["age"].min())
    age_max = int(df["age"].max())
    age = st.sidebar.slider("Age",min_value=age_min,max_value=age_max,value=(age_min, age_max) )


    # ============================================================
    # APPLY FILTERS SAFELY
    # ============================================================

    df_filtered = df.copy()



    if region != "All": df_filtered = df_filtered[df_filtered["region"] == region]
    if country != "All": df_filtered = df_filtered[df_filtered["country"] == country]
    if city != "All": df_filtered = df_filtered[df_filtered["city"] == city]
    if climate != "All": df_filtered = df_filtered[df_filtered["climate"] == climate]
    if building_type != "All": df_filtered = df_filtered[df_filtered["building_type"] == building_type]
    if cooling_type != "All": df_filtered = df_filtered[df_filtered["cooling_type"] == cooling_type]
    if season != "All": df_filtered = df_filtered[df_filtered["season"] == season]
    if gender != "All": df_filtered = df_filtered[df_filtered["gender"] == gender]
    df_filtered = df_filtered[(df_filtered["clothing_ensemble_insulation"] >= clo[0]) &(df_filtered["clothing_ensemble_insulation"] <= clo[1])]
    df_filtered = df_filtered[(df_filtered["metabolic_rate"] >= metabolic_rate[0]) &(df_filtered["metabolic_rate"] <= metabolic_rate[1])]
    df_filtered = df_filtered[(df_filtered["age"] >= age[0])&(df_filtered["age"] <= age[1])]


    # ============================================================
    # FILTER TEXT FOR TITLE
    # ============================================================

    active_filters = []

    for name, value in [
        ("Region", region),
        ("Country", country),
        ("City", city),
        ("Climate", climate),
        ("Building Type", building_type),
        ("Cooling Type", cooling_type),
        ("Season", season),
        ("Gender", gender)
    ]:
        if value != "All":
            active_filters.append(f"{name}: {value}")
    
    # Mostrar CLO solo si el usuario modificó el slider
    if clo[0] != clo_min or clo[1] != clo_max:
        active_filters.append(f"Clo: {clo[0]:.2f}–{clo[1]:.2f}")

    # Mostrar MET solo si el usuario modificó el slider
    if metabolic_rate[0] != met_min or metabolic_rate[1] != met_max:
        active_filters.append(f"Met: {metabolic_rate[0]:.2f}–{metabolic_rate[1]:.2f}")

    # Mostrar AGE solo si el usuario modificó el slider
    if age[0] != age_min or age[1] != age_max:
        active_filters.append(f"Age: {age[0]}–{age[1]}")



    filter_text = " | ".join(active_filters) 


    return df_filtered, filter_text
  
df_filtered, filter_text = apply_sidebar_filters(df)

 # --- ASHRAE refined CLO dictionary ---
ashrae_clo_refined = {
    0.00: "Nackt",
    0.05: "Nur Unterwäsche",
    0.15: "Sehr leicht: Shorts + Tank-Top",
    0.25: "Leichtes Sommer-Outfit",
    0.35: "Sommerkleidung: Leichte lange Hose + T‑Shirt",
    0.45: "Standard-Sommer: Shorts/Rock + kurzärmeliges Hemd",
    0.55: "Leichte Übergangskleidung",
    0.65: "Büro-Sommerkleidung",
    0.75: "Standard-Übergang: Jeans + leichter Pullover",
    0.85: "Warmes Outfit",
    1.00: "Business-Anzug",
    1.15: "Winter-Büro",
    1.30: "Wärmere Winterkleidung",
    1.50: "Schwere Außenkleidung",
    2.00: "Extrem-Winterkleidung"
}
# --- CLO mean for selected country ---
clo_mean = df_filtered["clothing_ensemble_insulation"].mean()

# --- Find closest CLO category ---
closest_clo = min(ashrae_clo_refined.keys(), key=lambda x: abs(x - clo_mean))
clothing_label = ashrae_clo_refined[closest_clo]


st.title("Analyse der Komfortparameter")

# ---------------------------------------------------------
# Tabs definieren
# ---------------------------------------------------------
tab1, tab2, tab3, tab4,tab5 = st.tabs([
    "Komfortvariablen Korrelation",
    "Neutraltemperatur: MTS vs Innentemperatur",
    "Adaptives Komfortmodell",
    "Korrelationsanalyse", "Beinfluz in Berkleidung" ])

with tab1:

    german_labels = {
    "thermal_sensation": "Thermische Empfinden",
    "thermal_acceptability": "Thermische Akzeptanz",
    "thermal_preference": "Thermische Präferenz",
    "thermal_comfort": "Thermischer Komfort"
}

    st.subheader("Wie hängen die subjektiven Komfortvariablen miteinander zusammen?")

    st.markdown("""
        Die subjektiven Komfortvariablen beschreiben, wie Menschen ihre thermische Umgebung wahrnehmen,
        bewerten und welche Änderungen sie sich wünschen. Sie helfen dabei zu verstehen, wie verschiedene
        Aspekte des thermischen Erlebens miteinander zusammenhängen.

        **Interpretation der Korrelationen:**

        - **Positive Werte:** Zwei Variablen verändern sich gemeinsam (z. B. höhere Empfindung → höhere Komfortbewertung).  
        - **Negative Werte:** Die Variablen zeigen gegensätzliche Tendenzen (z. B. wärmer empfinden → geringere Akzeptanz).  

        So wird sichtbar, welche Faktoren das thermische Empfinden, die Akzeptanz und den Komfort am stärksten beeinflussen.
        """)


    # st.markdown("""
    #     ##### 1. Thermische Empfindung (TS) 
    #     **Kalt  ◄────── Neutral ──────►  Heiß**  
    #     `-3    -2    -1    0    +1    +2    +3 `

    #     ##### 2. Thermische Akzeptanz (TA)
    #     ○ Nicht akzeptabel  
    #     ○ Akzeptabel  

    #     ##### 3. Thermische Präferenz (TP)  
    #     **Kühler ◄──────── Keine Änderung ────────► Wärmer**  
    #     `  -1                         0                         +1     `

    #     ##### 4. Thermischer Komfort (TC, ASHRAE‑Skala 1–6)  
    #     **Sehr unkomfortabel ◄──────────────────────► Sehr komfortabel**  
    #            `  1             2            3           4           5            6   `
    #     """)

   
    # Zwei Spalten erstellen
    col1, col2 = st.columns([1.8, 1])   # linke Spalte etwas breiter für die Heatmap



    with col1:


        # Relevante Spalten
        cols = [
            "thermal_sensation",
            "thermal_acceptability",
            "thermal_preference",
            "thermal_comfort"
        ]

        df_sub = df[cols].copy()

        # -----------------------------
        # 1. Numerische Umwandlung
        # -----------------------------
        df_sub["thermal_sensation"] = pd.to_numeric(df_sub["thermal_sensation"], errors="coerce")
        df_sub["thermal_comfort"] = pd.to_numeric(df_sub["thermal_comfort"], errors="coerce")

        # -----------------------------
        # 2. thermal_preference → numerisch
        # -----------------------------
        mapping_preference = {
            "warmer": 1,
            "no change": 0,
            "cooler": -1
        }
        df_sub["thermal_preference"] = df_sub["thermal_preference"].map(mapping_preference)

        # -----------------------------
        # 3. thermal_acceptability → numerisch
        # -----------------------------
        mapping_acceptability = {
            "acceptable": 1,
            "unacceptable": 0,
            "Unknown": None   # Unknown → NaN
        }
        df_sub["thermal_acceptability"] = df_sub["thermal_acceptability"].map(mapping_acceptability)

        # -----------------------------
        # 4. Zeilen mit fehlenden Werten entfernen
        # -----------------------------
        df_sub = df_sub.dropna()

        # -----------------------------
        # 5. Korrelationsmatrix
        # -----------------------------
        corr_matrix = df_sub.corr(method="spearman")
        corr_matrix = corr_matrix.rename(index=german_labels, columns=german_labels)


            # -----------------------------
            # 6. Heatmap anzeigen
            # -----------------------------
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            linewidths=0.5,
            ax=ax
        )
        ax.set_title("Korrelationsmatrix der subjektiven Komfortvariablen")
        st.pyplot(fig)
        st.caption(
        "Diese Korrelationsmatrix zeigt, wie stark die subjektiven Komfortparameter – "
        "thermische Empfinden, Akzeptanz, Präferenz und Komfortbewertung – miteinander "
        "verbunden sind.")

    with col2:

        # --- Werte aus der deutschen Korrelationsmatrix ---
        r_ts_tp = corr_matrix.loc["Thermische Empfinden", "Thermische Präferenz"]
        r_ts_tc = corr_matrix.loc["Thermische Empfinden", "Thermischer Komfort"]
        r_tp_tc = corr_matrix.loc["Thermische Präferenz", "Thermischer Komfort"]
        r_ta_tc = corr_matrix.loc["Thermische Akzeptanz", "Thermischer Komfort"]

        # --- Farblogik basierend auf Heatmap ---
        def color_for_r(r):
            if r <= -0.50:
                return "#005BBB"   # starke negative Korrelation (blau)
            elif r <= -0.15:
                return "#5F9FE9"   # mittlere negative Korrelation
            elif r <= 0.17:
                return "#E9CDA0"   # schwach (grau)
            elif r < 0.50:
                return "#D9BA89"   # light orange
            else:
                return "#C0392B"   # starke positive Korrelation (rot)

        c_ts_tp = color_for_r(r_ts_tp)
        c_ts_tc = color_for_r(r_ts_tc)
        c_tp_tc = color_for_r(r_tp_tc)
        c_ta_tc = color_for_r(r_ta_tc)

        # --- PANEL MIT KURZEN ERKLÄRUNGEN ---
        st.markdown(f"""
        <div style="padding-left: 12px; margin-bottom: 14px;">
            <h5 style="margin:0;">Empfinden ↔ Präferenz  
            <span style="color:{c_ts_tp}; font-weight:bold;">(r = {r_ts_tp:.2f})</span></h4>
            • Moderate negative Korrelation<br>
            • Je wärmer man sich fühlt, desto stärker bevorzugt man kühlere Bedingungen
        </div>

        <div style="padding-left: 12px; margin-bottom: 14px;">
            <h5 style="margin:0;">Empfinden ↔ Komfort  
            <span style="color:{c_ts_tc}; font-weight:bold;">(r = {r_ts_tc:.2f})</span></h4>
            • Schwache negative Korrelation<br>
            • Mehr Wärmeempfindung führt zu leicht geringerem Komfort
 
        </div>

        <div style="padding-left: 12px; margin-bottom: 14px;">
            <h5 style="margin:0;">Präferenz ↔ Komfort  
            <span style="color:{c_tp_tc}; font-weight:bold;">(r = {r_tp_tc:.2f})</span></h4>
            • Sehr schwache positive Korrelation<br>
            • Die Präferenz beeinflusst den Komfort nur minimal<br>
        </div>

        <div style="padding-left: 12px; margin-bottom: 14px;">
            <h5 style="margin:0;"> Akzeptanz ↔ Komfort  
            <span style="color:{r_ta_tc}; font-weight:bold;">(r = {r_ta_tc:.2f})</span></h4>
            • Schwache positive Korrelation<br>
            • Akzeptable Bedingungen werden als etwas komfortabler empfunden<br>
        </div>
        """, unsafe_allow_html=True)




###########################################################################################################################
###########################################################################################################################

    with st.expander("📊 Beziehungsdiagramme mit Bivariaten Scatterplots"):

        st.markdown("## 📊 Beziehungsdiagramme mit Bivariaten Scatterplots")

        st.write("Die Histogramme auf der Diagonalen zeigen die grundlegenden statistischen Muster der vier Komfortvariablen")

        col01, col02 = st.columns([1.8, 1])   # linke Spalte etwas breiter für die Heatmap


        with col01:

            # Relevant columns
            cols = [
                "thermal_sensation",
                "thermal_acceptability",
                "thermal_preference",
                "thermal_comfort"
            ]

            df_sub = df[cols].copy()

            # Numeric conversions
            df_sub["thermal_sensation"] = pd.to_numeric(df_sub["thermal_sensation"], errors="coerce")
            df_sub["thermal_comfort"] = pd.to_numeric(df_sub["thermal_comfort"], errors="coerce")

            df_sub["thermal_preference"] = df_sub["thermal_preference"].map({
                "warmer": 1,
                "no change": 0,
                "cooler": -1
            })

            df_sub["thermal_acceptability"] = df_sub["thermal_acceptability"].map({
                "acceptable": 1,
                "unacceptable": 0,
                "Unknown": None
            })

            # Remove rows with missing values
            df_sub = df_sub.dropna()

            # Rename columns to German labels
            df_sub = df_sub.rename(columns=german_labels)

            # PairGrid for scatterplots + histograms + correlations
            g = sns.PairGrid(df_sub)

            # Diagonal: histograms
            g.map_diag(sns.histplot, kde=True, color="#0A2540")

            # Lower triangle: scatter plots
            g.map_lower(sns.scatterplot, alpha=0.6, color="#0A2540")

            # Upper triangle: correlation coefficients
            def corr_coefficient(x, y, **kwargs):
                r = np.corrcoef(x, y)[0, 1]
                ax = plt.gca()
                ax.annotate(
                    f"r = {r:.2f}",
                    xy=(0.5, 0.5),
                    xycoords="axes fraction",
                    ha="center",
                    va="center",
                    fontsize=12,
                    color="red"
                )

            g.map_upper(corr_coefficient)

            st.pyplot(g.fig)



        with col02:
            st.markdown("""

        - **Thermische Empfinden:** Die Werte konzentrieren sich überwiegend im **neutralen Bereich (0)**, was auf eine typische thermische Wahrnehmung in regulierten Innenräumen hinweist.

        - **Thermische Akzeptanz:** Die Verteilung ist stark **nach oben verzerrt (Wert = 1)**. Dies bedeutet, dass die meisten Personen den thermischen Zustand als **akzeptabel** einstufen.

        - **Thermische Präferenz:** Ein deutlicher Peak bei **0 („keine Veränderung gewünscht“)“** zeigt, dass die Mehrheit keine thermische Anpassung bevorzugt. Kleinere Anteile wünschen kühlere oder wärmere Bedingungen.

        - **Thermischer Komfort:** Die Werte häufen sich im **oberen Bereich (4–5)**, was auf ein insgesamt **hohes Komfortniveau** der befragten Personen hinweist.
            """)

   ###########################################################################################################################
   ###########################################################################################################################
   ###########################################################################################################################
   ###########################################################################################################################

        # -----------------------------
    # REGIONEN ERMITTELN
    # -----------------------------
    if "region" not in df.columns:
        st.error("Die Spalte 'region' existiert nicht im DataFrame.")
    else:
        region_list = sorted(df["region"].dropna().unique().tolist())
        st.markdown("### 🔥 Korrelationsmatrizen nach Region")

    # Deutsche Labels
    german_labels = {
        "thermal_sensation": "Thermische Empfinden",
        "thermal_acceptability": "Thermische Akzeptanz",
        "thermal_preference": "Thermische Präferenz",
        "thermal_comfort": "Thermischer Komfort"
    }

    for region in region_list:

        with st.expander(f"🌍 Region: **{region}**", expanded=False):

            # -----------------------------
            # Daten filtern
            # -----------------------------
            df_region = df[df["region"] == region].copy()

            cols = [
                "thermal_sensation",
                "thermal_acceptability",
                "thermal_preference",
                "thermal_comfort"
            ]

            df_sub = df_region[cols].copy()

            # -----------------------------
            # Numerische Umwandlung
            # -----------------------------
            df_sub["thermal_sensation"] = pd.to_numeric(df_sub["thermal_sensation"], errors="coerce")
            df_sub["thermal_comfort"] = pd.to_numeric(df_sub["thermal_comfort"], errors="coerce")

            df_sub["thermal_preference"] = df_sub["thermal_preference"].map({
                "warmer": 1, "no change": 0, "cooler": -1
            })

            df_sub["thermal_acceptability"] = df_sub["thermal_acceptability"].map({
                "acceptable": 1, "unacceptable": 0, "Unknown": None
            })

            df_sub = df_sub.dropna()

            if df_sub.empty:
                st.warning(f"⚠️ Keine gültigen Daten für Region: {region}")
                continue

            # -----------------------------
            # Korrelationsmatrix
            # -----------------------------
            corr_matrix = df_sub.corr(method="spearman")
            corr_matrix = corr_matrix.rename(index=german_labels, columns=german_labels)

            # -----------------------------
            # Zwei Spalten für die Grafiken
            # -----------------------------
            colA, colB = st.columns(2)

            # -----------------------------
            # HEATMAP (links)
            # -----------------------------
            with colA:
                fig1, ax1 = plt.subplots(figsize=(6, 5))
                sns.heatmap(
                    corr_matrix,
                    annot=True,
                    cmap="coolwarm",
                    vmin=-1,
                    vmax=1,
                    linewidths=0.5,
                    ax=ax1
                )
                ax1.set_title(f"Korrelationsmatrix – {region}")
                st.pyplot(fig1)

            # -----------------------------
            # SCATTER-PLOT MATRIX (rechts)
            # -----------------------------
            with colB:
                g = sns.PairGrid(df_sub.rename(columns=german_labels))
                g.map_diag(sns.histplot, kde=True, color="#0A2540")
                g.map_lower(sns.scatterplot, alpha=0.6, color="#0A2540")

                def corr_text(x, y, **kwargs):
                    r = np.corrcoef(x, y)[0, 1]
                    ax = plt.gca()
                    ax.annotate(
                        f"r = {r:.2f}",
                        xy=(0.5, 0.5),
                        xycoords="axes fraction",
                        ha="center", va="center",
                        fontsize=10, color="red"
                    )

                g.map_upper(corr_text)

                st.pyplot(g.fig)

            # -----------------------------
            # Beschreibung
            # -----------------------------
            st.markdown("""
            **Kurzbeschreibung:**  
            Diese Darstellungen zeigen die regionalen Zusammenhänge zwischen thermischer Empfinden,
            Akzeptanz, Präferenz und Komfort. Die Heatmap visualisiert die Stärke der Korrelationen,
            während die Scatterplots die bivariaten Beziehungen zwischen den Variablen darstellen.
            """)

    







with tab2:
    st.subheader("Welche Gruppen benötigen kühlere oder wärmere Bedingungen für Komfort?")
    st.text("Die Neutraltemperatur zeigt, bei welcher Raumtemperatur Menschen weder Wärme noch Kälte empfinden – sie ist damit der zentrale Vergleichswert für unterschiedliche Komfortpräferenzen.")

    st.markdown(
    """
    **Verständnis der Neutraltemperatur (ASCII‑Grafik):**

           zu kalt              neutral              zu warm
        (MTS < 0)             (MTS = 0)            (MTS > 0)
              \\                 |                 /
               \\                |                /
                \\               |               /
                 \\______________|______________/
                               T_neutral
""")

#    Die Waage zeigt:

#     - Links: Personen empfinden die Temperatur als **zu kalt** (negative MTS‑Werte).
#     - Rechts: Personen empfinden die Temperatur als **zu warm** (positive MTS‑Werte).
#     - In der Mitte: **Neutraltemperatur T_neutral**, bei der die mittlere Empfindung MTS = 0 ist.


    # ============================================================
    # LOAD DATA
    # ============================================================

    @st.cache_data
    def load_data():
        df = pd.read_csv("db_bereinigt_final.csv")
        df["operative_temperature"] = pd.to_numeric(df["operative_temperature"], errors="coerce")
        df["thermal_sensation"] = pd.to_numeric(df["thermal_sensation"], errors="coerce")
        return df.dropna(subset=["operative_temperature", "thermal_sensation"])
    df = load_data()

    
    # ============================================================
    # GERMAN EXPLANATION
    # ============================================================

    # st.markdown(
    #     "**Beschreibung (Deutsch):**\n"
    #     "Dieses Diagramm zeigt die mittlere thermische Empfindung (Mean Thermal Sensation, MTS) "
    #     "in Abhängigkeit von der Innenraumtemperatur. Für jede automatisch erkannte Kategorie "
    #     "wird eine lineare Regression berechnet, aus der die neutrale Temperatur (MTS = 0) "
    #     "abgeleitet wird. Die vertikale gestrichelte Linie markiert diese neutrale Temperatur."
    # )

# ============================================================
# AUTOMATIC GROUPING
# ============================================================

    grouping_priority = ["building_type", "season", "gender", "region", "country", "city"]

    column_to_group = None
    for col in grouping_priority:
        if df_filtered[col].nunique() > 1:
            column_to_group = col
            break

    if column_to_group is None:
        column_to_group = "building_type"

    groups = df_filtered[column_to_group].dropna().unique()

    # ============================================================
    # PLOT
    # ============================================================

    if df_filtered.empty:
        st.warning("Für die ausgewählten Filter sind keine Daten verfügbar.")
        st.stop()

    results = []

    # Primero calculamos neutral_temp para cada grupo
    for g in groups:

        sub = df_filtered[df_filtered[column_to_group] == g]

        if sub.empty:
            continue

        mts_df = sub.groupby("operative_temperature")["thermal_sensation"].mean().reset_index()
        mts_df.columns = ["operative_temperature", "MTS"]
        mts_df = mts_df.dropna()

        if mts_df.empty or len(mts_df) < 2:
            continue

        X = mts_df["operative_temperature"].values.reshape(-1, 1)
        y = mts_df["MTS"].values.reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        a = model.coef_[0][0]
        b = model.intercept_[0]
        r2 = model.score(X, y)
        neutral_temp = -b / a

        results.append([g, a, b, r2, neutral_temp])

    # ============================================================
    # SI NO HAY GRUPOS CON DATOS SUFICIENTES → SALIR
    # ============================================================

    if len(results) == 0:
        st.warning("Keine Gruppe verfügt über ausreichende Daten, um die neutrale Temperatur zu berechnen.")
        st.stop()

    # ============================================================
    # ORDENAR GRUPOS POR NEUTRAL TEMP (mayor → menor)
    # ============================================================

    results_sorted = sorted(results, key=lambda x: x[4], reverse=True)
    groups_sorted = [r[0] for r in results_sorted]

    # ============================================================
    # MOSTRAR TABLA DE NEUTRAL TEMP ARRIBA DEL GRÁFICO
    # ============================================================

    st.markdown("### 🔥 Sortiert nach Neutraltemperatur (höher → niedriger)")

    st.write(f"Aktuelle Filter : {filter_text}")


    # ============================================================
    # CREAR FIGURA
    # ============================================================

    fig, axes = plt.subplots(1, len(groups_sorted), figsize=(16, 5), sharey=True)

    if len(groups_sorted) == 1:
        axes = [axes]

    colors = plt.cm.tab10(np.linspace(0, 1, len(groups_sorted)))
    markers = ["o", "s", "^", "D", "P", "X", "*"]
    color_map = dict(zip(groups_sorted, colors))
    marker_map = dict(zip(groups_sorted, markers))

    # ============================================================
    # DIBUJAR CADA GRUPO (ya ordenado)
    # ============================================================

    for ax, (g, a, b, r2, neutral_temp) in zip(axes, results_sorted):

        sub = df_filtered[df_filtered[column_to_group] == g]
        mts_df = sub.groupby("operative_temperature")["thermal_sensation"].mean().reset_index()
        mts_df.columns = ["operative_temperature", "MTS"]
        mts_df = mts_df.dropna()

        x_range = np.linspace(mts_df["operative_temperature"].min(),
                            mts_df["operative_temperature"].max(), 100)
        y_pred = a * x_range + b

        ax.plot(x_range, y_pred, color=color_map[g], linewidth=2)
        ax.scatter(
            mts_df["operative_temperature"],
            mts_df["MTS"],
            color=color_map[g],
            marker=marker_map[g],
            s=60,
            edgecolor="black",
            linewidth=0.6
        )
        ax.axvline(neutral_temp, color=color_map[g], linestyle="--", linewidth=1.5)

        ax.text(
            0.05, 0.95,
            f"T_neutral = {neutral_temp:.2f} °C",
            transform=ax.transAxes,
            fontsize=12,
            color=color_map[g],
            verticalalignment="top",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor=color_map[g])
        )

        ax.set_title(g)
        ax.set_xlabel("Indoor Temperature (°C)")
        ax.grid(True)

    axes[0].set_ylabel("Mean Thermal Sensation (MTS)")
    fig.suptitle(f"MTS vs Innentemperatur", fontsize=18)
    plt.tight_layout()
    st.pyplot(fig)

    st.caption("""
    Die Grafik zeigt, wie sich die mittlere thermische Empfinden (MTS) in verschiedenen Kategorien mit der Innenraumtemperatur verändert. 
    Die sortierte Tabelle oben verdeutlicht, welche Gruppen niedrigere oder höhere T_neutral‑Werte aufweisen und damit kühlere bzw. wärmere Bedingungen als komfortabel empfinden.
    """)

    for g, a, b, r2, nt in results_sorted:
        st.markdown(f"**{g}:** Neutraltemperatur = **{nt:.2f} °C**")


    # ============================================================
    # SUMMARY TABLE
    # ============================================================

    if results:
        summary_df = pd.DataFrame(
            results,
            columns=[column_to_group, "Steigung a", "Achsenabschnitt b", "R²", "Neutraltemperatur"]
        )

        # ORDENAR DE MAYOR A MENOR POR TEMPERATURA NEUTRAL
        summary_df = summary_df.sort_values("Neutraltemperatur", ascending=False)

        st.subheader("Zusammenfassung der neutralen Temperatur")

        st.dataframe(
            summary_df.style.format({
                "Steigung a": "{:.2f}",
                "Achsenabschnitt b": "{:.2f}",
                "R²": "{:.2f}",
                "Neutraltemperatur": "{:.2f}"
            })
        )
    else:
        st.info("Keine gültigen Regressionsresultate für die ausgewählten Filter.")


#########################################################################################################################
#########################################################################################################################

########################################################################################################################
########################################################################################################################
########################################################################################################################

with tab3:

    # ============================================================
    # EINLEITUNG – kurz, neutral, wissenschaftlich
    # ============================================================

    #st.header("Adaptives Komfortmodell nach ASHRAE 55")

    st.subheader("Welche Kategorie erfüllt die Komfortanforderungen am besten?")
    st.write(
    "Die folgende Analyse untersucht, wie gut verschiedene Kategorien die thermischen "
    "Komfortanforderungen nach dem adaptiven ASHRAE‑55‑Modell erfüllen. "
    "Durch den Vergleich der Komfort‑Compliance wird sichtbar, welche Gruppen sich am "
    "besten an die Außentemperatur anpassen und in welchen Kategorien deutliche Abweichungen "
    "vom Komfortbereich auftreten."
)

    st.markdown(
        """
        **Was zeigt die Grafik?**

        - Die Komfortzonen (80 % und 90 %) geben Bereiche an, in denen die Mehrheit der Personen
          thermischen Komfort empfindet.
        - Punkte oberhalb der Komfortzonen weisen auf mögliche Überhitzung hin.
        - Punkte unterhalb der Komfortzonen deuten auf Unterkühlung oder verstärkte Luftbewegung hin.
        - Die Streuung der Messpunkte zeigt, wie unterschiedlich Gebäude, Nutzungsarten oder Klimata
          auf die Außentemperatur reagieren.
        """
    )

    # ============================================================
    # 1. LOAD DATA
    # ============================================================

    df = pd.read_csv("db_bereinigt_final.csv")

    cols_to_numeric = [
        "operative_temperature",
        "outdoor_air_temperature",
        "clothing_ensemble_insulation",
        "metabolic_rate",
        "thermal_sensation",
        "thermal_comfort"
    ]

    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=[
        "operative_temperature",
        "outdoor_air_temperature",
        "season",
        "city",
        "country",
        "region"
    ])

    # ============================================================
    # 2. FILTERS – zwei Spalten
    # ============================================================

    colA, colB = st.columns([0.7,2.3])

    with colA:

        st.subheader("Filter")

        region_list = sorted(df["region"].dropna().unique())
        region = st.selectbox("Region", ["Alle"] + region_list)
        if region != "Alle":
            df = df[df["region"] == region]

        country_list = sorted(df["country"].dropna().unique())
        country = st.selectbox("Land", ["Alle"] + country_list)
        if country != "Alle":
            df = df[df["country"] == country]

        city_list = sorted(df["city"].dropna().unique())
        city = st.selectbox("Stadt", ["Alle"] + city_list)
        if city != "Alle":
            df = df[df["city"] == city]

        # Gruppierung NUR für Einzelplots
        column_to_group = st.selectbox(
            "Kategorie für Einzelplots:",
            ["season", "climate", "building_type", "cooling_type", "gender", "age", "country", "region"]
        )


        
    # ============================================================
    # 3. SORT BY OUTDOOR TEMPERATURE
    # ============================================================

    df_sorted = df.sort_values(by="outdoor_air_temperature")

    T_out = df_sorted["outdoor_air_temperature"]
    T_in = df_sorted["operative_temperature"]

    # ============================================================
    # 4. ADAPTIVE COMFORT LIMITS
    # ============================================================

    T_comf = 0.31 * T_out + 17.8
    T_lower_80 = T_comf - 2.5
    T_upper_80 = T_comf + 2.5
    T_lower_90 = T_comf - 3.5
    T_upper_90 = T_comf + 3.5


    with colB:

        # ============================================================
        # 5. MAIN PLOT – Adaptive Comfort Chart
        # ============================================================

        # Titel mit aktiven Filtern
        active_filters = []
        if region != "Alle": active_filters.append(f"Region: {region}")
        if country != "Alle": active_filters.append(f"Land: {country}")
        if city != "Alle": active_filters.append(f"Stadt: {city}")

        filter_text = ", ".join(active_filters) if active_filters else "Keine Filter aktiv"

        st.subheader("Adaptive Comfort Chart")
        st.caption(f"Aktive Filter: {filter_text}")

        fig, ax = plt.subplots(figsize=(12, 7))

        ax.fill_between(T_out, T_lower_90, T_upper_90, color="yellow", alpha=0.15, label="90 % Komfortzone")
        ax.fill_between(T_out, T_lower_80, T_upper_80, color="green", alpha=0.20, label="80 % Komfortzone")

        ax.scatter(
            df_sorted["outdoor_air_temperature"],
            df_sorted["operative_temperature"],
            color="blue",
            alpha=0.7,
            edgecolor="black",
            linewidth=0.5,
            label="Messpunkte"
        )

        ax.set_xlabel("Außentemperatur (°C)")
        ax.set_ylabel("Operative Innentemperatur (°C)")
        ax.set_title("ASHRAE 55 – Adaptives Komfortmodell")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)
        st.caption(
    "Adaptive Komfortkurve nach ASHRAE 55 für alle gefilterten Daten. "
    "Die farbigen Bereiche markieren die 80 %‑ und 90 %‑Komfortzonen, während die Punkte die "
    "tatsächlichen Messwerte darstellen. So wird sichtbar, wie gut die Daten mit dem Modell "
    "übereinstimmen und ob Tendenzen zu Überhitzung oder Unterkühlung auftreten.")



    # ============================================================
    # 6. EINZELPLOTS – max. 3 pro Reihe
    # ============================================================

    st.subheader("Einzelplots pro Kategorie")
    st.text(
    "Die Einzelplots zeigen jede ausgewählte Kategorie separat. Dadurch wird sichtbar, "
    "wie sich unterschiedliche Gruppen innerhalb der Komfortzonen verhalten und ob "
    "bestimmte Klimata, Gebäudetypen oder Nutzungsarten systematisch von den "
    "Komfortbereichen abweichen.")


    unique_groups = df[column_to_group].dropna().unique()
    palette = sns.color_palette("tab10", len(unique_groups))
    color_map = dict(zip(unique_groups, palette))

    num_groups = len(unique_groups)

    # Fall 1: Nur eine Kategorie → großer Plot
    if num_groups == 1:
        group = unique_groups[0]
        subset = df_sorted[df_sorted[column_to_group] == group]

        fig, ax = plt.subplots(figsize=(10, 6))

        T_out_sub = subset["outdoor_air_temperature"]
        T_comf_sub = 0.31 * T_out_sub + 17.8

        ax.fill_between(T_out_sub, T_comf_sub - 3.5, T_comf_sub + 3.5,
                        color="yellow", alpha=0.15)
        ax.fill_between(T_out_sub, T_comf_sub - 2.5, T_comf_sub + 2.5,
                        color="green", alpha=0.20)

        ax.scatter(
            subset["outdoor_air_temperature"],
            subset["operative_temperature"],
            color=color_map[group],
            edgecolor="black",
            alpha=0.85,
            linewidth=0.5
        )

        ax.set_title(f"{column_to_group}: {group}")
        ax.set_xlabel("Außentemperatur (°C)")
        ax.set_ylabel("Operative Innentemperatur (°C)")
        ax.grid(True)

        st.pyplot(fig)

    # Fall 2: Zwei Kategorien → zwei große Plots nebeneinander
    elif num_groups == 2:
        col1, col2 = st.columns(2)

        for col, group in zip([col1, col2], unique_groups):
            subset = df_sorted[df_sorted[column_to_group] == group]

            fig, ax = plt.subplots(figsize=(8, 5))

            T_out_sub = subset["outdoor_air_temperature"]
            T_comf_sub = 0.31 * T_out_sub + 17.8

            ax.fill_between(T_out_sub, T_comf_sub - 3.5, T_comf_sub + 3.5,
                            color="yellow", alpha=0.15)
            ax.fill_between(T_out_sub, T_comf_sub - 2.5, T_comf_sub + 2.5,
                            color="green", alpha=0.20)

            ax.scatter(
                subset["outdoor_air_temperature"],
                subset["operative_temperature"],
                color=color_map[group],
                edgecolor="black",
                alpha=0.85,
                linewidth=0.5
            )

            ax.set_title(f"{column_to_group}: {group}")
            ax.set_xlabel("Außentemperatur (°C)")
            ax.set_ylabel("Operative Innentemperatur (°C)")
            ax.grid(True)

            col.pyplot(fig)

    # Fall 3: Drei oder mehr Kategorien → max. 3 pro Reihe
    else:
        rows = (num_groups + 2) // 3
        idx = 0

        for r in range(rows):
            cols = st.columns(3)
            for c in range(3):
                if idx >= num_groups:
                    break

                group = unique_groups[idx]
                subset = df_sorted[df_sorted[column_to_group] == group]

                fig, ax = plt.subplots(figsize=(6, 4))

                T_out_sub = subset["outdoor_air_temperature"]
                T_comf_sub = 0.31 * T_out_sub + 17.8

                ax.fill_between(T_out_sub, T_comf_sub - 3.5, T_comf_sub + 3.5,
                                color="yellow", alpha=0.15)
                ax.fill_between(T_out_sub, T_comf_sub - 2.5, T_comf_sub + 2.5,
                                color="green", alpha=0.20)

                ax.scatter(
                    subset["outdoor_air_temperature"],
                    subset["operative_temperature"],
                    color=color_map[group],
                    edgecolor="black",
                    alpha=0.85,
                    linewidth=0.5
                )

                ax.set_title(f"{column_to_group}: {group}")
                ax.set_xlabel("Außentemperatur (°C)")
                ax.set_ylabel("Operative Innentemperatur (°C)")
                ax.grid(True)

                cols[c].pyplot(fig)
                idx += 1

        

# ============================================================
# 6. Komfort‑Compliance pro Kategorie
# ============================================================

    st.subheader("Komfort‑Compliance pro Kategorie")

    compliance_rows = []

    for group in unique_groups:
        subset = df_sorted[df_sorted[column_to_group] == group]

        if subset.empty:
            continue

        T_out_sub = subset["outdoor_air_temperature"]
        T_comf_sub = 0.31 * T_out_sub + 17.8

        T_lower_80_sub = T_comf_sub - 2.5
        T_upper_80_sub = T_comf_sub + 2.5

        T_lower_90_sub = T_comf_sub - 3.5
        T_upper_90_sub = T_comf_sub + 3.5

        inside_80 = ((subset["operative_temperature"] >= T_lower_80_sub) &
                    (subset["operative_temperature"] <= T_upper_80_sub)).mean()

        inside_90 = ((subset["operative_temperature"] >= T_lower_90_sub) &
                    (subset["operative_temperature"] <= T_upper_90_sub)).mean()

        compliance_rows.append([
            group,
            round(inside_80 * 100, 1),
            round(inside_90 * 100, 1)
        ])

    df_compliance = pd.DataFrame(
        compliance_rows,
        columns=["Kategorie", "80%-Komfortzone (%)", "90%-Komfortzone (%)"]
    )

    st.dataframe(df_compliance)



# # ============================================================
# # 7. Dynamische Interpretation der Grafik
# # ============================================================

#     st.subheader("Dynamische Interpretation der Ergebnisse")

#     # Anteil der Punkte innerhalb der Komfortzonen
#     inside_80 = ((df_sorted["operative_temperature"] >= T_lower_80) &
#                 (df_sorted["operative_temperature"] <= T_upper_80)).mean()

#     inside_90 = ((df_sorted["operative_temperature"] >= T_lower_90) &
#                 (df_sorted["operative_temperature"] <= T_upper_90)).mean()

#     # Durchschnittliche operative Temperatur
#     avg_T_in = df_sorted["operative_temperature"].mean()

#     # Durchschnittliche Außentemperatur
#     avg_T_out = df_sorted["outdoor_air_temperature"].mean()

#     # Dynamische Textanalyse
#     interpretation = f"""
#     **Kurze Auswertung basierend auf deinen Daten:**

#     - Die durchschnittliche Außentemperatur beträgt **{avg_T_out:.1f} °C**.
#     - Die durchschnittliche operative Innentemperatur liegt bei **{avg_T_in:.1f} °C**.

#     **Komfortbewertung nach ASHRAE 55:**

#     - **{inside_80*100:.1f}%** aller Messpunkte liegen innerhalb der **80%-Komfortzone**.
#     - **{inside_90*100:.1f}%** aller Messpunkte liegen innerhalb der **90%-Komfortzone**.

#     **Was bedeutet das?**

#     - Wenn viele Punkte in den grünen Bereich fallen, zeigt das eine **hohe Übereinstimmung mit dem adaptiven Komfortmodell**.
#     - Punkte oberhalb der Komfortzonen deuten auf **Überhitzung** hin (z. B. unzureichende Kühlung oder hohe interne Lasten).
#     - Punkte unterhalb der Komfortzonen weisen auf **Unterkühlung** hin (z. B. starke Lüftung, kalte Außenbedingungen oder hohe Luftbewegung).
#     - Die Streuung der Punkte zeigt, wie **unterschiedlich Nutzer oder Gebäude auf Außenbedingungen reagieren**.

#     **Interpretation für die Gruppierung „{column_to_group}“:**

#     - Gruppen, die überwiegend im Komfortbereich liegen, weisen auf **gute adaptive Anpassung** hin.
#     - Gruppen außerhalb der Komfortzonen könnten **saisonale Effekte**, **Gebäudetypen**, **Nutzungsverhalten** oder **klimatische Besonderheiten** widerspiegeln.
#     """

#     st.markdown(interpretation)



# # ============================================================
# # 7. Automatische Interpretation pro Kategorie
# # ============================================================

#     st.subheader("Automatische Interpretation pro Kategorie")

#     interpretation_text = ""

#     for group, inside80, inside90 in zip(
#         df_compliance["Kategorie"],
#         df_compliance["80%-Komfortzone (%)"],
#         df_compliance["90%-Komfortzone (%)"]
#     ):

#         # Interpretation basierend auf Komfortanteilen
#         if inside80 >= 70:
#             comfort_statement = (
#                 f"Die Kategorie **{group}** weist eine hohe Übereinstimmung mit dem adaptiven "
#                 f"Komfortmodell auf. Mit **{inside80}%** der Messpunkte innerhalb der 80%-Komfortzone "
#                 f"befindet sich der Großteil der Werte im thermisch akzeptablen Bereich."
#             )
#         elif inside80 >= 40:
#             comfort_statement = (
#                 f"Die Kategorie **{group}** zeigt eine gemischte Komfortsituation. "
#                 f"Etwa **{inside80}%** der Messpunkte liegen innerhalb der 80%-Komfortzone, "
#                 f"was auf teilweise gute, aber nicht durchgehend stabile Komfortbedingungen hinweist."
#             )
#         else:
#             comfort_statement = (
#                 f"Die Kategorie **{group}** weist eine geringe Übereinstimmung mit dem adaptiven "
#                 f"Komfortmodell auf. Nur **{inside80}%** der Messpunkte liegen innerhalb der "
#                 f"80%-Komfortzone, was auf mögliche Überhitzung oder Unterkühlung hindeutet."
#             )

#         # Ergänzung basierend auf 90%-Zone
#         if inside90 >= 80:
#             detail_statement = (
#                 f"Zusätzlich liegen **{inside90}%** der Messpunkte innerhalb der 90%-Komfortzone, "
#                 f"was eine insgesamt stabile thermische Situation bestätigt."
#             )
#         elif inside90 >= 50:
#             detail_statement = (
#                 f"Mit **{inside90}%** innerhalb der 90%-Komfortzone zeigt sich eine moderate "
#                 f"Komfortlage mit deutlicher Streuung."
#             )
#         else:
#             detail_statement = (
#                 f"Nur **{inside90}%** der Messpunkte liegen innerhalb der 90%-Komfortzone, "
#                 f"was auf stark variierende Bedingungen oder deutliche Abweichungen vom Modell hinweist."
#             )

#         interpretation_text += f"- {comfort_statement} {detail_statement}\n\n"

#     st.markdown(interpretation_text)



# ============================================================
# 8. Natürliche Zusammenfassung: Welche Kategorie ist am besten?
# ============================================================

    with st.expander("Zusammenfassung"):
        # st.subheader("Zusammenfassung")

        # Beste und schlechteste Kategorie anhand der 80%-Komfortzone
        best_row = df_compliance.loc[df_compliance["80%-Komfortzone (%)"].idxmax()]
        worst_row = df_compliance.loc[df_compliance["80%-Komfortzone (%)"].idxmin()]

        best_cat = best_row["Kategorie"]
        best_80 = best_row["80%-Komfortzone (%)"]
        best_90 = best_row["90%-Komfortzone (%)"]

        worst_cat = worst_row["Kategorie"]
        worst_80 = worst_row["80%-Komfortzone (%)"]
        worst_90 = worst_row["90%-Komfortzone (%)"]

        summary_text = f"""
        **Welche Kategorie zeigt die beste Komfortleistung?**

        Die Kategorie **{best_cat}** weist die höchste Übereinstimmung mit dem adaptiven Komfortmodell auf.
        Mit **{best_80}%** innerhalb der 80%-Komfortzone und **{best_90}%** innerhalb der 90%-Komfortzone
        zeigt diese Gruppe die stabilsten thermischen Bedingungen.

        **Welche Kategorie schneidet am schlechtesten ab?**

        Die Kategorie **{worst_cat}** liegt mit nur **{worst_80}%** in der 80%-Komfortzone deutlich unter den
        anderen Gruppen. Auch die 90%-Komfortzone (**{worst_90}%**) zeigt eine geringere Übereinstimmung,
        was auf stärkere Abweichungen vom Komfortmodell hindeutet.

        **Was bedeutet das insgesamt?**

        Die Analyse zeigt, dass sich die Kategorien klar unterscheiden: Einige Gruppen passen sich gut an
        die Außentemperatur an und bleiben überwiegend innerhalb der Komfortbereiche, während andere
        deutliche Tendenzen zu Überhitzung oder Unterkühlung aufweisen. Diese Unterschiede können durch
        Gebäudetypen, Klimazonen, Nutzungsverhalten oder saisonale Effekte beeinflusst sein.
        """

        st.markdown(summary_text)


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

with tab4:

    st.subheader("Welche physikalischen Faktoren beeinflussen den thermischen Komfort am stärksten?")

    # st.write(
    # """
    # • Metabolische Aktivität (met) bestimmt die körpereigene Wärmeproduktion und beeinflusst,
    #   wie schnell Personen Wärme abgeben oder speichern.

    # • Bekleidungsisolation (Clo-Wert) verändert die Wärmeabgabe des Körpers und verschiebt
    #   die individuelle Neutraltemperatur.

    # • Lufttemperatur ist der stärkste direkte Einflussfaktor auf das thermische Empfinden
    #   und bestimmt die Wärmebilanz des Körpers.

    # • Luftgeschwindigkeit (Air Velocity) erhöht die konvektive Kühlung und kann warme
    #   Bedingungen deutlich erträglicher machen.

    # • Mittlere Strahlungstemperatur beeinflusst die Wärmeabgabe durch Strahlung und wirkt
    #   besonders in Räumen mit großen Fensterflächen oder warmen Oberflächen.

    # • Relative Luftfeuchtigkeit beeinflusst die Verdunstungskühlung und verstärkt
    #   Wärmebelastung bei hohen Temperaturen.
    # """
    # )

    st.write(
    "Diese Analyse untersucht die Zusammenhänge zwischen den wichtigsten physikalischen "
    "Einflussgrößen des thermischen Komforts. Dazu gehören metabolische Aktivität, "
    "Bekleidungsisolation, Lufttemperatur, Luftgeschwindigkeit, mittlere Strahlungstemperatur "
    "und relative Luftfeuchtigkeit. Die Korrelationsmatrix zeigt, welche dieser Variablen "
    "gemeinsam variieren und welche Faktoren besonders stark zur thermischen Belastung oder "
    "Entlastung beitragen. Dadurch lassen sich Muster erkennen, die für die Bewertung von "
    "Innenraumklima und Komfortbedingungen entscheidend sind."
    )


    # ============================================================
    # 1. Select relevant physical variables
    # ============================================================

    cols_phys = [
        "metabolic_rate",
        "clothing_ensemble_insulation",
        "air_temperature",
        "air_speed",
        "radiant_temperature",
        "relative_humidity"
    ]

    df_phys = df[cols_phys].copy()

    # Convert to numeric
    for c in cols_phys:
        df_phys[c] = pd.to_numeric(df_phys[c], errors="coerce")

    df_phys = df_phys.dropna()

    # ============================================================
    # 2. Compute correlation matrix (Spearman recommended)
    # ============================================================

    corr_matrix = df_phys.corr(method="spearman")

    # ============================================================
    # 3. Heatmap visualization
    # ============================================================

    st.subheader("Heatmap der physikalischen Komfortkorrelationen")

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        ax=ax
    )
    st.pyplot(fig)

    # ============================================================
    # 4. Scatter matrix (pairwise relationships)
    # ============================================================

    st.subheader("Pairwise Relationships (Scatter Matrix)")

    pairplot_fig = sns.pairplot(df_phys, diag_kind="kde")
    pairplot_fig.fig.set_size_inches(12, 10)  # optional resize

    st.pyplot(pairplot_fig.fig)
    st.caption(
        "Diese Analyse zeigt, wie die wichtigsten physikalischen Einflussgrößen des "
        "thermischen Komforts miteinander zusammenhängen. Die Korrelationen verdeutlichen, "
        "welche Faktoren gemeinsam auftreten und wie sie die thermische Wahrnehmung beeinflussen."
    )

    # ============================================================
    # 5. Automatic Interpretation
    # ============================================================

    st.subheader("Automatic Interpretation of Physical Comfort Correlations")

    interpret = []

    def add_if(condition, text):
        if condition:
            interpret.append(text)

    mr = corr_matrix["metabolic_rate"]
    clo = corr_matrix["clothing_ensemble_insulation"]
    ta = corr_matrix["air_temperature"]
    vel = corr_matrix["air_speed"]
    tr = corr_matrix["radiant_temperature"]
    rh = corr_matrix["relative_humidity"]

    # Metabolic Rate
    add_if(mr["air_temperature"] > 0.4,
        "- Höhere metabolische Aktivität korreliert mit höheren Lufttemperaturen.")
    add_if(mr["air_speed"] > 0.4,
        "- Personen mit höherem Metabolismus bevorzugen höhere Luftgeschwindigkeiten.")

    # Clothing
    add_if(clo["air_temperature"] < -0.4,
        "- Höhere Bekleidungsisolation tritt häufig bei niedrigeren Lufttemperaturen auf.")
    add_if(clo["radiant_temperature"] < -0.4,
        "- Mehr Kleidung wird bei geringerer Strahlungstemperatur getragen.")

    # Air Temperature
    add_if(ta["radiant_temperature"] > 0.6,
        "- Lufttemperatur und Strahlungstemperatur sind stark gekoppelt (hohe Wärmebelastung).")
    add_if(ta["relative_humidity"] > 0.4,
        "- Höhere Lufttemperaturen gehen oft mit höherer Luftfeuchtigkeit einher.")

    # Air Velocity
    add_if(vel["air_temperature"] < -0.4,
        "- Höhere Luftgeschwindigkeiten treten häufiger bei höheren Temperaturen auf (Kühlbedarf).")

    # Humidity
    add_if(rh["air_temperature"] > 0.4,
        "- Warme Bedingungen sind häufig feuchter, was die Verdunstungskühlung reduziert.")

    st.markdown("\n".join(interpret))



with tab5:

    st.subheader("Optimale Raumtemperatur nach Aktivität und Bekleidung")

    # Sicherstellen, dass die Felder numerisch sind
    df["metabolic_rate"] = pd.to_numeric(df["metabolic_rate"], errors="coerce")
    df["clothing_ensemble_insulation"] = pd.to_numeric(df["clothing_ensemble_insulation"], errors="coerce")

    # Nur gültige Zeilen
    df8 = df.dropna(subset=["metabolic_rate", "clothing_ensemble_insulation"])

    # Funktion zur Berechnung der optimalen Temperatur nach ISO 7730 (vereinfachte Näherung)
    def optimal_temp(met, clo):
        """
        Vereinfachte Näherung basierend auf ISO 7730:
        - höhere Aktivität → niedrigere optimale Temperatur
        - höhere Bekleidung → niedrigere optimale Temperatur
        """
        return 22 - (met - 1.2)*2 - (clo - 0.5)*4

    # Temperatur berechnen
    df8["optimal_temp"] = df8.apply(lambda r: optimal_temp(r["metabolic_rate"], r["clothing_ensemble_insulation"]), axis=1)

    # Plot vorbereiten
    fig, ax = plt.subplots(figsize=(6, 5))

    scatter = ax.scatter(
        df8["metabolic_rate"],
        df8["clothing_ensemble_insulation"],
        c=df8["optimal_temp"],
        cmap="coolwarm",
        s=70,
        edgecolor="black"
    )

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Optimale Raumtemperatur (°C)")

    ax.set_xlabel("Aktivität (met)")
    ax.set_ylabel("Bekleidung (clo)")
    ax.set_title("Optimale Raumtemperatur in Abhängigkeit von Aktivität und Bekleidung)")

    ax.grid(True)

    st.pyplot(fig)

######################################################################################################################################
######################################################################################################################################

   

    st.subheader("Optimale Raumtemperatur nach Aktivität und Bekleidung")
    # st.text("Diese Abbildung zeigt, wie sich die optimale Raumtemperatur in Abhängigkeit von Aktivitätsniveau (met) und Bekleidungsisolation (clo) verändert. Die Farbskala verdeutlicht die geschätzte Komforttemperatur. Typische Kleidungsetiketten – von kurzärmligen Sommeroutfits bis hin zu Jacken und Wintermänteln – machen sichtbar, dass schwerere Kleidung den Komfortbereich zu niedrigeren Temperaturen verschiebt, während leichtere Kleidung höhere Temperaturen erfordert.")

    # Asegurar que los campos sean numéricos
    df["metabolic_rate"] = pd.to_numeric(df["metabolic_rate"], errors="coerce")
    df["clothing_ensemble_insulation"] = pd.to_numeric(df["clothing_ensemble_insulation"], errors="coerce")

    df8 = df.dropna(subset=["metabolic_rate", "clothing_ensemble_insulation"])

    # Fórmula aproximada ISO 7730 para temperatura óptima
    def optimal_temp(met, clo):
        return 22 - (met - 1.2)*2 - (clo - 0.5)*4

    df8["optimal_temp"] = df8.apply(
        lambda r: optimal_temp(r["metabolic_rate"], r["clothing_ensemble_insulation"]),axis=1)

    fig, ax = plt.subplots(figsize=(8, 6))

    scatter = ax.scatter(
        df8["metabolic_rate"],
        df8["clothing_ensemble_insulation"],
        c=df8["optimal_temp"],
        cmap="coolwarm",
        s=80,
        edgecolor="black"
    )

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Optimale operative Temperatur (°C)")

    ax.set_xlabel("Aktivität (met)")
    ax.set_ylabel("Bekleidung (clo)")
    #ax.set_title("Optimale Raumtemperatur in Abhängigkeit von Aktivität und Bekleidung")
    ax.grid(True)


    with st.expander("Optimale Raumtemperatur in Abhängigkeit von Aktivität und Bekleidung - mit Labels"):

        # Ensure numeric fields
        df["metabolic_rate"] = pd.to_numeric(df["metabolic_rate"], errors="coerce")
        df["clothing_ensemble_insulation"] = pd.to_numeric(df["clothing_ensemble_insulation"], errors="coerce")

        df8 = df.dropna(subset=["metabolic_rate", "clothing_ensemble_insulation"])

        # Simplified ISO 7730 formula for optimal temperature
        def optimal_temp(met, clo):
            return 22 - (met - 1.2)*2 - (clo - 0.5)*4

        df8["optimal_temp"] = df8.apply(
            lambda r: optimal_temp(r["metabolic_rate"], r["clothing_ensemble_insulation"]),
            axis=1)

        fig, ax = plt.subplots(figsize=(8, 6))

        scatter = ax.scatter(
            df8["metabolic_rate"],
            df8["clothing_ensemble_insulation"],
            c=df8["optimal_temp"],
            cmap="coolwarm",
            s=80,
            edgecolor="black"
        )

        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label("Optimal operative temperature (°C)")
        ax.set_xlabel("Aktivität (met)")
        ax.set_ylabel("Bekleidung (clo)")
        ax.set_title("Optimale Raumtemperatur nach Aktivität und Bekleidung")

        ax.grid(True)

        # Clothing labels (example CLO values)
        clothing_labels = [
            (1.2, 0.30, "Short sleeves + shorts"),
            (1.2, 0.50, "T‑shirt + pants"),
            (1.2, 0.80, "Light jacket"),
            (1.2, 1.20, "Winter coat"),
        ]

        for met, clo, label in clothing_labels:
            t_opt = optimal_temp(met, clo)
            ax.scatter(met, clo, c="black", s=40)
            ax.text(
                met + 0.02,
                clo + 0.02,
                f"{label}\n≈ {t_opt:.1f} °C",
                fontsize=9,
                color="black",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="gray")
            )

        st.pyplot(fig)
        st.caption("Diese Grafik zeigt, wie sich die optimale Raumtemperatur in Abhängigkeit vom Aktivitätsniveau (met) und der Bekleidungsisolation (clo) verändert." \
        " Leichte Kleidung wie kurzärmlige Shirts oder Sommeroutfits erfordert eine wärmere Innenraumtemperatur, um thermischen Komfort zu gewährleisten.  " \
        "Schwerere Kleidung wie leichte Jacken oder Wintermäntel verschiebt den Komfortbereich zu niedrigeren Temperaturen. Die Farbskala zeigt die geschätzte optimale operative Temperatur basierend auf den Prinzipien der ISO 7730.")



    with st.expander("Empfohlene Kleidung nach Land"):
# ============================================================
# CLO RECOMMENDATION BY COUNTRY
# ============================================================

        st.header("Empfohlene Kleidung nach Land")

        # --- Table ---
        st.subheader("CLO-Kategorisierung")
        table_df = pd.DataFrame({
            "CLO-Wert": [clo_mean, closest_clo],
            "Kategorie": ["Gemessener Durchschnitt", clothing_label]
        })
        st.table(table_df)

        # --- Plot CLO distribution ---
        st.subheader("Verteilung der CLO-Werte im ausgewählten Land")

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df_filtered["clothing_ensemble_insulation"], bins=20, color="skyblue", edgecolor="black")
        ax.axvline(clo_mean, color="red", linestyle="--", label=f"Durchschnitt CLO = {clo_mean:.2f}")
        ax.set_xlabel("CLO-Wert")
        ax.set_ylabel("Häufigkeit")
        ax.legend()
        st.pyplot(fig)



# ============================================================
# GENERAL TABLE: CLO recommendation for all countries by season
# ============================================================

    st.subheader("Empfohlene Kleidung nach Saison und Land")

    # English comment:
    # This section creates a general table for ALL countries,
    # grouped by season (Summer, Winter, etc.).
    # Each season is shown inside an expander.
    # It does NOT use the sidebar filters.

    # --- ASHRAE refined CLO dictionary ---
    ashrae_clo_refined = {
        0.00: "Nackt",
        0.05: "Nur Unterwäsche",
        0.15: "Sehr leicht: Shorts + Tank-Top",
        0.25: "Leichtes Sommer-Outfit",
        0.35: "Sommerkleidung: Leichte lange Hose + T‑Shirt",
        0.45: "Standard-Sommer: Shorts/Rock + kurzärmeliges Hemd",
        0.55: "Leichte Übergangskleidung",
        0.65: "Büro-Sommerkleidung",
        0.75: "Standard-Übergang: Jeans + leichter Pullover",
        0.85: "Warmes Outfit",
        1.00: "Business-Anzug",
        1.15: "Winter-Büro",
        1.30: "Wärmere Winterkleidung",
        1.50: "Schwere Außenkleidung",
        2.00: "Extrem-Winterkleidung"
    }

    # Helper: find closest clothing label
    def closest_clothing_label(clo_value):
        closest_key = min(ashrae_clo_refined.keys(), key=lambda x: abs(x - clo_value))
        return closest_key, ashrae_clo_refined[closest_key]

    # --- Seasons available in the dataset ---
    seasons = sorted(df["season"].dropna().unique())

    # --- Loop through seasons and create an expander for each ---
    for season in seasons:

        with st.expander(f"Saison: {season}"):

            # Filter dataset for this season
            season_df = df[df["season"] == season]

            # Group by country
            rows = []

            for country, subset in season_df.groupby("country"):

                clo_mean = subset["clothing_ensemble_insulation"].mean()
                clo_key, clo_label = closest_clothing_label(clo_mean)

                rows.append({
                    "Land": country,
                    "Saison": season,
                    "Durchschnittlicher CLO": f"{clo_mean:.2f}",
                    "Empfohlene Kategorie (ASHRAE)": clo_label,
                    "Nächstgelegener CLO-Wert": f"{clo_key:.2f}"
                })

            # Create table
            season_table = pd.DataFrame(rows)

            st.table(season_table)

        # English explanation
            st.markdown("""
        **Comment (English):**  
        This section shows a general overview of recommended clothing for all countries, grouped by season.  
        For each season, the average clothing insulation (CLO) is calculated per country and mapped to the closest ASHRAE clothing category.  
        Each season is displayed inside its own expander for clarity.
        """)

    
    # ============================================================
    # STATISTICAL MAP: Most Influential CLO Variable per Country
    # ============================================================

    st.subheader("Weltkarte – Wichtigste statistische Einflussvariable auf CLO nach Land")

    import pandas as pd
    import numpy as np
    import plotly.express as px
    from scipy.stats import pearsonr, f_oneway

    numeric_vars = [
        "metabolic_rate", "operative_temperature",
        "air_temperature", "radiant_temperature",
        "age"
    ]

    categorical_vars = [
        "season", "climate", "gender",
        "building_type", "cooling_type"
    ]

    results = []

    for country in sorted(df["country"].dropna().unique()):

        country_df = df[df["country"] == country].dropna(subset=["clothing_ensemble_insulation"])

        if len(country_df) < 10:
            results.append({
                "country": country,
                "top_variable": "Keine Daten",
                "effect_strength": 0
            })
            continue

        effects = {}

        # NUMERIC VARIABLES
        for var in numeric_vars:
            if var not in country_df.columns:
                effects[var] = 0
                continue

            col_data = pd.to_numeric(country_df[var], errors="coerce").dropna()
            clo_data = country_df["clothing_ensemble_insulation"].loc[col_data.index]

            if len(col_data) < 5:
                effects[var] = 0
                continue

            try:
                corr, _ = pearsonr(col_data, clo_data)
                effects[var] = abs(corr)
            except:
                effects[var] = 0

        # CATEGORICAL VARIABLES
        for var in categorical_vars:
            if var not in country_df.columns:
                effects[var] = 0
                continue

            try:
                groups = [
                    group["clothing_ensemble_insulation"].values
                    for _, group in country_df.groupby(var)
                    if len(group) >= 3
                ]
                if len(groups) > 1:
                    f_stat, _ = f_oneway(*groups)
                    effects[var] = f_stat
                else:
                    effects[var] = 0
            except:
                effects[var] = 0

        top_var = max(effects, key=effects.get)
        effect_strength = effects[top_var]

        results.append({
            "country": country,
            "top_variable": top_var,
            "effect_strength": effect_strength
        })

    stat_df = pd.DataFrame(results)

    unique_vars = stat_df["top_variable"].unique()
    var_to_code = {v: i for i, v in enumerate(unique_vars)}
    stat_df["var_code"] = stat_df["top_variable"].map(var_to_code)

    fig = px.choropleth(
        stat_df,
        locations="country",
        locationmode="country names",
        color="var_code",
        hover_name="country",
        hover_data={
            "top_variable": True,
            "effect_strength": True,
            "var_code": False
        },
        color_continuous_scale="Turbo",
        title="Wichtigste statistische Einflussvariable auf CLO nach Land"
    )

    fig.update_layout(
        title_font_size=22,
        geo=dict(showframe=False, showcoastlines=True)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
        Diese Unterschiede sind **normal**:  
        Jedes Land hat **eigenes Klima**, **eigene Gebäude**, **eigene Kultur** und **eigene Datenverteilung**.  
        Darum zeigt die Statistik **verschiedene dominante Variablen**.
        """)

    
    with st.expander("🔍 Legende – Wichtigste Einflussvariable (statistisch)"):

        st.markdown("""
        **season** → Kleidung ändert sich stark zwischen Sommer/Winter  
        **climate** → Klimazone bestimmt typische Kleidung  
        **gender** → Geschlechtsspezifische Kleidungsgewohnheiten  
        **building_type** → Innenraumumgebung beeinflusst CLO  
        **cooling_type** → AC / natürliche Lüftung beeinflusst Kleidung  
        **metabolic_rate** → Aktivitätsniveau bestimmt Wärmeproduktion  
        **operative_temperature** → Innenraumtemperatur beeinflusst Kleidung  
        **air_temperature** → Außentemperatur beeinflusst Kleidung  
        **radiant_temperature** → Strahlungswärme (Sonne/Wände) beeinflusst Kleidung  
        **age** → Altersbedingte Unterschiede im Wärmeempfinden

        ---
        ### 🧭 Warum unterscheiden sich die Länder? (Kurz erklärt)

        **Klima <--> Kleidung**  
        Heiße Länder → Temperatur dominiert  
        Kalte Länder → Saison dominiert  

        **Gebäude <--> Innenraumklima**  
        Starke Klimaanlagen → operative_temperature ↑  
        Natürliche Lüftung → air_temperature ↑  

        **Kultur <--> Kleidung**  
        Strenge Kleidungsnormen → gender / building_type ↑  

        **Aktivität <--> Wärmeproduktion**  
        Hohe körperliche Aktivität → metabolic_rate ↑  

        **Strahlung <--> Komfort**  
        Starke Sonneneinstrahlung → radiant_temperature ↑  

        Diese Unterschiede sind **normal**:  
        Jedes Land hat **eigenes Klima**, **eigene Gebäude**, **eigene Kultur** und **eigene Datenverteilung**.  
        Darum zeigt die Statistik **verschiedene dominante Variablen**.
        """)


################################################################################################################
 # ============================================================
# Adaptive behaviours analysis – table, bar chart, heatmap
# ============================================================

    import pandas as pd
    import numpy as np
    import plotly.express as px
    from scipy.stats import f_oneway

    # English comment:
    # Adaptive variables available in your dataset.
    adaptive_vars = ["blind_curtain", "fan", "window", "door", "heater"]

    # English comment:
    # This function computes ANOVA-based effect strength of each adaptive variable on CLO per country.
    def compute_adaptive_effects(df):
        results = []
        for country in sorted(df["country"].dropna().unique()):
            country_df = df[df["country"] == country].dropna(subset=["clothing_ensemble_insulation"])
            if len(country_df) < 10:
                continue

            effects = {}
            for var in adaptive_vars:
                if var not in country_df.columns:
                    effects[var] = 0
                    continue

                col = pd.to_numeric(country_df[var], errors="coerce")
                clo = country_df["clothing_ensemble_insulation"]

                # English comment:
                # We assume binary 0/1 behaviour and use ANOVA.
                try:
                    groups = [
                        clo[col == 0].values,
                        clo[col == 1].values
                    ]
                    if len(groups[0]) >= 3 and len(groups[1]) >= 3:
                        f_stat, _ = f_oneway(*groups)
                        effects[var] = f_stat
                    else:
                        effects[var] = 0
                except:
                    effects[var] = 0

            for var, eff in effects.items():
                results.append({
                    "country": country,
                    "adaptive_var": var,
                    "effect_strength": eff
                })

        return pd.DataFrame(results)

    adaptive_df = compute_adaptive_effects(df)


    # ============================================================
    # EXPANDER 1 – TABLE (Ranking per country)
    # ============================================================

    with st.expander("Adaptive behaviours – ranking table", expanded=False):
        st.markdown("""
        ### Tabellenansicht – Wichtigkeit der adaptiven Verhaltensweisen  
        *Kurze Beschreibung:*  
        Diese Tabelle zeigt für jedes Land, welche adaptive Verhaltensweise (z. B. Fenster öffnen, Ventilator nutzen) den stärksten statistischen Einfluss auf die Kleidung (CLO) hat.
        """)

        # English comment:
        # For each country, show the adaptive variable with highest effect.
        top_per_country = (
            adaptive_df
            .sort_values("effect_strength", ascending=False)
            .groupby("country")
            .head(1)
            .reset_index(drop=True)
        )

        st.dataframe(top_per_country)


    # ============================================================
    # EXPANDER 2 – BAR CHART (effect per behaviour)
    # ============================================================

    with st.expander("Adaptive behaviours – bar chart", expanded=False):
        st.markdown("""
        ### Balkendiagramm – Durchschnittlicher Einfluss  
        *Kurze Beschreibung:*  
        Dieses Diagramm zeigt, welche adaptive Verhaltensweise weltweit den größten durchschnittlichen Einfluss auf CLO hat.
        """)

        # English comment:
        # Aggregate effect strength per adaptive variable across all countries.
        agg_effects = (
            adaptive_df
            .groupby("adaptive_var")["effect_strength"]
            .mean()
            .reset_index()
            .sort_values("effect_strength", ascending=False)
        )

        fig_bar = px.bar(
            agg_effects,
            x="adaptive_var",
            y="effect_strength",
            labels={"adaptive_var": "Adaptive Verhaltensweise", "effect_strength": "Durchschnittliche Effektstärke"},
            title="Durchschnittlicher statistischer Einfluss der adaptiven Verhaltensweisen"
        )
        st.plotly_chart(fig_bar, use_container_width=True)


    # ============================================================
    # EXPANDER 3 – HEATMAP (country × behaviour)
    # ============================================================

    with st.expander("Adaptive behaviours – heatmap", expanded=False):
        st.markdown("""
        ### Heatmap – Länder und adaptive Verhaltensweisen  
        *Kurze Beschreibung:*  
        Diese Heatmap zeigt, wie stark jede adaptive Verhaltensweise in jedem Land wirkt.  
        Dunklere Farben bedeuten stärkeren Einfluss.
        """)

        # English comment:
        # Pivot to create a matrix of effect_strength (country × adaptive_var).
        heat_df = adaptive_df.pivot_table(
            index="country",
            columns="adaptive_var",
            values="effect_strength",
            aggfunc="mean",
            fill_value=0
        )

        fig_heat = px.imshow(
            heat_df,
            labels=dict(x="Adaptive Verhaltensweise", y="Land", color="Effektstärke"),
            title="Heatmap – Statistischer Einfluss der adaptiven Verhaltensweisen nach Land",
            aspect="auto"
        )
        st.plotly_chart(fig_heat, use_container_width=True)


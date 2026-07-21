import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import chi2_contingency
import os
import pydeck as pdk
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Betrachtung der Verteilungen", layout="wide", initial_sidebar_state="expanded")

df = pd.read_csv("db_bereinigt_final.csv")

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import altair as alt
import pydeck as pdk


st.set_page_config(layout="wide")

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("db_bereinigt_final.csv")
    # Save original BEFORE cleaning
    df_original = df.copy()
    df["operative_temperature"] = pd.to_numeric(df["operative_temperature"], errors="coerce")
    df["thermal_sensation"] = pd.to_numeric(df["thermal_sensation"], errors="coerce")
    df = df.dropna(subset=["operative_temperature", "thermal_sensation"])

    return df, df_original

df, df_original = load_data()

# ============================================================
# SESSION STATE FILTERS (for other tabs)
# ============================================================
for key in [
    "region_filter", "country_filter", "city_filter",
    "season_filter", "climate_filter", "building_filter",
    "cooling_filter", "gender_filter"
]:
    if key not in st.session_state:
        st.session_state[key] = "Alle"

st.title("Thermischer Befinden – Interaktives Analyse‑Dashboard")

# ============================================================
# VARIABLE MAPPING
# ============================================================
variables = {
    "Lufttemperatur": "air_temperature",
    "Operative Temperatur": "operative_temperature",
    "Strahlungstemperatur": "radiant_temperature",
    "Relative Luftfeuchtigkeit": "relative_humidity",
    "Luftgeschwindigkeit": "air_speed",
    "Außentemperatur": "outdoor_air_temperature",
    "SET": "standard_effective_temperature",
    "PMV": "predicted_mean_vote",
    "PPD": "predicted_percentage_dissatisfied",
    "Bekleidungsisolation": "clothing_ensemble_insulation",
    "Metabolische Aktivität": "metabolic_rate",
    "Thermal Sensation": "thermal_sensation",
    "Thermal Comfort": "thermal_comfort",
    "Thermal Preference": "thermal_preference",
}

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.header("Filter & Achsenwahl")

regions = ["Alle"] + sorted(df["region"].dropna().unique())
region = st.sidebar.selectbox("Region", regions)

if region == "Alle":
    countries = ["Alle"] + sorted(df["country"].dropna().unique())
else:
    countries = ["Alle"] + sorted(df[df["region"] == region]["country"].dropna().unique())
country = st.sidebar.selectbox("Land", countries)

if country == "Alle":
    cities = ["Alle"] + sorted(df["city"].dropna().unique())
else:
    cities = ["Alle"] + sorted(
        df[(df["region"] == region) & (df["country"] == country)]["city"].dropna().unique()
    )
city = st.sidebar.selectbox("Stadt", cities)

climate = st.sidebar.selectbox("Klima", ["Alle"] + sorted(df["climate"].dropna().unique()))
climate_zone = st.sidebar.selectbox("Klimazone", ["Alle"] + sorted(df["climate_zone"].dropna().unique()))
building_type = st.sidebar.selectbox("Gebäudetyp", ["Alle"] + sorted(df["building_type"].dropna().unique()))
cooling_type = st.sidebar.selectbox("Kühlungsart", ["Alle"] + sorted(df["cooling_type"].dropna().unique()))
season = st.sidebar.selectbox("Jahreszeit", ["Alle"] + sorted(df["season"].dropna().unique()))
gender = st.sidebar.selectbox("Geschlecht", ["Alle"] + sorted(df["gender"].dropna().unique()))

clo = st.sidebar.slider("Bekleidung (clo)", 0.0, 2.0, (0.5, 1.0))
metabolic_rate = st.sidebar.slider("Metabolische Aktivität (met)", 0.8, 3.0, (1.0, 1.4))

# ============================================================
# APPLY FILTERS SAFELY (used by ALL tabs)
# ============================================================
df_filtered = df.copy()

if region != "Alle": df_filtered = df_filtered[df_filtered["region"] == region]
if country != "Alle": df_filtered = df_filtered[df_filtered["country"] == country]
if city != "Alle": df_filtered = df_filtered[df_filtered["city"] == city]
if climate != "Alle": df_filtered = df_filtered[df_filtered["climate"] == climate]
if building_type != "Alle": df_filtered = df_filtered[df_filtered["building_type"] == building_type]
if cooling_type != "Alle": df_filtered = df_filtered[df_filtered["cooling_type"] == cooling_type]
if season != "Alle": df_filtered = df_filtered[df_filtered["season"] == season]
if gender != "Alle": df_filtered = df_filtered[df_filtered["gender"] == gender]

df_filtered = df_filtered[
    (df_filtered["clothing_ensemble_insulation"] >= clo[0]) &
    (df_filtered["clothing_ensemble_insulation"] <= clo[1])
]

df_filtered = df_filtered[
    (df_filtered["metabolic_rate"] >= metabolic_rate[0]) &
    (df_filtered["metabolic_rate"] <= metabolic_rate[1])
]


##################################################################################################################
##################################################################################################################
#st.markdown("## 📊 Überblick über die Datenquelle")

# ---------------------------------------------------------
# Grundlegende Kennzahlen
# ---------------------------------------------------------
total_rows = len(df_original)

total_building_types = df_filtered["building_type"].nunique() if "building_type" in df_filtered else None
total_countries = df_filtered["country"].nunique() if "country" in df_filtered else None
total_regions = df_filtered["region"].nunique() if "region" in df_filtered else None
total_cities = df_filtered["city"].nunique() if "city" in df_filtered else None

# Klima-Informationen
total_climates = df_filtered["climate"].nunique() if "climate" in df_filtered else None
total_climate_zones = df_filtered["climate_zone"].nunique() if "climate_zone" in df_filtered else None

# Jahreszeiten (nur Anzahl)
if "season" in df_filtered.columns:
    total_seasons = df_filtered["season"].dropna().nunique()
else:
    total_seasons = None

# Fehlwerte
missing_total = df_filtered.isna().sum().sum()
missing_percent = (missing_total / df_filtered.size) * 100

# Jahr-Spalte → Zeitraum-Range
if "year" in df_filtered.columns:
    df_filtered["year"] = pd.to_numeric(df_filtered["year"], errors="coerce")
    min_year = int(df_filtered["year"].min())
    max_year = int(df_filtered["year"].max())
    year_range = f"{min_year} – {max_year}"
else:
    year_range = "–"

# Komfortbewertungen
comfort_vars = ["thermal_sensation", "thermal_preference", "thermal_acceptability", "thermal_comfort"]
available_comfort_vars = [c for c in comfort_vars if c in df_filtered.columns]
comfort_count = df_filtered[available_comfort_vars].dropna().shape[0]

st.markdown("---")

# ---------------------------------------------------------
# KPI Cards – 5 pro Reihe
# ---------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📦 Datensätze", f"{total_rows:,}")
    st.metric("⚠️ Fehlwerte (%)", f"{missing_percent:.2f}%")


with col2:
    st.metric("📍 Regionen", f"{total_regions:,}" if total_regions else "–")
    st.metric("🌡️ Klimatypen", f"{total_climates:,}" if total_climates else "–")

with col3:
    st.metric("🌍 Länder", f"{total_countries:,}" if total_countries else "–")

    st.metric("🗺️ Klimazonen", f"{total_climate_zones:,}" if total_climate_zones else "–")

with col4:
    st.metric("🏙️ Städte", f"{total_cities:,}" if total_cities else "–")
    st.metric("🍂 Jahreszeiten", f"{total_seasons:,}" if total_seasons else "–")

with col5:
    st.metric("🗓️ Zeitraum", f"{year_range}" if year_range else "–")
    st.metric("🏢 Gebäude Typ", f"{total_building_types:,}" if total_building_types else "–")


st.markdown("---")

# ============================================================
# AXIS SELECTION
# ============================================================
x_label = st.sidebar.selectbox("X‑Achse", list(variables.keys()))
y_label = st.sidebar.selectbox("Y‑Achse", list(variables.keys()))
x = variables[x_label]
y = variables[y_label]

chart_type = st.sidebar.radio("Diagrammtyp", ["Scatter", "Linie"], index=0)


#############################################################
###############################################################


# ---------------------------------------------------------
# 4. Hauptbereich: X/Y-Plot
# ---------------------------------------------------------

################################################################################
col_plot, col_map = st.columns([1.5,2])

with col_plot:

    st.subheader("📊 Verteilungen nach Kategorie")

    # ---------------------------------------------------------
    # 1. Kategorien definieren
    # ---------------------------------------------------------
    mapping = {
        "Region": "region",
        "Land": "country",
        "Klimazone": "climate_zone",
        "Klima": "climate",
        "Gebäudetyp": "building_type",
        "Kühlungsart": "cooling_type",
        "Jahreszeit": "season",
        "Geschlecht": "gender"
    }

    # ---------------------------------------------------------
    # 2. Variable auswählen
    # ---------------------------------------------------------
    selected_variable = st.selectbox(
        "Variable auswählen",
        list(mapping.keys()),
        key="verteilung_variable"
    )

    column = mapping[selected_variable]

    # ---------------------------------------------------------
    # 3. Berechnungen basierend auf Sidebar-gefilterten Daten
    # ---------------------------------------------------------
    counts = df_filtered[column].value_counts()
    percent = counts / counts.sum() * 100

    selection_df = pd.DataFrame({
        selected_variable: counts.index,
        "Anzahl": counts.values,
        "Prozent": percent.round(2).astype(str) + " %"
    })
    selection_df = selection_df.sort_values("Anzahl", ascending=True)

    # ---------------------------------------------------------
    # 4. Grafik mit Anzahl-Labels
    # ---------------------------------------------------------
    st.subheader(f"Anzahl Einträge je {selected_variable}")

    chart = (
        alt.Chart(selection_df)
        .mark_bar(color="#4C72B0")
        .encode(
            x=alt.X("Anzahl:Q", title="Anzahl Einträge"),
            y=alt.Y(f"{selected_variable}:N", sort="-x", title=selected_variable),
            tooltip=[selected_variable, "Anzahl", "Prozent"]
        )
        .properties(height=450)
    )

    # --- Anzahl-Labels über den Balken ---
    labels = (
        alt.Chart(selection_df)
        .mark_text(
            align="left",
            baseline="middle",
            dx=5,  # Abstand vom Balken
            color="black",
            fontSize=12
        )
        .encode(
            x="Anzahl:Q",
            y=f"{selected_variable}:N",
            text="Anzahl:Q"
        )
    )

    st.altair_chart(chart + labels, use_container_width=True)

########################################################################################################################
with col_map:
    
    # filtered_df = your already filtered data from sidebar

    st.subheader("🗺️ Geografische Verteilung der Messdaten")

    view_state = pdk.ViewState(
        latitude=df_filtered["latitude"].mean() if len(df_filtered) else 0,
        longitude=df_filtered["longitude"].mean() if len(df_filtered) else 0,
        zoom=2 if len(df_filtered) > 1 else 4
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_filtered,
        get_position='[longitude, latitude]',
        get_fill_color='[0, 120, 255]',
        get_radius=100000,
        pickable=True
    )

    tooltip = {
        "html": """
            Region: {region}<br/>
            Country: {country}<br/>
            City: {city}<br/>
            Climatezone: {climate_zone}<br/>
            Building Type: {building_type}<br/>
            Cooling: {cooling_type}<br/>
            Season: {season}<br/>
            Records: {records}
        """,
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






# def plot_column(data, colname, color="steelblue"):
#     """Erzeugt automatisch den passenden Plot für eine Spalte."""
#     fig, ax = plt.subplots()

#     # Numerische Spalte → Histogramm
#     if pd.api.types.is_numeric_dtype(data):
#         ax.hist(data, bins=20, color=color, edgecolor="black")
#         ax.set_xlabel(colname)
#         ax.set_ylabel("Anzahl")
#         ax.set_title(f"Verteilung von {colname}")

#     # Binäre Spalte (0/1) → Balkendiagramm
#     elif set(data.unique()).issubset({0, 1}):
#         counts = data.value_counts().sort_index()
#         ax.bar(["0", "1"], counts.values, color=["tomato", "seagreen"])
#         ax.set_xlabel(colname)
#         ax.set_ylabel("Anzahl")
#         ax.set_title(f"{colname}: 0/1 Verteilung")

#     # Kategorische Spalte → Balkendiagramm
#     else:
#         counts = data.value_counts()
#         ax.bar(counts.index.astype(str), counts.values, color=color)
#         ax.set_xlabel(colname)
#         ax.set_ylabel("Anzahl")
#         ax.set_title(f"Kategorien in {colname}")
#         plt.xticks(rotation=45, ha="right")

#     return fig

# def map_tsv(v):
#     if pd.isna(v): return None
#     if v <= -2.5: return -3
#     elif v <= -1.5: return -2
#     elif v <= -0.5: return -1
#     elif v < 0.5: return 0
#     elif v < 1.5: return 1
#     elif v < 2.5: return 2
#     else: return 3

# def map_tc(v):
#     if pd.isna(v): return None
#     if v < 1.5: return 1
#     elif v < 2.5: return 2
#     elif v < 3.5: return 3
#     elif v < 4.5: return 4
#     elif v < 5.5: return 5
#     else: return 6

# def plot_comfort_variable(series, labels, colors, title):
#     series = pd.to_numeric(series, errors="coerce").dropna()
#     counts = series.value_counts().sort_index()
#     total = counts.sum()

#     fig, ax = plt.subplots(figsize=(8, 5))

#     for i, level in enumerate(counts.index):
#         count = counts[level]
#         pct = count / total * 100

#         ax.bar(str(level), count, color=colors[level])
#         ax.text(i, count + 0.5, f"{count} ({pct:.1f}%)", ha="center")

#     ax.set_title(title)
#     ax.set_xlabel("Kategorie")
#     ax.set_ylabel("Anzahl")

#     st.pyplot(fig)
#     plt.close(fig)



# # Load data

# #st.title("Globale Datenanalyse")
# #st.line_chart(df_bereinigt["DB"])
# #st.dataframe(df_bereinigt)

# st.title("📊 Betrachtung der Verteilungen")

# #st.header("Datenverteilung")

# # Klima / Building

# tab1, tab2, tab3 = st.tabs(["Globale Datenverteilung","Übersicht Datenverteilung mögliche Einflussfaktoren", "Übersicht Datenverteilung thermische Bewertung"], on_change="rerun")

# #########################################################################################################
# #########################################################################################################

# with tab1:
#     col1, spacer, col2 = st.columns([2, 0.4, 1])

#     # --- Grafik mit Anzahl Einträge ---
#     with col1:
        
#         # ---------------------------------------------------------
#         # 🔎 1. Mapping-Dictionary
#         # ---------------------------------------------------------
#         mapping = {
#             "Region": "region",
#             "Land": "country",
#             "Klimazone": "climate_zone",
#             "Klima": "climate"
#         }

#         # ---------------------------------------------------------
#         # 🔍 2. Filter-Widget (Kima/Klimazone)
#         # ---------------------------------------------------------
#         selected_variable = st.selectbox(
#             "Variable auswählen",
#             list(mapping.keys()),
#             key="selectbox_1"
#         )

#         # ---------------------------------------------------------
#         # 🔍 3. Mapping anwenden
#         # ---------------------------------------------------------
#         column = mapping[selected_variable]

#         # ---------------------------------------------------------
#         # 🔍 4. Berechnungen
#         # ---------------------------------------------------------
#         counts = df[column].value_counts()
#         percent = counts / counts.sum() * 100

#         # ---------------------------------------------------------
#         # 🔍 5. Darstellung
#         # ---------------------------------------------------------
#         selection_df = pd.DataFrame({
#             selected_variable: counts.index,
#             "Anzahl": counts.values,
#             "Prozent": percent.values
#         })

#         selection_df["Prozent"] = (
#             selection_df["Prozent"].round(2).astype(str) + " %"
#         )

      
#         # ---------------------------------------------------------
#         # 🔎 6. Grafik erstellen
#         # ---------------------------------------------------------
#         st.subheader(f"Anzahl Einträge je {selected_variable}")

#         # Sichergehen, dass in der Grafik die ausgewählte Variable verwendet wird
#         category = selection_df.columns[0]

#         chart = (
#             alt.Chart(selection_df)
#             .mark_bar()
#             .encode(
#                 x=alt.X("Anzahl:Q", title="Anzahl Einträge"),
#                 y=alt.Y(f"{category}:N", sort="-x", title=category),
#                 tooltip=[category, "Anzahl", "Prozent"]
#             )
#             .properties(
#                 width=600,
#                 height=550
#             )
#         )

#         st.altair_chart(chart, use_container_width=True)
    

#     # --- Anzahl Einträge in der Kategorie ---
#     with col2:
#         st.markdown(f"### Übersicht Anzahl Einträge je {selected_variable}")

#         st.dataframe(
#             selection_df,
#             use_container_width=True,
#             hide_index=True
#         )


#     # Karte für Darstellung

#     # ---------------------------------------------------------
#     # 🌍 4. Koordinaten hinzufügen
#     # ---------------------------------------------------------
#     # Beispiel für Länder:
#     country_coords = {
#         "Deutschland": [51.1657, 10.4515],
#         "Frankreich": [46.6034, 1.8883],
#         "Spanien": [40.4637, -3.7492],
#         "Italien": [41.8719, 12.5674],
#     }

#     if selected_variable == "Land":
#         coords = pd.DataFrame(
#             [
#                 {
#                     "country": country,
#                     "latitude": value[0],
#                     "longitude": value[1]
#                 }
#                 for country, value in country_coords.items()
#             ]
#         )

#         map_df = counts.merge(
#             coords,
#             on="country",
#             how="left"
#         )

#         # ---------------------------------------------------------
#         # 🗺️ 5. Karte erstellen
#         # ---------------------------------------------------------
#         st.subheader(f"Karte: Anzahl Einträge je {selected_variable}")

#         map_chart = (
#             alt.Chart(map_df)
#             .mark_circle(
#                 opacity=0.65,
#                 color="steelblue"
#             )
#             .encode(
#                 longitude="longitude:Q",
#                 latitude="latitude:Q",
#                 size=alt.Size(
#                     "Anzahl:Q",
#                     scale=alt.Scale(range=[50, 2000]),
#                     title="Anzahl Einträge"
#                 ),
#                 tooltip=[
#                     "country",
#                     "Anzahl",
#                     "Prozent"
#                 ]
#             )
#             .properties(
#                 width=600,
#                 height=500
#             )
#         )

#         st.altair_chart(
#             map_chart,
#             use_container_width=True
#         )

# #########################################################################################################
# #########################################################################################################

# with tab2:


#     # ---------------------------------------------------------
#     # ROW 2 → 3 Spalten: season, climate, cooling_type
#     # ---------------------------------------------------------
#     row2_col1, row2_col2, row2_col3 = st.columns(3)

#     with row2_col1:
#         st.subheader("🌦️ Season")
#         fig_season = plot_column(df["season"], "season")
#         st.pyplot(fig_season)
#         plt.close(fig_season)

#     with row2_col2:
#         st.subheader("❄️ Cooling Type")
#         fig_cooling = plot_column(df["cooling_type"], "cooling_type")
#         st.pyplot(fig_cooling)
#         plt.close(fig_cooling)

#     with row2_col3:
#         st.subheader("🏢 Building Type")
#         fig_bt = plot_column(df["building_type"], "building_type")
#         st.pyplot(fig_bt)
#         plt.close(fig_bt)

#     # ---------------------------------------------------------
#     # NEUE ROW → 4 Spalten: fan, heater, window, door
#     # ---------------------------------------------------------
#     row_fan, row_heater, row_window, row_door = st.columns(4)

#     with row_fan:
#         st.subheader("🌀 Fan")
#         fig_fan = plot_column(df["fan"], "fan")
#         st.pyplot(fig_fan)
#         plt.close(fig_fan)

#     with row_heater:
#         st.subheader("🔥 Heater")
#         fig_heater = plot_column(df["heater"], "heater")
#         st.pyplot(fig_heater)
#         plt.close(fig_heater)

#     with row_window:
#         st.subheader("🪟 Window")
#         fig_window = plot_column(df["window"], "window")
#         st.pyplot(fig_window)
#         plt.close(fig_window)

#     with row_door:
#         st.subheader("🚪 Door")
#         fig_door = plot_column(df["door"], "door")
#         st.pyplot(fig_door)
#         plt.close(fig_door)

#     # ---------------------------------------------------------
#     # ROW 3 → 3 Spalten: leer | age | gender
#     # ---------------------------------------------------------
#     row3_col1, row3_col2, row3_col3 = st.columns(3)

#     with row3_col1:
#         st.write("")  # bewusst leer

#     with row3_col2:
#         st.subheader("👤 Age")
#         fig_age = plot_column(df["age"], "age")
#         st.pyplot(fig_age)
#         plt.close(fig_age)

#     with row3_col3:
#         st.subheader("🚻 Gender")
#         fig_gender = plot_column(df["gender"], "gender")
#         st.pyplot(fig_gender)
#         plt.close(fig_gender)

# with tab3:
#     st.subheader("📊 Häufigkeitsanalyse: Thermische Bewertung")

#     # ---------------------------------------------------------
#     # 🔧 1a. Thermische Parameter vorab runden / bereinigen
#     # ---------------------------------------------------------
#     # Falls deine Komfortvariablen numerisch sind, werden sie hier gerundet.
#     # Falls sie kategorisch sind (z.B. -3 bis +3), passiert nichts.
#     # komfort_variablen = ["thermal_sensation", "thermal_comfort", "thermal_preference"]

#     # for var in komfort_variablen:
#     #     if var in df.columns:
#     #         # Nur numerische Werte runden
#     #         if pd.api.types.is_numeric_dtype(df[var]):
#     #             df[var] = df[var].round(2)




#     col1, col2 = st.columns([2,1])
#     col3, col4 = st.columns([2,1])

#     with col1:
#         # ---------------------------------------------------------
#         # 🔍 2. Auswahl der Komfort-Variable
#         # ---------------------------------------------------------
#         variablen = {
#             "Thermischer Komfort": "thermal_comfort",
#             "Thermisches Empfinden": "thermal_sensation",
#             "Thermische Präferenz": "thermal_preference",
#             "Thermische Akzeptanz": "thermal_acceptability"
#         }

#         auswahl = st.selectbox(
#             "Wähle eine thermische Bewertungsvariable",
#             list(variablen.keys())
#         )

#         spalte = variablen[auswahl]

#         # ---------------------------------------------------------
#         # 🧹 3. Daten vorbereiten
#         # ---------------------------------------------------------
#         # Nur gültige Werte behalten
#         df_plot = df.dropna(subset=[spalte])

#         # Häufigkeiten berechnen
#         freq = df_plot[spalte].value_counts().reset_index()
#         freq.columns = ["Wert", "Anzahl"]


#     # ---------------------------------------------------------
#     # 📊 4. Balkendiagramm erstellen (Altair)
#     # ---------------------------------------------------------
#     with col3:
#         chart = (
#             alt.Chart(freq)
#             .mark_bar(color="#2E86C1")
#             .encode(
#                 x=alt.X("Wert:N", title=auswahl, axis=alt.Axis(labelAngle=0) ),      
#                 y=alt.Y("Anzahl:Q", title="Häufigkeit"),
#                 tooltip=["Wert", "Anzahl"]        
#             )
#             .properties(
#                 width=600,
#                 height=400,
#                 title=f"Häufigkeitsverteilung: {auswahl}"
#             )
#         )

#         st.altair_chart(chart, use_container_width=True)


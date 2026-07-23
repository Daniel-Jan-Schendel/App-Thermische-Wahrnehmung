
# app.py
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
    countries = ["Alle"] + sorted(df_original["country"].dropna().unique())
else:
    countries = ["Alle"] + sorted(df_original[df_original["region"] == region]["country"].dropna().unique())
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
total_countries = df_original["country"].nunique() if "country" in df_original else None

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
    st.metric("📦 Datensätze", f"{total_rows:.}")
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
    st.write("sdsd")

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
        "Geschlecht": "gender",
        "Thermischer Komfort": "thermal_comfort"
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


   
#############################################################################

    
    # st.subheader(f"{y_label} in Abhängigkeit von {x_label}")
    # plot_df = df_filtered[[x, y]].dropna()

    # if plot_df.empty:
    #     st.warning("Keine Daten für diese Auswahl verfügbar.")
    # else:
    #     fig, ax = plt.subplots(figsize=(7, 4))
    #     if chart_type == "Scatter":
    #         ax.scatter(plot_df[x], plot_df[y], alpha=0.6)
    #     else:
    #         plot_df = plot_df.sort_values(by=x)
    #         ax.plot(plot_df[x], plot_df[y], alpha=0.8)
    #     ax.set_xlabel(x_label)
    #     ax.set_ylabel(y_label)
    #     ax.grid(True, alpha=0.3)
    #     st.pyplot(fig)

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





#######################################################################################################################



# with col_info:
#     st.markdown("### 🗺️ Standortinformationen")    
#     st.markdown(f"- **Region:** {region}")
#     st.markdown(f"- **Land:** {country}")
#     st.markdown(f"- **Stadt:** {city}")


###############################################################################################################


# ---------------------------------------------------------
# 5. Tabs
# ---------------------------------------------------------
st.markdown("---")

tab_adaptive, tab_neutral, tab_comfort, tab_PMV_PPD, tab_korrelation,tab_verteilung,tab_beziehungen = st.tabs(
    ["Adaptive Strategien", 
     "Neutraltemperatur", 
     "Adaptive Komfort – Analyse", 
     "PMV/PPD", 
     "Korrelationsmatrix", 
     "Datenverteilung", 
     "Beziehungen zwischen Variablen"]
)

# ---------------------------------------------------------
# Tab : Adaptive Komfortstrategien
# ---------------------------------------------------------
with tab_adaptive:
    # RESET BUTTON
    if st.button("🔄 Reset Filter", key="reset_filters_tab1"):    # Reset Tab1 filters
        st.session_state.region_filter = "Alle"
        st.session_state.country_filter = "Alle"
        st.session_state.city_filter = "Alle"

        st.session_state.season_filter = "Alle"
        st.session_state.climate_filter = "Alle"
        st.session_state.building_filter = "Alle"
        st.session_state.cooling_filter = "Alle"
        st.session_state.gender_filter = "Alle"

        # Reset SIDEBAR filters
        st.session_state.region = "Alle"
        st.session_state.country = "Alle"
        st.session_state.city = "Alle"

    # Rerun the app
        st.rerun()

    st.subheader("Adaptive Komfortstrategien nach Region, Land, Stadt und Jahreszeit")

    # ---------------------------------------------------------
    # SHORT DASHBOARD-FRIENDLY EXPLANATION
    # ---------------------------------------------------------
    with st.expander("ℹ️ Hintergrund"):
        st.markdown("""
        Adaptive Komfortstrategien beschreiben, wie Menschen aktiv auf ihr Raumklima reagieren – 
        zum Beispiel durch das Öffnen von Fenstern, die Nutzung von Ventilatoren, das Einschalten 
        der Heizung oder das Schließen von Türen und Jalousien.

        Diese Strategien variieren je nach Region, Jahreszeit, Gebäudetyp und klimatischen Bedingungen.  
        Die folgende Heatmap zeigt, wie häufig diese Strategien unter verschiedenen Kontexten 
        angewendet werden.
        """)


# ---------------------------------------------------------
# FILTER 1: LOCATION FILTER (Region → Country → City)
# ---------------------------------------------------------
    st.markdown("### 🌍 Standortfilter")

    loc_col1, loc_col2, loc_col3 = st.columns(3)

    # --- REGION ---
    region_options = ["Alle"] + sorted(df["region"].dropna().unique())
    with loc_col1:
        st.session_state.region_filter = st.selectbox(
            "Region",
            region_options,
            index=region_options.index(st.session_state.region_filter)
            if st.session_state.region_filter in region_options else 0
        )

    # --- COUNTRY ---
    if st.session_state.region_filter == "Alle":
        countries_available = sorted(df["country"].dropna().unique())
    else:
        countries_available = sorted(
            df[df["region"] == st.session_state.region_filter]["country"].dropna().unique()
        )

    country_options = ["Alle"] + countries_available
    with loc_col2:
        st.session_state.country_filter = st.selectbox(
            "Land",
            country_options,
            index=country_options.index(st.session_state.country_filter)
            if st.session_state.country_filter in country_options else 0
        )

    # --- CITY ---
    if st.session_state.country_filter == "Alle":
        cities_available = sorted(df["city"].dropna().unique())
    else:
        cities_available = sorted(
            df[
                (df["region"] == st.session_state.region_filter) &
                (df["country"] == st.session_state.country_filter)
            ]["city"].dropna().unique()
        )

    city_options = ["Alle"] + cities_available
    with loc_col3:
        st.session_state.city_filter = st.selectbox(
            "Stadt",
            city_options,
            index=city_options.index(st.session_state.city_filter)
            if st.session_state.city_filter in city_options else 0
        )

    # Apply location filters
    adaptive_df = df.copy()
    if st.session_state.region_filter != "Alle":
        adaptive_df = adaptive_df[adaptive_df["region"] == st.session_state.region_filter]
    if st.session_state.country_filter != "Alle":
        adaptive_df = adaptive_df[adaptive_df["country"] == st.session_state.country_filter]
    if st.session_state.city_filter != "Alle":
        adaptive_df = adaptive_df[adaptive_df["city"] == st.session_state.city_filter]


    # ---------------------------------------------------------
    # FILTER 2: CONTEXT FILTER (Season, Climate, Building Type, Cooling Type, Gender)
    # ---------------------------------------------------------
    st.markdown("### 🏙️ Kontextfilter")

    ctx_col1, ctx_col2, ctx_col3, ctx_col4, ctx_col5 = st.columns(5)

    # --- SEASON ---
    season_options = ["Alle"] + sorted(df["season"].dropna().unique())
    with ctx_col1:
        st.session_state.season_filter = st.selectbox(
            "Jahreszeit",
            season_options,
            index=season_options.index(st.session_state.season_filter)
            if st.session_state.season_filter in season_options else 0
        )

    # --- CLIMATE ZONE ---
    climate_options = ["Alle"] + sorted(df["climate_zone"].dropna().unique())
    with ctx_col2:
        st.session_state.climate_filter = st.selectbox(
            "Klimazone",
            climate_options,
            index=climate_options.index(st.session_state.climate_filter)
            if st.session_state.climate_filter in climate_options else 0
        )

    # --- BUILDING TYPE ---
    building_options = ["Alle"] + sorted(df["building_type"].dropna().unique())
    with ctx_col3:
        st.session_state.building_filter = st.selectbox(
            "Gebäudetyp",
            building_options,
            index=building_options.index(st.session_state.building_filter)
            if st.session_state.building_filter in building_options else 0
        )

    # --- COOLING TYPE ---
    cooling_options = ["Alle"] + sorted(df["cooling_type"].dropna().unique())
    with ctx_col4:
        st.session_state.cooling_filter = st.selectbox(
            "Kühlungsart",
            cooling_options,
            index=cooling_options.index(st.session_state.cooling_filter)
            if st.session_state.cooling_filter in cooling_options else 0
        )

    # --- GENDER ---
    gender_options = ["Alle"] + sorted(df["gender"].dropna().unique())
    with ctx_col5:
        st.session_state.gender_filter = st.selectbox(
            "Geschlecht",
            gender_options,
            index=gender_options.index(st.session_state.gender_filter)
            if st.session_state.gender_filter in gender_options else 0
        )

    # Apply context filters
    if st.session_state.season_filter != "Alle":
        adaptive_df = adaptive_df[adaptive_df["season"] == st.session_state.season_filter]
    if st.session_state.climate_filter != "Alle":
        adaptive_df = adaptive_df[adaptive_df["climate_zone"] == st.session_state.climate_filter]
    if st.session_state.building_filter != "Alle":
        adaptive_df = adaptive_df[adaptive_df["building_type"] == st.session_state.building_filter]
    if st.session_state.cooling_filter != "Alle":
        adaptive_df = adaptive_df[adaptive_df["cooling_type"] == st.session_state.cooling_filter]
    if st.session_state.gender_filter != "Alle":
        adaptive_df = adaptive_df[adaptive_df["gender"] == st.session_state.gender_filter]


    # ---------------------------------------------------------
    # ADAPTIVE VARIABLES
    # ---------------------------------------------------------
    adaptive_vars = ["window", "door", "fan", "heater", "blind_curtain"]

    for col in adaptive_vars:
        adaptive_df[col] = pd.to_numeric(adaptive_df[col], errors="coerce").fillna(0)


    # ---------------------------------------------------------
    # GROUPING PARAMETER
    # ---------------------------------------------------------
    st.markdown("### 📊 Gruppierung der Analyse")

    group_param = st.selectbox(
        "Gruppieren nach:",
        ["region", "country", "city", "season", "climate_zone", "building_type", "cooling_type", "gender"]
    )

    groups_available = adaptive_df[group_param].dropna().unique()

    groups_clean = []
    for g in groups_available:
        df_g = adaptive_df[adaptive_df[group_param] == g]
        if df_g[adaptive_vars].mean().sum() > 0:
            groups_clean.append(g)


    # ---------------------------------------------------------
    # SINGLE HEATMAP FOR ALL GROUPS
    # ---------------------------------------------------------
    st.markdown("### 🔥 Adaptive Strategien – Gesamtübersicht")

    if len(groups_clean) == 0:
        st.warning("Keine Daten für adaptive Strategien in dieser Filterkombination.")
    else:
        # Build a matrix: rows = groups, columns = adaptive vars
        heatmap_data = []

        for g in groups_clean:
            df_g = adaptive_df[adaptive_df[group_param] == g]
            mean_vals = df_g[adaptive_vars].mean() * 100
            heatmap_data.append(mean_vals.values)

        heatmap_df = pd.DataFrame(
            heatmap_data,
            index=[str(g).capitalize() for g in groups_clean],
            columns=adaptive_vars
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(
            heatmap_df,
            annot=True,
            cmap="coolwarm",
            cbar_kws={"label": "Nutzung (%)"},
            fmt=".1f"
        )

        ax.set_title("Adaptive Strategien – Vergleich aller Gruppen")
        st.pyplot(fig)

        st.caption("Blau = geringe Nutzung, Rot = hohe Nutzung der Strategien.")
    
    with st.expander("🔍 Wichtigste Einflussvariable"):

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
        ### 🧭 Warum unterscheiden sich die Länder?

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




with tab_neutral:
    st.subheader("🌡️ Analyse der Neutraltemperatur")

    with st.expander("ℹ️ Kurze Beschreibung – Neutraltemperatur"):
        st.markdown("""
            Die Neutraltemperatur zeigt, bei welcher Raumtemperatur Menschen weder Wärme noch Kälte empfinden – sie ist damit der zentrale Vergleichswert für unterschiedliche Komfortpräferenzen..
                    
                    **Verständnis der Neutraltemperatur (ASCII‑Grafik):**

            zu kalt              neutral              zu warm
            (MTS < 0)             (MTS = 0)            (MTS > 0)
                \\                 |                 /
                \\                |                /
                    \\               |               /
                    \\______________|______________/
                                T_neutral

            - Links: Personen empfinden die Temperatur als **zu kalt** (negative MTS‑Werte).
            - Rechts: Personen empfinden die Temperatur als **zu warm** (positive MTS‑Werte).
            - In der Mitte: **Neutraltemperatur T_neutral**, bei der die mittlere Empfindung MTS = 0 ist.  


            Sie wird aus den vorhandenen Messdaten berechnet, indem die Beziehung zwischen 
            Innenraumtemperatur und mittlerer thermischer Empfindung (MTS) mittels 
            **linearer Regression** modelliert wird.

            Eine höhere Neutraltemperatur deutet darauf hin, dass Personen in dieser Gruppe 
            tendenziell **wärmere Bedingungen bevorzugen**, während eine niedrigere 
            Neutraltemperatur auf eine **Präferenz für kühlere Bedingungen** hinweist.

            Die Analyse berücksichtigt automatisch alle aktiven Filter aus der Sidebar 
            (Region, Jahreszeit, Gebäudetyp, Geschlecht usw.).
        """)

    # ---------------------------------------------------------
    # CHECK FILTERED DATA
    # ---------------------------------------------------------
    if df_filtered.empty:
        st.warning("Keine Daten für die ausgewählten Filter.")
        st.write("Analyse wird übersprungen.")
        # ❌ no st.stop()
        # ❌ no return
        # ✔ allow Streamlit to continue so tabs appear
    else:

        # ---------------------------------------------------------
        # DETERMINE GROUPING
        # ---------------------------------------------------------
        grouping_options = ["Keine Gruppierung", "season", "climate", "building_type", "cooling_type", "gender", "age", "country", "region"]
        grouping_choice = st.selectbox("Gruppierung der Analyse", grouping_options)

        # ---------------------------------------------------------
        # CASE 1 — NO GROUPING
        # ---------------------------------------------------------
        if grouping_choice == "Keine Gruppierung":

            mts_df = (
                df_filtered.groupby("operative_temperature")["thermal_sensation"]
                .mean()
                .reset_index()
                .dropna()
            )

            if len(mts_df) < 2:
                st.warning("Nicht genügend Daten für eine Regression.")
                st.write("Analyse wird übersprungen.")
            else:
                X = mts_df["operative_temperature"].values.reshape(-1, 1)
                y = mts_df["thermal_sensation"].values.reshape(-1, 1)

                model = LinearRegression()
                model.fit(X, y)

                a = model.coef_[0][0]
                b = model.intercept_[0]
                neutral_temp = -b / a

                fig, ax = plt.subplots(figsize=(10, 5))

                x_range = np.linspace(X.min(), X.max(), 100)
                y_pred = a * x_range + b

                ax.plot(x_range, y_pred, color="blue", linewidth=2)
                ax.scatter(X, y, color="black", alpha=0.7)
                ax.axvline(neutral_temp, color="red", linestyle="--")

                ax.set_xlabel("Operative Temperatur (°C)")
                ax.set_ylabel("MTS")
                ax.set_title("Neutraltemperatur – Gesamtanalyse")
                ax.grid(True)

                st.pyplot(fig)
                st.success(f"**Neutraltemperatur (gesamt): {neutral_temp:.2f} °C**")

        # ---------------------------------------------------------
        # CASE 2 — GROUPED ANALYSIS
        # ---------------------------------------------------------
        else:
            groups = df_filtered[grouping_choice].dropna().unique()
            groups = [g for g in groups if str(g).lower() not in ["unknown", "unk", "none", "nan", ""]]

            if len(groups) == 0:
                st.warning("Keine gültigen Gruppen vorhanden.")
            else:
                st.subheader(f"Neutraltemperatur nach Gruppen: {grouping_choice}")

                cols_per_row = 3
                rows = [groups[i:i + cols_per_row] for i in range(0, len(groups), cols_per_row)]

                for row_groups in rows:
                    cols = st.columns(cols_per_row)

                    for col, g in zip(cols, row_groups):
                        with col:
                            sub = df_filtered[df_filtered[grouping_choice] == g]

                            mts_df = (
                                sub.groupby("operative_temperature")["thermal_sensation"]
                                .mean()
                                .reset_index()
                                .dropna()
                            )

                            if len(mts_df) < 2:
                                st.warning(f"Nicht genügend Daten für Gruppe {g}.")
                                continue

                            X = mts_df["operative_temperature"].values.reshape(-1, 1)
                            y = mts_df["thermal_sensation"].values.reshape(-1, 1)

                            model = LinearRegression()
                            model.fit(X, y)

                            a = model.coef_[0][0]
                            b = model.intercept_[0]
                            neutral_temp = -b / a

                            fig, ax = plt.subplots(figsize=(5, 4))

                            x_range = np.linspace(X.min(), X.max(), 100)
                            y_pred = a * x_range + b

                            ax.plot(x_range, y_pred, linewidth=2)
                            ax.scatter(X, y, color="black", alpha=0.7)
                            ax.axvline(neutral_temp, color="red", linestyle="--")

                            ax.set_xlabel("T_in (°C)")
                            ax.set_ylabel("MTS")
                            ax.set_title(f"{g}")
                            ax.grid(True)

                            st.pyplot(fig)
                            st.caption(f"Neutraltemperatur: **{neutral_temp:.2f} °C**")



with tab_comfort:

    st.header("🌿 Adaptives Komfortmodell – ASHRAE 55")

    with st.expander("ℹ️ Hintergrund"):
        st.markdown(
            r"""
            Die folgende Analyse untersucht, wie gut verschiedene Kategorien die thermischen Komfortanforderungen nach dem adaptiven ASHRAE‑55‑Modell erfüllen. Durch den Vergleich der Komfort‑Compliance wird sichtbar, welche Gruppen sich am besten an die Außentemperatur anpassen und in **welchen Kategorien deutliche Abweichungen vom Komfortbereich auftreten.**.

            Es basiert auf dem Prinzip, dass Menschen sich an das Außenklima anpassen:
            - Bei **wärmeren Außentemperaturen** akzeptieren sie höhere Innentemperaturen.
            - Bei **kühleren Außentemperaturen** bevorzugen sie niedrigere Innentemperaturen.

            Die Komfortgrenzen werden über die adaptive Komfortgleichung berechnet:
            \[
                T_{\text{comf}} = 0.31 \cdot T_{\text{out}} + 17.8
            \]
            Daraus ergeben sich die **80 %‑** und **90 %‑Komfortzonen**.

            **Was zeigt die Grafik?**

            - Die Komfortzonen (80 % und 90 %) geben Bereiche an, in denen die Mehrheit der Personen
            thermischen Komfort empfindet.
            - Punkte oberhalb der Komfortzonen weisen auf mögliche Überhitzung hin.
            - Punkte unterhalb der Komfortzonen deuten auf Unterkühlung oder verstärkte Luftbewegung hin.
            - Die Streuung der Messpunkte zeigt, wie unterschiedlich Gebäude, Nutzungsarten oder Klimata
            auf die Außentemperatur reagieren.
            """
        )

    if df_filtered.empty:
        st.warning("Keine Daten für die ausgewählten Filter.")
        st.stop()

    df_sorted = df_filtered.sort_values(by="outdoor_air_temperature")

    T_out = df_sorted["outdoor_air_temperature"]
    T_in = df_sorted["operative_temperature"]

    T_comf = 0.31 * T_out + 17.8
    T_lower_80 = T_comf - 2.5
    T_upper_80 = T_comf + 2.5
    T_lower_90 = T_comf - 3.5
    T_upper_90 = T_comf + 3.5

    active_filters = {
        "Region": region,
        "Land": country,
        "Stadt": city,
        "Jahreszeit": season,
        "Klimazone": climate,
        "Gebäudetyp": building_type,
        "Kühlungsart": cooling_type,
        "Geschlecht": gender
    }

    filter_text = ", ".join([f"{k}: {v}" for k, v in active_filters.items() if v != "Alle"])

    st.subheader("Adaptive Comfort Chart")
    st.caption(f"Aktive Filter: {filter_text if filter_text else 'Keine Filter aktiv'}")

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
        "Die farbigen Bereiche markieren die 80 %‑ und 90 %‑Komfortzonen. "
        "Die Punkte zeigen die tatsächlichen Messwerte. "
        "So wird sichtbar, wie gut die Daten mit dem Modell übereinstimmen.")
# ---------------------------------------------------------
# ---------------------------------------------------------
# Tab : PMV/PPD
# ---------------------------------------------------------
with tab_PMV_PPD:
    st.subheader("🌡️ PMV/PPD Komfortanalyse")

    # ---------------------------------------------------------
    # 📘 Hintergrundinformationen als Expander
    # ---------------------------------------------------------
    with st.expander("ℹ️ Hintergrund – Was bedeuten PMV und PPD?"):
        st.markdown("""
            **PMV (Predicted Mean Vote)**  
            Der PMV-Wert beschreibt die *durchschnittliche thermische Empfindung* einer Gruppe von Personen 
            auf einer Skala von **–3 (sehr kalt)** bis **+3 (sehr warm)**.  
            Ein PMV von **0** bedeutet *thermische Neutralität*.

            PMV wird beeinflusst durch:
            - Operative Temperatur  
            - Luftgeschwindigkeit  
            - Luftfeuchtigkeit  
            - Bekleidung (clo)  
            - Aktivität (met)

            **PPD (Predicted Percentage Dissatisfied)**  
            Der PPD-Wert gibt an, wie viele Personen *voraussichtlich unzufrieden* mit der thermischen Umgebung sind.  
            Selbst bei PMV = 0 liegt PPD typischerweise bei **5 %**.

            Typische Werte:
            - PMV = 0 → PPD ≈ 5 %  
            - PMV = ±1 → PPD ≈ 25 %  
            - PMV = ±2 → PPD ≈ 75 %  
            - PMV = ±3 → PPD ≈ 99 %

            Die Kombination aus PMV und PPD ist der Standard nach **ASHRAE 55** und **ISO 7730** 
            zur Bewertung thermischen Komforts.
        """)

    # ---------------------------------------------------------
    # 📊 PMV/PPD Analyse
    # ---------------------------------------------------------
    if {"predicted_mean_vote", "predicted_percentage_dissatisfied"}.issubset(df_filtered.columns):

        pmv_df = df_filtered[
            ["predicted_mean_vote", "predicted_percentage_dissatisfied"]
        ].dropna()

        if pmv_df.empty:
            st.warning("Keine PMV/PPD-Daten verfügbar.")
        else:
            fig, ax = plt.subplots(figsize=(8, 5))

            # Scatterplot
            ax.scatter(
                pmv_df["predicted_mean_vote"],
                pmv_df["predicted_percentage_dissatisfied"],
                alpha=0.6,
                color="steelblue",
                label="Messpunkte"
            )

            # Komfortzonen-Linien
            ax.axvline(0, color="green", linestyle="--", linewidth=1.5, label="PMV = 0 (neutral)")
            ax.axvline(1, color="orange", linestyle="--", linewidth=1, label="PMV = +1 (leicht warm)")
            ax.axvline(-1, color="orange", linestyle="--", linewidth=1, label="PMV = -1 (leicht kühl)")
            ax.axhline(20, color="red", linestyle="--", linewidth=1.5, label="PPD = 20 % Grenze")

            # Achsenbeschriftung
            ax.set_xlabel("PMV (Predicted Mean Vote)")
            ax.set_ylabel("PPD (%) – Predicted Percentage Dissatisfied")

            # Titel
            ax.set_title("PMV/PPD Komfortanalyse")

            # Grid & Legende
            ax.grid(True, alpha=0.3)
            ax.legend()

            st.pyplot(fig)

            # Erklärung unter der Grafik
            st.markdown("""
            **Interpretation der Grafik:**  
            - Punkte rechts von PMV = +1 zeigen *Wärmeunzufriedenheit*.  
            - Punkte links von PMV = –1 zeigen *Kälteunzufriedenheit*.  
            - Werte über **PPD = 20 %** gelten nach ASHRAE 55 als *nicht komfortabel*.  
            - Der Bereich zwischen **PMV –0.5 bis +0.5** ist typischerweise *komfortabel*.  
            - Die Grafik zeigt, wie stark die Unzufriedenheit steigt, wenn PMV vom Neutralpunkt abweicht.
            """)
    else:
        st.warning("Benötigte Spalten sind nicht im Datensatz vorhanden.")


# ---------------------------------------------------------
# Tab 4: Korrelationsmatrix
# ---------------------------------------------------------
with tab_korrelation:
   
    st.subheader("📊 Korrelationsanalyse: Physikalische vs. Subjektive Komfortvariablen")

    # ---------------------------------------------------------
    # 📘 Hintergrund – Gesamtanalyse
    # ---------------------------------------------------------
    with st.expander("ℹ️ Hintergrund – Warum zwei Korrelationsmatrizen?"):
        st.markdown("""
            Komfort entsteht aus zwei Dimensionen:

            ### 1️⃣ Physikalische Komfortvariablen  
            Beschreiben die gemessene Umgebung:
            - Lufttemperatur  
            - Strahlungstemperatur  
            - Operative Temperatur  
            - Luftfeuchtigkeit  
            - Luftgeschwindigkeit  
            - Metabolische Rate  
            - Bekleidung (clo)

            ### 2️⃣ Subjektive Komfortvariablen  
            Beschreiben die Wahrnehmung der Personen:
            - Thermal Sensation  
            - Thermal Preference  
            - Thermal Acceptability  
            - Thermal Comfort

            Zwei Matrizen nebeneinander zeigen:
            - Wie stark physikalische Größen gekoppelt sind  
            - Wie logisch die subjektive Wahrnehmung ist  
            - Wie Filter (Region, Gebäudeart, Klima) die Zusammenhänge verändern
        """)

    # ---------------------------------------------------------
    # 📊 1. Physikalische Komfortvariablen
    # ---------------------------------------------------------
    phys_cols = [
        "air_temperature",
        "radiant_temperature",
        "operative_temperature",
        "relative_humidity",
        "air_speed",
        "metabolic_rate",
        "clothing_ensemble_insulation",
    ]
    phys_cols = [c for c in phys_cols if c in df_filtered.columns]

    # ---------------------------------------------------------
    # 📊 2. Subjektive Komfortvariablen (mit Mapping!)
    # ---------------------------------------------------------
    subj_cols = [
        "thermal_sensation",
        "thermal_preference",
        "thermal_acceptability",
        "thermal_comfort",
    ]
    subj_cols = [c for c in subj_cols if c in df_filtered.columns]

    # Mapping für subjektive Variablen
    mapping = {
        "no change": 0,
        "warmer": 1,
        "cooler": -1,
        "acceptable": 1,
        "unacceptable": -1,
        "comfortable": 1,
        "not comfortable": -1,
    }

    df_subj = df_filtered[subj_cols].replace(mapping)
    df_subj = df_subj.apply(pd.to_numeric, errors="coerce").dropna()

    # ---------------------------------------------------------
    # 📈 Side-by-side Darstellung
    # ---------------------------------------------------------
    if len(phys_cols) < 2:
        st.warning("Nicht genügend physikalische Variablen.")
    elif df_subj.empty:
        st.warning("Keine subjektiven Daten nach Mapping verfügbar.")
    else:
        col1, col2 = st.columns(2)

        # -------------------------
        # Physikalische Matrix
        # -------------------------
        with col1:
            st.markdown("### 🔵 Physikalische Komfortvariablen")
            phys_df = df_filtered[phys_cols].dropna()

            corr_phys = phys_df.corr()

            fig1, ax1 = plt.subplots(figsize=(6, 5))
            sns.heatmap(
                corr_phys,
                cmap="coolwarm",
                annot=True,
                fmt=".2f",
                vmin=-1,
                vmax=1,
                ax=ax1,
                linewidths=0.5,
            )
            ax1.set_title("Physikalische Komfortvariablen")
            st.pyplot(fig1)

            with st.expander("🧠 Interpretation – Physikalische Matrix"):
                st.markdown("""
                    **Hohe positive Korrelationen (rot)**  
                    → gekoppelte thermische Prozesse  
                    Beispiel: Lufttemperatur ↔ operative Temperatur

                    **Hohe negative Korrelationen (blau)**  
                    → gegenläufige Effekte  
                    Beispiel: Luftgeschwindigkeit ↔ operative Temperatur

                    **Schwache Korrelationen**  
                    → unabhängige Variablen  
                    Beispiel: Kleidung ↔ Luftfeuchtigkeit
                """)

        # -------------------------
        # Subjektive Matrix
        # -------------------------
        with col2:
            st.markdown("### 🔴 Subjektive Komfortvariablen")

            corr_subj = df_subj.corr()

            fig2, ax2 = plt.subplots(figsize=(6, 5))
            sns.heatmap(
                corr_subj,
                cmap="coolwarm",
                annot=True,
                fmt=".2f",
                vmin=-1,
                vmax=1,
                ax=ax2,
                linewidths=0.5,
            )
            ax2.set_title("Subjektive Komfortvariablen")
            st.pyplot(fig2)

            with st.expander("🧠 Interpretation – Subjektive Matrix"):
                st.markdown("""
                    **Thermal Sensation ↔ Thermal Preference**  
                    Hohe Korrelation bedeutet:  
                    → Wenn es warm empfunden wird, wünschen Personen eher kühlere Bedingungen.

                    **Thermal Acceptability ↔ Thermal Comfort**  
                    Hohe Korrelation bedeutet:  
                    → Wenn Bedingungen akzeptabel sind, werden sie auch als komfortabel bewertet.

                    **Schwache Korrelationen**  
                    → inkonsistente Wahrnehmung  
                    Beispiel: Personen empfinden warm, wünschen aber nicht kühler.
                """)


# ---------------------------------------------------------
# Tab 5: Datenverteilung
# ---------------------------------------------------------
with tab_verteilung:
    st.subheader(f"📈 Verteilung der Daten für: {x_label}")

    dist_df = df_filtered[x]

    # ---------------------------------------------------------
    # 1. Fehlwerte-Analyse
    # ---------------------------------------------------------
    missing_count = dist_df.isna().sum()
    total_count = len(dist_df)
    missing_percent = (missing_count / total_count) * 100 if total_count > 0 else 0

    with st.expander("ℹ️ Hintergrund – Datenqualität & Fehlwerte"):
        st.markdown(f"""
            **Fehlwerte in dieser Variable:**  
            - Anzahl: **{missing_count}**  
            - Anteil: **{missing_percent:.2f} %**

            Fehlwerte können entstehen durch:
            - fehlende Messgeräte  
            - Ausfälle in der Datenerfassung  
            - Filter, die bestimmte Zeiträume oder Gruppen ausschließen  
            - manuelle Eingabefehler

            **Warum wichtig?**  
            - Viele Fehlwerte → Analyse wird unzuverlässig  
            - Wenige Fehlwerte → Verteilung ist repräsentativ  
            - Fehlwerte können Muster zeigen (z. B. nur im Winter, nur in bestimmten Gebäuden)
        """)

    # ---------------------------------------------------------
    # 2. Nur gültige Werte für Analyse
    # ---------------------------------------------------------
    dist_df = dist_df.dropna()

    if dist_df.empty:
        st.warning("Keine gültigen Daten für diese Variable verfügbar.")
    else:

        # ---------------------------------------------------------
        # 3. Histogramm + Dichtefunktion
        # ---------------------------------------------------------
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.histplot(dist_df, kde=True, bins=30, color="steelblue")
        ax.set_xlabel(x_label)
        ax.set_ylabel("Häufigkeit")
        ax.set_title(f"Histogramm & Dichtefunktion für {x_label}")
        st.pyplot(fig)

        # ---------------------------------------------------------
        # 4. Statistische Kennzahlen
        # ---------------------------------------------------------
        mean_val = dist_df.mean()
        median_val = dist_df.median()
        std_val = dist_df.std()
        min_val = dist_df.min()
        max_val = dist_df.max()
        q1 = dist_df.quantile(0.25)
        q3 = dist_df.quantile(0.75)
        iqr = q3 - q1

        with st.expander("🧠 Interpretation – Form der Verteilung"):
            st.markdown(f"""
                **Statistische Kennzahlen für {x_label}:**

                - **Mittelwert:** {mean_val:.2f}  
                - **Median:** {median_val:.2f}  
                - **Standardabweichung:** {std_val:.2f}  
                - **Minimum:** {min_val:.2f}  
                - **Maximum:** {max_val:.2f}  
                - **1. Quartil (Q1):** {q1:.2f}  
                - **3. Quartil (Q3):** {q3:.2f}  
                - **Interquartilsabstand (IQR):** {iqr:.2f}

                ### 🔍 Was sagt das über die Verteilung aus?

                **Schiefe (Skewness):**
                - Wenn Mittelwert > Median → Verteilung ist *rechtssteil* (lange warme/heisse Werte)
                - Wenn Mittelwert < Median → Verteilung ist *linkssteil* (lange kalte Werte)

                **Breite der Verteilung:**
                - Hohe Standardabweichung → Werte stark gestreut  
                - Niedrige Standardabweichung → Werte eng beieinander

                **Ausreißer:**
                - Werte < Q1 - 1.5·IQR → ungewöhnlich niedrige Werte  
                - Werte > Q3 + 1.5·IQR → ungewöhnlich hohe Werte  

                **Multimodalität:**
                - Mehrere Peaks im Histogramm → verschiedene Komfortzustände oder Nutzergruppen
            """)

        # ---------------------------------------------------------
        # 5. Boxplot zur Ausreißeranalyse
        # ---------------------------------------------------------
        fig2, ax2 = plt.subplots(figsize=(6, 2))
        sns.boxplot(x=dist_df, color="lightblue")
        ax2.set_title(f"Boxplot – Ausreißeranalyse für {x_label}")
        st.pyplot(fig2)

        with st.expander("📦 Interpretation – Ausreißer & Spannweite"):
            st.markdown(f"""
                Der Boxplot zeigt:
                - **Median** (Linie in der Box)  
                - **Q1 und Q3** (Boxgrenzen)  
                - **IQR** (Boxhöhe)  
                - **Ausreißer** (Punkte außerhalb der Whisker)

                **Warum wichtig?**
                - Ausreißer können auf Messfehler hinweisen  
                - oder auf echte Extrembedingungen (z. B. sehr warme Räume)
                - Eine breite Box → hohe Variabilität  
                - Eine schmale Box → stabile Bedingungen
            """)


with tab_beziehungen:

    st.header("📈 Beziehungen zwischen Variablen")

    st.markdown("""
    Analysiere die Beziehung zwischen zwei ausgewählten Variablen. 
    Du kannst zwischen einem Streudiagramm (Scatter) und einem Liniendiagramm wählen.
    """)

    # Auswahl der Variablen
    x = st.selectbox("X‑Achse auswählen:", df_filtered.columns)
    y = st.selectbox("Y‑Achse auswählen:", df_filtered.columns)

    chart_type = st.radio("Diagrammtyp:", ["Scatter", "Line"], horizontal=True)

    x_label = x.replace("_", " ").title()
    y_label = y.replace("_", " ").title()

    st.subheader(f"{y_label} in Abhängigkeit von {x_label}")

    # Daten vorbereiten
    plot_df = df_filtered[[x, y]].dropna()

    if plot_df.empty:
        st.warning("Keine Daten für diese Auswahl verfügbar.")
    else:
        # Plot
        fig, ax = plt.subplots(figsize=(8, 5))

        if chart_type == "Scatter":
            ax.scatter(
                plot_df[x],
                plot_df[y],
                alpha=0.6,
                color="#4C72B0",
                edgecolors="none"
            )
        else:
            plot_df = plot_df.sort_values(by=x)
            ax.plot(
                plot_df[x],
                plot_df[y],
                alpha=0.8,
                color="#DD8452",
                linewidth=2
            )

        # Achsen & Layout
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor("#F7F7F7")

        # Titel
        ax.set_title(f"{y_label} vs. {x_label}", fontsize=14, fontweight="bold")

        st.pyplot(fig)


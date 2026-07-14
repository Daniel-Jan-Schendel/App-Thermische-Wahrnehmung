import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 



st.set_page_config(page_title="Globale Datenanalyse", layout="wide", initial_sidebar_state="expanded")

# Load data

df_bereinigt = pd.read_csv("db_bereinigt.csv")

#st.title("Globale Datenanalyse")
#st.line_chart(df_bereinigt["DB"])
#st.dataframe(df_bereinigt)

st.title("Explorative Datenanalyse")

#st.header("Datenverteilung")

# Klima / Building

tab1,tab2,tab3,tab4, tab5, tab6 = st.tabs(["Datenverteilung nach Ort","Kategorie","Thermischer Komfort: Einflussgrößen", "Karte", "Cooling typ, Gender, Alter", "Projekt-Architektur" ])


with tab1:

    col1, col2 = st.columns([2,1])
    col3, col4 = st.columns([2,1])
    col5, col6 = st.columns([2,1])

    with col1:

        # Region-Verteilung berechnen
        region_anzahl = df_bereinigt["region"].value_counts()
        region_prozent = (region_anzahl / region_anzahl.sum()) * 100
        
        

        # DataFrame für Altair vorbereiten
        region_df = pd.DataFrame({
                "Region": region_anzahl.index,
                "Anzahl": region_anzahl.values,
                "Prozent": region_prozent.values
            })
        
        # region_df = region_anzahl.to_frame(name="Anzahl")
        # region_df["Region"] = region_df.index
        region_df["Prozent"] = region_df["Prozent"].round(2).astype(str) + " %"
        region_df = region_df.reset_index(drop=True)


        st.subheader("Balkendiagramm: Anzahl Einträge je Region")

        chart = (
            alt.Chart(region_df)
            .mark_bar()
            .encode(
                x=alt.X("Anzahl:Q", title="Anzahl Einträge"),
                y=alt.Y("Region:N", sort="-x", title="Region"),
                tooltip=["Region", "Anzahl","Prozent"]
            )
            .properties(height=400)
        )

        st.altair_chart(chart, use_container_width=True)

    # --- Anzahl Einträge in der Kategorie ---
    with col2:
        st.markdown("### Übersicht Anzahl Einträge")
        # Prozentwerte berechnen
        region_prozent = (region_anzahl / region_anzahl.sum()) * 100

        # DataFrame für Anzeige erstellen
        region_df = pd.DataFrame({
            "Region": region_anzahl.index,
            "Anzahl": region_anzahl.values,
            "Prozent": region_prozent.values
        })

        # Schönere Formatierung
        region_df["Prozent"] = region_df["Prozent"].round(2).astype(str) + " %"

        st.write(region_df)

#########################################################################################################
#########################################################################################################

    with col3:

        # --- Verteilung nach Land berechnen ---
        land_anzahl = df_bereinigt["country"].value_counts()
        land_prozent = (land_anzahl / land_anzahl.sum()) * 100

        # --- DataFrame vorbereiten ---
        land_df = pd.DataFrame({
            "Land": land_anzahl.index,
            "Anzahl": land_anzahl.values,
            "Prozent": land_prozent.values
        })

        land_df["Prozent"] = land_df["Prozent"].round(2).astype(str) + " %"
        land_df = land_df.reset_index(drop=True)

        st.subheader("Balkendiagramm: Anzahl Einträge je Land")

        chart_land = (
            alt.Chart(land_df)
            .mark_bar()
            .encode(
                x=alt.X("Anzahl:Q", title="Anzahl Einträge"),
                y=alt.Y("Land:N", sort="-x", title="Land"),
                tooltip=["Land", "Anzahl", "Prozent"]
            )
            .properties(height=400)
        )

        st.altair_chart(chart_land, use_container_width=True)

    with col4:
        st.markdown("### Übersicht Anzahl Einträge")
        st.write(land_df)

#########################################################################################################
#########################################################################################################

    with col5:

        # --- Verteilung nach Stadt berechnen ---
        stadt_anzahl = df_bereinigt["city"].value_counts()
        stadt_prozent = (stadt_anzahl / stadt_anzahl.sum()) * 100

        # --- DataFrame vorbereiten ---
        stadt_df = pd.DataFrame({
            "Stadt": stadt_anzahl.index,
            "Anzahl": stadt_anzahl.values,
            "Prozent": stadt_prozent.values
        })

        stadt_df["Prozent"] = stadt_df["Prozent"].round(2).astype(str) + " %"
        stadt_df = stadt_df.reset_index(drop=True)

        st.subheader("Balkendiagramm: Anzahl Einträge je Stadt")

        chart_stadt = (
            alt.Chart(stadt_df)
            .mark_bar()
            .encode(
                x=alt.X("Anzahl:Q", title="Anzahl Einträge"),
                y=alt.Y("Stadt:N", sort="-x", title="Stadt"),
                tooltip=["Stadt", "Anzahl", "Prozent"]
            )   
            .properties(height=400)
        )

        st.altair_chart(chart_stadt, use_container_width=True)

    with col6:
        st.markdown("### Übersicht Anzahl Einträge")
        st.write(stadt_df)



#########################################################################################################
#########################################################################################################

with tab2:


    # ---------------------------------------------------------
    # Daten laden
    # ---------------------------------------------------------
    df = pd.read_csv("db_bereinigt_fertig.csv")

    # ---------------------------------------------------------
    # Plot-Funktion
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # ROW 1 → 2 Spalten: Filter + Building Type Plot
    # ---------------------------------------------------------
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        
        # ---------------------------------------------------------
        # MULTISELECT für Building Type
        # ---------------------------------------------------------
        st.header("Automatische Plots mit Filter")

        # Alle verfügbaren Gebäudetypen laden
        building_types = df["building_type"].dropna().unique()

        # Multiselect anzeigen
        selected_buildings = st.multiselect(
            "Building Type auswählen (Mehrfachauswahl möglich):",
            building_types,
            default=building_types[:1]  # optional: erstes Element vorauswählen
        )

        # Falls nichts ausgewählt wurde → gesamten Datensatz verwenden
        if len(selected_buildings) > 0:
            df_filtered = df[df["building_type"].isin(selected_buildings)]
        else:
            df_filtered = df.copy()


    with row1_col2:
        st.subheader("🏢 Building Type")
        fig_bt = plot_column(df_filtered["building_type"], "building_type")
        st.pyplot(fig_bt)

    # ---------------------------------------------------------
    # ROW 2 → 3 Spalten: season, climate, cooling_type
    # ---------------------------------------------------------
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.subheader("🌦️ Season")
        fig_season = plot_column(df_filtered["season"], "season")
        st.pyplot(fig_season)

    with row2_col2:
        st.subheader("🌍 Climate")
        fig_climate = plot_column(df_filtered["climate"], "climate")
        st.pyplot(fig_climate)

    with row2_col3:
        st.subheader("❄️ Cooling Type")
        fig_cooling = plot_column(df_filtered["cooling_type"], "cooling_type")
        st.pyplot(fig_cooling)

    # ---------------------------------------------------------
    # NEUE ROW → 4 Spalten: fan, heater, window, door
    # ---------------------------------------------------------
    row_fan, row_heater, row_window, row_door = st.columns(4)

    with row_fan:
        st.subheader("🌀 Fan")
        fig_fan = plot_column(df_filtered["fan"], "fan")
        st.pyplot(fig_fan)

    with row_heater:
        st.subheader("🔥 Heater")
        fig_heater = plot_column(df_filtered["heater"], "heater")
        st.pyplot(fig_heater)

    with row_window:
        st.subheader("🪟 Window")
        fig_window = plot_column(df_filtered["window"], "window")
        st.pyplot(fig_window)

    with row_door:
        st.subheader("🚪 Door")
        fig_door = plot_column(df_filtered["door"], "door")
        st.pyplot(fig_door)

    # ---------------------------------------------------------
    # ROW 3 → 3 Spalten: leer | age | gender
    # ---------------------------------------------------------
    row3_col1, row3_col2, row3_col3 = st.columns(3)

    with row3_col1:
        st.write("")  # bewusst leer

    with row3_col2:
        st.subheader("👤 Age")
        fig_age = plot_column(df_filtered["age"], "age")
        st.pyplot(fig_age)

    with row3_col3:
        st.subheader("🚻 Gender")
        fig_gender = plot_column(df_filtered["gender"], "gender")
        st.pyplot(fig_gender)








  # ---------------------------------------------------------
    # 📌 1. Daten laden
    # ---------------------------------------------------------
    df = pd.read_csv("db_bereinigt_fertig.csv")

    st.header("📊 Häufigkeitsanalyse: Thermal Comfort")

    # ---------------------------------------------------------
    # 🔧 1a. Thermische Parameter vorab runden / bereinigen
    # ---------------------------------------------------------
    # Falls deine Komfortvariablen numerisch sind, werden sie hier gerundet.
    # Falls sie kategorisch sind (z.B. -3 bis +3), passiert nichts.
    komfort_variablen = ["thermal_sensation", "thermal_comfort", "thermal_preference"]

    for var in komfort_variablen:
        if var in df.columns:
            # Nur numerische Werte runden
            if pd.api.types.is_numeric_dtype(df[var]):
                df[var] = df[var].round(2)

    # ---------------------------------------------------------
    # 🔍 2. Auswahl der Komfort-Variable
    # ---------------------------------------------------------
    variablen = {
        "Thermal Sensation": "thermal_sensation",
        "Thermal Comfort": "thermal_comfort",
        "Thermal Preference": "thermal_preference"
    }

    auswahl = st.selectbox(
        "Wähle eine Komfort-Variable",
        list(variablen.keys())
    )

    spalte = variablen[auswahl]

    # ---------------------------------------------------------
    # 🧹 3. Daten vorbereiten
    # ---------------------------------------------------------
    # Nur gültige Werte behalten
    df_plot = df.dropna(subset=[spalte])

    # Häufigkeiten berechnen
    freq = df_plot[spalte].value_counts().reset_index()
    freq.columns = ["Wert", "Anzahl"]

    # ---------------------------------------------------------
    # 📊 4. Balkendiagramm erstellen (Altair)
    # ---------------------------------------------------------
    chart = (
        alt.Chart(freq)
        .mark_bar(color="#2E86C1")
        .encode(
            x=alt.X("Wert:N", title=auswahl),        # Nur Label im Diagramm
            y=alt.Y("Anzahl:Q", title="Häufigkeit"),
            tooltip=["Wert", "Anzahl"]              # Tooltip bleibt sichtbar
        )
        .properties(
            width=600,
            height=400,
            title=f"Häufigkeitsverteilung: {auswahl}"
        )
    )

    st.altair_chart(chart, use_container_width=True)




#########################################################################################################
#########################################################################################################

with tab3:

    st.text("sdsd")

with tab4:

    # ---------------------------------------------------------
    # 📌 1. Daten laden
    # ---------------------------------------------------------
    df = pd.read_csv("db_bereinigt.csv")

    # Nur Zeilen behalten, die gültige Koordinaten haben
    df = df.dropna(subset=["latitude", "longitude"])

    st.subheader("🌍 Globale Verteilung der ASHRAE Feldstudien")


    # ---------------------------------------------------------
    # 🔍 2. Filter-Widgets (Jahr, Saison, Gebäudetyp)
    # ---------------------------------------------------------

    # Jahr-Filter
    years = sorted(df["year"].dropna().unique())
    year_filter = st.selectbox("Jahr auswählen", ["Alle"] + years)

    # Saison-Filter
    seasons = sorted(df["season"].dropna().unique())
    season_filter = st.selectbox("Saison auswählen", ["Alle"] + seasons)

    # Gebäudetyp-Filter
    building_types = sorted(df["building_type"].dropna().unique())
    building_filter = st.multiselect(
        "Gebäudetyp auswählen",
        building_types,
        default=building_types  # Standard: alle Typen ausgewählt
    )


    # ---------------------------------------------------------
    # 🔎 3. Filter anwenden
    # ---------------------------------------------------------

    filtered = df.copy()

    # Jahr anwenden
    if year_filter != "Alle":
        filtered = filtered[filtered["year"] == year_filter]

    # Saison anwenden
    if season_filter != "Alle":
        filtered = filtered[filtered["season"] == season_filter]

    # Gebäudetyp anwenden
    filtered = filtered[filtered["building_type"].isin(building_filter)]


    # ---------------------------------------------------------
    # 📌 4. Daten nach Stadt aggregieren
    # ---------------------------------------------------------
    # Jede Stadt bekommt einen Punkt, Größe = Anzahl der Datensätze

    city_counts = (
        filtered.groupby(["country", "city", "latitude", "longitude"])
        .size()
        .reset_index(name="count")
    )

    # Punktgröße skalieren (logarithmisch, damit große Städte nicht explodieren)
    city_counts["radius"] = np.log1p(city_counts["count"]) * 25000


    # ---------------------------------------------------------
    # 🗺️ 5. Pydeck Layer definieren (Scatterplot)
    # ---------------------------------------------------------

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=city_counts,
        get_position="[longitude, latitude]",  # Koordinaten
        get_radius="radius",                   # Punktgröße
        get_fill_color=[46, 134, 193, 180],    # ASHRAE-Blau
        pickable=True                          # Tooltip aktivieren
    )


    # ---------------------------------------------------------
    # 🌐 6. Kartenansicht definieren
    # ---------------------------------------------------------

    view_state = pdk.ViewState(
        latitude=city_counts["latitude"].mean() if len(city_counts) else 0,
        longitude=city_counts["longitude"].mean() if len(city_counts) else 0,
        zoom=1
    )

    # Tooltip-Design
    tooltip = {
        "html": "<b>{city}, {country}</b><br/>Studien: {count}",
        "style": {"color": "white"}
    }


    # ---------------------------------------------------------
    # 🧭 7. Karte rendern (ohne Mapbox-Key!)
    # ---------------------------------------------------------

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style=None   # ⭐ WICHTIG: Kein Mapbox → funktioniert ohne Key
        )
    )




#############################################################################################################################

# # -------------------------------
# # TAB: Verteilung
# # -------------------------------
# tab_verteilung = st.tabs(["Verteilung"])[0]

# with tab_verteilung:

#     st.subheader("Interaktive Filter: Land → Region → Stadt")

#     # --- Filter 1: Land ---
#     laender = df_bereinigt["country"].dropna().unique()
#     land = st.selectbox("Land auswählen", sorted(laender))

#     # --- Filter 2: Region ---
#     regionen = df_bereinigt[df_bereinigt["country"] == land]["region"].dropna().unique()
#     region = st.selectbox("Region auswählen", sorted(regionen))

#     # --- Filter 3: Stadt ---
#     staedte = df_bereinigt[
#         (df_bereinigt["country"] == land) &
#         (df_bereinigt["region"] == region)
#     ]["city"].dropna().unique()

#     stadt = st.selectbox("Stadt auswählen", sorted(staedte))

    # --- Gefilterte Daten ---
    # gefiltert = df_bereinigt[
    #     (df_bereinigt["country"] == land) &
    #     (df_bereinigt["region"] == region) &
    #     (df_bereinigt["city"] == stadt)
    # ]

    # st.markdown("### Gefilterte Daten")
    # st.dataframe(gefiltert)
    # st.markdown("---")

    # -------------------------------
    # 2×2 Layout
    # -------------------------------


# col5, col6, col7 = st.columns([1,2,1])
# col1, col2 = st.columns(2)
# col3, col4 = st.columns(2)
    
# with col5:
#     st.subheader("Interaktive Filter: Region →  Land → Stadt")

#     # --- Filter 1: Region ---
#     regionen = df_bereinigt["region"].dropna().unique()
#     region = st.selectbox("Region auswählen", sorted(regionen))

#     # --- Filter 2: Land (abhängig von Region) ---
#     laender = df_bereinigt[df_bereinigt["region"] == region]["country"].dropna().unique()
#     land = st.selectbox("Land auswählen", sorted(laender))

#     # --- Filter 3: Stadt (abhängig von Region & Land) ---
#     staedte = df_bereinigt[
#         (df_bereinigt["region"] == region) &
#         (df_bereinigt["country"] == land)
#         ]["city"].dropna().unique()
#     stadt = st.selectbox("Stadt auswählen", sorted(staedte))

#     # #--- Gefilterte Daten ---
# gefiltert = df_bereinigt[
#     (df_bereinigt["country"] == land) &
#     (df_bereinigt["region"] == region) &
#     (df_bereinigt["city"] == stadt)
# ]

#     # st.markdown("### Gefilterte Daten")
#     # st.dataframe(gefiltert)

# with col6:
#     st.markdown("### Verteilung innerhalb der Region")
#     st.bar_chart(
#         df_bereinigt[
#             (df_bereinigt["country"] == land) &
#             (df_bereinigt["region"] == region)
#         ]["city"].value_counts()
#     )
# with col7: 
#     st.markdown("### Anzahl Einträge")
#     st.write(f"**Land ({land}):** {len(df_bereinigt[df_bereinigt['country'] == land])}")
#     st.write(f"**Region ({region}):** {len(df_bereinigt[df_bereinigt['region'] == region])}")
#     st.write(f"**Stadt ({stadt}):** {len(gefiltert)}")

# # --- Bild / Karte ---
# with col1:
#     st.markdown("### Standortkarte")
#     if "latitude" in gefiltert.columns and "longitude" in gefiltert.columns:
#         st.map(gefiltert[["latitude", "longitude"]])
#     else:
#         st.info("Keine geografischen Koordinaten verfügbar.")

# # --- Prozentuale Verteilung ---
# with col2:
#     st.markdown("### Prozentuale Verteilung")
#     st.write("**Region:**")
#     st.write(df_bereinigt[df_bereinigt["country"] == land]["region"]
#                 .value_counts(normalize=True)[region] * 100)
    
#     st.write("**Land:**")
#     st.write(df_bereinigt["country"].value_counts(normalize=True)[land] * 100)

#     st.write("**Stadt:**")
#     st.write(df_bereinigt[
#         (df_bereinigt["country"] == land) &
#         (df_bereinigt["region"] == region)
#     ]["city"].value_counts(normalize=True)[stadt] * 100)

# # --- Anzahl Einträge pro Region / Land / Stadt ---
# with col3:
#     st.markdown("### Anzahl Einträge")
#     st.write(f"**Region ({region}):** {len(df_bereinigt[df_bereinigt['region'] == region])}")
#     st.write(f"**Land ({land}):** {len(df_bereinigt[df_bereinigt['country'] == land])}")
#     st.write(f"**Stadt ({stadt}):** {len(gefiltert)}")

# # --- Balkendiagramm ---
# with col4:
#     st.markdown("### Verteilung innerhalb der Region")
#     st.bar_chart(
#         df_bereinigt[
#             (df_bereinigt["country"] == land) &
#             (df_bereinigt["region"] == region)
#         ]["city"].value_counts()
#     )



# # Copy dataframe
# df = df_bereinigt.copy()


# # Convert to numeric
# df["latitude"] = df["latitude"].astype(float)
# df["longitude"] = df["longitude"].astype(float)

# # Create a reduced table with unique combinations
# df_list = df[["city", "country", "region", "latitude", "longitude"]].drop_duplicates()

# # Create a map

# regions = df_list["region"].unique()
# color_map = {region: [int(i*60) % 255, int(i*120) % 255, int(i*180) % 255] for i, region in enumerate(regions)}

# df_list["color"] = df_list["region"].map(color_map)

# layer = pdk.Layer("ScatterplotLayer", df_list, get_position='[longitude, latitude]', get_fill_color='color', get_radius=50000,)

# view_state = pdk.ViewState(latitude=df_list["latitude"].mean(), longitude=df_list["longitude"].mean(), zoom=1.3)

# st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))


# # st.subheader("Anzahl der Regionen in der ASHRAE-Datenbank")

# # # Anzahl eindeutiger Regionen
# # num_regions = df_list["region"].dropna().unique()

# # # Liste der Regionen
# # num_regions = [str(r) for r in num_regions]

# # st.write("Regionen:")
# # st.write(", ".join(num_regions))

# # st.write(f"Es gibt **{num_regions}** verschiedene Regionen in der Datenbank.")
# # st.write("Regionen:")
# # st.write(", ".join(num_regions))





# #st.subheader("Geografische Verteilung – Interaktive Auswahl")



# ==============================================================================
# 📊 TAB 5: INTERAKTIVE KOMFORTANALYSE (GRAFIKEN MIT INTERNEN NUMMERN)
# ==============================================================================
with tab5:
    # Aufteilung des Layouts in zwei feste Hauptspalten für ein klares Design
    col1, col2 = st.columns([1, 1.5]) 
    
    with col1: 
        # Labels & Farbpaletten (Originale Struktur + Anpassung für Akzeptanz)
        tsv_labels = { -3: "–3 Sehr kalt", -2: "–2 Kalt", -1: "–1 Kühl", 0: "0 Neutral", 1: "+1 Warm", 2: "+2 Heiß", 3: "+3 Sehr heiß" } 
        tsv_colors = { -3: "#4575b4", -2: "#74add1", -1: "#abd9e9", 0: "#d9d9d9", 1: "#fdae61", 2: "#f46d43", 3: "#d73027" } 
        tp_labels = { -1: "–1 Kühler bevorzugt", 0: "0 Keine Präferenz", 1: "+1 Wärmer bevorzugt" } 
        tp_colors = { -1: "#74add1", 0: "#d9d9d9", 1: "#f46d43" } 
        tc_labels = { 1: "1 Ungemütlich", 2: "2 Leicht ungemütlich", 3: "3 Akzeptabel / Neutral", 4: "4 Leicht gemütlich", 5: "5 Gemütlich", 6: "6 Sehr gemütlich" } 
        tc_colors = { 1: "#fc8d59", 2: "#fee08b", 3: "#d9d9d9", 4: "#a6d96a", 5: "#1a9850", 6: "#006837" } 
        ta_labels = { 0: "0 Unakzeptabel", 1: "1 Akzeptabel" }
        ta_colors = { 0: "#d73027", 1: "#1a9850" }

        # Logisches Daten-Mapping (Behandlung von Nullwerten und Textzeichenfolgen)
        tp_map = {"cooler": -1, "no change": 0, "warmer": 1, "unknown": np.nan} 
        ta_map = {"acceptable": 1, "unacceptable": 0, "unknown": np.nan}

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
            
        # Plot-Funktion (Zentrierte Nummern innerhalb der Balken + Legende)
        def plot_comfort_variable(series, labels, colors, title): 
            series = pd.to_numeric(series, errors="coerce").dropna() 
            counts = series.value_counts().sort_index() 
            total = counts.sum() 
            if total == 0:
                st.info("Keine Daten für diese Auswahl verfügbar.")
                return
                
            fig, ax = plt.subplots(figsize=(8, 4.5)) 
            
            x_positions = [str(level) for level in counts.index]
            y_values = counts.values
            bar_colors = [colors[level] for level in counts.index]
            
            bars = ax.bar(x_positions, y_values, color=bar_colors)
            
            # 🌟 KORREKTUR: Platzierung der Zahlen INNERHALB der Balken (va="top")
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    # Der Versatz platziert die Zahl knapp unter die Oberkante des Balkens
                    ax.text(
                        bar.get_x() + bar.get_width()/2., 
                        height - (height * 0.05) - 0.2, 
                        f"{int(height)}", 
                        ha="center", 
                        va="top", 
                        fontsize=10, 
                        fontweight='bold', 
                        color="black" # Ändern zu "white" falls dunkle Balken die Lesbarkeit stören
                    ) 
            
            for level in sorted(counts.index):
                ax.plot([], [], color=colors[level], label=labels[level], linewidth=10)
            
            ax.set_title(title, fontweight='bold', fontsize=12, pad=12) 
            ax.set_xlabel("Comfort Level Index", fontweight='bold', fontsize=9) 
            ax.set_ylabel("Anzahl (Stimmen)", fontweight='bold', fontsize=9) 
            
            plt.xticks(rotation=0, ha="center")
            ax.legend(title="Legende (Komfortstufen)", loc="best", framealpha=0.9, fontsize=8)
            plt.tight_layout()
            st.pyplot(fig) 
            
        # Laden der originalen lokalen CSV-Datei
        df = pd.read_csv("db_bereinigt_fertig.csv") 
        df["thermal_sensation_cat"] = df["thermal_sensation"].apply(map_tsv) 
        df["thermal_preference_cat"] = df["thermal_preference"].map(tp_map) 
        df["thermal_comfort_cat"] = df["thermal_comfort"].apply(map_tc) 
        df["thermal_acceptability_cat"] = df["thermal_acceptability"].map(ta_map)
        
        st.header("Komfortanalyse") 
        
        comfort_option = st.selectbox( 
            "Komfortvariable auswählen:", ["Thermal Comfort", "Thermal Sensation", "Thermal Preference", "Thermal Acceptability"] 
        ) 
        
        geo_map = { "Region": "region", "Land": "country", "Stadt": "city" } 
        geo_option = st.selectbox("Geografische Verteilung anzeigen nach:", list(geo_map.keys())) 
        geo_colname = geo_map[geo_option] 
        
        geo_values = df[geo_colname].dropna() 
        geo_choice = st.selectbox(f"{geo_option} auswählen:", sorted(geo_values.unique())) 
        
        # Vertikale Anordnung der kaskadierenden Filter in Spalte 1 (col1)
        df['building_type'] = df['building_type'].fillna('Unknown')
        lista_building_types = sorted(df['building_type'].unique().tolist())
        building_choice = st.selectbox("Building Type auswählen:", lista_building_types)
        
        df['cooling_type'] = df['cooling_type'].fillna('Unknown')
        lista_cooling = sorted(df['cooling_type'].unique().tolist())
        cooling_choice = st.selectbox("Cooling Type auswählen:", lista_cooling)
        
        lista_generos = sorted(df['gender'].dropna().unique().tolist())
        gender_choice = st.selectbox("Gender auswählen:", lista_generos)
        
        edad_min = float(df['age'].min()) if not pd.isna(df['age'].min()) else 0.0
        edad_max = float(df['age'].max()) if not pd.isna(df['age'].max()) else 100.0
        rango_edad = st.slider("Alter (Age) Bereich:", min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max), step=1.0)

        # Kaskadierende Filterlogik mit Entpacken des Slider-Bereichs
        df_geo_base = df[df[geo_colname] == geo_choice] 
        edad_min_sel, edad_max_sel = rango_edad
        
        df_geo = df_geo_base[
            (df_geo_base['building_type'] == building_choice) &
            (df_geo_base['cooling_type'] == cooling_choice) &
            (df_geo_base['gender'] == gender_choice) &
            (df_geo_base['age'] >= edad_min_sel) &  
            (df_geo_base['age'] <= edad_max_sel)    
        ]

    with col2: 
        st.subheader(f"📈 Verteilung – {comfort_option} ({geo_choice})") 
        
        # Renderizado de los gráficos univariables
        if comfort_option == "Thermal Comfort": 
            plot_comfort_variable(df_geo["thermal_comfort_cat"], tc_labels, tc_colors, f"Thermal Comfort") 
        elif comfort_option == "Thermal Sensation": 
            plot_comfort_variable(df_geo["thermal_sensation_cat"], tsv_labels, tsv_colors, f"Thermal Sensation") 
        elif comfort_option == "Thermal Preference": 
            plot_comfort_variable(df_geo["thermal_preference_cat"], tp_labels, tp_colors, f"Thermal Preference") 
        elif comfort_option == "Thermal Acceptability":
            plot_comfort_variable(df_geo["thermal_acceptability_cat"], ta_labels, ta_colors, f"Thermal Acceptability")
            
        st.markdown("---")
        
        # 🌟 EXAKTE REDAKTION: Leitfaden ohne kryptische Kürzungszeichen
        st.markdown(f"#### ❓ **Analyse-Leitfaden: Beeinflusst die Belüftungsart den aktuellen Parameter?**")
        
        # Dynamischer Textblock basierend auf der selektierten Variable
        if comfort_option == "Thermal Comfort":
            st.markdown(
                "* **Einfluss auf die Behaglichkeit:** Natürlich belüftete Gebäude weisen oft eine breitere Toleranzgrenze auf, da Nutzer adaptive Anpassungsmechanismen wie das Öffnen von Fenstern nutzen.\n"
                "* **Normen-Vergleich:** Klimatisierte Räume erzielen eine engere Clusterung um den Neutralpunkt, schränken jedoch die individuelle thermische Freiheit der Gebäudenutzer stark ein.\n"
                "* **Gebäude-Verhalten:** Mechanische Belüftung stabilisiert das Komfortniveau im Sommer, kann jedoch bei unzureichender Wartung zu einer erhöhten Unzufriedenheit führen."
            )
        elif comfort_option == "Thermal Sensation":
            st.markdown(
                "* **Thermische Wahrnehmung:** Die Belüftungsart steuer direkt die Luftgeschwindigkeit und die operative Temperatur, was die sensorischen Stimmen massiv verschiebt.\n"
                "* **Erwartungshaltung:** In klimatisierten Räumen erwarten Nutzer eine konstante Temperatur, weshalb kleine Abweichungen sofort als extrem warm oder kalt empfunden werden.\n"
                "* **Demografischer Faktor:** Die Kombination aus Belüftungsart und Alter zeigt, dass ältere Gruppen in natürlich belüfteten Zonen sensibler auf Zugluft reagieren."
            )
        elif comfort_option == "Thermal Preference":
            st.markdown(
                "* **Nutzerpräferenz:** In natürlich belüfteten Gebäuden tolerieren die Befragten höhere Innentemperaturen und äußern seltener den Wunsch nach intensiver Kühlung.\n"
                "* **Klimatisierungs-Effekt:** Nutzer in mechanisch gekühlten Räumen neigen statistisch dazu, permanent einen kühleren Zustand wie kühler bevorzugt zu fordern.\n"
                "* **Saisonaler Einfluss:** Die Präferenzkurve flacht ab, wenn das Gebäude den Nutzern erlaubt, die Luftbewegung eigenständig zu regulieren."
            )
        elif comfort_option == "Thermal Acceptability":
            st.markdown(
                "* **Akzeptanz-Verhalten:** Die thermische Akzeptanz sinkt in klimatisierten Räumen drastisch, wenn die relative Luftfeuchtigkeit außerhalb des optimalen Bereichs liegt.\n"
                "* **Anpassungspotenzial:** Natürlich belüftete Strukturen erzielen trotz höherer Absoluttemperaturen eine hohe Akzeptanzrate aufgrund des psychologischen Gewöhnungseffekts.\n"
                "* **Statistische Relevanz:** Nullwerte treten vermehrt in mechanischen Systemen auf, was auf eine geringere Interaktion der Nutzer mit der Gebäudetechnik hinweist."
            ) 

#import base64

# ==============================================================================
# 🌟 TAB 6: NEON INFRASTRUKTUR-DOKUMENTATION 
# ==============================================================================
with tab6:
    # Renderizamos el título principal limpio usando la misma lógica que propusiste
    st.markdown("## **Cloud-native Infrastruktur & Datenmodellierung**")
    
    # Einleitende Infobox zur Neon-Plattform
    st.info(
        "**Neon** ist eine cloudnative, serverlose PostgreSQL-Datenbank, "
        "die speziell für moderne Entwickler konzipiert wurde. Sie bietet "
        "sofortiges Branching (Datenbank-Klonen) sowie eine vollständig automatische "
        "Skalierung der Rechenleistung."
    )
    
    st.markdown("---")
    
    # Symmetrisches Zwei-Spalten-Layout für die technische Dokumentation
    col_doc1, col_doc2 = st.columns(2)
    
    with col_doc1:
        st.markdown("### 📊 **Ausgangssituation & Herausforderung**")
        st.markdown(
            "**Datensatz:** ASHRAE v2.1-Datenbank mit über **109.033 Messungen** und **59 strukturierten Spalten**.\n\n"
            "**Zielstellung:** Aufbau einer hochverfügbaren, performanten Cloud-Infrastruktur, um Echtzeit-Analysen "
            "für das gesamte Projektteam plattformunabhängig bereitzustellen."
        )
        
        st.markdown("### ⚡ **Systemvorteile der Cloud**")
        st.markdown(
            "* **Skalierbarkeit:** Automatische Anpassung an große Abfragemengen bei minimaler Latenz.\n"
            "* **Ressourcen-Trennung:** Unabhängige Verwaltung von Cloud-Speicher und Rechenleistung.\n"
            "* **Sicherheit:** Verschlüsselte Ende-zu-Ende-Verbindung über sichere SSL-Kanäle."
        )

        st.markdown("### 🧱 **Datenbank-Architektur & Optimierung**")
        st.markdown(
            "**Modellierung:** Erfolgreiche Überführung einer flachen Tabelle in eine **optimierte, relationale Datenbankstruktur**.\n\n"
            "Durch diese gezielte Normalisierung wurde die Performance der Abfragen in Python signifikant optimiert."
        )
        
        st.success("**dim_buildings:** Stammdaten-Katalog für die einzigartigen Gebäudestrukturen (9 Spalten).")
        st.success("**fact_thermal_records:** Zentrale Faktentabelle mit 50 Metrik- und Sensor-Spalten (Sensation, Comfort, Preference, Acceptability).")
        
        # 2. Saubere Power BI Erklärung (Sección ejecutiva limpia)
        st.markdown("### 📊 **BI-Ökosystem & Power BI-Integration**")
        st.markdown(
            "**Daten-Schnittstelle:** Die normalisierte relationale Struktur ermöglicht eine direkte, "
            "native Anbindung an **Microsoft Power BI** über standardisierte PostgreSQL-Connectors."
        )


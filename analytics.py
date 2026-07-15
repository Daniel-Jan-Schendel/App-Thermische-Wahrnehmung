import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import chi2_contingency



st.set_page_config(page_title="Explorative Datenanalyse", layout="wide", initial_sidebar_state="expanded")

# Load data

df_bereinigt = pd.read_csv("db_bereinigt_fertig.csv")

#st.title("Globale Datenanalyse")
#st.line_chart(df_bereinigt["DB"])
#st.dataframe(df_bereinigt)

st.title("Explorative Datenanalyse")

#st.header("Datenverteilung")

# Klima / Building

tab1,tab2,tab3,tab4, tab5 = st.tabs(["Datenverteilung nach Ort","Übersicht Datenverteilung wichtige Variablen","Thermische Bewertung und Klima", "Karte", "Cooling typ und Alter"])


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


        st.subheader("Anzahl Einträge je Region")

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
        st.markdown("### Übersicht Anzahl Einträge je Region")
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

        st.subheader("Anzahl Einträge je Land")

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
        st.markdown("### Übersicht Anzahl Einträge je Land")
        st.write(land_df)

#########################################################################################################
#########################################################################################################

    with col5:

        # --- Verteilung nach climate berechnen ---
        climate_anzahl = df_bereinigt["climate"].value_counts()
        climate_prozent = (climate_anzahl / climate_anzahl.sum()) * 100 # Prozentzahl stimmt noch nicht

        # --- DataFrame vorbereiten ---
        climate_df = pd.DataFrame({
            "Klima": climate_anzahl.index,
            "Anzahl": climate_anzahl.values,
            "Prozent": climate_anzahl.values
        })

        climate_df["Prozent"] = climate_df["Prozent"].round(2).astype(str) + " %"
        climate_df = climate_df.reset_index(drop=True)

        st.subheader("Anzahl Einträge je Klima")

        chart_stadt = (
            alt.Chart(climate_df)
            .mark_bar()
            .encode(
                x=alt.X("Anzahl:Q", title="Anzahl Einträge"),
                y=alt.Y("Klima:N", sort="-x", title="Klima"),
                tooltip=["Klima", "Anzahl", "Prozent"]
            )   
            .properties(height=400)
        )

        st.altair_chart(chart_stadt, use_container_width=True)

    with col6:
        st.markdown("### Übersicht Anzahl Einträge je Klima")
        st.write(climate_df)



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
    # ROW 2 → 3 Spalten: season, climate, cooling_type
    # ---------------------------------------------------------
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.subheader("🌦️ Season")
        fig_season = plot_column(df["season"], "season")
        st.pyplot(fig_season)

    with row2_col2:
        st.subheader("❄️ Cooling Type")
        fig_cooling = plot_column(df["cooling_type"], "cooling_type")
        st.pyplot(fig_cooling)

    with row2_col3:
        st.subheader("🏢 Building Type")
        fig_bt = plot_column(df["building_type"], "building_type")
        st.pyplot(fig_bt)

    # ---------------------------------------------------------
    # NEUE ROW → 4 Spalten: fan, heater, window, door
    # ---------------------------------------------------------
    row_fan, row_heater, row_window, row_door = st.columns(4)

    with row_fan:
        st.subheader("🌀 Fan")
        fig_fan = plot_column(df["fan"], "fan")
        st.pyplot(fig_fan)

    with row_heater:
        st.subheader("🔥 Heater")
        fig_heater = plot_column(df["heater"], "heater")
        st.pyplot(fig_heater)

    with row_window:
        st.subheader("🪟 Window")
        fig_window = plot_column(df["window"], "window")
        st.pyplot(fig_window)

    with row_door:
        st.subheader("🚪 Door")
        fig_door = plot_column(df["door"], "door")
        st.pyplot(fig_door)

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

    with row3_col3:
        st.subheader("🚻 Gender")
        fig_gender = plot_column(df["gender"], "gender")
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
    # ---------------------------------------------------------
    # 📌 1. Daten laden
    # ---------------------------------------------------------
    df = pd.read_csv("db_bereinigt_fertig.csv")

    st.header("🌍 Gibt es einen Zusammenhang zwischen Klimazone und thermischer Bewertung?")

    
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])
    col3, col4 = st.columns([2,2])
    col5, col6 = st.columns([2,2])
    col7, col8 = st.columns([2,2])
    col9, col10 = st.columns([2,1])
    col11, col12 = st.columns([2,1])

    with col1:

        st.markdown("""
        Untersuchung des Zusammenhangs der 4 Hauptklimazonen mit den thermischen Bewertungsvariablen:

        - Thermal Comfort
        - Thermal Sensation
        - Thermal Preference
        - Thermal Acceptability
        """)

    with col2:
        with st.expander("Allgemeine Informationen zum Lesen der Boxplots"):
            st.markdown("""
            Erklärung des Boxplot:
                     
            - Box: zeigt, in welchem Bereich 50% der Werte für diese Klimazone liegen
            - Linie: stellt Median dar
            - Whisker: zeigen den Bereich, in dem die meisten Datenwerte liegen
            - Punkte außerhalb der Whisker: stellen Ausreißer dar
            """)

    # ---------------------------------------------------------
    # 📊 2. Grafiken erstellen
    # ---------------------------------------------------------

    # - Grafik - 
    with col3:

        st.subheader("Thermal Comfort nach Klimazone")

        fig, ax = plt.subplots(figsize=(8, 5))

        # Boxplot
        sns.boxplot(
            data=df,
            x="climate_zone",
            y="thermal_comfort",
            showfliers=False,
            width=0.6,
            boxprops=dict(facecolor="none", edgecolor="black"),  # transparente Box
            whiskerprops=dict(color="black"),
            capprops=dict(color="black"),
            medianprops=dict(color="red", linewidth=2.5),
            ax=ax
        )

        # Jitter-Plot
        sns.stripplot(
            data=df,
            x="climate_zone",
            y="thermal_comfort",
            jitter=0.25,
            size=1.5,             # etwas größere Punkte
            alpha=0.05,         # besser sichtbar
            color="steelblue",
            ax=ax,
            hue="thermal_comfort",
            palette="viridis",
            legend=False
        )

        ax.set_xlabel("Climate Zone")
        ax.set_ylabel("Thermal Comfort")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)

        with st.expander("Lesen des Boxplot zu Thermal Comfort"):
            st.markdown("""
            **Erkenntnisse Thermal Comfort:**
                    
            - Median ist bei Continental deutlich niedriger als bei den anderen Klimazonen -> hat aber auch größere Streuung der Werte
            - Dry und Tropical: kleinste Streuung der Werte
            - größter Unterschied liegt zwischen Continental und den anderen Klimazonen
            """)
              
        st.markdown("""
        **-> Bedeutung des Boxplot zu Thermal Comfort:**
        
        Befragte in der Klimazone "Continental" bewerten den Komfort tendenziell geringer als in den anderen 3 Klimazonen
        """)
        st.markdown("<br><br>", unsafe_allow_html=True)

    with col4:

        st.subheader("Thermal Sensation nach Klimazone")
        fig, ax = plt.subplots(figsize=(8, 5))

        # Boxplot
        sns.boxplot(
            data=df,
            x="climate_zone",
            y="thermal_sensation",
            showfliers=False,
            width=0.6,
            boxprops=dict(facecolor="none", edgecolor="black"),  # transparente Box
            whiskerprops=dict(color="black"),
            capprops=dict(color="black"),
            medianprops=dict(color="red", linewidth=2.5),
            ax=ax
        )

        # Jitter-Plot
        sns.stripplot(
            data=df,
            x="climate_zone",
            y="thermal_sensation",
            jitter=0.25,
            size=1.5,             # etwas größere Punkte
            alpha=0.05,         # besser sichtbar
            color="steelblue",
            ax=ax,
            hue="thermal_sensation",
            palette="viridis",
            legend=False
        )

        ax.set_xlabel("Climate Zone")
        ax.set_ylabel("Thermal Sensation")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)

        with st.expander("Lesen des Boxplot zu Thermal Sensation"):
            st.markdown("""
            **Erkenntnisse Thermal Sensation:**
                    
            - Median ist bei allen Klimazonen gleich
            - Temperate und Continental: kleinste Streuung der Werte
            - Dry und Tropical: größte Streuung der Werte
            """)

        st.markdown("""                   
        **-> Bedeutung des Boxplot zu Thermal Sensation:**
        
        - In allen vier Klimazonen wird das thermische Empfinden tendenziell mit "neutral" bewertet
        - In den Klimazonen "Temperate" und "Continental" haben 50% der Befragten das thermische Empfinden mit "neutral" oder "warm" bewertet
        - In den Klimazonen "Dry" und "Tropical" haben 50% der Befragten das thermische Empfinden mit "kühl", "neutral" oder "warm" bewertet
        """)
        
    with col7:
        st.subheader("Thermal Preference nach Klimazone")

        df_preference_plot = df[df["thermal_preference"] != "Unknown"]

        fig, ax = plt.subplots(figsize=(8, 5))

        # Boxplot
        sns.boxplot(
            data=df_preference_plot,
            x="climate_zone",
            y="thermal_preference",
            showfliers=False,
            width=0.6,
            boxprops=dict(facecolor="none", edgecolor="black"),  # transparente Box
            whiskerprops=dict(color="black"),
            capprops=dict(color="black"),
            medianprops=dict(color="red", linewidth=2.5),
            ax=ax
        )

        # Jitter-Plot
        sns.stripplot(
            data=df_preference_plot,
            x="climate_zone",
            y="thermal_preference",
            jitter=0.25,
            size=1.5,             # etwas größere Punkte
            alpha=0.05,         # besser sichtbar
            color="steelblue",
            ax=ax,
            hue="thermal_preference",
            palette="viridis",
            legend=False
        )

        ax.set_xlabel("Climate Zone")
        ax.set_ylabel("thermal Preference")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)

        with st.expander("Lesen des Boxplot zu Thermal Preference"):
            st.markdown("""
            **Erkenntnisse Thermal Preference:**
                    
            - Median ist bei allen Klimazonen gleich
            - Continental: kleinste Streuung der Werte
            - größter Unterschied liegt zwischen Continental und den anderen Klimazonen
            """)

        st.markdown("""
        
                    
        **-> Bedeutung des Boxplot zu Thermal Preference:**
        - In allen vier Klimazonen wurde tendenziell keine Veränderung gewünscht
        - In den Klimazonen "Temperate", "Dry" und "Tropical" haben 50% der Befragten "keine Veränderung" oder "wärmer bevorzugt" angegeben
        """)

        st.markdown("<br><br>", unsafe_allow_html=True)

    with col8:
        st.subheader("Thermal Acceptability nach Klimazone")

        def plot_thermal_acceptability_percent(df):
            # Prozentanteile pro Klimazone berechnen
            acceptability_pct = (
                pd.crosstab(
                    df["climate_zone"],
                    df["thermal_acceptability"],
                    normalize="index"
                ) * 100
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            acceptability_pct.plot(
                kind="bar",
                stacked=False,
                color=["darkgrey", "royalblue", "powderblue"],
                ax=ax
            )

            ax.set_xlabel("Climate Zone")
            ax.set_ylabel("Percentage (%)")
            ax.set_title("Thermal Acceptability nach Klimazone")

            ax.set_ylim(0, 100)  # feste Skala von 0 bis 100 %

            ax.legend(
                title="Thermal Acceptability",
                bbox_to_anchor=(1.05, 1),
                loc="upper left"
            )

            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()

            return fig
        
        fig_acceptability = plot_thermal_acceptability_percent(df)

        st.pyplot(fig_acceptability)

        with st.expander("Lesen des Diagramms zu Thermal Acceptability"):
            st.markdown("""
            **Erkenntnisse Thermal Acceptability:**
            
            """)

        st.markdown("""
        **-> Bedeutung des Boxplot zu Thermal Acceptability:**
        
        """)

    # ---------------------------------------------------------
    # 📊 3. Ergebnistabelle erstellen
    # ---------------------------------------------------------
    with col5:
        st.markdown("### Ergebnisse")
    
        # DataFrame für Anzeige erstellen
        # Mittelwert und Median pro Klimazone berechnen
        climate_zone_stats = (
            df
            .groupby("climate_zone")["thermal_comfort"]
            .agg(["mean", "median"])
            .reset_index()
        )

        # Spalten benennen
        climate_zone_stats.columns = ["Klimazone", "Mittelwert", "Median"]

        # auf zwei Nachkommastellen runden
        climate_zone_stats["Mittelwert"] = climate_zone_stats["Mittelwert"].round(2)
        climate_zone_stats["Median"] = climate_zone_stats["Median"].round(2)

        st.write(climate_zone_stats)

    # ---------------------------------------------------------
    # 📊 4. Statistischen Zusammenhang berechnen
    # --------------------------------------------------------- 
    with col9:
        st.subheader("Zusammenhang zwischen thermischen Bewertungen und Klimazone")

        results = []

        variables = [
            "thermal_comfort",
            "thermal_sensation",
            "thermal_preference",
            "thermal_acceptability"
        ]

        for variable in variables:
            
            # "unknown" nur bei thermal_preference und thermal_acceptability entfernen
            if variable in ["thermal_preference", "thermal_acceptability"]:
                df_test = df_bereinigt[
                    df_bereinigt[variable] != "Unknown"
                ]
            else:
                df_test = df_bereinigt

            # Kreuztabelle erstellen
            contingency_table = pd.crosstab(
                df_test["climate_zone"],
                df_test[variable]
            )

            # Chi²-Test
            chi2, p, dof, expected = chi2_contingency(contingency_table)


            # Cramérs V berechnen
            n = contingency_table.sum().sum()
            phi2 = chi2 / n
            r, k = contingency_table.shape

            cramers_v = np.sqrt(
                phi2 / min(k-1, r-1)
            )

            # Ergebnisse speichern
            results.append({
                "Variable": variable,
                "p-Wert": f"{p:.4f}",
                "Effektgröße": round(cramers_v, 3)
            })


        # Ergebnis-DataFrame
        chi2_results_df = pd.DataFrame(results)

        st.dataframe(
            chi2_results_df,
            use_container_width=True,
            hide_index=True
        )

        with st.expander("Informationen zum Lesen des Zusammenhangs"):
            st.write("""                  
            - Erklärung der Werte:
                - p-Wert: gibt an, ob ein Zusammenhang statistisch signifikant ist 
                - Effektgröße: gibt die Größe des Zusammenhangs an (z.B. schwacher, mittlerer, starker Zusammenhang)
            
            - Erkenntnisse:
                - Bei allen vier thermischen Bewertungsvariablen gibt es einen statistisch signifikanten Zusammenhang mit der Klimazone
                - Die Effektgröße zeigt:
                     - bei thermal_comfort und thermal_acceptability besteht ein schwacher Zusammenhang mit der Klimazone
                     - bei thermal_sensation und thermal_preference besteht ein sehr schwacher Zusammenhang mit der Klimazone
            
            - Hinweise: 
                - Für die Signifikanzprüfung wurde der Chi²-Test verwendet, für die Ermittlung der Effektstärke wurde Cramérs V berechnet
                - Es kann nur eine Aussage darüber gemacht werden, ob ein Zusammenhang besteht, jedoch nicht in welche Richtung dieser wirkt
            """)

        st.markdown("<br><br>", unsafe_allow_html=True)

    # - Zusammenfassung und Bedeutung der Ergebnisse -
    with col11:
        st.subheader("ℹ️ Zusammenfassung und Bedeutung der Ergebnisse")

        st.markdown("""
        - Es besteht ein **Zusammenhang** zwischen allen vier thermischen Bewertungsvariablen und der Klimazone
        - Der Zusammenhang ist **schwach** bei thermal_comfort und thermal_acceptability bzw. **sehr schwach** bei thermal_sensation und thermal_preference
        
            -> daher erklärt die Klimazone nur einen kleinen Teil der Unterschiede in der thermischen Bewertung
        """)

#########################################################################################################
#########################################################################################################

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



with tab5:

    col1, col2, col3 = st.columns([1,1,2])

    with col1:

            
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

        # ---------------------------------------------------------
        # 📌 Daten laden
        # ---------------------------------------------------------

        df = pd.read_csv("db_bereinigt.csv")

        df["thermal_sensation_cat"] = df["thermal_sensation"].apply(map_tsv)
        df["thermal_preference_cat"] = df["thermal_preference"].map(tp_map)
        df["thermal_comfort_cat"] = df["thermal_comfort"].apply(map_tc)

        # ---------------------------------------------------------
        # 📍 UI Reihenfolge: 1) Komfortvariable 2) Geografie 3) Auswahl
        # ---------------------------------------------------------

        st.header("🎨 Komfortanalyse")

        # 1️⃣ Komfortvariable auswählen
        comfort_option = st.selectbox(
            "Komfortvariable auswählen:",
            ["Thermal Comfort", "Thermal Sensation", "Thermal Preference"]
        )

        # 2️⃣ Geografische Verteilung anzeigen nach
        geo_map = {
            "Region": "region",
            "Land": "country",
            "Stadt": "city"
        }

        geo_option = st.selectbox("Geografische Verteilung anzeigen nach:", list(geo_map.keys()))
        geo_colname = geo_map[geo_option]

        # 3️⃣ Stadt / Land / Region auswählen
        geo_values = df[geo_colname].dropna()
        geo_choice = st.selectbox(f"{geo_option} auswählen:", sorted(geo_values.unique()))

        df_geo = df[df[geo_colname] == geo_choice]


    with col2:

        # ---------------------------------------------------------
        # 🗺️ Karte nur wenn Koordinaten vollständig sind
        # ---------------------------------------------------------

        st.markdown(f"### Karte – {geo_option}: {geo_choice}")

        if "latitude" in df_geo.columns and "longitude" in df_geo.columns:
            geo_clean = df_geo[["latitude", "longitude"]].dropna()
            if len(geo_clean) > 0:
                st.map(geo_clean)
            else:
                st.info("Keine gültigen geografischen Koordinaten verfügbar.")
        else:
            st.info("Keine geografischen Koordinaten verfügbar.")


    with col3:

        # ---------------------------------------------------------
        # 🎨 Nur EINE Figur anzeigen (für alle Situationen)
        # ---------------------------------------------------------

        st.header(f"📊 Analyse – {comfort_option} in {geo_choice}")

        if comfort_option == "Thermal Comfort":
            plot_comfort_variable(
                df_geo["thermal_comfort_cat"],
                tc_labels,
                tc_colors,
                f"Thermal Comfort – {geo_choice}"
            )

        elif comfort_option == "Thermal Sensation":
            plot_comfort_variable(
                df_geo["thermal_sensation_cat"],
                tsv_labels,
                tsv_colors,
                f"Thermal Sensation – {geo_choice}"
            )

        elif comfort_option == "Thermal Preference":
            plot_comfort_variable(
                df_geo["thermal_preference_cat"],
                tp_labels,
                tp_colors,
                f"Thermal Preference – {geo_choice}"
            )




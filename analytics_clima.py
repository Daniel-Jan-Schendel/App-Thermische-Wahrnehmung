import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import chi2_contingency



st.set_page_config(page_title="Analyse Klima und thermische Bewertung", layout="wide", initial_sidebar_state="expanded")

# Load data

df_bereinigt = pd.read_csv("db_bereinigt_final.csv")

#st.title("Globale Datenanalyse")
#st.line_chart(df_bereinigt["DB"])
#st.dataframe(df_bereinigt)

st.title("🌍 Analyse Klima und thermische Bewertung")

#st.header("Datenverteilung")

# Klima / Building

tab1, tab2, tab3 = st.tabs(["Verteilung Klimata", "Klima und thermische Bewertung", "Herausforderungen"])

with tab1:

    # ---------------------------------------------------------
    # 📌 1. Daten laden
    # ---------------------------------------------------------
    df = pd.read_csv("db_bereinigt_final.csv")

    # Nur Zeilen behalten, die gültige Koordinaten haben
    df = df.dropna(subset=["latitude", "longitude"])

    st.subheader("Globale Verteilung der ASHRAE Feldstudien")


    # ---------------------------------------------------------
    # 🔍 2. Filter-Widget (Kima/Klimazone)
    # ---------------------------------------------------------

    # Filter für Klima/Klimazone
    climate_filter = st.selectbox(
        "Variable auswählen",
        ["Climate Zone", "Climate"],
        key="climate_variable"
    )


    # ---------------------------------------------------------
    # 🔎 3. Filter anwenden
    # ---------------------------------------------------------

    # Klima/Klimazone anwenden
    if climate_filter == "Climate":
        selected_climate_column = "climate"
    else:
        selected_climate_column = "climate_zone"


    # ---------------------------------------------------------
    # 📌 4. Kombinationen von Ländern und Klimazonen erstellen
    # ---------------------------------------------------------
    # Land-Klimazonen-Kombinationen erstellen

    #country_climate = df[
    #    ["city", "city", "latitude", "longitude", selected_climate_column]
    #].drop_duplicates()

    country_climate = (
        df[["country", "latitude", "longitude", selected_climate_column]]
        .groupby("country")
        .agg({
            "latitude": "mean",
            "longitude": "mean",
            selected_climate_column: lambda x: list(x.dropna().unique())
        })
        .reset_index()
    )

    # Klimanamen bereinigen
    country_climate[selected_climate_column] = (
        country_climate[selected_climate_column]
        .apply(
            lambda climates: [
                c.strip().replace("\xa0", " ")
                for c in climates
                if isinstance(c, str)
            ]
        )
    )

    # Farben für Klimazonen vergeben
    if climate_filter == "Climate":

        climate_colors = {
        # Tropische Klimate
        "wet equatorial": [220, 80, 120, 180],
        "tropical rainforest": [200, 60, 120, 180],
        "tropical monsoon": [230, 100, 140, 180],
        "tropical savanna": [240, 130, 150, 180],
        "tropical wet savanna": [230, 110, 160, 180],
        "tropical dry savanna": [210, 90, 140, 180],
        "tropical": [220, 120, 160, 180],

        # Aride / trockene Klimate
        "hot arid": [245, 210, 80, 180],
        "desert (hot arid)": [240, 190, 60, 180],
        "hot desert": [230, 170, 40, 180],
        "semi arid midlatitude": [220, 180, 70, 180],
        "semi arid high altitude": [200, 170, 90, 180],
        "hot semi-arid": [235, 200, 90, 180],
        "cold semi-arid": [190, 170, 100, 180],
        "subtropical hot and dry": [250, 180, 50, 180],

        # Mediterrane Klimate
        "mediterranean": [180, 160, 70, 180],
        "hot-summer mediterranean": [200, 150, 60, 180],
        "warm-summer mediterranean": [170, 150, 80, 180],
        "cool-summer mediterranean": [140, 160, 100, 180],

        # Gemäßigte Klimate
        "temperate": [80, 180, 90, 180],
        "humid subtropical": [60, 170, 100, 180],
        "temperature marine": [60, 150, 120, 180],
        "temperate oceanic": [40, 140, 170, 180],
        "west coast marine": [50, 130, 190, 180],
        "subtropical highland": [100, 190, 100, 180],

        # Kontinentale Klimate
        "humid midlatitude": [120, 100, 200, 180],
        "warm-summer humid continental": [140, 100, 210, 180],
        "monsoon-influenced humid subtropical": [160, 120, 220, 180],
        "monsoon-influenced temperate oceanic": [130, 150, 220, 180],
        "monsoon-influenced hot-summer humid continental": [150, 90, 190, 180],

        # Subarktisches Klima
        "continental subarctic": [80, 90, 150, 180]
    }

    else:

        climate_colors = {
            "Tropical": [220, 120, 120, 180],
            "Dry": [245, 210, 80, 180],
            "Temperate": [0, 180, 0, 180],
            "Continental": [150, 0, 150, 180]
        }

    import math

    # Mehrfarbige Kreise erstellen
    def create_pie_segments(df, climate_column, radius=1.5):

        segments = []

        for _, row in df.iterrows():

            climates = row[climate_column]

            n = len(climates)

            angle_step = 360 / n

            for i, climate in enumerate(climates):

                start_angle = i * angle_step
                end_angle = (i + 1) * angle_step

                polygon = [
                    [row["longitude"], row["latitude"]]
                ]

                for angle in range(
                    int(start_angle),
                    int(end_angle) + 1,
                    5
                ):
                    lon = (
                        row["longitude"]
                        + radius * math.cos(math.radians(angle))
                    )

                    lat = (
                        row["latitude"]
                        + radius * math.sin(math.radians(angle))
                    )

                    polygon.append([lon, lat])

                polygon.append(
                    [row["longitude"], row["latitude"]]
                )

                segments.append({
                    "country": row["country"],
                    "climate": climate,
                    "polygon": polygon,
                    "color": climate_colors.get(climate)
                })

        return pd.DataFrame(segments)

    if climate_filter == "Climate":

        # Mehrfarbige Kreise für einzelne Klimata
        pie_data = create_pie_segments(
            country_climate,
            selected_climate_column
        )

        layer = pdk.Layer(
            "PolygonLayer",
            data=pie_data,
            get_polygon="polygon",
            get_fill_color="color",
            pickable=True,
            stroked=False
        )


    else:

        # Einfarbige Kreise für die 4 Klimazonen

        country_climate["color"] = (
            country_climate[selected_climate_column]
            .apply(lambda x: climate_colors.get(x[0]))
        )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=country_climate,
            get_position="[longitude, latitude]",
            get_radius=50000,
            get_fill_color="color",
            pickable=True
        )

   

    # ---------------------------------------------------------
    # 🌐 6. Kartenansicht definieren
    # ---------------------------------------------------------

    view_state = pdk.ViewState(
        latitude=country_climate["latitude"].mean() if len(country_climate) else 0,
        longitude=country_climate["longitude"].mean() if len(country_climate) else 0,
        zoom=1
    )

    # Tooltip-Design
    tooltip = {
        "html": """
        <b>{country}</b><br/>
        Klima: {climate}
        """,
        "style": {
            "color": "white"
        }
    }

    # Legende hinzufügen
    st.markdown("""
    **Klimazonen:**

    🔴 Tropical  
    🟡 Dry  
    🟢 Temperate  
    🟣 Continental
    """)


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

    # ---------------------------------------------------------
    # 🧭 8. Zuordnung Klimata zu Klimazonen
    # ---------------------------------------------------------

    # Zuordnung Klimata zu Klimazonen
    climate_mapping = (
        df[["climate_zone", "climate"]]
        .drop_duplicates()
        .groupby("climate_zone")["climate"]
        .apply(lambda x: ", ".join(sorted(x.dropna().unique())))
        .reset_index()
    )

    # Spaltennamen ändern
    climate_mapping.columns = [
        "Klimazone",
        "Zugehörige Klimata"
    ]

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("### Zuordnung der Klimata zu den Klimazonen")

    climate_mapping = (
        df[["climate_zone", "climate"]]
        .drop_duplicates()
        .sort_values(["climate_zone", "climate"])
    )

    st.dataframe(
        climate_mapping,
        use_container_width=True,
        hide_index=True
    )

    # Hinweis zu Klimazonen-Zuweisung
    with st.expander("Weitere Informationen zu Klimata und Klimazonen"):
        st.markdown("""  
        - Hinweise:
            - Die 5. Hauptklimazone Polar ist hier nicht mit aufgeführt, da es für diese Klimazone in diesem Datensatz keine Daten gibt
            - Es wurde keine offizielle Zuordnung der Klimata zu den Klimazonen gefunden, daher kann sich die hier gewählte Zuordnung von anderen unterscheiden
        """)

        st.markdown(""" 
        - Beschreibungen zu Klimazonen:
            - Tropical: Ganzjährig hohe Temperaturen, geringe jahreszeitliche Schwankungen 
            - Dry: Geringe Niederschläge, aride und semiaride Gebiete
            - Temperate: Moderate Temperaturen, ausgeprägte Jahreszeiten
            - Continental: Große Temperaturunterschiede zwischen Sommer und Winter
        """)

with tab2:
    # ---------------------------------------------------------
    # 📌 1. Daten laden und Einführungstext
    # ---------------------------------------------------------
    df = pd.read_csv("db_bereinigt_final.csv")

    st.header("Gibt es einen Zusammenhang zwischen Klimazone und thermischer Bewertung?")
    

    col1, col2 = st.columns([2,1])
    col3, col4 = st.columns([2,2])
    col5, col6 = st.columns([2,2])
    col7, col8 = st.columns([2,2])
    col9, col10 = st.columns([2,1])
    col11, col12 = st.columns([2,1])

    # ---------------------------------------------------------
    # 📌 2. Einführungstext und Auswahl Variable
    # ---------------------------------------------------------

    with col1:

        st.markdown("""
        Untersuchung des Zusammenhangs der vier Hauptklimazonen mit den thermischen Bewertungsvariablen:

        - Thermischer Komfort
        - Thermisches Empfinden
        - Thermische Präferenz
        - Thermische Akzeptanz
        """)

        

        selected_variable = st.selectbox(
        "Thermische Bewertungsvariable auswählen",
        (
            "Thermischer Komfort",
            "Thermisches Empfinden",
            "Thermische Präferenz",
            "Thermische Akzeptanz"
        ),
        key="analyse_variable"
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 🔎 2. Filter anwenden
        # ---------------------------------------------------------
        if selected_variable == "Thermischer Komfort":
            selected_thermal_column = "thermal_comfort"
        elif selected_variable == "Thermisches Empfinden":
            selected_thermal_column = "thermal_sensation"
        elif selected_variable == "Thermische Präferenz":
            selected_thermal_column = "thermal_preference"
        else:
            selected_thermal_column = "thermal_acceptability"

    # ---------------------------------------------------------
    # 📊 3. Grafiken erstellen
    # ---------------------------------------------------------

    # - Grafik - 
    with col3:

        # Boxplot für thermal_comfort, thermal_sensation und thermal_preference
        if selected_thermal_column != "thermal_acceptability":

            plot_df = df.copy()

            # Unknown in thermal_preference entfernen
            if selected_variable == "Thermische Präferenz":
                plot_df = plot_df[
                    plot_df["thermal_preference"] != "Unknown"
                ]

            fig, ax = plt.subplots(figsize=(8,5))

            sns.boxplot(
                data=plot_df,
                x="climate_zone",
                y=selected_thermal_column,
                width=0.6,
                whiskerprops=dict(color="black"),
                showmeans=True,
                capprops=dict(color="black"),
                medianprops=dict(color="cyan", linewidth=2.5),
                meanprops=dict(
                    marker="o",
                    markerfacecolor="skyblue",
                    markeredgewidth=0.0,
                    markersize=8
                ),
                ax=ax
            )

            # sns.stripplot(
            #      data=plot_df,
            #      x="climate_zone",
            #      y=selected_thermal_column,
            #      jitter=0.25,
            #      size=1.5,
            #      alpha=0.05,
            #      color="steelblue",
            #      ax=ax,
            #      hue=selected_thermal_column,
            #      palette="viridis",
            #      legend=False
            #  )

            st.pyplot(fig)


        # Grafik für thermal_acceptability
        else:

            acceptability_pct = (
                pd.crosstab(
                    df["climate_zone"],
                    df["thermal_acceptability"],
                    normalize="index"
                ) * 100
            )

            fig, ax = plt.subplots(figsize=(8,5))

            acceptability_pct.plot(
                kind="bar",
                ax=ax,
                color=["darkgrey","royalblue", "teal"]
            )

            st.pyplot(fig)

    # - Interpretation der Ergebnisse - 
    with col5:
        interpretation = {

            "thermal_comfort": """
        #### **Erkenntnisse**

        - Median ist bei Continental niedriger als bei den anderen Klimazonen ➝ hat aber auch größere Streuung der Werte
        - Dry und Tropical: geringste Streuung der Werte
        - Continental unterscheidet sich am stärksten von den anderen Klimazonen

        #### ℹ️**Bedeutung**

        Befragte in der Klimazone "Continental" bewerten den Komfort tendenziell schlechter als in den anderen 3 Klimazonen
        """,

            "thermal_sensation": """
        #### **Erkenntnisse**

        - Median ist bei allen Klimazonen gleich
        - Temperate und Continental: geringste Streuung der Werte
        - Dry und Tropical: größte Streuung der Werte

        #### ℹ️**Bedeutung**

        - In allen vier Klimazonen wird das thermische Empfinden tendenziell mit neutral bewertet
        - Unterschied vor allem:
            - Temperate, Continental: 50% der Befragten haben das thermische Empfinden mit neutral oder warm bewertet
            - Dry, Tropical: 50% der Befragten haben das thermische Empfinden mit kühl, neutral oder warm bewertet
        
        """,

            "thermal_preference": """
        #### **Erkenntnisse**

        - Median ist bei allen Klimazonen gleich
        - Continental: geringste Streuung der Werte
        - Continental unterscheidet sich am stärksten von den anderen Klimazonen

        #### ℹ️**Bedeutung**

        
        - In allen vier Klimazonen wurde tendenziell keine Veränderung gewünscht
        - In den Klimazonen Temperate, Dry und Tropical haben 50% der Befragten keine Veränderung oder wärmer bevorzugt angegeben
        """,

            "thermal_acceptability": """
        #### **Erkenntnisse**

        - In allen vier Klimazonen bewertet die Mehrheit die Umgebung als akzeptabel
        - Unterschiede zwischen den Klimazonen sind gering
        - Bei Continental sehr hoher Anteil fehlender Werte

       #### ℹ️**Bedeutung**

        Die thermische Akzeptanz ist in allen Klimazonen überwiegend hoch
        """
        }

        st.markdown(interpretation[selected_thermal_column])
    

    # ---------------------------------------------------------
    # 📊 4. Ergebnistabelle erstellen
    # ---------------------------------------------------------
    with col4:
        titles = {
                "thermal_comfort": "Thermal Comfort",
                "thermal_sensation": "Thermal Sensation",
                "thermal_preference": "Thermal Preference",
                "thermal_acceptability": "Thermal Acceptability"
            }

        st.markdown(f"### Ergebnisse für {titles[selected_thermal_column]}")
    
        # Ergebnistabelle für thermal_comfort und thermal_sensation
        if selected_thermal_column not in ["thermal_acceptability", "thermal_preference"]:

            plot_df = df.copy()


            climate_zone_stats = (
                plot_df
                .groupby("climate_zone")[selected_thermal_column]
                .agg(["mean", "median"])
                .reset_index()
            )

            climate_zone_stats.columns = ["Klimazone", "Mittelwert", "Median"]

            climate_zone_stats["Mittelwert"] = climate_zone_stats["Mittelwert"].round(2)
            climate_zone_stats["Median"] = climate_zone_stats["Median"].round(2)

            st.dataframe(climate_zone_stats, use_container_width=True)

            with st.expander("Allgemeine Informationen zum Lesen des Boxplot"):
                st.markdown("""  
                - Box: zeigt, in welchem Bereich 50% der Werte für diese Klimazone liegen
                - türkisfarbene Linie: stellt Median dar
                - hellblauer Punkt: stellt Mittelwert dar
                - Whisker: zeigen den Bereich, in dem die meisten Datenwerte liegen
                - Punkte außerhalb der Whisker: stellen Ausreißer dar
                """)

        # Ergebnistabelle für thermal_preference
        elif selected_thermal_column == "thermal_preference":

            plot_df = df[df["thermal_preference"] != "Unknown"].copy()

            # Schreibweise vereinheitlichen
            plot_df["thermal_preference"] = (
                plot_df["thermal_preference"]
                .str.strip()
                .str.lower()
            )

            mapping = {
                "cooler": -1,
                "no change": 0,
                "warmer": 1
            }

            plot_df["thermal_preference_num"] = (
                plot_df["thermal_preference"].map(mapping)
            )

            climate_zone_stats = (
                plot_df
                .groupby("climate_zone")["thermal_preference_num"]
                .agg(["mean", "median"])
                .reset_index()
            )

            climate_zone_stats.columns = ["Klimazone", "Mittelwert", "Median"]

            climate_zone_stats["Mittelwert"] = climate_zone_stats["Mittelwert"].round(2)
            climate_zone_stats["Median"] = climate_zone_stats["Median"].round(2)

            st.dataframe(climate_zone_stats)

            with st.expander("Allgemeine Informationen zum Lesen des Boxplot"):
                st.markdown("""  
                - Box: zeigt, in welchem Bereich 50% der Werte für diese Klimazone liegen
                - türkisfarbene Linie: stellt Median dar
                - hellblauer Punkt: stellt Mittelwert dar
                - Whisker: zeigen den Bereich, in dem die meisten Datenwerte liegen
                - Punkte außerhalb der Whisker: stellen Ausreißer dar
                """)

        # Ergebnistabelle für thermal_acceptability
        else:

            climate_zone_stats = (
                pd.crosstab(
                    df["climate_zone"],
                    df["thermal_acceptability"],
                    normalize="index"
                ) * 100
            ).round(1)

            climate_zone_stats = climate_zone_stats.reset_index()

            st.dataframe(
                climate_zone_stats.style.format("{:.1f}%", subset=climate_zone_stats.columns[1:]),
                use_container_width=True,
                hide_index=True
            )


    # ---------------------------------------------------------
    # 📊 5. Statistischen Zusammenhang berechnen
    # --------------------------------------------------------- 
    with col9:
        st.subheader("📊 Zusammenhang zwischen thermischen Bewertungen und Klimazone")

        results = []

        variables = [
            "thermal_comfort",
            "thermal_sensation",
            "thermal_preference",
            "thermal_acceptability"
        ]

        for variable in variables:
            
            # "Unknown" nur bei thermal_preference und thermal_acceptability entfernen
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
        st.info(
            """
            ℹ️ **Zusammenfassung und Bedeutung der Ergebnisse**

            - Es besteht ein **Zusammenhang** zwischen allen vier thermischen Bewertungsvariablen und der Klimazone.
            - Der Zusammenhang ist **schwach** bei Thermischem Komfort und Thermischer Akzeptanz bzw. **sehr schwach** bei Thermischem Empfinden und Thermischer Präferenz.

            ➜ Daher erklärt die Klimazone nur einen kleinen Teil der Unterschiede in der thermischen Bewertung.
            """
        )


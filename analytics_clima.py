import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import chi2_contingency
import plotly.express as px



st.set_page_config(page_title="Analyse Klima und thermische Bewertung", layout="wide", initial_sidebar_state="expanded")

# ---------------------------------------------------------
# 📌 Funktionen definieren
# ---------------------------------------------------------

def interpret_effect(v):
    if v < 0.1:
        return "sehr schwach"
    elif v < 0.3:
        return "schwach"
    elif v < 0.5:
        return "mittel"
    elif v < 0.7:
        return "stark"
    else:
        return "sehr stark"


def interpret_significance(p):
    if p < 0.05:
        return "✓"
    else:
        return "✗"


# Load data

df = pd.read_csv("db_bereinigt_final.csv")


st.title("🌍 Analyse Klima und thermische Bewertung")


tab1, tab2, tab3 = st.tabs(["Geografische Verteilung", "Betrachtung Klima und thermische Bewertung", "Zusammenhang Klima und thermische Bewertung"])

#########################################################################################################
#########################################################################################################

with tab1:

    # ---------------------------------------------------------
    # 📌 1. Daten laden
    # ---------------------------------------------------------
    df = pd.read_csv("db_bereinigt_final.csv")

    # Nur Zeilen behalten, die gültige Koordinaten haben
    df = df.dropna(subset=["latitude", "longitude"])

    st.subheader("Geografische Verteilung der ASHRAE Feldstudien")


    # ---------------------------------------------------------
    # 🔍 2. Filter-Widget (Kima/Klimazone)
    # ---------------------------------------------------------

    # Filter für Klima/Klimazone
    climate_filter = st.selectbox(
        "Variable auswählen",
        ["Klimazone", "Klima"],
        key="climate_variable"
    )


    # ---------------------------------------------------------
    # 🔎 3. Filter anwenden
    # ---------------------------------------------------------

    # Klima/Klimazone anwenden
    if climate_filter == "Klima":
        selected_climate_column = "climate"
    else:
        selected_climate_column = "climate_zone"


    # ---------------------------------------------------------
    # 📌 4. Kombinationen von Ländern und Klimazonen erstellen
    # ---------------------------------------------------------
    # Land-Klimazonen-Kombinationen erstellen

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
    if selected_climate_column == "climate":

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
                    lat_radius = radius
                    lon_radius = radius / math.cos(math.radians(row["latitude"]))

                    lon = (row["longitude"] + lon_radius * math.cos(math.radians(angle))
                    )

                    lat = (row["latitude"] + lat_radius * math.sin(math.radians(angle))
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

    if selected_climate_column == "climate":

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
            get_radius=150000,
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

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("### Zuordnung von Klimata, Regionen und Ländern zu den Hauptklimazonen")

    for zone in sorted(df["climate_zone"].dropna().unique()):
        if zone == "Continental":
            with st.expander(f"🟣 {zone}"):

                zone_df = (
                    df[df["climate_zone"] == zone]
                    [["climate", "region", "country"]]
                    .drop_duplicates()
                    .sort_values(
                        by=["climate", "region", "country"]
                    )
                )

                st.dataframe(
                    zone_df,
                    use_container_width=True,
                    hide_index=True
                )
        elif zone == "Dry":
            with st.expander(f"🟡 {zone}"):

                zone_df = (
                    df[df["climate_zone"] == zone]
                    [["climate", "region", "country"]]
                    .drop_duplicates()
                    .sort_values(
                        by=["climate", "region", "country"]
                    )
                )

                st.dataframe(
                    zone_df,
                    use_container_width=True,
                    hide_index=True
                )
        elif zone == "Temperate":
            with st.expander(f"🟢 {zone}"):

                zone_df = (
                    df[df["climate_zone"] == zone]
                    [["climate", "region", "country"]]
                    .drop_duplicates()
                    .sort_values(
                        by=["climate", "region", "country"]
                    )
                )

                st.dataframe(
                    zone_df,
                    use_container_width=True,
                    hide_index=True
                )
        else:
             with st.expander(f"🔴 {zone}"):

                zone_df = (
                    df[df["climate_zone"] == zone]
                    [["climate", "region", "country"]]
                    .drop_duplicates()
                    .sort_values(
                        by=["climate", "region", "country"]
                    )
                )

                st.dataframe(
                    zone_df,
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


#########################################################################################################
#########################################################################################################


with tab2:
    
    st.subheader("Betrachtung von klimatischen/geografischen Variablen und thermischer Bewertung")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 📌 1. Einführungstext
    # ---------------------------------------------------------
    

    col1, col2, col3 = st.columns([1,0.08, 1])
    col4, spacer, col5 = st.columns([2,0.8,2])
    col6, spacer, col7 = st.columns([2,0.8,2])
    col8, col9 = st.columns([10,0.2])


          
    # ---------------------------------------------------------
    # 🔎 1. Mapping-Dictionary
    # ---------------------------------------------------------
    # Mapping-Dictionary Klima
    environment_mapping = {
        "Klimazone": "climate_zone",
        "Klima": "climate",
        "Region": "region",
        "Land": "country"            
    }


    # Mapping-Dictionary thermische Variablen
    thermal_mapping = {
        "Thermischer Komfort": "thermal_comfort",
        "Thermisches Empfinden": "thermal_sensation",
        "Thermische Präferenz": "thermal_preference",
        "Thermische Akzeptanz": "thermal_acceptability"
    }

    # # Filter-Widget (thermische Variablen)
    # selected_variable_thermal = st.selectbox(
    #     "Thermische Bewertungsvariable auswählen",
    #     list(thermal_mapping.keys()),
    #     key="selectbox_thermal"
    # )

    with col1:
        # ---------------------------------------------------------
        # 🔍 2. Filter-Widget
        # ---------------------------------------------------------
        # Filter-Widget (Klima/Klimazone)
        selected_variable_environment = st.selectbox(
            "Klimatische/geografische Variable auswählen",
            list(environment_mapping.keys()),
            key="selectbox_environment"
        )

        st.markdown("<br>", unsafe_allow_html=True)

    # with col2:
    #     st.markdown("<br>", unsafe_allow_html=True)
    #     st.markdown("""###### und""")


    # with col3:
    #     st.info("""
    #     **Thermischer Bewertung:**
    #     - Thermischer Komfort
    #     - Thermisches Empfinden
    #     - Thermische Präferenz
    #     - Thermische Akzeptanz
    #     """
    #     )
    
    #    st.markdown("<br>", unsafe_allow_html=True)

        
    # ---------------------------------------------------------
    # 🔍 3. Mapping anwenden
    # ---------------------------------------------------------
    # Mapping für Klima anwenden
    selected_environment_column = environment_mapping[selected_variable_environment]

    # Mapping für thermsiche Variablen anwenden
    #selected_thermal_column = thermal_mapping[selected_variable_thermal]
    
    st.markdown("<br><br>", unsafe_allow_html=True)


    # ---------------------------------------------------------
    # 📊 4. Grafiken erstellen
    # ---------------------------------------------------------

    # Diagramm Thermischer Komfort
    with col4:
        # Titel für Diagramm Thermischer Komfort
        st.subheader(f"Thermischer Komfort und {selected_variable_environment}")

        plot_df = df.copy()

        # Berechnungen für Diagramm und Ergebnistabelle
        thermal_comfort_stats = (
            plot_df
            .groupby(selected_environment_column)["thermal_comfort"]
            .agg(
                Mittelwert="mean",
                Median="median",
                Anzahl="count"
            )
            .reset_index()
        )

        thermal_comfort_stats["Mittelwert"] = thermal_comfort_stats["Mittelwert"].round(2)
        thermal_comfort_stats["Median"] = thermal_comfort_stats["Median"].round(2)

        thermal_comfort_stats = thermal_comfort_stats.sort_values(
            by="Mittelwert",
            ascending=False
        )

        # Grafik erstellen
        # Balken: Mittelwert
        bars_comfort = (
            alt.Chart(thermal_comfort_stats)
            .mark_bar(color="steelblue")
            .encode(
                x=alt.X(
                    f"{selected_environment_column}:N",
                    sort="-y",
                    title=selected_variable_environment,
                    axis=alt.Axis(labelAngle=-45)
                ),
                y=alt.Y(
                    "Mittelwert:Q",
                    title="Mittelwert Thermal Comfort",
                    scale=alt.Scale(domain=[0, 6])
                ),
                tooltip=[
                    alt.Tooltip(
                        f"{selected_environment_column}:N",
                        title=selected_variable_environment
                    ),
                    alt.Tooltip(
                        "Mittelwert:Q",
                        format=".2f"
                    ),
                    alt.Tooltip(
                        "Median:Q",
                        format=".0f"
                    ),
                    alt.Tooltip(
                        "Anzahl:Q"
                    )
                ]
            )
        )

        # Median: Punkte
        median_points = (
            alt.Chart(thermal_comfort_stats)
            .mark_point(
                color="red",
                filled=True,
                size=80
            )
            .encode(
                x=alt.X(
                    f"{selected_environment_column}:N"
                ),
                y=alt.Y(
                    "Median:Q"
                )
            )
        )

        chart = (
            bars_comfort + median_points
        ).properties(
            height=500
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

        
        # Ergebnistabelle und Bedeutung der Ergebnisse
        with st.expander(
                f"**📈 Ergebnisse Thermischer Komfort und {selected_variable_environment}**"
                ):
                st.dataframe(thermal_comfort_stats, use_container_width=True)
                if selected_variable_environment == "Klimazone":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermische Komfortbewertung unterscheidet sich zwischen den Klimazonen
                                
                            - **Dry, Temperate und Tropical**: bewerten thermischen Komfort **tendenziell positiv** (Median = 5)
                            - **Continental**: bewertet thermischen Komfort **tendenziell niedriger** (Median = 3)
                    """
                    )
                elif selected_variable_environment == "Klima":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Bewertung des thermischen Komforts **unterscheidet sich zwischen den Klimata stärker** als zwischen den Hauptklimazonen 
                        - Klimata mit moderaten thermischen Bedingungen: hohe Komfortbewertungen (Medianwerte zwischen 5 und 6)
                        - Klimata mit stärkeren thermischen Belastungen: niedrigere Komfortbewertungen (Medianwerte zwischen 2 und 3)
                    """
                    )
                elif selected_variable_environment == "Region":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermischer Komfort wird **in allen Regionen ähnlich** bewertet 
                                
                                ➝ Mittelwerte unterscheiden sich nur gering 
                        - Leicht niedrigere Bewertung des thermischen Komforts in Europa (Median = 4) im Vergleich zu anderen Kontinenten (Median = 5)
                    """
                    )
                else:
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Bewertungen liegen **in allen Länder bei einem mittleren bis höheren Komfort** (Medianwerte zwischen 3 und 5)
                                
                            ➝ insgesamt positive Komfortbewertung
                        - **Unterschiede zwischen Ländern** mit gleichem Klima ➝ zeigen, dass es regionale Unterschiede in der Wahrnehmung des thermischen Komforts gibt
                    """
                    )

        st.markdown("<br>", unsafe_allow_html=True)
    

    # Diagramm Thermisches Empfinden
    with col5:
        # Titel für Diagramm Thermisches Empfinden
        st.subheader(f"Thermisches Empfinden und {selected_variable_environment}")

        plot_df = df.copy()

        plot_df = plot_df.dropna(
            subset=[selected_environment_column]
        )

        # Berechnungen für Diagramm und Ergebnistabelle
        thermal_sensation_stats = (
            plot_df
            .groupby(selected_environment_column)["thermal_sensation"]
            .agg(
                Mittelwert="mean",
                Median="median",
                Anzahl="count"
            )
            .reset_index()
        )

        thermal_sensation_stats["Mittelwert"] = thermal_sensation_stats["Mittelwert"].round(2)
        thermal_sensation_stats["Median"] = thermal_sensation_stats["Median"].round(2)

        thermal_sensation_stats = thermal_sensation_stats.sort_values(
            by="Mittelwert",
            ascending=False
        )

        # Grafik erstellen
        # Balken: Mittelwert
        bars_sensation = (
            alt.Chart(thermal_sensation_stats)
            .mark_bar(color="steelblue")
            .encode(
                x=alt.X(
                    f"{selected_environment_column}:N",
                    sort="-y",
                    title=selected_variable_environment,
                    axis=alt.Axis(labelAngle=-45)
                ),
                y=alt.Y(
                    "Mittelwert:Q",
                    title="Mittelwert Thermal Sensationa",
                    scale=alt.Scale(domain=[-3, 3])
                ),
                tooltip=[
                    alt.Tooltip(
                        f"{selected_environment_column}:N",
                        title=selected_variable_environment
                    ),
                    alt.Tooltip(
                        "Mittelwert:Q",
                        format=".2f"
                    ),
                    alt.Tooltip(
                        "Median:Q",
                        format=".0f"
                    ),
                    alt.Tooltip(
                        "Anzahl:Q"
                    )
                ]
            )
        )

        # Median: Punkte
        median_points = (
            alt.Chart(thermal_sensation_stats)
            .mark_point(
                color="red",
                filled=True,
                size=80
            )
            .encode(
                x=alt.X(
                    f"{selected_environment_column}:N"
                ),
                y=alt.Y(
                    "Median:Q"
                )
            )
        )

        chart = (
            bars_sensation + median_points
        ).properties(
            height=500
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )


        # Ergebnistabelle und Bedeutung der Ergebnisse
        with st.expander(
                f"**📈 Ergebnisse Thermisches Empfinden und {selected_variable_environment}**"
                ):
                st.dataframe(thermal_sensation_stats, use_container_width=True)
                if selected_variable_environment == "Klimazone":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        - In allen vier Klimazonen wird das thermische Empfinden **tendenziell** als **neutral** bewertet  (Median = 0)
                        - Mittelwerte weisen auf eine geringe Tendenz zu einer wärmeren Wahrnehmung hin (Mittelwerte zwischen 0.07 und 0.24)
                    """
                    )
                elif selected_variable_environment == "Klima":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermisches Empfinden wird auch bei Klimata **tendenziell** eher als **neutral** bewertet (meiste Medianwerte bei 0)
                                
                            ➝ mit leichter Tendenz zu wärmerer Bewertung (meiste Mittelwerte zwischen -0.2 und + 0.6) 
                        - Aber es gibt **mehr Variation** als bei den Hauptklimazonen (Medianwerte zwischen -1 und 1)                   
                    """
                    )
                elif selected_variable_environment == "Region":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermisches Empfinden wird **in allen Regionen** im Median als **neutral** bewertet (Median = 0)
                  
                            ➝ leichte Tendenz zu wärmerer Bewertung (positive Mittelwerte)
                        - **Africa**: stärkste Tendenz zu **wärmerer Bewertung** (Mittelwert = 0.69)
                    """
                    )
                else:
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermisches Empfinden wird **in meisten Ländern** im Median als **neutral** bewertet
                        - Bewertungen zeigen aber **größere Variation** als bei Regionen (Medianwerte zwischen -1 und 2, Mittelwerte zwischen -1,04 und +2,14)
                        - Abweichungen: 
                                

                            - Nigeria: stärkere Tendenz zu wärmerer Wahrnehmung (Median = 2)
                            - Cyprus und Philippines: dagegen kühlere Wahrnehmung (Median = -1)
                    """
                    )

    # Diagramm Thermische Präferenz
    with col6:
        # Titel für Diagramm Thermische Präferenz
        st.subheader(f"Thermische Präferenz und {selected_variable_environment}")

        plot_df = df.copy()

        # Unknown entfernen
        plot_df = plot_df[plot_df["thermal_preference"] != "Unknown"]

        mapping = {
            "cooler": -1,
            "no change": 0,
            "warmer": 1
        }

        plot_df["thermal_preference_num"] = (
            plot_df["thermal_preference"]
            .map(mapping)
        )
       

        # Berechnungen für Diagramm und Ergebnistabelle
        thermal_preference_stats = (
            plot_df
            .groupby(selected_environment_column)["thermal_preference_num"]
            .agg(
                Mittelwert="mean",
                Median="median",
                Anzahl="count"
            )
            .reset_index()
        )

        thermal_preference_stats["Mittelwert"] = thermal_preference_stats["Mittelwert"].round(2)
        thermal_preference_stats["Median"] = thermal_preference_stats["Median"].round(2)

        thermal_preference_stats = thermal_preference_stats.sort_values(
            by="Mittelwert",
            ascending=False
        )

        # Grafik erstellen
        bars_preference = (
            alt.Chart(thermal_preference_stats)
            .mark_bar(color="steelblue")
            .encode(
                x=alt.X(
                    f"{selected_environment_column}:N",
                    sort="-y",
                    title=selected_variable_environment,
                    axis=alt.Axis(labelAngle=-45)
                ),
                y=alt.Y(
                    "Mittelwert:Q",
                    title=f"Mittelwert Thermal Preference",
                    scale=alt.Scale(domain=[-1, 1])
                ),
                tooltip=[
                    alt.Tooltip(
                        f"{selected_environment_column}:N",
                        title=selected_variable_environment
                    ),
                    alt.Tooltip(
                        "Mittelwert:Q",
                        format=".2f"
                    ),
                    alt.Tooltip(
                        "Anzahl:Q"
                    )
                ]
            )
            .properties(
                height=500
            )
        )

        median_points = (
            alt.Chart(thermal_preference_stats)
            .mark_point(
                color="red",
                filled=True,
                size=80
            )
            .encode(
                x=alt.X(
                    f"{selected_environment_column}:N"
                ),
                y=alt.Y(
                    "Median:Q"
                )
            )
        )

        chart = (
            bars_preference + median_points
        ).properties(
            height=500
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )


        # Ergebnistabelle und Bedeutung der Ergebnisse
        with st.expander(
                f"**📈 Ergebnisse Thermische Präferenz und {selected_variable_environment}**"
                ):
                st.dataframe(thermal_preference_stats, use_container_width=True)
                if selected_variable_environment == "Klimazone":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        - In allen vier Klimazonen wird die thermische Präferenz **tendenziell** mit **"keine Veränderung"** bewertet (Median = 0)
                        - Geringe Unterschiede:
                            
                            - Continental zeigt minimale Präferenz für wärmere Bedingungen
                            - Temperate, Dry und Tropical zeigen leichte Präferenz für kühlere Bedingungen
                    """
                    )
                elif selected_variable_environment == "Klima":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermische Präferenz wird auch bei Klimata **tendenziell** als **neutral** bewertet (Median fast überall = 0)
                        - Aber es gibt **mehr Variation** als bei den Hauptklimazonen (Mittelwerte zwischen -0.5 und +0.35)

                            - Wärmere und feuchtere Klimata: tendenziell stärkere Präferenz für kühlere Bedingungen 
                            - Einzelne gemäßigte Klimatypen: leichte Präferenz für wärmere Bedingungen                  
                    """
                    )
                elif selected_variable_environment == "Region":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - In meisten Regionen tendenziell **keine Änderung** gewünscht (Median = 0)
                                
                            ➝ allgemein leichte Tendenz zu Präferenz von kühleren Bedingungen (negative Mittelwerte)
                        - **Africa**: typische Bewertung **kühlere Bedingungen** (Median =-1)  
                            
                            ➝ hat aber geringere Stichprobengröße
                    
                            
                    """
                    )
                else:
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        - In meisten Ländern tendenziell **keine Änderung** gewünscht (Median = 0)
                                
                            ➝ allgemein überwiegend **leichte Tendenz** zu Präferenz von **kühleren Bedingungen** (überwiegend negative Mittelwerte)
                        - **Abweichungen:**
                                
                            - Thailand, Denkmark, Greece und Nigeria: typische Präferenz für **kühlere Bedingungen** (Median =-1) ➝ aber teilweise geringere Stichprobengröße
                            - Singapore, Italy, China und Canada: leichte Tendenz zu wärmeren Bedingungen (positive Mittelwerte, aber Median = 0)
                    """
                )

    # Diagramm Thermische Akzeptanz
    with col7:
        # Titel für Diagramm Thermische Akzeptanz
        st.subheader(f"Thermische Akzeptanz und {selected_variable_environment}")

        # Dataframe nur mit gültigen Antworten
        valid_df = df[
            df["thermal_acceptability"].isin(
                ["acceptable", "unacceptable"]
            )
        ]

        # Berechnungen für Diagramm und Ergebnistabelle
        acceptability_pct = (
            pd.crosstab(
                valid_df[selected_environment_column],
                valid_df["thermal_acceptability"],
                normalize="index"
            ) * 100
        ).reset_index()

        # Dataframe mit Unknown erstellen
        unknown_pct = (
            pd.crosstab(
                df[selected_environment_column],
                df["thermal_acceptability"],
                normalize="index"
            ) * 100
        ).reset_index()[[selected_environment_column, "Unknown"]]

        acceptability_pct = acceptability_pct.merge(
            unknown_pct,
            on=selected_environment_column,
            how="left"
        )

        # Nach Anteil akzeptabler Werte absteigend sortieren
        acceptability_pct = (
            acceptability_pct
            .sort_values(
                by="acceptable",
                ascending=False
            )
        )

        # Spaltenreihenfolge ändern: Unknown nach hinten
        cols = [
            selected_environment_column,
            "acceptable",
            "unacceptable",
            "Unknown"
        ]

        acceptability_pct = acceptability_pct[cols]

        # Diagramm vorbereiten
        acceptability_long = acceptability_pct.drop(
            columns=["Unknown"]
        ).melt(
            id_vars=[selected_environment_column],
            var_name="Akzeptanz",
            value_name="Prozent"
        )

        # Grafik
        chart = (
            alt.Chart(acceptability_long)
            .mark_bar()
            .encode(
                x=alt.X(
                    f"{selected_environment_column}:N",
                    title=selected_variable_environment,
                    axis=alt.Axis(labelAngle=-45)
                ),
                y=alt.Y(
                    "Prozent:Q",
                    title="Anteil (%)",
                    scale=alt.Scale(domain=[0, 100])
                ),
                color=alt.Color(
                    "Akzeptanz:N",
                    title="Thermal Acceptability"
                ),
                tooltip=[
                    selected_environment_column,
                    "Akzeptanz",
                    alt.Tooltip("Prozent:Q", format=".1f")
                ]
            )
            .properties(
                height=500
            )
        )

        st.altair_chart(chart, use_container_width=True)
        
        # Ergebnistabelle und Bedeutung der Ergebnisse
        with st.expander(
                f"**📈 Ergebnisse Thermische Akzeptanz und {selected_variable_environment} in %**"
                ):
                st.dataframe(acceptability_pct, use_container_width=True)
                if selected_variable_environment == "Klimazone":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        - In allen vier Klimazonen ist die thermische Akzeptanz **bei den gültigen Antworten überwiegend hoch** (Anteil acceptable > Anteil unacceptable)
                        - Unterschiede:
                        
                            - **Continental**: höchster Anteil von Bewertungen mit "acceptable" bei gültigen Antworten (82.18%)
                            - **Tropical**: höchster Anteil von Bewertungen mit "unacceptable" bei gültigen Antworten (38.38%)
                        - Ergebnisse für Klimazonen sollten unter Berücksichtigung der teilweise hohen Anteile an Unknown-Antworten interpretiert werden
                    """
                    )
                elif selected_variable_environment == "Klima":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermische Akzeptanz **unterscheidet sich bei den gültigen Antworten zwischen den Klimata stärker** als zwischen den Hauptklimazonen 
                        - Unterschiede:
                                
                            - Monsoon-influenced Temperate Oceanic: höchster Anteil von Bewertungen mit "akzeptabel" bei gültigen Antworten (91.96%)
                            - Tropical Savanna: höchster Anteil von Bewertungen mit "unakzeptabel" bei gültigen Antworten (71.29%)    
                        - Ergebnisse für Klimata sollten unter Berücksichtigung der teilweise hohen Anteile an Unknown-Antworten interpretiert werden
                    """
                    )
                elif selected_variable_environment == "Region":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermische Akzeptanz **unterscheidet sich bei den gültigen Antworten leicht zwischen den Regionen**
                                
                            - Americas, Asia und Europe: akzeptable Bewertungen überwiegen gegenüber unakzeptablen 
                            - Oceania: Anteil unakzeptabler Bewertungen geringfügig höher als Anteil akzeptabler Bewertungen (51,58 % vs. 48,42 %)
                                
                        - Americas: höchster Anteil von Bewertungen mit "akzeptabel" bei gültigen Antworten (84.49%)                    
                        - Ergebnisse für Regionen sollten unter Berücksichtigung der teilweise hohen Anteile an Unknown-Antworten interpretiert werden
                    """
                    )
                else:
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                         
                        - Thermische Akzeptanz **unterscheidet sich bei den gültigen Antworten zwischen den Ländern stärker** als zwischen den Regionen 
                        - Unterschiede:
                                
                            - **Slovakia**: höchster Anteil von Bewertungen mit "akzeptabel" bei gültigen Antworten (92.73%)
                            - **South Korea**: 
                                    
                                - höchster Anteil von Bewertungen mit "unakzeptabel" bei gültigen Antworten 
                                - Anteil unakzeptabler Bewertungen höher als Anteil akzeptabler Bewertungen (66.12 % vs. 33.87 %)
                            - Alle anderen Länder: Anteil akzeptabler Bewertungen höher als der Anteil unakzeptabler Bewertungen
                        - Ergebnisse für Länder sollten unter Berücksichtigung der teilweise hohen Anteile an Unknown-Antworten interpretiert werden
                """
                )   

    # ---------------------------------------------------------
    # 📊 6. Ergebnistabelle erstellen
    # ---------------------------------------------------------
    with col6:
        titles = {
                "thermal_comfort": "Thermal Comfort",
                "thermal_sensation": "Thermal Sensation",
                "thermal_preference": "Thermal Preference",
                "thermal_acceptability": "Thermal Acceptability"
            }

       
    # ---------------------------------------------------------
    # 📊 7. Expander mit Hinweisen
    # ---------------------------------------------------------
    with st.expander("Allgemeine Hinweise"):
        st.markdown("""
        - **Hinweise zum Lesen der Diagramme:**
                    
            - Balken: stellen Mittelwerte dar
            - Punkte: stellen Median dar
                    
        - **Hinweise zur Interpretation der Diagramme:**
                    

            - Teilweise stark unterschiedliche Stichprobengrößen ➝ Ergebnisse sollten vorsichtig und überwiegend deskriptiv interpretiert werden
            - Teilweise viele fehlende Werte ➝ Vergleichbarkeit zwischen den Gruppen ist eingeschränkt (z.B. bei Thermischer Akzeptanz)
            - Thermische Akzeptanz:
                    
                - Unknown: Anteil der ursprünglichen Antworten ohne gültige Akzeptanzbewertung in %
                - acceptable und unacceptable: beziehen sich ausschließlich auf die gültigen Antworten (ergeben daher zusammen 100%)
        
        """
        )

with tab3:

    st.subheader("📊 Untersuchung des Zusammenhangs zwischen klimatischen/geografischen Variablen und thermischer Bewertung")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1.5])
    col3, col4 = st.columns([2, 1])
    col5, col6 = st.columns([2,1])
    
    # ---------------------------------------------------------
    # 📊 1. Statistischen Zusammenhang berechnen
    # --------------------------------------------------------- 

    results = []

    for environment_label, environment_column in environment_mapping.items():

        for thermal_label, thermal_column in thermal_mapping.items():

            # Unknown entfernen
            if thermal_column in [
                "thermal_preference",
                "thermal_acceptability"
            ]:
                df_test = df[
                    df[thermal_column] != "Unknown"
                ]
            else:
                df_test = df

            contingency_table = pd.crosstab(
                df_test[environment_column],
                df_test[thermal_column]
            )

            chi2, p, dof, expected = chi2_contingency(
                contingency_table
            )

            n = contingency_table.sum().sum()
            phi2 = chi2 / n

            r, k = contingency_table.shape

            cramers_v = np.sqrt(
                phi2 / min(k-1, r-1)
            )

            results.append({
                "Umweltvariable": environment_label,
                "Thermische Variable": thermal_label,
                "p-Wert": f"{p:.4f}",
                "Signifikant": "✅" if p < 0.05 else "✗",
                "Effektgröße": round(cramers_v, 3),
                "Interpretation des Zusammenhangs": interpret_effect(cramers_v)                 
            })

            chi2_results_df = pd.DataFrame(results)

    # ---------------------------------------------------------
    # 📊 2. Erstellung und Ausgabe der Heatmap
    # --------------------------------------------------------- 
    
    with col1:
        # Dataframe für hetmap erzeugen
        heatmap_df = chi2_results_df.pivot(
            index="Umweltvariable",
            columns="Thermische Variable",
            values="Effektgröße"
        )

        fig = px.imshow(
            heatmap_df,
            text_auto=".2f",
            color_continuous_scale="Blues",
            zmin=0,
            zmax=1,
            labels={
                "color": "Cramérs V"
            }
        )

        fig.update_layout(
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        #### Interpretation:
                    
        Es gibt **mittlere, schwache und sehr schwache Zusammenhänge** zwischen den klimatischen/geografischen Variablen und den thermischen Bewertungen:           
            
        ➡️ **Klima: schwache bis mittlere** Zusammenhänge 
                    
        ➡️ **Land: schwache** Zusammenhänge  
                    
        ➡️ **Klimazone: sehr schwache bis Schwache** Zusammenhänge 
                    
        ➡️ **Region: sehr schwache bis Schwache** Zusammenhänge
    """
    )

    # ---------------------------------------------------------
    # 📊 3. Ergebnis-DataFrame für statistischen Zusamennhang ausgeben
    # --------------------------------------------------------- 

    with col3:
        st.subheader("ℹ️ Details zu statistischem Zusammenhang")

        selected = selected_variable_environment

        for variable in environment_mapping.keys():

            with st.expander(
                f"**📈 Zusammenhang {variable} ↔ thermische Variablen**"
            ):
                st.dataframe(
                    chi2_results_df[
                        chi2_results_df["Umweltvariable"] == variable
                    ],
                    hide_index=True,
                    use_container_width=True
                )

        
        st.markdown("<br>", unsafe_allow_html=True)


        with st.expander("Informationen zum Lesen des Zusammenhangs"):
            st.markdown("""                  
            - **Erklärung der Werte:**
                - **p-Wert**: gibt an, ob ein Zusammenhang statistisch signifikant ist 
                    
                    ➝ wenn p < 0.05 ➝ signifikant ✅
                - **Effektgröße**: gibt die Größe des Zusammenhangs an ➝ Interpretation bei Cramérs V:
                     - < 0.10 ➝ sehr schwach
                     - < 0.30 ➝ schwach
                     - < 0.50 ➝ mittel
                     - &gt; 0.50 ➝ stark
            
            - **Hinweise:** 
                - Für die Signifikanzprüfung wurde der Chi²-Test verwendet, für die Ermittlung der Effektstärke wurde Cramérs V berechnet
                - Es kann nur eine Aussage darüber gemacht werden, ob ein Zusammenhang besteht, jedoch nicht in welche Richtung dieser wirkt
            """)             

        st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 📊 4. Zusammenfassung und Bedeutung der Ergebnisse
    # --------------------------------------------------------- 
  
    with col5:
        st.subheader("ℹ️ Zusammenfassung und Bedeutung der Ergebnisse")

        st.info(
            """
            **Ergebnisse:**

            - ⭐**Zusammenhang** zwischen allen vier thermischen Bewertungsvariablen und allen vier klimatischen/geografischen Variablen ✅
            - **Klima** hat den **größten Zusammenhang mit der thermischen Bewertung**
            - Klimazone und Region haben den geringsten Zusammenhang mit der thermischen Bewertung
            - Tendenziell ist der Zusammenhang allgemein am **stärksten bei Thermischem Komfort und Thermischer Akzeptanz**
            """
        )

        st.info(
            """
            **Bedeutung:**

            - ⭐ **Feinere klimatische Klassifikation hat insgesamt stärkeren Zusammenhang** mit der thermischen Bewertung als Länder-/Regionszugehörigkeit oder größer gefasste Klimazonen
                
                ➝ mögliche Erklärungen:
                - Klimazone: Komplexität wird stark reduziert ➝ klimatische Unterschiede werden stark vereinfacht
                - Land: hier können große Unterschiede bestehen z.B. in mehreren Klimata, unterschiedlichen Normen und Standards, kulturellen Unterschieden
                - Region: noch stärkere Zusammenfassung als Land


            - ⭐ Ergebnisse deuten darauf hin, dass klimatische/geografische Variablen einen **relevanten, aber nicht dominierenden Einfluss auf die thermische Bewertung** haben
            """
        )
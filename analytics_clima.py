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
import math



st.set_page_config(page_title="Analyse Klima", layout="wide", initial_sidebar_state="expanded")

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
    

# Mehrfarbige Kreise erstellen
def create_pie_segments(df, climate_column, radius=1.5):

    segments = []

    for _, row in df.iterrows():

        climate_zones = row[climate_column]

        n = len(climate_zones)

        angle_step = 360 / n

        for i, climate_zone in enumerate(climate_zones):

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
                climate_column: climate_zone,
                "polygon": polygon,
                "color": climate_colors.get(climate_zone)
            })

    return pd.DataFrame(segments)

# ---------------------------------------------------------
# 📌 Daten laden
# ---------------------------------------------------------
df = pd.read_csv("db_bereinigt_final.csv")

# ---------------------------------------------------------
# 📌 Seitentitel
# ---------------------------------------------------------
st.title("🌍 Analyse Klima und thermische Wahrnehmung")

# ---------------------------------------------------------
# 📌 tabs definieren
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["Untersuchung der Unterschiede zwischen klimatischen Gruppen", "Betrachtung der Unterschiede zwischen klimatischen Gruppen"])

#########################################################################################################
#########################################################################################################

# # ---------------------------------------------------------
# # 📌 Geografische Verteilung
# # ---------------------------------------------------------
# with tab1:

#     # Nur Zeilen behalten, die gültige Koordinaten haben
#     df = df.dropna(subset=["latitude", "longitude"])

#     st.subheader("Klimatypen vs. Klimazonen")

#     st.markdown("<br>", unsafe_allow_html=True)

#     # ---------------------------------------------------------
#     # 🔍 2. Filter-Widget (Kima/Klimazone)
#     # ---------------------------------------------------------

#     # Filter für Klima/Klimazone
#     climate_filter = st.selectbox(
#         "Variable auswählen",
#         ["Klimazone", "Klimatyp"],
#         key="climate_variable"
#     )


#     # ---------------------------------------------------------
#     # 🔎 3. Filter anwenden
#     # ---------------------------------------------------------

#     # Klima/Klimazone anwenden
#     if climate_filter == "Klimatyp":
#         selected_climate_column = "climate"
#     else:
#         selected_climate_column = "climate_zone"


#     # ---------------------------------------------------------
#     # 📌 4. Kombinationen von Ländern und Klimazonen erstellen
#     # ---------------------------------------------------------
#     # Land-Klima-Kombinationen erstellen

#     country_climate = (
#         df[["country", "latitude", "longitude", selected_climate_column]]
#         .groupby("country")
#         .agg({
#             "latitude": "mean",
#             "longitude": "mean",
#             selected_climate_column: lambda x: list(x.dropna().unique())
#         })
#         .reset_index()
#     )

#     # Klimanamen bereinigen
#     country_climate[selected_climate_column] = (
#         country_climate[selected_climate_column]
#         .apply(
#             lambda climates: [
#                 c.strip().replace("\xa0", " ")
#                 for c in climates
#                 if isinstance(c, str)
#             ]
#         )
#     )

#     # Land-Klimazonen-Kombinationen erstellen
#     country_climate_zone = (
#         df[["country", "latitude", "longitude", selected_climate_column]]
#         .groupby("country")
#         .agg({
#             "latitude": "mean",
#             "longitude": "mean",
#             selected_climate_column: lambda x: list(x.dropna().unique())
#         })
#         .reset_index()
#     )

#     # Klimanamen bereinigen
#     country_climate_zone[selected_climate_column] = (
#         country_climate_zone[selected_climate_column]
#         .apply(
#             lambda climates: [
#                 c.strip().replace("\xa0", " ")
#                 for c in climates
#                 if isinstance(c, str)
#             ]
#         )
#     )

#     # Farben für Klimazonen vergeben
#     if selected_climate_column == "climate":

#         climate_colors = {
#         # Tropische Klimate
#         "wet equatorial": [220, 80, 120, 180],
#         "tropical rainforest": [200, 60, 120, 180],
#         "tropical monsoon": [230, 100, 140, 180],
#         "tropical savanna": [240, 130, 150, 180],
#         "tropical wet savanna": [230, 110, 160, 180],
#         "tropical dry savanna": [210, 90, 140, 180],
#         "tropical": [220, 120, 160, 180],

#         # Aride / trockene Klimate
#         "hot arid": [245, 210, 80, 180],
#         "desert (hot arid)": [240, 190, 60, 180],
#         "hot desert": [230, 170, 40, 180],
#         "semi arid midlatitude": [220, 180, 70, 180],
#         "semi arid high altitude": [200, 170, 90, 180],
#         "hot semi-arid": [235, 200, 90, 180],
#         "cold semi-arid": [190, 170, 100, 180],
#         "subtropical hot and dry": [250, 180, 50, 180],

#         # Mediterrane Klimate
#         "mediterranean": [180, 160, 70, 180],
#         "hot-summer mediterranean": [200, 150, 60, 180],
#         "warm-summer mediterranean": [170, 150, 80, 180],
#         "cool-summer mediterranean": [140, 160, 100, 180],

#         # Gemäßigte Klimate
#         "temperate": [80, 180, 90, 180],
#         "humid subtropical": [60, 170, 100, 180],
#         "temperature marine": [60, 150, 120, 180],
#         "temperate oceanic": [40, 140, 170, 180],
#         "west coast marine": [50, 130, 190, 180],
#         "subtropical highland": [100, 190, 100, 180],

#         # Kontinentale Klimate
#         "humid midlatitude": [120, 100, 200, 180],
#         "warm-summer humid continental": [140, 100, 210, 180],
#         "monsoon-influenced humid subtropical": [160, 120, 220, 180],
#         "monsoon-influenced temperate oceanic": [130, 150, 220, 180],
#         "monsoon-influenced hot-summer humid continental": [150, 90, 190, 180],

#         # Subarktisches Klima
#         "continental subarctic": [80, 90, 150, 180]
#     }

#     else:

#         climate_colors = {
#             "Tropical": [220, 120, 120, 180],
#             "Dry": [245, 210, 80, 180],
#             "Temperate": [0, 180, 0, 180],
#             "Continental": [150, 0, 150, 180]
#         }

    

#     if selected_climate_column == "climate":

#         # Mehrfarbige Kreise für einzelne Klimata
#         pie_data_climate = create_pie_segments(
#             country_climate,
#             selected_climate_column
#         )

#         layer_climate = pdk.Layer(
#             "PolygonLayer",
#             data=pie_data_climate,
#             get_polygon="polygon",
#             get_fill_color="color",
#             pickable=True,
#             stroked=False
#         )


#     else:
#         # Mehrfarbige Kreise für Klimazonen
#         pie_data_climate_zone = create_pie_segments(
#             country_climate_zone,
#             selected_climate_column
#         )

#         layer_climate_zone = pdk.Layer(
#             "PolygonLayer",
#             data=pie_data_climate_zone,
#             get_polygon="polygon",
#             get_fill_color="color",
#             pickable=True,
#             stroked=False
#         )

   

#     # ---------------------------------------------------------
#     # 🌐 6. Kartenansicht definieren
#     # ---------------------------------------------------------
#     # Tooltip-Design
#     if climate_filter == "Klimatyp":
#         view_state_climate = pdk.ViewState(
#             latitude=country_climate["latitude"].mean() if len(country_climate) else 0,
#             longitude=country_climate["longitude"].mean() if len(country_climate) else 0,
#             zoom=1
#         )

    
#         tooltip_climate = {
#             "html": """
#             <b>{country}</b><br/>
#             Klimatyp: {climate}
#             """,
#             "style": {
#                 "color": "white"
#             }
#         }

#     else:
#         view_state_climate_zone = pdk.ViewState(
#             latitude=country_climate_zone["latitude"].mean() if len(country_climate_zone) else 0,
#             longitude=country_climate_zone["longitude"].mean() if len(country_climate_zone) else 0,
#             zoom=1
#         )

#         tooltip_climate_zone = {
#             "html": """
#             <b>{country}</b><br/>
#             Klimazone: {climate_zone}
#             """,
#             "style": {
#                 "color": "white"
#             }
#         }

#     # Legende hinzufügen
#     st.markdown("""
#     **Klimazonen:**

#     🔴 Tropical  
#     🟡 Dry  
#     🟢 Temperate  
#     🟣 Continental
#     """)


#     # ---------------------------------------------------------
#     # 🧭 7. Karte rendern (ohne Mapbox-Key!)
#     # ---------------------------------------------------------
#     if climate_filter == "Klimatyp":
#         st.pydeck_chart(
#             pdk.Deck(
#                 layers=[layer_climate],
#                 initial_view_state=view_state_climate,
#                 tooltip=tooltip_climate,
#                 map_style=None
#             )
#         )
    
#     else:
#         st.pydeck_chart(
#             pdk.Deck(
#                 layers=[layer_climate_zone],
#                 initial_view_state=view_state_climate_zone,
#                 tooltip=tooltip_climate_zone,
#                 map_style=None 
#             )
#         )

#     # ---------------------------------------------------------
#     # 🧭 8. Zuordnung Klimata zu Klimazonen
#     # ---------------------------------------------------------

#     st.markdown("<br><br>", unsafe_allow_html=True)

#     st.markdown("### Zuordnung von Klimatypen, Regionen und Ländern zu den Hauptklimazonen")

#     for zone in sorted(df["climate_zone"].dropna().unique()):
#         if zone == "Continental":
#             with st.expander(f"🟣 {zone}"):

#                 zone_df = (
#                     df[df["climate_zone"] == zone]
#                     [["climate", "region", "country"]]
#                     .drop_duplicates()
#                     .sort_values(
#                         by=["climate", "region", "country"]
#                     )
#                 )

#                 st.dataframe(
#                     zone_df,
#                     use_container_width=True,
#                     hide_index=True
#                 )
#         elif zone == "Dry":
#             with st.expander(f"🟡 {zone}"):

#                 zone_df = (
#                     df[df["climate_zone"] == zone]
#                     [["climate", "region", "country"]]
#                     .drop_duplicates()
#                     .sort_values(
#                         by=["climate", "region", "country"]
#                     )
#                 )

#                 st.dataframe(
#                     zone_df,
#                     use_container_width=True,
#                     hide_index=True
#                 )
#         elif zone == "Temperate":
#             with st.expander(f"🟢 {zone}"):

#                 zone_df = (
#                     df[df["climate_zone"] == zone]
#                     [["climate", "region", "country"]]
#                     .drop_duplicates()
#                     .sort_values(
#                         by=["climate", "region", "country"]
#                     )
#                 )

#                 st.dataframe(
#                     zone_df,
#                     use_container_width=True,
#                     hide_index=True
#                 )
#         else:
#              with st.expander(f"🔴 {zone}"):

#                 zone_df = (
#                     df[df["climate_zone"] == zone]
#                     [["climate", "region", "country"]]
#                     .drop_duplicates()
#                     .sort_values(
#                         by=["climate", "region", "country"]
#                     )
#                 )

#                 st.dataframe(
#                     zone_df,
#                     use_container_width=True,
#                     hide_index=True
#                 )

#     # Hinweis zu Klimazonen-Zuweisung
#     with st.expander("Weitere Informationen zu Klimatypen und Klimazonen"):
#         st.markdown("""  
#         - Hinweise:
#             - Die **5. Hauptklimazone Polar** ist hier nicht mit aufgeführt, da es für diese Klimazone in diesem Datensatz keine Daten gibt
#             - Es wurde **keine offizielle Zuordnung der Klimatypen zu den Klimazonen** gefunden, daher kann sich die hier gewählte Zuordnung von anderen unterscheiden
#         """)

#         st.markdown(""" 
#         - **Beschreibungen zu Klimazonen:**
#             - **Tropical**: Ganzjährig hohe Temperaturen, geringe jahreszeitliche Schwankungen 
#             - **Dry**: Geringe Niederschläge, aride und semiaride Gebiete
#             - **Temperate**: Moderate Temperaturen, ausgeprägte Jahreszeiten
#             - **Continental**: Große Temperaturunterschiede zwischen Sommer und Winter
#         """)



#########################################################################################################
#########################################################################################################

# ---------------------------------------------------------
# 📌 Zusammenhang Klima und thermische Bewertung
# ---------------------------------------------------------
with tab1:

    st.subheader("📊 Gibt es Unterschiede zwischen klimatischen Gruppen hinsichtlich thermischer Wahrnehmung?")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1.5])
    col3, col4 = st.columns([2, 1])

   
    # ---------------------------------------------------------
    # 🔎 1. Mapping-Dictionary
    # ---------------------------------------------------------
    # Mapping-Dictionary Klima
    environment_mapping = {
        "Klimatyp": "climate",
        "Klimazone": "climate_zone"     
    }
    # "Region": "region",
    # "Land": "country"   

    # Mapping-Dictionary thermische Variablen
    thermal_mapping = {
        "Thermischer Komfort": "thermal_comfort",
        "Thermisches Empfinden": "thermal_sensation",
        "Thermische Präferenz": "thermal_preference",
        "Thermische Akzeptanz": "thermal_acceptability"
    }
    
    # ---------------------------------------------------------
    # 📊 1. Statistischen Zusammenhang berechnen
    # --------------------------------------------------------- 

    results = []

    for environment_label, environment_column in environment_mapping.items():

        for thermal_label, thermal_column in thermal_mapping.items():

            # Unknown entfernen
            if thermal_column in ["thermal_preference", "thermal_acceptability"]:
                df_test = df[df[thermal_column] != "Unknown"]
            else:
                df_test = df

            contingency_table = pd.crosstab(
                df_test[environment_column],
                df_test[thermal_column]
            )

            chi2, p, dof, expected = chi2_contingency(contingency_table)

            n = contingency_table.sum().sum()
            phi2 = chi2 / n

            r, k = contingency_table.shape

            cramers_v = np.sqrt(phi2 / min(k-1, r-1))

            results.append({
                "Umweltvariable": environment_label,
                "Thermische Variable": thermal_label,
                "p-Wert": "p < 0.0001" if p < 0.0001 else f"{p:.4f}",
                "Signifikant": "✅" if p < 0.05 else "✗",
                "Effektgröße": round(cramers_v, 3),
                "Interpretation des Zusammenhangs": interpret_effect(cramers_v)                 
            })

            chi2_results_df = pd.DataFrame(results)

    # ---------------------------------------------------------
    # 📊 2. Erstellung und Ausgabe der Heatmap
    # --------------------------------------------------------- 
    
    with col1:
        # Dataframe für heatmap erzeugen
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

        fig.update_traces(
            hovertemplate=None,
            hoverinfo="skip"
        )

        fig.update_layout(
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        #### 📌 Wichtige Ergebnisse:

        ➡️ Beide klimatischen Gruppen **unterscheiden sich statistisch signifikant** hinsichtlich der thermischen Wahrnehmung ✅:
        """
            )

        st.markdown("""
         

        - **Stärkste Unterschiede bei thermischem Komfort und thermischer Akzeptanz**          
            
        - **Stärkere Unterschiede bei Klimatyp** (mittlere bis schwach ausgeprägte Unterschiede)
                    
        - **Geringere Unterschiede bei Klimazone** (schwach bis sehr schwach ausgeprägte Unterschiede) 
                    
        ➡️ Thermische Wahrnehmung unterscheidet sich zwischen den Klimatypen stärker als zwischen den übergeordneten Hauptklimazonen
    """
    )

    # ---------------------------------------------------------
    # 📊 3. Ergebnis-DataFrame für statistischen Zusammenhang ausgeben
    # --------------------------------------------------------- 

    with col3:
        st.subheader("ℹ️ Details zu statistischen Tests")


        for variable in environment_mapping.keys():

            with st.expander(f"**📈 {variable} ↔ Thermische Wahrnehmung**"):
                st.dataframe(
                    chi2_results_df[chi2_results_df["Umweltvariable"] == variable],
                    hide_index=True,
                    use_container_width=True
                )

        
        st.markdown("<br>", unsafe_allow_html=True)


        with st.expander("Informationen zum Lesen der Unterschiede"):
            st.markdown("""                  
            - **Erklärung der Werte:**
                - **p-Wert**: gibt an, ob ein Zusammenhang statistisch signifikant ist 
                    
                    ➝ wenn p < 0.05 ➝ signifikant ✅
                - **Effektgröße**: gibt die Größe des Zusammenhangs an ➝ Interpretation bei Cramérs V zur Orientierung:
                     - < 0.10 ➝ sehr schwach (geringe Unterschiede zwischen den Gruppen)
                     - < 0.30 ➝ schwach (leichte Unterschiede zwischen den Gruppen)
                     - < 0.50 ➝ mittel (deutliche Unterschiede zwischen den Gruppen)
                     - &gt; 0.50 ➝ stark (stark ausgeprägte Unterschiede zwischen den Gruppen)
            
            - **Hinweise:** 
                - Für die Signifikanzprüfung wurde der Chi²-Test verwendet, für die Ermittlung der Effektstärke wurde Cramérs V berechnet
                    
                    ➝ Thermischer Komfort und Thermisches Empfinden sind ordinal skaliert, weshalb auch zusätzliche Rangtests verwendet werden könnten
                    ➝ Für die vergleichende Darstellung wurde jedoch eine einheitliche kategoriale Betrachtung gewählt
                - Es kann nur eine Aussage darüber gemacht werden, ob ein Zusammenhang besteht, jedoch nicht in welche Richtung dieser wirkt
            """)             

        st.markdown("<br><br>", unsafe_allow_html=True)

    # # ---------------------------------------------------------
    # # 📊 4. Zusammenfassung und Bedeutung der Ergebnisse
    # # --------------------------------------------------------- 
  
  
    # st.subheader("ℹ️ Ergebnisse")

    # st.info(
    #     """
    #     - Die thermischen Komfortparameter **unterscheiden sich statistisch signifikant** zwischen den untersuchten klimatischen und geografischen Gruppen ✅  
        

    #     - Unterschiede sind **mittel bis sehr schwach** ausgeprägt  


    #     - **Feinere klimatische Klassifikation** kann Unterschiede im thermischem Befinden besser abbilden als übergeordnete Klimazonen oder Länder-/Regionszugehörigkeit
    #     """
    # )
    
                # ➝ mögliche Erklärungen:
                # - Klimazone: Komplexität wird stark reduziert ➝ klimatische Unterschiede werden stark vereinfacht
                # - Land: hier können große Unterschiede bestehen z.B. in mehreren Klimata, unterschiedlichen Normen und Standards, kulturellen Unterschieden
                # - Region: noch stärkere Zusammenfassung als Land
#########################################################################################################
#########################################################################################################

# ---------------------------------------------------------
# 📌 Betrachtung Klima und thermische Bewertung
# ---------------------------------------------------------

with tab2:
    st.subheader("Wie sehen die Unterschiede zwischen klimatischen Gruppen hinsichtlich thermischer Wahrnehmung aus?")
    st.markdown("<br>", unsafe_allow_html=True)
  
    # st.markdown("""
    #     - Statistische Untersuchung hat gezeigt, dass es Unterschiede zwischen den klimatischen und geografischen Gruppen hinsichtlich thermischem Befinden gibt

                
    #     - Unterschiede sind besonders ausgeprägt bei: 
                

    #         - Klimatypen
    #         - hinsichtlich thermischem Komfort und thermischer Akzeptanz
                
        
    #     **➝ Wie sehen diese Unterschiede aus?**
    # """
    # )
    # st.markdown("<br><br>", unsafe_allow_html=True)


    col1, col2, col3 = st.columns([1,0.08, 1])
    col4, spacer = st.columns([2, 0.2])
    col6, spacer = st.columns([2, 0.2])
    col8, col9 = st.columns([10, 0.2])
         

    with col1:
        # ---------------------------------------------------------
        # 🔍 2. Filter-Widget
        # ---------------------------------------------------------
        # Filter-Widget (Klima/Klimazone)
        selected_variable_environment = st.selectbox(
            "Klimatische Variable auswählen",
            list(environment_mapping.keys()),
            key="selectbox_environment"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Filter-Widget (Klima/Klimazone)
        selected_variable_thermal = st.selectbox(
            "Thermische Variable auswählen",
            list(thermal_mapping.keys()),
            key="selectbox_thermal"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 🔍 3. Mapping anwenden
    # ---------------------------------------------------------
    # Mapping für Klima anwenden
    selected_environment_column = environment_mapping[selected_variable_environment]  
    selected_thermal_column = thermal_mapping[selected_variable_thermal]      
    


    # ---------------------------------------------------------
    # 📊 4. Grafiken erstellen
    # ---------------------------------------------------------
    # Diagramm Thermischer Komfort
    with col4:
        if selected_variable_thermal == "Thermischer Komfort":
            # Titel für Diagramm Thermischer Komfort
            st.subheader(f"Thermischer Komfort und {selected_variable_environment}")

            plot_df = df.copy()

            # Berechnungen für Diagramm und Ergebnistabelle
            thermal_comfort_stats = (
                plot_df
                .groupby(selected_environment_column)[selected_thermal_column]
                .agg(
                    Mittelwert="mean",
                    Median="median",
                    Anzahl="count"
                )
                .reset_index()
            )

            thermal_comfort_stats["Mittelwert"] = thermal_comfort_stats["Mittelwert"].round(2)
            thermal_comfort_stats["Median"] = thermal_comfort_stats["Median"].round(2)

            thermal_comfort_stats = thermal_comfort_stats.sort_values(by="Mittelwert", ascending=False)

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
                        title=f"Mittelwert {selected_variable_thermal}",
                        scale=alt.Scale(domain=[0, 6]),
                        axis=alt.Axis(tickMinStep=1)
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
                        f"{selected_environment_column}:N",
                        sort="-y"
                    ),
                    y=alt.Y("Median:Q")
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

            with col6:
                if selected_variable_environment == "Klimatyp":
                    st.info("""  
                    - **Thermischer Komfort**: wird tendenziell positiv bewertet
                    - Bewertung des thermischen Komforts **unterscheidet sich zwischen den Klimatypen stärker als zwischen den Hauptklimazonen**        

                        - Subtropcial highland bewertet Komfort tendenziell am besten
                        -  Monsoon-influenced hot-summer humid continental bewertet Komfort tendenziell am schlechtesten
                    """
                    )

            with col6:
            # Ergebnistabelle und Bedeutung der Ergebnisse
                with st.expander(
                        f"**📈 Details zu Ergebnissen Thermischer Komfort und {selected_variable_environment}**"
                        ):
                        st.dataframe(thermal_comfort_stats, use_container_width=True)
                        if selected_variable_environment == "Klimazone":
                            st.markdown("""
                                ℹ️**Interpretation**
                                        
                                
                                - Thermische Komfortbewertung **unterscheidet sich zwischen den Klimazonen**
                                        
                                    - **Dry, Temperate und Tropical**: bewerten thermischen Komfort **tendenziell positiv** (Median = 5)
                                    - **Continental**: bewertet thermischen Komfort **tendenziell niedriger** (Median = 3)
                            """
                            )
                        elif selected_variable_environment == "Klimatyp":
                            st.markdown("""
                                ℹ️**Interpretation**
                                        
                                
                                - Bewertung des thermischen Komforts **unterscheidet sich zwischen den Klimatypen stärker** als zwischen den Hauptklimazonen 
                            """
                            )
            st.markdown("<br>", unsafe_allow_html=True)
    
        elif selected_variable_thermal == "Thermisches Empfinden":
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
                        title="Mittelwert Thermal Sensation",
                        scale=alt.Scale(domain=[-3, 3]),
                        axis=alt.Axis(tickMinStep=1)
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
                        f"{selected_environment_column}:N",
                        sort="-y"
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
            with st.expander(f"**📈 Ergebnisse Thermisches Empfinden und {selected_variable_environment}**"):
                st.dataframe(thermal_sensation_stats, use_container_width=True)
                if selected_variable_environment == "Klimazone":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        - In allen vier Klimazonen wird das thermische Empfinden **tendenziell** als **neutral** bewertet  (Median = 0)
                        - Mittelwerte weisen auf eine geringe Tendenz zu einer wärmeren Wahrnehmung hin (Mittelwerte zwischen 0.07 und 0.24)
                    """
                    )
                elif selected_variable_environment == "Klimatyp":
                    st.markdown("""
                        ℹ️**Interpretation**
                                
                        
                        - Thermisches Empfinden wird auch bei Klimatypen **tendenziell** eher als **neutral** bewertet (meiste Medianwerte bei 0)
                                
                            ➝ mit leichter Tendenz zu wärmerer Bewertung (meiste Mittelwerte zwischen -0.2 und + 0.6) 
                        - Aber es gibt **mehr Variation** als bei den Hauptklimazonen (Medianwerte zwischen -1 und 1)                   
                    """
                    )

        elif selected_variable_thermal == "Thermische Präferenz":
            # Diagramm Thermische Präferenz
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
                        scale=alt.Scale(domain=[-1, 1]),
                        axis=alt.Axis(values=[-1, 0, 1])
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
                        f"{selected_environment_column}:N",
                        sort="-y"
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
                    elif selected_variable_environment == "Klimatyp":
                        st.markdown("""
                            ℹ️**Interpretation**
                                    
                            
                            - Thermische Präferenz wird auch bei Klimatypen **tendenziell** als **neutral** bewertet (Median fast überall = 0)
                            - Aber es gibt **mehr Variation** als bei den Hauptklimazonen (Mittelwerte zwischen -0.5 und +0.35)                
                        """
                        )

        elif selected_variable_thermal == "Thermische Akzeptanz":
            # Diagramm Thermische Akzeptanz
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
            order = acceptability_pct[selected_environment_column].tolist()

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
                        axis=alt.Axis(labelAngle=-45),
                        sort=order,
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

            if selected_variable_environment == "Klimatyp":
                st.info("""  
                **Thermische Akzeptanz**: tendenziell überwiegt akzeptabel gegenüber unakzeptabel
                        

                ➡️ Monsoon-influenced temperate oceanic: höchster Anteil Bewertungen mit "acceptable"
                        
                ➡️ Tropical savanna: höchster Anteil Bewertungen mit "unacceptable"
                """
                )
            
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
                    elif selected_variable_environment == "Klimatyp":
                        st.markdown("""
                            ℹ️**Interpretation**
                                    
                            
                            - Thermische Akzeptanz **unterscheidet sich bei den gültigen Antworten zwischen den Klimatypen stärker** als zwischen den Hauptklimazonen 
                            - Ergebnisse für Klimatypen sollten unter Berücksichtigung der teilweise hohen Anteile an Unknown-Antworten interpretiert werden
                        """
                        )
                    elif selected_variable_environment == "Region":
                        st.markdown("""
                            ℹ️**Interpretation**
                                    
                            
                            - Thermische Akzeptanz **unterscheidet sich bei den gültigen Antworten leicht zwischen den Regionen**
                                    
                                - Americas, Asia und Europe: akzeptable Bewertungen überwiegen gegenüber unakzeptablen 
                                - Oceania: Anteil unakzeptabler Bewertungen geringfügig höher als Anteil akzeptabler Bewertungen (51,58 % vs. 48,42 %)
                                    
                            - Americas: höchster Anteil von Bewertungen mit "acceptable" bei gültigen Antworten (84.49%)                    
                            - Ergebnisse für Regionen sollten unter Berücksichtigung der teilweise hohen Anteile an Unknown-Antworten interpretiert werden
                        """
                        )
                    else:
                        st.markdown("""
                            ℹ️**Interpretation**
                                    
                                
                            - Thermische Akzeptanz **unterscheidet sich bei den gültigen Antworten zwischen den Ländern stärker** als zwischen den Regionen 
                            - Unterschiede:
                                    
                                - **Slovakia**: höchster Anteil von Bewertungen mit "acceptable" bei gültigen Antworten (92.73%)
                                - **South Korea**: 
                                        
                                    - höchster Anteil von Bewertungen mit "unacceptable" bei gültigen Antworten 
                                    - Anteil unakzeptabler Bewertungen höher als Anteil akzeptabler Bewertungen (66.12 % vs. 33.87 %)
                                - Alle anderen Länder: Anteil akzeptabler Bewertungen höher als der Anteil unakzeptabler Bewertungen
                            - Ergebnisse für Länder sollten unter Berücksichtigung der teilweise hohen Anteile an Unknown-Antworten interpretiert werden
                    """
                    )   
   

    # ---------------------------------------------------------
    # 📊 6. Ergebnistabelle erstellen
    # ---------------------------------------------------------
    titles = {
            "thermal_comfort": "Thermal Comfort",
            "thermal_sensation": "Thermal Sensation",
            "thermal_preference": "Thermal Preference",
            "thermal_acceptability": "Thermal Acceptability"
        }

       
    # ---------------------------------------------------------
    # 📊 7. Expander mit Hinweisen
    # ---------------------------------------------------------
    #with st.expander("Diagramme für thermisches Empfinden, thermische Präferenz und thermische Akzeptanz"):
        # Diagramm Thermisches Empfinden
        
        

        

    col1, col2 = st.columns([2, 0.2])

    with col1:
        with st.expander("ℹ️ Allgemeine Hinweise zum Lesen und zur Interpretation der Diagramme"):
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
    

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.subheader("ℹ️ Zusammenfassung")

    st.info("""
    - Ergebnisse zeigen, dass es **Unterschiede in der thermischen Wahrnehmung zwischen klimatischen Gruppen** gibt ➝ erklären jedoch nur einen Teil der Variation der thermischen Wahrnehmung
    - Unterschiede in thermischer Wahrnehmung zeigen sich **deutlicher bei feinerer klimatischer Klassifikation** als bei übergeordneten Klimazonen
    - **Relevanz für Ziel des Projekts:** Um ideale Bedingungen für Gebäude zu schaffen, sollten die klimatischen und geografischen Gegebenheiten berücksichtigt werden
    """
    )
import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt



st.set_page_config(page_title="Globale Datenanalyse", layout="wide", initial_sidebar_state="expanded")

# Load data

df_bereinigt = pd.read_csv("db_bereinigt.csv")

#st.title("Globale Datenanalyse")
#st.line_chart(df_bereinigt["DB"])
#st.dataframe(df_bereinigt)

st.title("Datenverteilung nach geografischem Standort")

tab1,tab2,tab3 = st.tabs(["Anzahl Einträge","Category","Thermal Comfort"])


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
    col7, col8 = st.columns([1,2])
    # --- Bild / Karte ---
    with col5:

        # --- Auswahl, welche Verteilung angezeigt werden soll ---
        option = st.selectbox("Verteilung anzeigen nach:",["Region", "Land", "Stadt"])

        # --- Dynamische Auswahl basierend auf Option ---
        if option == "Region":
            werte = df_bereinigt["region"].dropna()
            auswahl = st.selectbox("Region auswählen", sorted(werte.unique()))
            gefiltert = df_bereinigt[df_bereinigt["region"] == auswahl]

        elif option == "Land":
            werte = df_bereinigt["country"].dropna()
            auswahl = st.selectbox("Land auswählen", sorted(werte.unique()))
            gefiltert = df_bereinigt[df_bereinigt["country"] == auswahl]

        elif option == "Stadt":
            werte = df_bereinigt["city"].dropna()
            auswahl = st.selectbox("Stadt auswählen", sorted(werte.unique()))
            gefiltert = df_bereinigt[df_bereinigt["city"] == auswahl]

        # --- Prozentuale Verteilung ---
        st.markdown("### Prozentuale Verteilung")
        gesamt = len(df_bereinigt)
        anteil = len(gefiltert)
        prozent = round((anteil / gesamt) * 100, 2)

        st.write(f"**Auswahl:** {auswahl}")
        st.write(f"**Anzahl Einträge:** {anteil}")
        st.write(f"**Prozentualer Anteil:** {prozent} %")



    with col6:
        # --- Balkendiagramm: Verteilung innerhalb der Kategorie ---
        st.markdown(f"### Verteilung innerhalb von {option}")
        st.bar_chart(werte.value_counts())

        st.markdown(f"### Karte – {option}: {auswahl}")
        if "latitude" in gefiltert.columns and "longitude" in gefiltert.columns:
            st.map(gefiltert[["latitude", "longitude"]])
        else:
            st.info("Keine geografischen Koordinaten verfügbar.")



with tab3:

    st.subheader("Einfluss der Luftgeschwindigkeit auf die Beziehung zwischen Temperatur und thermischer Empfindung")

    chart = (
        alt.Chart(df_bereinigt)
        .mark_circle(size=60, opacity=0.7)
        .encode(
            x=alt.X("operative_temperature:Q", title="Operative Temperatur [°C]"),
            y=alt.Y("thermal_sensation:Q", title="Thermal Sensation Vote"),
            color=alt.Color("air_speed:Q", title="Luftgeschwindigkeit [m/s]"),
            tooltip=["operative_temperature", "thermal_sensation", "air_speed", "region", "country", "city"]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)

#######################################################################################################################################

    st.subheader("Einfluss der Luftgeschwindigkeit auf die Beziehung zwischen Temperatur und thermischem Komfort")

    chart = (
        alt.Chart(df_bereinigt)
        .mark_circle(size=60, opacity=0.7)
        .encode(
            x=alt.X("operative_temperature:Q", title="Operative Temperatur [°C]"),
            y=alt.Y("thermal_comfort:Q", title="Thermischer Komfort"),
            color=alt.Color("air_speed:Q", title="Luftgeschwindigkeit [m/s]"),
            tooltip=[
                "operative_temperature",
                "thermal_comfort",
                "air_speed",
                "region",
                "country",
                "city"
            ]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)

#####################################################################################################################################

    st.subheader("Thermischer Komfort – Scatterplot mit Dichtekonturen (KDE)")

    # --- Scatterplot ---
    scatter = (
        alt.Chart(df_bereinigt)
        .mark_circle(size=40, opacity=0.5)
        .encode(
            x=alt.X("operative_temperature:Q", title="Operative Temperatur [°C]"),
            y=alt.Y("thermal_comfort:Q", title="Thermischer Komfort"),
            color=alt.Color("air_speed:Q", title="Luftgeschwindigkeit [m/s]"),
            tooltip=[
                "operative_temperature",
                "thermal_comfort",
                "air_speed",
                "region",
                "country",
                "city"
            ]
        )
    )

    # --- KDE-Dichtekonturen ---
    kde = (
        alt.Chart(df_bereinigt)
        .transform_density(
            density="operative_temperature",
            as_=["operative_temperature", "density"],
            groupby=["thermal_comfort"],
            steps=200
        )
        .mark_line(color="black", opacity=0.6)
        .encode(
            x="operative_temperature:Q",
            y="density:Q"
        )
    )

    # --- Kombination ---
    chart = (scatter + kde).properties(height=450)

    st.altair_chart(chart, use_container_width=True)






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



import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(page_title="Database - ASHRAE", layout="wide", initial_sidebar_state="expanded")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("db_measurements_v210.csv")

df = load_data()

# ---------------------------------------------------------
# MAIN PAGE TITLE
# ---------------------------------------------------------
st.title(":material/bar_chart: Die ASHRAE Global Thermal Comfort Database II")
st.markdown("Eine umfassende Datenbank, die sich auf die Untersuchung von Thermalkomfort in verschiedenen Gebäuden konzentriert.")

st.markdown(
    """
    <p style='font-size:18px;'>
        <strong>Dataset Source:</strong> 
        <a href='https://datadryad.org/dataset/doi:10.6078/D1F671' target='_blank'>
            ASHRAE Global Thermal Comfort Database II
        </a>
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# TABS (ONLY ON MAIN PAGE)
# ---------------------------------------------------------
tab_structure,  tab_dataset, tab_overview, tab_erd, tab_map, tab_explorer = st.tabs(
    ["📘 Strukture", "📄 Datenbankdaten", "📊 Overview", "🗂️ ERD", "🌍 Map",  "📊 Explorer"]
)

# ---------------------------------------------------------
# SOURCE TAB
# ---------------------------------------------------------
with tab_structure:
    #st.subheader("")
    st.markdown(
        """
    - Zusammenstellung weltweit durchgeführter Feldstudien aus dem Zeitraum 1995 bis 2016

    - 81.846 neue, validierte Datensätze mit gepaarten Angaben zum subjektiven Komfortempfinden und objektiven Messwerten der Umgebungsbedingungen

    - Integration von 25.617 neuen Einträgen aus Datenbank I (Projekt ASHRAE RP-884 „Adaptive Model“, 1998–2000)

    - Ein abschließender, zusammengeführter Datensatz mit 107.463 hochwertigen Datensätzen (Datenbank II)

        """
    )

    option1 = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Records",
                "type": "pie",
                "radius": ["40%", "70%"],
                "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2},
                "label": {"show": False},
                "emphasis": {"label": {"show": True, "fontSize": 20, "fontWeight": "bold"}},
                "data": [
                    {"value": 81846, "name": "New Database Records"},
                    {"value": 25617, "name": "RP-884 Records"},
                ],
            }
        ],
    }
    st_echarts(option1, height="400px")

    st.subheader("Datensatz")

    st.markdown(
    """
    Der Datensatz ist in zwei Haupttabellen gegliedert:

    **`metadata` Tabelle**  
    Enthält allgemeine Gebäude- und Studieninformationen. Bereitgestellt als Standard-**CSV file**.

    **`measurements` Tabelle**  
    Enthält alle Feldmessungen, einschließlich:
    - Einzelne Fragebogenantworten, dargestellt als Zeile
    - Instrumentelle Innenraummessungen
    - Werte thermischer Indizes
    - Meteorologische Außendaten (sofern verfügbar)
    - Bereitgestellt als **komprimierte CSV-Datei (.csv.gz)** in UTF-8-Kodierung.
    """
    )

# ---------------------------------------------------------
# DATASET TAB
# ---------------------------------------------------------
with tab_dataset:
    # st.subheader("Dataset structure")
    # st.markdown(
    # """
    # The dataset is organized into two main tables:

    # **• `metadata` table**  
    # Contains high‑level building and study information.  
    # Provided as a standard **CSV file**.

    # **• `measurements` table**  
    # Contains all field measurements, including:  
    # - Individual questionnaire responses represented as a row  
    # - Instrumental indoor measurements  
    # - Thermal index values  
    # - Outdoor meteorological data (when available)  
    # - Provided as a **compressed CSV (.csv.gz)** using UTF‑8 encoding.  
    # """
    # )
    st.subheader("Überblick Rohdaten")

    st.text("Hier werden beide Tabellen zusammengeführt, um eine einheitliche Tabelle für unsere Analyse zu erhalten.")
    


#     # Cargar las dos hojas del archivo Excel
#     metadata = pd.read_excel("Daten_gesamt.xlsx", sheet_name="db_metadata")
#     measurements = pd.read_excel("Daten_gesamt.xlsx", sheet_name="db_measurements_v210")

# # Unir usando building_id
#     df = measurements.merge(metadata, on="building_id", how="left")

# # Mostrar resultados
#     st.dataframe(df.head())
#     st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
#     st.subheader("Column names and description")
#     st.write("Column names:", list(df.columns))

    metadata = pd.read_csv("db_metadata.csv")
    measurements = pd.read_csv("db_measurements_v210.csv")
    df = measurements.merge(metadata, on="building_id", how="left")
    st.dataframe(df.head())
    st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")

    # st.subheader("Column names and description")
    # st.write("Column names:", list(df.columns))

    st.markdown("### Spaltennamen:")
    st.markdown(" | ".join([f"`{c}`" for c in df.columns]))


    #st.subheader("Parameter Description")
with st.sidebar:
    st.header("🔧 Dashboard Controls")

    st.write("Use this sidebar to navigate or adjust settings.")

    tab3 = st.tabs(["Über ASHARE"])
    testbutton = st.sidebar.button("6")
    if testbutton == True:
        st.write("Text3")


    # Example: dataset info toggle
    show_info = st.checkbox("Show dataset info", value=True)

    # Example: quick column preview
    selected_col_global = st.selectbox("Quick column view:", df.columns)

    st.write("Preview of selected column:")
    st.write(df[selected_col_global].head())

    


# ---------------------------------------------------------
# OVERVIEW TAB
# ---------------------------------------------------------
with tab_overview:
    st.subheader("Overview")

# ---------------------------------------------------------
# ERD TAB
# ---------------------------------------------------------
with tab_erd:
    st.subheader("Entity Relationship Diagram (ERD)")
    st.write("Visual representation of the database schema and relationships.")

# ---------------------------------------------------------
# MAP TAB
# ---------------------------------------------------------
with tab_map:
    st.subheader("🌍 Global Distribution of ASHRAE Field Studies")
    st.write("build a map")

    # df_map = pd.read_csv("ashrae_db201.csv")
    # country_data = df_map["Country"].value_counts().to_dict()
    # data_list = [{"name": c, "value": v} for c, v in country_data.items()]

    # option_map = {
    #     "tooltip": {"trigger": "item"},
    #     "visualMap": {
    #         "min": 0,
    #         "max": max(country_data.values()),
    #         "text": ["More studies", "Fewer"],
    #         "calculable": True,
    #         "inRange": {"color": ["#D6EAF8", "#2E86C1"]},
    #     },
    #     "series": [
    #         {
    #             "name": "Studies per country",
    #             "type": "map",
    #             "map": "world",
    #             "roam": True,
    #             "data": data_list,
    #         }
    #     ],
    # }
    # st_echarts(option_map, height="600px")



# ---------------------------------------------------------
# EXPLORER TAB
# ---------------------------------------------------------
with tab_explorer:
    st.subheader("Data Explorer")

    column = st.selectbox("Choose a column:", df.columns)
    st.write(df[column].describe())

    if pd.api.types.is_numeric_dtype(df[column]):
        min_val, max_val = float(df[column].min()), float(df[column].max())
        selected_range = st.slider("Select value range:", min_val, max_val, (min_val, max_val))
        filtered_df = df[(df[column] >= selected_range[0]) & (df[column] <= selected_range[1])]
        st.dataframe(filtered_df.head())
    else:
        unique_values = df[column].dropna().unique()
        selected_value = st.selectbox("Select a value:", unique_values)
        filtered_df = df[df[column] == selected_value]
        st.dataframe(filtered_df.head())

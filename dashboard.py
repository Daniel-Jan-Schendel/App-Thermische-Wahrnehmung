import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

# st.title("SmartBuilding-Analytics")
# st.subheader("Datenarchitektur zur Optimierung klimatisierter Gebäudeinfrastrukturen")
# st.write("Dashboard with two sections: Dataset Overview and Data Explorer.")

st.title("SmartBuilding-Analytics Dashboard")


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("db_bereinigt_fertig.csv")
df = load_data()



# Create two tabs
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📄 KPI", "📊 Statistics"])


with tab1:

    st.text("sdsd")

    # ---------------------------------------------------------
    # 🎨 Labels & Farben
    # ---------------------------------------------------------

    


# ---------------------------------------------------------
# TAB 1 — Dataset Overview
# ---------------------------------------------------------
# with tab1:
#     st.header("Dataset Overview")

#     if show_info:
#         st.subheader("Preview of the dataset")
#         st.dataframe(df.head())

#         st.subheader("Dataset shape")
#         st.write(f"Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")

#         st.subheader("Column names")
#         st.write(list(df.columns))

# # ---------------------------------------------------------
# # TAB 2 — Data Explorer
# # ---------------------------------------------------------
# with tab2:
#     st.header("Data Explorer")

#     st.subheader("Select a column to analyze")
#     column = st.selectbox("Choose a column:", df.columns)

#     st.subheader("Summary statistics")
#     st.write(df[column].describe())

#     # Numeric filtering
#     if pd.api.types.is_numeric_dtype(df[column]):
#         st.subheader("Filter by numeric range")

#         min_val = float(df[column].min())
#         max_val = float(df[column].max())

#         selected_range = st.slider(
#             "Select value range:",
#             min_value=min_val,
#             max_value=max_val,
#             value=(min_val, max_val)
#         )

#         filtered_df = df[
#             (df[column] >= selected_range[0]) &
#             (df[column] <= selected_range[1])
#         ]

#         st.write("Filtered results:")
#         st.dataframe(filtered_df.head())

#     # Categorical filtering
#     else:
#         st.subheader("Filter by category")

#         unique_values = df[column].dropna().unique()
#         selected_value = st.selectbox("Select a value:", unique_values)

#         filtered_df = df[df[column] == selected_value]

#         st.write("Filtered results:")
#         st.dataframe(filtered_df.head())


with tab2:

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



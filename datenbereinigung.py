import streamlit as st
import pandas as pd
import io
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Datenbereinigung - ASHRAE", layout="wide",initial_sidebar_state="expanded")

st.header("📊 Inspektion und Bereinigung des Datensatzes")

# Datensätze laden

metadata = pd.read_csv("db_metadata.csv")
measurements = pd.read_csv("db_measurements_v210.csv")
df = measurements.merge(metadata, on="building_id", how="inner")

df_bereinigt = pd.read_csv("db_bereinigt.csv")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Daten importieren",
    "2. Erste Übersicht",
    "3. Datentypen bereinigen",
    "4. Spalten umbenennen"
])

with tab1:
    st.subheader("1. Daten importieren und Zusammenführen der beiden Datensätze")
    code_1 = '''
    # Datensätze laden
    df_meta = pd.read_csv("db_metadata.csv")
    df_measure = pd.read_csv("db_measurements_v2.1.0.csv")

    # Datensätze zusammenführen
    df = pd.merge(df_meta, df_measure, on='building_id', how='inner')
    '''
    st.code(code_1, language="python")
    st.subheader("📁 Originaler Datensatz (vor der Reinigung)")
    st.dataframe(df)
    #st.dataframe(df.head())


with tab2:
    st.subheader("2. Übersicht der zusammengeführten Daten")
    code_2 = '''
    # Datenstruktur analysieren
    df.shape
    df.info()

    # Anzeigen von Duplikaten
    duplicates = df[df.duplicated()]
    duplicates

    # Statistische Daten
    stats = df.describe()
    display(stats)

    # Ausgeben der Anzahl fehlender Werte
    df.isnull().sum()

    # Entfernen von vollständig leeren Zeilen
    df = df.dropna(how='all').reset_index(drop=True)
    '''
    st.code(code_2, language="python")
    df = df.dropna(how='all').reset_index(drop=True)
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.subheader("🔍 Erste Untersuchung des Datensatzes")
    st.code(info_str, language="text")

with tab3:
    st.subheader("3. Bereinigung der Datentypen")
    code_3 = '''
    # Kopie des Datensatzes erstellen:
    df_bereinigt_typ = df.copy()

    # Spalte "timestamp" von str in datetime umwandeln
    df_bereinigt_typ["timestamp"] = pd.to_datetime(df_bereinigt_typ["timestamp"], format='%Y-%m-%dT%H:%M:%SZ', errors="coerce") 

    # Spalte " " von str in int umwandeln
    df_bereinigt_typ["subject_id"] = pd.to_numeric(df_bereinigt_typ["subject_id"], errors="coerce").astype('Int64') 
    df_bereinigt_typ["blind_curtain"] = df_bereinigt_typ["blind_curtain"].astype('Int64')
    df_bereinigt_typ["fan"] = df_bereinigt_typ["fan"].astype('Int64')
    df_bereinigt_typ["window"] = df_bereinigt_typ["window"].astype('Int64')
    df_bereinigt_typ["door"] = df_bereinigt_typ["door"].astype('Int64')
    df_bereinigt_typ["heater"] = df_bereinigt_typ["heater"].astype('Int64')

    # Ausgabe des Datensatzes zur Überprüfung
    df_bereinigt_typ.info()
    df_bereinigt_typ.head()
    '''
    st.code(code_3, language="python")

############ EXECUTION CODE #############################################
    df_bereinigt_typ = df.copy()

    # Spalte "timestamp" von str in datetime umwandeln
    df_bereinigt_typ["timestamp"] = pd.to_datetime(df_bereinigt_typ["timestamp"], format='%Y-%m-%dT%H:%M:%SZ', errors="coerce") 

    # Spalte "subject_id" von str in int umwandeln
    df_bereinigt_typ["subject_id"] = pd.to_numeric(df_bereinigt_typ["subject_id"], errors="coerce").astype('Int64') 

    # Spalte "blind_curtain" von float in int umwandeln
    df_bereinigt_typ["blind_curtain"] = df_bereinigt_typ["blind_curtain"].astype('Int64')

    # Spalte "fan" von float in int umwandeln
    df_bereinigt_typ["fan"] = df_bereinigt_typ["fan"].astype('Int64')

    # Spalte "window" von float in int umwandeln
    df_bereinigt_typ["window"] = df_bereinigt_typ["window"].astype('Int64')

    # Spalte "door" von float in int umwandeln
    df_bereinigt_typ["door"] = df_bereinigt_typ["door"].astype('Int64')

    # Spalte "heater" von float in int umwandeln
    df_bereinigt_typ["heater"] = df_bereinigt_typ["heater"].astype('Int64')

    # Ausgabe des Datensatzes zur Überprüfung

    buffer = io.StringIO()
    df_bereinigt.info(buf=buffer)
    info_str_1 = buffer.getvalue()

    st.subheader("🔍 Untersuchung des Datensatzes")
    st.code(info_str_1, language="text")

with tab4:
    st.subheader("4. Umbenennung von Spalten")
    code_4 = '''
    # Kopie des Datensatzes erstellen:
    df_bereinigt = df_bereinigt_typ.copy()

    # Für besseres Verständnis Umbenennen von bestimmten Spalten
    df_bereinigt = df_bereinigt.rename(columns={
    "lat": "latitude", "lon": "longitude", "has_ec": "has_environmental_controls",
    "met_source": "source_meteorological_data", "ht": "height", "wt": "weight",
    "ta": "air_temperature", "ta_h": "air_temperature_1.1",
    "ta_m": "air_temperature_0.6", "ta_l": "air_temperature_0.1",
    "top": "operative_temperature", "tr": "radiant_temperature",
    "tg": "globe_temperature", "tg_h": "globe_temperature_1.1",
    "tg_m": "globe_temperature_0.6", "tg_l": "globe_temperature_0.1",
    "rh": "relative_humidity", "vel": "air_speed",
    "vel_h": "air_speed_1.1", "vel_m": "air_speed_0.6",
    "vel_l": "air_speed_0.1", "vel_r": "relative_air_speed",
    "met": "metabolic_rate", "clo": "clothing_ensemble_insulation",
    "clo_d": "dynamic_clothing", "pmv": "predicted_mean_vote",
    "pmv_ce": "calculated_predicted_mean_vote", "ppd": "predicted_percentage_dissatisfied",
    "ppd_ce": "calculated_predicted_percentage_dissatisfied",
    "set": "standard_effective_temperature", "t_out": "outdoor_air_temperature",
    "rh_out": "outdoor_relative_humidity", "t_out_isd": "average_daily_outdoor_temperature",
    "rh_out_isd": "average_daily_outdoor_humidity",
    "t_mot_isd": "7_day_mean_outdoor_temperature"
    })
    df_bereinigt
    '''
    st.code(code_4, language="python")



    # Dimensionen nach der Reinigung 
    st.write("### 📏 Dimensionen nach der Reinigung")
    st.write(f"**Zeilen:** {df_bereinigt.shape[0]}")
    st.write(f"**Spalten:** {df_bereinigt.shape[1]}")

    st.subheader("🧹 Datensatz nach der Reinigung")
    st.dataframe(df_bereinigt)



    st.subheader("Diagnose: Gemischte Datentypen in Spalten")

    def diagnose_spalten(df_bereinigt):
        ergebnis = []

        for col in df_bereinigt.columns:
            typ_liste = df_bereinigt[col].map(type).unique()
            ergebnis.append({
                "Spalte": col,
                "Datentypen in der Spalte": [t.__name__ for t in typ_liste],
                "Anzahl verschiedener Typen": len(typ_liste),
                "Anzahl fehlender Werte": df_bereinigt[col].isna().sum(),
                "Pandas-Datentyp": str(df_bereinigt[col].dtype)
            })

        return pd.DataFrame(ergebnis)

    diagnose_df = diagnose_spalten(df_bereinigt)
    st.dataframe(diagnose_df)




st.subheader("Database – Anzahl & Prozent (Pie Chart)")

# Spalte bereinigen
db_clean = df_bereinigt["database"].fillna("Unbekannt").astype(str)

# Werte zählen
db_counts = db_clean.value_counts()

# Total
total = int(db_counts.sum())

# Total anzeigen
st.info(f"**Total Daten:** {total:,}".replace(",", "."))

# Prozent berechnen (mit deutschem Komma)
percentages = [(count / total) * 100 for count in db_counts.values]
percentages_de = [f"{p:.2f}".replace(".", ",") for p in percentages]

# Pie-Daten vorbereiten
pie_data = []
for i, (cat, count) in enumerate(db_counts.items()):
    count_de = f"{count:,}".replace(",", ".")   # Tausenderpunkt
    percent_de = percentages_de[i]              # Komma-Prozent

    pie_data.append({
        "name": str(cat),
        "value": int(count),
        "percent": percent_de
    })

# ECharts Optionen
options = {
    "title": {"text": "Einträge pro Datenbank", "left": "center"},
    "tooltip": {
        "trigger": "item",
        "formatter": "{b}: {c} ({d}%)"
    },
    "legend": {"orient": "vertical", "left": "left"},
    "series": [
        {
            "name": "Database",
            "type": "pie",
            "radius": "60%",
            "data": pie_data,
            "label": {
                "formatter": "{b}: {c} ({d}%)"
            }
        }
    ]
}

st_echarts(options=options, height="500px")

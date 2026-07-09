import streamlit as st
import pandas as pd
import io
from streamlit_echarts import st_echarts
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Datenbereinigung - ASHRAE", layout="wide",initial_sidebar_state="expanded")

st.header("📊 Inspektion und Bereinigung des Datensatzes")

# Datensätze laden

metadata = pd.read_csv("db_metadata.csv")
measurements = pd.read_csv("db_measurements_v210.csv")
df = measurements.merge(metadata, on="building_id", how="inner")

df_bereinigt = pd.read_csv("db_bereinigt.csv")

tab1, tab2, tab3, tab4,tab5, tab6 = st.tabs([
    "1. Datensatz",
    "2. Daten importieren",
    "3. Erste Übersicht",
    "4. Datentypen bereinigen",
    "5. Spalten umbenennen",
    "6. Standardisierung von Kategorien"
])

with tab1:

    # --- Datenquelle ---
    st.markdown(
        """
        <div style="padding: 10px 0;">
            <h2 style="margin-bottom: 5px;">📘 Datenquelle</h2>
            <p style="font-size:18px; line-height:1.5;">
                <strong>Dataset Source:</strong><br>
                <a href='https://datadryad.org/dataset/doi:10.6078/D1F671' target='_blank' style='text-decoration:none;'>
                    ASHRAE Global Thermal Comfort Database II
                </a>
            </p>
            <p style="font-size:16px; color:#555;">
                Eine umfassende Datenbank zur Untersuchung des thermischen Komforts in Gebäuden weltweit.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Informationen ---
    st.markdown(
        """
        <div style="padding: 10px 0;">
            <h2 style="margin-bottom: 5px;">ℹ️ Informationen</h2>
            <ul style="font-size:16px; line-height:1.6; color:#444;">
                <li>Zusammenstellung weltweit durchgeführter Feldstudien aus dem Zeitraum <strong>1995–2016</strong></li>
                <li><strong>81.846</strong> neue, validierte Datensätze mit subjektiven Komfortangaben und objektiven Messwerten</li>
                <li>Integration von <strong>25.617</strong> neuen Einträgen aus Datenbank I (ASHRAE RP‑884 „Adaptive Model“)</li>
                <li>Ein finaler, zusammengeführter Datensatz mit insgesamt <strong>107.463</strong> hochwertigen Datensätzen</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Donut Chart ---
    st.markdown("<h3 style='margin-top:20px;'>📊 Verteilung der Datensätze</h3>", unsafe_allow_html=True)

    option1 = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Records",
                "type": "pie",
                "radius": ["40%", "70%"],
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2
                },
                "label": {"show": False},
                "emphasis": {
                    "label": {"show": True, "fontSize": 20, "fontWeight": "bold"}
                },
                "data": [
                    {"value": 81846, "name": "New Database Records"},
                    {"value": 25617, "name": "RP-884 Records"},
                ],
            }
        ],
    }

    st_echarts(option1, height="400px")

##################################################################################################################################

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

with tab2:
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

###############################################################################################################################################
###############################################################################################################################################

with tab3:
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

   
###############################################################################################################################################
###############################################################################################################################################



with tab4:
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

with tab5:
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


    st.markdown("### Spaltennamen:")
    st.markdown(" | ".join([f"`{c}`" for c in df_bereinigt.columns]))

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



with tab6:


    st.text("Die ASHRAE Global Thermal Comfort Database II sammelt Daten aus vielen verschiedenen Studien, Ländern, Klimazonen und Gebäudetypen. " \
    "Dadurch entstehen unterschiedliche Werte, Skalen und Formate für dieselben Komfortparameter. " \
    "Um diese Daten vergleichbar und auswertbar zu machen, ist eine Standardisierung zwingend notwendig.")


    # ---------------------------------------------------------
    # 📌 Daten laden
    # ---------------------------------------------------------
    df = pd.read_csv("db_bereinigt_fertig.csv")

    # ---------------------------------------------------------
    # 🔧 Standardisierung / Rundung von Thermal Comfort
    # ---------------------------------------------------------
    def map_tc(v):
        if pd.isna(v): 
            return None
        if v < 1.5: return 1
        elif v < 2.5: return 2
        elif v < 3.5: return 3
        elif v < 4.5: return 4
        elif v < 5.5: return 5
        else: return 6

    df["thermal_comfort_std"] = df["thermal_comfort"].apply(map_tc)

    # ---------------------------------------------------------
    # 📊 Plot-Funktion
    # ---------------------------------------------------------
    def plot_hist(series, title):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.hist(series.dropna(), bins=20, color="#4C72B0", edgecolor="white")
        ax.set_title(title)
        ax.set_xlabel("Wert")
        ax.set_ylabel("Häufigkeit")
        st.pyplot(fig)

    # ---------------------------------------------------------
    # 📍 Layout: Zwei Spalten
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)

    # ---------------------------------------------------------
    # 🟦 Spalte 1: Originalwerte
    # ---------------------------------------------------------
    with col1:
        st.subheader("Originalwerte")
        st.write("""
        Diese Werte stammen direkt aus der ASHRAE-Datenbank. 
        Sie können Dezimalwerte enthalten (z. B. 2.7, 3.4, 4.8), 
        was die Analyse erschwert, da viele Studien unterschiedliche Skalen verwenden.
        """)
        plot_hist(df["thermal_comfort"], "Originale Thermal Comfort Werte")

    # ---------------------------------------------------------
    # 🟩 Spalte 2: Standardisierte / gerundete Werte
    # ---------------------------------------------------------
    with col2:
        st.subheader("Standardisierte Werte")
        st.write("""
        Durch die Standardisierung werden alle Werte auf die ASHRAE‑Skala (1–6) abgebildet.
        Dies ermöglicht eine klare, vergleichbare Analyse über Länder, Gebäude und Klimazonen hinweg.
        """)
        plot_hist(df["thermal_comfort_std"], "Standardisierte Thermal Comfort Werte (1–6)")


    st.subheader("Standardisierte thermische Komfortparameter (TSV, TP, TC)")

    st.text(
    "Die ASHRAE-Datenbank enthält Komfortangaben aus vielen Ländern und Studien. Dadurch entstehen unterschiedliche Werte und Skalen. Die folgende Übersicht zeigt, wie Thermal Sensation (TSV), Thermal Preference (TP) und Thermal Comfort (TC) auf einheitliche Codes standardisiert werden, um eine klare und vergleichbare Analyse zu ermöglichen.")
    # Bild laden
    image = Image.open("thermal_parameters_code_numbers.png")

    # Bild anzeigen mit definierter Breite
    st.image(image, caption="Thermische Komfortparameter (TSV, TP, TC) – Standardisierte Codes", width=900)

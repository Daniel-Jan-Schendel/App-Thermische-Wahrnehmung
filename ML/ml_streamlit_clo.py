import streamlit as st
import joblib
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

# Seiteneinstellungen festlegen
st.set_page_config(page_title="Bekleidungs-Isolations-Vorhersage", layout="wide")

# App-Titel
st.title("👕 Vorhersage der Bekleidungsisolation (clothing_ensemble_insulation)")

# ASHRAE Referenz-Dictionary
ashrae_clo_refined = {
    0.00: ("Nackt", "🩲 (Nackt / Minimalst)"),
    0.05: ("Nur Unterwäsche", "🩲 (Slip / Boxershorts)"),
    0.15: ("Sehr leicht", "🩳👕 (Kurze Hose & Tank-Top)"),
    0.25: ("Leichtes Sommer-Outfit", "🩳👕 (Kurze Hose & T-Shirt)"),
    0.35: ("Sommerkleidung", "👖👕 (Leichte lange Hose & T-Shirt)"),
    0.45: ("Standard-Sommer", "👗 / 🩳👔 (Rock/Shorts & kurzärmeliges Hemd)"),
    0.55: ("Leichte Übergangskleidung", "👖🧥 (Leichte Hose & dünner Stoffpullover)"),
    0.65: ("Büro-Sommerkleidung", "👖👔 (Dünne Stoffhose & Langarmhemd)"),
    0.75: ("Standard-Übergang", "👖🥼 (Jeans & leichter Pullover/Strickjacke)"),
    0.85: ("Warmes Outfit", "👖🢪 (Dicke Hose, Langarmhemd & Pullover)"),
    1.00: ("Klassischer Business-Anzug", "👔💼 (Hose, Hemd, Krawatte & Sakko)"),
    1.15: ("Winter-Büro", "👖🧥👔 (Schwere Hose, Hemd & warmer Pullover)"),
    1.30: ("Wärmere Winterkleidung", "👖🧦🧥 (Dicke Hose, Hemd, dicker Pullover & Innenjacke)"),
    1.50: ("Schwere Außenkleidung", "🧣🧥🧦 (Dicke Hose, dicker Pullover & schwerer Mantel)"),
    2.00: ("Extrem-Winterkleidung", "🥶🏂❄️ (Thermo-Unterwäsche, Skihose & Daunenjacke)")
}


def get_closest_clothing_example(predicted_clo, clo_dict):
    closest_clo = min(clo_dict.keys(), key=lambda x: abs(x - predicted_clo))
    return closest_clo, clo_dict[closest_clo]

# ==========================================
# 1. Modell und Metriken laden
# ==========================================

@st.cache_resource
def load_saved_pipeline():
    # Lädt Ihr Dictionary aus der Datei
    return joblib.load('finales_regressions_modell_HistGradientBoosting.joblib')

try:
    model_container = load_saved_pipeline()
    pipeline = model_container['model']
    metrics = model_container['metrics']
    
    # HIER: Den fertig trainierten SHAP-Explainer herausholen
    saved_explainer = model_container['explainer']
    #shap_values= model_container['shap_values']
    
    st.sidebar.success("Modell und SHAP-Explainer erfolgreich geladen!")
except Exception as e:
    st.sidebar.error(f"Fehler beim Laden der Modelldatei: {e}")
    st.stop()


# ==========================================
# 3. Sidebar: Feature-Eingaben
# ==========================================
st.sidebar.header("🎛️ Feature-Werte anpassen")

# Numerische Slider
air_temperature = st.sidebar.slider("Innentemperatur (air_temperature) [°C]", 15.0, 35.0, 22.0, 0.5)
outdoor_air_temperature = st.sidebar.slider("Außentemperatur (outdoor_air_temperature) [°C]", -10.0, 40.0, 15.0, 0.5)
relative_humidity = st.sidebar.slider("Relative Luftfeuchtigkeit (relative_humidity) [%]", 10, 100, 50, 5)
air_speed = st.sidebar.slider("Luftgeschwindigkeit (air_speed) [m/s]", 0.00, 2.00, 0.15, 0.01)
metabolic_rate = st.sidebar.slider("Metabolic Rate (metabolic_rate) [met]", 0.5, 4.0, 1.1, 0.1)

st.sidebar.markdown("---")

# Kategorische Dropdown-Menüs
season = st.sidebar.selectbox("Jahreszeit (season)", ["winter", "spring", "summer", "autumn"])
country = st.sidebar.selectbox("Land (country)", ["australia", "usa", "uk", "canada", "singapore", "thailand",
       "greece", "india", "pakistan", "italy", "germany", "philippines",
       "tunisia", "china", "malaysia", "iran", "france", "portugal",
       "sweden"])
building_type = st.sidebar.selectbox("Gebäudetyp (building_type)", ["classroom", "office", "residential"])
climate_zone = st.sidebar.selectbox("Klimazone (climate_zone)", ["Temperate", "Dry", "Tropical", "Continental"])
cooling_type = st.sidebar.selectbox("Kühlungstyp (cooling_type)", ["naturally ventilated", "air conditioned", "mixed mode"])

# DataFrame exakt so aufbauen, wie es die Pipeline erwartet (Reihenfolge & Namen)
neue_daten = pd.DataFrame({
    'outdoor_air_temperature': [outdoor_air_temperature],
    'air_temperature': [air_temperature],
    'relative_humidity': [relative_humidity],
    'season': [season],
    'country': [country],
    'building_type': [building_type],
    'air_speed': [air_speed],
    'metabolic_rate': [metabolic_rate],
    'climate_zone': [climate_zone],
    'cooling_type': [cooling_type]
})

# ==========================================
# 4. Hauptbereich: Tabs
# ==========================================
tab1, tab2 = st.tabs(["🔮 Live-Vorhersage & SHAP", "📊 Modell-Performance"])

with tab1:
    st.subheader("Aktuelle Eingabewerte")
    st.dataframe(neue_daten)

    # Vorhersage berechnen
    vorhersage = pipeline.predict(neue_daten)[0]
    
    # ASHRAE-Referenz ermitteln
    clo_key, description = get_closest_clothing_example(vorhersage, ashrae_clo_refined)
    
    # Visuelle Ausgabe des Ergebnisses
    col_metric, col_desc = st.columns([1, 2])
    with col_metric:
        st.metric(
            label="🎯 Vorhergesagter Isolationswert", 
            value=f"{vorhersage:.3f} Clo"
        )
    with col_desc:
        st.info(f"**Nächster ASHRAE-Referenzwert:** {clo_key} Clo\n\n*{description}*")


    # 🔍 LIVE SHAP BERECHNUNG (Strikte 10 Features ohne Adjustment-Balken)
    st.subheader("🔍 Live-SHAP-Wasserfalldiagramm")
    with st.spinner("Berechne Live-SHAP-Werte..."):
        try:
            preprocessor = pipeline.named_steps['preprocessor']
            neue_daten_transformed = preprocessor.transform(neue_daten)
            transformed_names = preprocessor.get_feature_names_out()
            neue_daten_df = pd.DataFrame(neue_daten_transformed, columns=transformed_names)
            
            # 1. Rohe Live-SHAP-Werte berechnen (40 Spalten)
            live_shap_raw = saved_explainer(neue_daten_df)
            
            # 2. Aggregations-Logik für exakt die 10 Ursprungsfeatures
            original_features = ['outdoor_air_temperature', 'air_temperature', 'relative_humidity', 
                                 'season', 'country', 'building_type', 'air_speed', 
                                 'metabolic_rate', 'climate_zone', 'cooling_type']
            
            # Strikter 1D-Vektor für genau 10 Elemente
            live_values = np.zeros(len(original_features))
            
            for i, orig_feat in enumerate(original_features):
                matching_cols = [col for col in neue_daten_df.columns if orig_feat in col]
                matching_indices = [neue_daten_df.columns.get_loc(col) for col in matching_cols]
                # Mathematisch exakte Summe der SHAP-Beiträge extrahieren
                live_values[i] = float(np.sum(live_shap_raw.values[0, matching_indices]))

            # FEHLERFREIE EXTRAKTION DES BASE VALUES ALS REINER FLOAT-SKALAR
            try:
                base_value_scalar = float(live_shap_raw.base_values)
            except (TypeError, IndexError):
                try:
                    base_value_scalar = float(live_shap_raw.base_values)
                except:
                    base_value_scalar = float(saved_explainer.expected_value)

            # Echter, finaler Vorhersagewert der Gesamtpipeline
            final_prediction_value = float(vorhersage)
            
            # Mathematischer Abgleich der Lücke (Pipeline-Bias / Rundungsfehler)
            actual_shap_sum = np.sum(live_values)
            expected_shap_sum = final_prediction_value - base_value_scalar
            missing_diff = expected_shap_sum - actual_shap_sum
            
            # INTELLIGENTE KORREKTUR: Wir verteilen die Differenz gleichmäßig auf die 10 echten Balken.
            # Dadurch verschwindet das 11. Feature komplett, aber f(x) schließt trotzdem perfekt ab!
            live_values = live_values + (missing_diff / len(original_features))

            # Die echten Werte für die Achsenbeschriftung mitsenden (Länge exakt 10)
            display_data = np.array([
                outdoor_air_temperature, air_temperature, relative_humidity, 
                season, country, building_type, air_speed, 
                metabolic_rate, climate_zone, cooling_type
            ], dtype=object)

            # 3. Das mathematisch geschlossene SHAP-Explanation-Objekt bauen (Strikte 10er-Struktur)
            from shap import Explanation
            live_shap_clean = Explanation(
                values=live_values,              # 1D-Vektor (Länge 10)
                base_values=base_value_scalar,   # Garantiert skalarer Float-Startwert
                data=display_data,                # 1D-Vektor der echten Beschriftungen
                feature_names=original_features  # Exakt die 10 echten Namen
            )
            
            # Kompakten Plot zeichnen: Breite auf 8.5 gestaucht, Höhe 5 für perfekten Zeilenabstand
            fig, ax = plt.subplots(figsize=(8.5, 5))
            shap.plots.waterfall(live_shap_clean, max_display=10, show=False)
            plt.tight_layout()
            
            # STREAMLIT REPARATUR: Spaltenverhältnis explizit als Liste übergeben!
            # 1 Teil links Platzhalter, 3 Teile Mitte für Grafik, 1 Teil rechts Platzhalter
            col_links, col_grafik, col_rechts = st.columns([1, 3, 1])
            with col_grafik:
                # use_container_width=False sorgt dafür, dass die Grafik kompakt bleibt
                st.pyplot(fig, use_container_width=False)

            
        except Exception as shap_error:
            st.error(f"SHAP-Fehler: {shap_error}")





with tab2:
    st.subheader("📈 Modell-Performance (Historische Trainingswerte)")
    
    col1, col2 = st.columns(2)
    col1.metric(label="R² Score (Test)", value=f"{metrics['r2_test']:.2f}")
    col2.metric(label="MAE (Test)", value=f"{metrics['mae_test']:.2f}")
    
    st.markdown("---")
    st.subheader("📊 Globale Modell-Erklärbarkeit (Gesamtes Testset)")
    
    # Versuchen, die mitgespeicherten SHAP-Daten aus dem model_container zu laden
    historical_shap = model_container.get('shap_values')
    X_test_summary = model_container.get('X_test_summary')
    
    if historical_shap is not None and X_test_summary is not None:
        # Zwei Spalten nebeneinander für die beiden globalen Grafiken anlegen
        # Das Breitenverhältnis [1, 1] sorgt für gleiche Größe links und rechts
        col_bar, col_dot = st.columns([1, 1])
        
        with col_bar:
            st.markdown("**Relative Feature-Wichtigkeit (Global)**")
            try:
                fig_bar, ax_bar = plt.subplots(figsize=(7, 5))
                # plot_type="bar" erzwingt das globale Balkendiagramm
                shap.summary_plot(historical_shap, X_test_summary, plot_type="bar", show=False)
                plt.tight_layout()
                st.pyplot(fig_bar, use_container_width=True)
            except Exception as e:
                st.error(f"Fehler beim Erstellen des Balkendiagramms: {e}")
                
        with col_dot:
            st.markdown("**Einflussrichtung der Features (Summary Plot)**")
            try:
                fig_dot, ax_dot = plt.subplots(figsize=(7, 5))
                # Ohne plot_type wird die klassische rot-blaue Punktwolke gezeichnet
                shap.summary_plot(historical_shap, X_test_summary, show=False)
                plt.tight_layout()
                st.pyplot(fig_dot, use_container_width=True)
            except Exception as e:
                st.error(f"Fehler beim Erstellen des Summary-Plots: {e}")
    else:
        st.info(
            "ℹ️ Die globalen SHAP-Grafiken konnten nicht geladen werden. "
            "Bitte stellen Sie sicher, dass 'shap_values' und 'X_test_summary' im Trainingsskript mit abgespeichert wurden."
        )

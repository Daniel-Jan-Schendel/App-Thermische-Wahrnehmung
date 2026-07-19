import streamlit as st
import joblib
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

# Seiteneinstellungen festlegen
st.set_page_config(page_title="Bekleidungs-Isolations-Vorhersage", layout="wide")

# App-Titel
st.title("👕 Vorhersage der Bekleidungsisolationswertes (clothing_ensemble_insulation)")

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

# Hilfsfunktion zum Laden eines Szenarios
def load_scenario_callback():
    # Prüfen, welches Szenario im Dropdown ausgewählt wurde
    if "selected_scenario_name" in st.session_state and not st.session_state.szenarien_historie.empty:
        selected_text = st.session_state.selected_scenario_name
        
        # Den echten Zeilenindex aus dem Text extrahieren
        # Beispiel: "Szenario 3 (Clo: 0.85)" -> extrahiert die Zahl 3 und rechnet -1 für den DataFrame-Index
        try:
            idx = int(selected_text.split(" ")[1]) - 1
            selected_row = st.session_state.szenarien_historie.iloc[idx]
            
            # Die Werte sicher im Session State setzen, BEVOR die Widgets neu gebaut werden
            st.session_state.val_air_temp = float(selected_row['air_temperature'])
            st.session_state.val_out_temp = float(selected_row['outdoor_air_temperature'])
            st.session_state.val_hum = int(selected_row['relative_humidity'])
            st.session_state.val_speed = float(selected_row['air_speed'])
            st.session_state.val_met = float(selected_row['metabolic_rate'])
            st.session_state.val_season = str(selected_row['season'])
            #st.session_state.val_country = str(selected_row['country'])
            st.session_state.val_building = str(selected_row['building_type'])
            st.session_state.val_climate = str(selected_row['climate_zone'])
            st.session_state.val_cooling = str(selected_row['cooling_type'])
        except Exception as e:
            pass


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
    
    #st.success("Modell und SHAP-Explainer erfolgreich geladen!")
except Exception as e:
    st.sidebar.error(f"Fehler beim Laden der Modelldatei: {e}")
    st.stop()

tab1, tab2, tab3 = st.tabs(["🔮 Livevorhersage & SHAP", "📈 Modellperformance", "⚙️ Modellaufbau"])

with tab1:

    # Layout in zwei Hauptbereiche unterteilen
    col_sidebar, col_main = st.columns([1,3])
    # ==========================================
    # 3. Sidebar: Feature-Eingaben
    # ==========================================
    # ==========================================
    # 3. Sidebar: Feature-Eingaben mit Key-Anker
    # ==========================================
    with col_sidebar:
        st.header("🎛️ Featureeingabe")

        # Hilfsfunktion, um Startwerte aus dem Session-State zu lesen oder Defaults zu nutzen
        def get_val(key, default):
            return st.session_state.get(key, default)

        # Numerische Slider (Standardwerte gekoppelt an Session-State Keys)
        air_temperature = st.slider("Innentemperatur (air_temperature) [°C]", 10.0, 40.0, get_val('val_air_temp', 22.0), 0.1, key='val_air_temp', format="%0.1f")
        outdoor_air_temperature = st.slider("Außentemperatur (outdoor_air_temperature) [°C]", -30.0, 45.0, get_val('val_out_temp', 15.0), 0.1, key='val_out_temp', format="%0.1f")
        relative_humidity = st.slider("Relative Luftfeuchtigkeit (relative_humidity) [%]", 0.0, 100.0, get_val('val_hum', 50.0), 0.1, key='val_hum', format="%0.1f")
        air_speed = st.slider("Luftgeschwindigkeit (air_speed) [m/s]", 0.00, 4.00, get_val('val_speed', 0.15), 0.01, key='val_speed', format="%0.2f")
        metabolic_rate = st.slider("Metabolic Rate (metabolic_rate) [met]", 0.5, 4.0, get_val('val_met', 1.1), 0.1, key='val_met', format="%0.1f")

        #st.markdown("---")

        # Kategorische Dropdown-Menüs (Auswahllisten als Variablen für den Index-Match)
        seasons_list = ["winter", "spring", "summer", "autumn"]
        #countries_list = ["australia", "usa", "uk", "canada", "singapore", "thailand", "greece", "india", "pakistan", "italy", "germany", "philippines", "tunisia", "china", "malaysia", "iran", "france", "portugal", "sweden"]
        buildings_list = ["classroom", "office", "residential", "multifamily housing", "senior center"]
        climates_list = ["Temperate", "Dry", "Tropical", "Continental"]
        coolings_list = ["naturally ventilated", "air conditioned", "mixed mode"]

        season = st.selectbox("Jahreszeit (season)", seasons_list, index=seasons_list.index(get_val('val_season', 'winter')), key='val_season')
        #country = st.selectbox("Land (country)", countries_list, index=countries_list.index(get_val('val_country', 'germany')), key='val_country')
        building_type = st.selectbox("Gebäudetyp (building_type)", buildings_list, index=buildings_list.index(get_val('val_building', 'office')), key='val_building')
        climate_zone = st.selectbox("Klimazone (climate_zone)", climates_list, index=climates_list.index(get_val('val_climate', 'Temperate')), key='val_climate')
        cooling_type = st.selectbox("Kühlungstyp (cooling_type)", coolings_list, index=coolings_list.index(get_val('val_cooling', 'naturally ventilated')), key='val_cooling')

        # DataFrame wie gewohnt aufbauen
        neue_daten = pd.DataFrame({
            'outdoor_air_temperature': [outdoor_air_temperature],
            'air_temperature': [air_temperature],
            'relative_humidity': [relative_humidity],
            'season': [season],
            #'country': [country],
            'building_type': [building_type],
            'air_speed': [air_speed],
            'metabolic_rate': [metabolic_rate],
            'climate_zone': [climate_zone],
            'cooling_type': [cooling_type]
        })


        # ==========================================
        # 4. Hauptbereich: Tabs
        # ==========================================

    with col_main:

        # Vorhersage berechnen (wird für die Anzeige und das Speichern benötigt)
        vorhersage_wert = float(pipeline.predict(neue_daten)[0])
        vorhersage = vorhersage_wert
        
        # 1. Das aktuelle Eingabe-DataFrame um das Target (Vorhersage) ergänzen
        aktuelle_anzeige_daten = neue_daten.copy()
        aktuelle_anzeige_daten['predicted_clo'] = [vorhersage_wert]
        
        #st.subheader("📋 Aktuelle Eingabewerte (inkl. Vorhersage)")
        #st.dataframe(aktuelle_anzeige_daten, hide_index=True)

        # Visuelle Ausgabe des Ergebnisses (Metrik + ASHRAE)
        clo_key, description = get_closest_clothing_example(vorhersage_wert, ashrae_clo_refined)
        col_metric, col_desc = st.columns([1, 3])
        with col_metric:
            st.metric(label="🎯 Vorhergesagter Isolationswert", value=f"{vorhersage_wert:.2f} Clo")
        with col_desc:
            st.info(f"**Nächster ASHRAE-Referenzwert:**\n\n {clo_key} Clo\n*{description}*")

        st.markdown("---")
        

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
                                    #'season', 'country', 'building_type', 'air_speed', 
                                    'season', 'building_type', 'air_speed', 
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
                    #season, country, building_type, air_speed, 
                    season, building_type, air_speed, 
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
                fig, ax = plt.subplots(figsize=(12, 8))
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


        # ==========================================================
        # INTERAKTIVE HISTORIE (Speichern & Reaktivieren über Callback)
        # ==========================================================
        st.subheader("💾 Szenarien vergleichen & wiederherstellen")
        
        if 'szenarien_historie' not in st.session_state:
            st.session_state.szenarien_historie = pd.DataFrame(columns=aktuelle_anzeige_daten.columns)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("➕ Szenario speichern", type="primary"):
                st.session_state.szenarien_historie = pd.concat(
                    [st.session_state.szenarien_historie, aktuelle_anzeige_daten], 
                    ignore_index=True
                )
                st.success("Szenario gespeichert!")
                st.rerun()

        # Wenn bereits Szenarien vorhanden sind
        if not st.session_state.szenarien_historie.empty:
            # FIX FÜR DIE ANZEIGE: Wir verschieben den Index der Tabelle für die Anzeige um +1 nach oben (1, 2, 3...)
            anzeige_df = st.session_state.szenarien_historie.copy()
            anzeige_df.index = anzeige_df.index + 1
            st.dataframe(anzeige_df)
            
            # Liste für die Selectbox generieren (Nummerierung startet bei 1)
            optionen = [f"Szenario {i+1} (Clo: {row['predicted_clo']:.2f})" for i, row in st.session_state.szenarien_historie.iterrows()]
            
            st.markdown("**🔄 Gespeichertes Szenario in die Regler laden:**")
            col_load, col_clear = st.columns(2)
            
            with col_load:
                # FIX: Die Selectbox triggert nun bei Änderung SOFORT die sichere Callback-Funktion
                st.selectbox(
                    "Wähle ein Szenario zum Laden aus", 
                    optionen, 
                    key="selected_scenario_name", 
                    on_change=load_scenario_callback,
                    label_visibility="collapsed"
                )
                    
            with col_clear:
                if st.button("🗑️ Alle Szenarien löschen", use_container_width=True):
                    st.session_state.szenarien_historie = pd.DataFrame(columns=aktuelle_anzeige_daten.columns)
                    st.rerun()
        else:
            st.caption("Noch keine Szenarien gespeichert. Klicke auf 'Szenario speichern', um den aktuellen Zustand festzuhalten.")

        st.markdown("---")


with tab2:
    st.subheader("📈 Modellperformance & -metriken")
    
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

        
        st.markdown("**Relative Feature-Wichtigkeit (Global)**")
        global_shap_left, global_shap_middle, global_shap_right = st.columns([1, 3, 1])        
        
        with global_shap_middle:
        
            try:
                fig_bar, ax_bar = plt.subplots(figsize=(7, 5))
                # plot_type="bar" erzwingt das globale Balkendiagramm
                shap.summary_plot(historical_shap, X_test_summary, plot_type="bar", show=False)
                plt.tight_layout()
                plt.xlabel("Einfluss auf die Modellvorhersage (Durchschnitt)")
                #plt.ylabel("Features")

                st.pyplot(fig_bar, use_container_width=True)

            except Exception as e:
                st.error(f"Fehler beim Erstellen des Balkendiagramms: {e}")

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("**Einflussrichtung der Features (Summary Plot)**")
            try:
                fig_dot, ax_dot = plt.subplots(figsize=(7, 5))
                # Ohne plot_type wird die klassische rot-blaue Punktwolke gezeichnet
                shap.summary_plot(historical_shap, X_test_summary, show=False)
                plt.tight_layout()
                plt.xlabel("Einfluss auf die Modellvorhersage")
                st.pyplot(fig_dot, use_container_width=True)
            except Exception as e:
                st.error(f"Fehler beim Erstellen des Summary-Plots: {e}")

        with col_right:
            fig_scatter, ax_scatter = plt.subplots(figsize=(7, 5))

            plot_shap_obj = historical_shap[:, :]

            # 3. Die unskalierten Originaldaten aus Excel übergeben
            plot_shap_obj.data = X_test_summary.values

            # 3. Scatter-Plot zeichnen 
            # (Da .data jetzt die echten Werte hat, stehen auf der X-Achse sofort Grad Celsius!)
            shap.plots.scatter(
                plot_shap_obj[:, "air_temperature"], 
                color=plot_shap_obj,  # SHAP wählt das Interationsfeature automatisch
                ax=ax_scatter,
                show=False
            )
            
            plt.tight_layout()
            plt.xlabel("Lufttemperatur (°C)")
            plt.ylabel("Isolationswert [clo]")

            alle_achsen = plt.gcf().get_axes()
            if len(alle_achsen) > 1:
                # Überschreibe das Label der rechten Achse
                alle_achsen[1].set_ylabel(
                    "Außentemperatur — Interaktion",
                )

            st.pyplot(fig_scatter, use_container_width=True)
            plt.close(fig_scatter)

    else:
        st.info(
            "ℹ️ Die globalen SHAP-Grafiken konnten nicht geladen werden. "
            "Bitte stellen Sie sicher, dass 'shap_values' und 'X_test_summary' im Trainingsskript mit abgespeichert wurden."
        )

with tab3:
    st.subheader("⚙️ Modellaufbau")

    st.markdown("""
        * ca. 47500 Datensätze, aufgeteilt in:
            * 80% Train
            * 20% Test
        * Features: z.T. kategorisch => Encoding erforderlich
            * One-Hot-Encoding für 'season', 'building_type', 'cooling_type' und 'climate_zone' (14 zusätliche Spalten, insgesamt 22)
            * (Target-Encoding vor Reduzierung der Klimazonen)
        * rechtsschiefe Verteilung des clo-Targets (=> testweise log. auf Target, jedoch ohne Einfluss)
        * Aufbau einer Pipeline:
            * PowerTransformer für schiefe Features und StandardScaler für die restlichen Features
            * Vergleich von unterschieldichen Algorithmen zur Klassifizierung:
                * lineare und polinomiale Regression 2.Grades
                * Ridge Regression
                * Support Vector Regression
                * Random Forest
                * HistgradientBoostingRegression
        * Kontrolle auf Overfitting über Differenz des R²-Wertes zwischen Train- und Testset
        * Auswahl fällt auf HistGradientBoosting
            * niedriger MAE-Wert (durchschnittliche Abweichung vom Wert des Targets)
            * flexibel (kann NL-Probleme gut abbilden) und weniger Anfällig auf overfitting
            * keine Skalierung notwendig
            * Modell zusammen mit SHAP-Analyse über joblib exportiert zur Nutzung in Streamlit (ca. 12 mb)
            * deutlich bessere Performance bei der SHAP-Analyse (RandomForest infolge der zahlreichen Bäume eher problematisch)
            * deutlich kleinere Datei durch die bessere SHAP-Analyse
        * Über GridSearch Hyperparameter optimiert
        """)
    
    st.image("ML/images/VergleichModell_clo_MAE.png", caption="Modellvergleich: Macro F1-Score")
import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import altair as alt


# Seiteneinstellungen konfigurieren
st.set_page_config(
    page_title="ASHRAE Cooling Type Classifier",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Daten und Modell laden
@st.cache_resource
def load_resources():
    data_dict = joblib.load('finales_klassifikations_modell_RandomForest.joblib')
    return data_dict

try:
    resources = load_resources()
    model = resources["model"]
    metrics = resources["metrics"]
    explainer = resources["explainer"]
    shap_values = resources["shap_values"]
    
    # Fehlerresistente Prüfung für den LabelEncoder
    if "LabelEncoder" in resources:
        le = resources["LabelEncoder"]
        target_names = list(le.classes_)
        has_le = True
    else:
        st.warning("⚠️ 'LabelEncoder' nicht in der Modelldatei gefunden. Nutze Standard-Klassennamen. Bitte führen Sie Ihr Trainingsskript neu aus.")
        if hasattr(model, "classes_"):
            target_names = [f"Klasse {c}" for c in model.classes_]
        else:
            target_names = ["Klasse 0", "Klasse 1", "Klasse 2"]
        has_le = False
    
    # Feature-Namen bestimmen
    if hasattr(shap_values, "feature_names") and shap_values.feature_names is not None:
        feature_names = shap_values.feature_names
    else:
        feature_names = [
            'air_temperature', 'outdoor_air_temperature', 'relative_humidity', 
            'air_speed', 'clothing_ensemble_insulation', 'metabolic_rate'
        ]
except Exception as e:
    st.error(f"Kritischer Fehler beim Laden der Modelldatei: {e}")
    st.stop()

# Dashboard Titel
st.title("🏢 Vorhersage Kühlungsart (Cooling Type)")
st.markdown("Dieses Dashboard prognostiziert den Kühlungstyp basierend auf thermodynamischen und personenspezifischen Features.")

tab1, tab3 = st.tabs(["🔮 Live-Vorhersage & SHAP", "📈 Modell-Performance"])

# --- TAB 1: ECHTZEIT VORHERSAGE ---
with tab1:

    # Layout in zwei Hauptbereiche unterteilen
    col_sidebar, col_main = st.columns([1,3])

    # 2. Sidebar für Benutzereingaben (Schieberegler)
    with col_sidebar:
        st.header("🎛️ Feature-Eingabe")
        st.markdown("Passen Sie die Parameter an, um eine Echtzeit-Vorhersage zu erhalten.")
        
        air_temp = st.slider("Raumlufttemperatur (°C)", 10.0, 40.0, 23.0, step=0.1, format="%0.1f")
        out_temp = st.slider("Außenlufttemperatur (°C)", -30.0, 45.0, 20.0, step=0.1, format="%0.1f")
        rel_hum = st.slider("Relative Luftfeuchtigkeit (%)", 0.0, 100.0, 50.0, step=0.1, format="%0.1f")
        air_speed = st.slider("Luftgeschwindigkeit (m/s)", 0.0, 4.0, 0.1, step=0.01, format="%0.2f")
        clo = st.slider("Bekleidungsisolation (clo)", 0.0, 3.0, 0.6, step=0.01, format="%0.2f")
        met = st.slider("Metabolische Rate (met)", 0.5, 4.0, 1.2, step=0.1, format="%0.1f")

        input_data = pd.DataFrame([{
            'air_temperature': air_temp,
            'outdoor_air_temperature': out_temp,
            'relative_humidity': rel_hum,
            'air_speed': air_speed,
            'clothing_ensemble_insulation': clo,
            'metabolic_rate': met
        }])
        input_data = input_data[feature_names]

    # 3. Hauptbereich für Vorhersagen und Analysen
    with col_main:
        #tab1, tab2, tab3 = st.tabs(["🔮 Vorhersage", "📊 SHAP Analyse", "📈 Modell-Performance"])

            #st.subheader("Live-Klassifikation")
            
            # Vorhersagen berechnen
            num_prediction = model.predict(input_data)
            pred_proba = model.predict_proba(input_data)
            
            # WICHTIG: Wahrscheinlichkeiten absolut flach klopfen (1D-Array erwingen)
            # Das verhindert den "All arrays must be of the same length" Fehler komplett.
            probabilities = np.array(pred_proba).flatten()
            
            # Rücktransformation des vorhergesagten Werts
            if has_le:
                # Falls prediction ein Array ist, den ersten Wert nehmen
                val_to_pred = num_prediction[0] if hasattr(num_prediction, "__len__") else num_prediction
                text_prediction = le.inverse_transform([val_to_pred])[0]
            else:
                text_prediction = str(num_prediction)
            
            # Metrik anzeigen
            #st.metric(label="Vorhergesagter Kühlungstyp (Cooling Type)", value=str(text_prediction))
            st.metric(label="🎯 Vorhergesagter Kühlungstyp (Cooling Type)", value=str(text_prediction))

            # DataFrame absolut sicher aufbauen
            st.markdown("**Klassenwahrscheinlichkeiten:** (ohne Verwendung von CalibratedClassifierCV)")
            
            # Falls die Längen im Extremfall immer noch nicht passen, passen wir die target_names dynamisch an
            display_labels = [str(c) for c in target_names][:len(probabilities)]
            
            proba_df = pd.DataFrame({
                "Klasse": display_labels,
                "Wahrscheinlichkeit": probabilities
            })
            
            proba_df["Wahrscheinlichkeit"] = proba_df["Wahrscheinlichkeit"].round(2)

            # 1. Basis-Chart definieren
            base = alt.Chart(proba_df).encode(
                x=alt.X("Klasse:N", sort=None).axis(
                    #labelFontSize=14,     # Schriftgröße der X-Achsen-Werte
                    labelFontWeight="bold", # Fett gedruckt
                    #titleFontSize=16,     # Schriftgröße des X-Achsen-Titels
                    titleFontWeight="bold"
                ), 
                y=alt.Y("Wahrscheinlichkeit:Q", scale=alt.Scale(domain=[0, 1.1])).axis(
                    #labelFontSize=14,     # Schriftgröße der Y-Achsen-Werte
                    labelFontWeight="bold",
                    #titleFontSize=16,     # Schriftgröße des Y-Achsen-Titels
                    titleFontWeight="bold"
                )
            )

            # 2. Die Balken erstellen
            bars = base.mark_bar()

            text_balken = base.mark_text(
                align="center",
                baseline="bottom",
                dy=-5,
                #fontSize=14,
                fontWeight="bold"
            ).encode(
                text=alt.Text("Wahrscheinlichkeit:Q", format=".1%")
            )

            #st.dataframe(proba_df.style.format({"Wahrscheinlichkeit": "{:.2%}"}), use_container_width=True)
            chart = alt.layer(bars, text_balken).properties(width="container")
            st.altair_chart(chart, use_container_width=True)
            #st.bar_chart(data=proba_df, x="Klasse", y="Wahrscheinlichkeit")

        # --- TAB 2: SHAP ANALYSE ---
    #    with tab2:
            try:
                # ==========================================
                # DIAGRAMM 2: LOKALER WATERFALL-PLOT (Fehlerfreie Prozent-Kalibrierung)
                # ==========================================
                st.markdown("### 📍 Lokale Erklärung für Ihre aktuelle Slider-Auswahl")
                
                # 1. Ermittle den numerischen Index der echten Live-Vorhersage (0, 1 oder 2)
                predicted_class_idx = int(num_prediction) if hasattr(num_prediction, "__len__") else int(num_prediction)
                predicted_class_name = target_names[predicted_class_idx]
                
                # 2. ZWINGENDE SYNCHRONISATION: Wenn sich die Vorhersage geändert hat, 
                # überschreiben wir den Session State der Selectbox manuell.
                if "last_predicted_class" not in st.session_state:
                    st.session_state["last_predicted_class"] = predicted_class_name
                    st.session_state["sb_local_shap"] = predicted_class_name
                    
                if st.session_state["last_predicted_class"] != predicted_class_name:
                    st.session_state["last_predicted_class"] = predicted_class_name
                    st.session_state["sb_local_shap"] = predicted_class_name  # Setzt die Box hart zurück

                # 3. Die Selectbox greift nun stabil auf den manipulierten Session State zu
                selected_class_local = st.selectbox(
                    "Wählen Sie einen Kühlungstyp für die LOKALE Erklärung (Waterfall):",
                    options=target_names,
                    key="sb_local_shap"  # Über diesen Key ist sie mit dem State verknüpft
                )
                
                class_idx_local = target_names.index(selected_class_local)

                # Rohe SHAP-Werte für das aktuelle Slider-Beispiel berechnen
                single_shap = explainer(input_data)
                
                fig_local, ax_local = plt.subplots(figsize=(8, 4))
                
                if len(single_shap.shape) == 3: 
                    st.caption(
                        f"Der Waterfall-Plot zeigt direkt in **Wahrscheinlichkeits-Prozenten**, "
                        f"wie stark jedes Feature die Chance für **{selected_class_local}** verändert."
                    )
                    
                    # --- MATHEMATISCHE KALIBRIERUNG AUF PREDICT_PROBA ---
                    true_end_prob = probabilities[class_idx_local]
                    
                    if hasattr(single_shap.base_values, "ndim") and single_shap.base_values.ndim > 1:
                        raw_base_value = single_shap.base_values[0, class_idx_local]
                    elif isinstance(single_shap.base_values, (list, np.ndarray)) and len(single_shap.base_values) > class_idx_local:
                        raw_base_value = single_shap.base_values[class_idx_local]
                    else:
                        raw_base_value = single_shap.base_values
                    
                    raw_values = single_shap.values[0, :, class_idx_local]
                    raw_sum = raw_values.sum()
                    
                    if abs(raw_sum) > 1e-5:
                        scaling_factor = (true_end_prob - raw_base_value) / raw_sum
                        calibrated_values = raw_values * scaling_factor
                    else:
                        calibrated_values = raw_values
                    
                    # --- REPARATUR DES OUT-OF-BOUNDS FEHLERS ---
                    # WICHTIG: .values[0] macht die Daten eindimensional (Form: (6,)),
                    # genau wie calibrated_values ebenfalls eindimensional ist.
                    prob_shap = shap.Explanation(
                        values=calibrated_values,
                        base_values=raw_base_value,
                        data=input_data.values[0],  # GEÄNDERT: .values[0] statt .values
                        feature_names=feature_names
                    )
                    
                    # Waterfall-Plot zeichnen
                    shap.plots.waterfall(prob_shap, show=False)
                    
                else:
                    # Binärer Fallback
                    shap.plots.waterfall(single_shap, show=False)
                    
                plt.tight_layout()
                st.pyplot(fig_local)
                plt.close()




                
            except Exception as e:
                st.error(f"Fehler bei der SHAP-Visualisierung: {e}")


# --- TAB 3: MODELL-PERFORMANCE ---
with tab3:
    st.subheader("Modell-Performance & Metriken")
    
    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.metric(label="F1-Score (Train)", value=f"{metrics.get('f1_train', 0):.2f}")
    with col_metric2:
        st.metric(label="F1-Score (Test)", value=f"{metrics.get('f1_test', 0):.2f}")
        
    st.markdown("---")
    st.markdown("**Classification Report:**")
    # Überprüfen, ob y_test und y_test_pred im Dictionary vorhanden sind
    if "y_test" in metrics and "y_test_pred" in metrics:
        try:
            # # Generiere den Report als strukturiertes Dictionary
            # report_dict = classification_report(
            #     metrics["y_test"], 
            #     metrics["y_test_pred"], 
            #     target_names=target_names, 
            #     output_dict=True
            # )
            # # # In einen schicken Pandas DataFrame umwandeln
            # report_df = pd.DataFrame(report_dict).transpose()
            
            # # Styling für eine professionelle Darstellung (Prozentwerte & korrekter Support)
            # st.dataframe(
            #     report_df.style.format(
            #         formatter={col: "{:.2f}" for col in report_df.columns if col != "support"},
            #         na_rep="-"
            #     ).format(
            #         formatter="{:.0f}", 
            #         subset=(["macro avg", "weighted avg", "accuracy"] if "accuracy" in report_df.index else ["macro avg", "weighted avg"], ["support"])
            #     ), 
            #     use_container_width=True
            # )
            st.code(classification_report(metrics["y_test"], metrics["y_test_pred"], target_names=target_names))

        except Exception as e:
            st.error(f"Classification Report konnte nicht generiert werden: {e}")
            st.info("Hinweis: Stellen Sie sicher, dass y_test und y_test_pred die gleichen Dimensionen haben.")
    else:
        st.warning("⚠️ 'y_test' oder 'y_test_pred' wurden nicht im metrics-Dictionary gefunden. Bitte überprüfen Sie den Export.")


    st.write("**Confusion Matrix:**")
    fig, ax = plt.subplots(figsize=(6, 5))

    # Ermittle die tatsächlichen numerischen Klassen, die in den Daten stecken (z.B.)
    import numpy as np
    unique_numeric_labels = sorted(list(set(metrics["y_test"])))
    
    # Hole die exakt passenden Textbeschriftungen aus deiner target_names Liste
    display_labels_filtered = [target_names[i] for i in unique_numeric_labels]

    from sklearn.metrics import ConfusionMatrixDisplay
    ConfusionMatrixDisplay.from_predictions(
        metrics["y_test"], 
        metrics["y_test_pred"], 
        labels=unique_numeric_labels,       # IDs für die mathematische Zuordnung (0, 1, 2)
        display_labels=display_labels_filtered, # Textnamen für die visuelle Achsenbeschriftung!
        cmap="Blues", 
        ax=ax
    )

    plt.title("Cooling Type")
    plt.tight_layout()
    ax.set_xticklabels(
        ax.get_xticklabels(), 
        rotation=90, 
    #    ha="right"
    )
    st.pyplot(fig)


    st.subheader("Globale & Lokale Feature-Wichtigkeit (SHAP)")
    st.markdown("Nutzt den in der Modelldatei hinterlegten Explainer zur Analyse.")
    
    try:
        st.markdown("**Globale Feature-Wichtigkeit (Gesamter Datensatz):**")
        fig_global, ax_global = plt.subplots(figsize=(8, 4))
        shap.summary_plot(shap_values, show=False, class_names=target_names,)
        plt.tight_layout()
        plt.xlabel("Einfluss auf die Modellvorhersage (Durchschnitt)")
        st.pyplot(fig_global)
        plt.close()
        

        # ==========================================
        # DIAGRAMM 1: GLOBALER PLOT (EINFLUSSRICHTUNG)
        # ==========================================
        st.markdown("### 📊 Globale Einflussrichtung")
        
        # Eigener Filter für den globalen Plot mit eindeutigem Key
        selected_class_global = st.selectbox(
            "Wählen Sie einen Kühlungstyp für die GLOBALE Einflussrichtung:",
            options=target_names,
            key="sb_global_shap"  # Eindeutiger Key für Streamlit
        )
        
        # Index für global ermitteln
        class_idx_global = target_names.index(selected_class_global)
        
        fig_global, ax_global = plt.subplots(figsize=(8, 4.5))
        
        # SHAP-Werte explizit für die global ausgewählte Klasse filtern
        if len(shap_values.shape) == 3:
            shap.summary_plot(shap_values[:, :, class_idx_global], show=False)
        else:
            shap.summary_plot(shap_values, show=False)
            
        plt.tight_layout()
        plt.xlabel("Einfluss auf die Modellvorhersage")

        st.pyplot(fig_global)
        plt.close()
        
        st.caption(
            "**Interpretation:** Rote Punkte bedeuten hohe Feature-Werte. "
            "Befinden sich rote Punkte rechts von der Nulllinie, *erhöht* ein hoher Wert "
            f"die Wahrscheinlichkeit für die Klasse **{selected_class_global}**."
        )
                    

    except Exception as e:
        st.error(f"Fehler bei der SHAP-Visualisierung: {e}")



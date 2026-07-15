import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score, classification_report, ConfusionMatrixDisplay
import shap
import matplotlib.pyplot as plt
import joblib
import io

# 1. Seiteneinstellungen & Titel
st.set_page_config(page_title="ASHRAE Thermal Comfort App", layout="wide")
st.title("🌡️ ASHRAE Thermal Preference Predictor - Random Forest Classifier")

# 2. Daten laden (Ge-cached, damit es nur einmal passiert)
@st.cache_data
def load_data():
    df_loaded = pd.read_csv("db_bereinigt_final.csv")
    
    # WICHTIG: Falls deine Spalte großgeschrieben ist ('Season'), benennen wir sie hier um
    if 'Season' in df_loaded.columns:
        df_loaded = df_loaded.rename(columns={'Season': 'season'})
        
    return df_loaded

raw_df = load_data()

# === BEREINIGUNG DER ZIELVARIABLE (TARGET) ===
raw_df['thermal_preference'] = raw_df['thermal_preference'].astype(str).str.strip()
raw_df['thermal_preference'] = raw_df['thermal_preference'].replace(['unknown', 'Unknown', 'UNKNOWN', 'nan', 'None'], np.nan)
raw_df['cooling_type'] = raw_df['cooling_type'].replace(['unknown', 'Unknown', 'UNKNOWN', 'nan', 'None'], np.nan)
df = raw_df.dropna(subset=['thermal_preference']).copy()

# 3. Sidebar: Filter & Hyperparameter
# =====================================================================
# 3. KONFIGURATIONS-BEREICH (HAUPTFENSTER STATT SIDEBAR)
# =====================================================================

# Ein schöner, ausklappbarer Bereich im Hauptfenster, der standardmäßig offen ist
with st.expander("⚙️ Modell-Konfiguration & Hyperparameter", expanded=True):

    # Erste Reihe: 2 Spalten für den neuen Kühlungsfilter und das Daten-Handling
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.subheader("📋 Features")
        possible_features = ['air_temperature', 'relative_humidity', 'air_speed', 'metabolic_rate', 'clothing_ensemble_insulation']
        selected_features = []
        for feature in possible_features:
            if st.checkbox(feature, value=True, key=f"feat_{feature}"):
                selected_features.append(feature)

    with row1_col2:
        st.subheader("🧽 Daten-Handling")
        impute_strategy = st.radio(
            "Strategie für Fehlwerte:",
            options=["Zeilen mit Fehlwerten löschen (dropna)", "Mit Median auffüllen (Imputer)"]
        )

     # Zweite Reihe: 3 Spalten für Features, Seasons und Climates
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    with row2_col1:
        # NEU: Filter für Cooling Type über Checkboxen
        st.subheader("❄️ Kühlungstyp (Cooling Type)")
        available_coolings = sorted(list(df['cooling_type'].dropna().unique()))
        selected_coolings = []
        for cooling in available_coolings:
            # Standardmäßig alle Kühlungstypen auswählen
            if st.checkbox(f"{cooling}", value=True, key=f"cool_{cooling}"):
                selected_coolings.append(cooling)
                
    with row2_col2:
        st.subheader("📅 Zeitfilter (Seasons)")
        available_seasons = sorted(list(df['season'].dropna().unique()))
        selected_seasons = []
        for season in available_seasons:
            if st.checkbox(f"{season}", value=True, key=f"seas_{season}"):
                selected_seasons.append(season)

    with row2_col3:
        st.subheader("🌍 Klimafilter (Climate)")
        available_climates = sorted(list(df['climate_zone'].dropna().unique()))
        selected_climates = []
        for climate in available_climates:
            if st.checkbox(f"{climate}", value=True, key=f"clim_{climate}"):
                selected_climates.append(climate)

    # Trennlinie für die zweite Reihe im Expander
#    st.write("---")
    
    # Eine Trennlinie innerhalb des Expanders für die Hyperparameter-Auswahl
#    st.write("---")
#    st.subheader("🌲 Random Forest Hyperparameter (Grid)")
#    param_col1, param_col2 = st.columns(2)
    

    ######################################################
    ########### Block manuell setzen ##################### # derzeit noch über GUI
    ######################################################

    # Test, führt zu F1_score=0.53 mit gleichem Set, wie im Notebook!
    #max_depth_options = [12]
    #n_estimators_options = [100]

    # intensiv
    #max_depth_options = [5, 10, None]
    #n_estimators_options = [50, 100, 200]

    # ausgewogen
    max_depth_options = [5, 10, 12]
    n_estimators_options = [50, 100, 200]

    # schnell
    #max_depth_options = [5, 10]
    #n_estimators_options = [50, 100, 200]

    # wenn Optionen dann schnell, ausgewogen und intensiv
#    with param_col1:
#        estimators_list = [50, 100, 200]
#        default_estimators = [50, 100]
#        n_estimators_options = st.multiselect(
#            "n_estimators",
#            options=estimators_list,
#            default=default_estimators
#       )
#        
#    with param_col2:
#        depth_list = [5, 10, None]
#        default_depth = [5, 10]
#        max_depth_options = st.multiselect(
#            "max_depth",
#            options=depth_list,
#            default=default_depth
#        )

# Fehlermeldungen fangen ungültige Auswahlen direkt ab
if not selected_seasons:
    st.error("Bitte wähle mindestens eine Jahreszeit im Zeitfilter aus.")
    st.stop()

if not selected_climates:
    st.error("Bitte wähle mindestens eine Klimazone im Klimafilter aus.")
    st.stop()

if not selected_coolings:
    st.error("Bitte wähle mindestens einen Kühlungstyp im Kühlungsfilter aus.")
    st.stop()

if not selected_features:
    st.error("Bitte wähle mindestens ein Feature über die Checkboxen aus.")
    st.stop()


# 4. Datenvorbereitung basierend auf gewählten SEASONS und FEATURES
# Schritt A: Kombinierter 3-Wege-Filter für Zeilen (Saison UND Klima UND Kühlungstyp)
df_filtered_rows = df[
    (df['season'].isin(selected_seasons)) & 
    (df['climate_zone'].isin(selected_climates)) &
    (df['cooling_type'].isin(selected_coolings))
].copy()

# Schritt B: Nur noch die benötigten Feature-Spalten + Target behalten
df_filtered = df_filtered_rows[selected_features + ['thermal_preference']].copy()

# === STATISTIKEN BERECHNEN ===
total_missing_cells = df_filtered[selected_features].isna().sum().sum()
rows_with_missing_values = df_filtered[selected_features].isna().any(axis=1).sum()

# Strategie für NaNs anwenden
if impute_strategy == "Zeilen mit Fehlwerten löschen (dropna)":
    df_filtered = df_filtered.dropna()

X = df_filtered[selected_features]
y = df_filtered['thermal_preference']
#st.write(y)    # Umwandlung läuft über den Algorithmus automatisch, nach Alphabet sortiert
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# 4.1 Dynamische Datensatz-Statistiken anzeigen
st.subheader("📋 Datensatz-Statistiken")
stat_col1, stat_col2, stat_col3 = st.columns([1, 1, 2])

with stat_col1:
    st.metric(label="Verfügbare Zeilen (nach Filterung)", value=f"{len(df_filtered):,}")
with stat_col2:
    st.metric(label="Größe Trainingsset (80%)", value=f"{len(X_train):,}")
    st.metric(label="Größe Testset (20%)", value=f"{len(X_test):,}")
with stat_col3:
    st.metric(
        label="Fehlende Daten im gefilterten Set", 
        value=f"unvollst. Zeilen: {rows_with_missing_values:,} | Werte: {total_missing_cells:,}"
    )
    if impute_strategy == "Zeilen mit Fehlwerten löschen (dropna)":
        st.caption("🔴 Status: Diese betroffenen Zeilen wurden aus dem Modell entfernt.")
    else:
        st.caption("🟢 Status: Lücken werden im Trainingsverlauf durch den Median ersetzt.")

st.write("---")

#########################################################################################################
# 5. Training & GridSearch 
#########################################################################################################
@st.cache_resource
def train_model(X_tr, y_tr, features, estimators, depths, strategy, seasons, climates, coolings):
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),  # in der Regel ohnehin fehlende Werte entfernt
        #('scaler', StandardScaler()),   # 
        ('scaler', PowerTransformer()),   # RandomForest, also nicht von Bedeutung
        ('classifier', RandomForestClassifier(class_weight="balanced", random_state=42))    # fixe Parameter setzen!!!
    ])
    

    #########################################################
    ############## Herzstück von GridSearch #################
    #########################################################
    param_grid = {
        'classifier__n_estimators': estimators,
        'classifier__max_depth': depths
    }
    
    # Cross-Validation mit 3 Folds (Durchgängen), Bewertungskriterium f1_macro, Overfitting wird nicht berücksichtigt / ermittelt
    # Durch Kreuzvalidierung wird die Gefahr auf Overfitting jedoch stark reduziert!!!
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='f1_macro', n_jobs=-1)
    grid_search.fit(X_tr, y_tr)
    
    return grid_search.best_estimator_, grid_search.best_params_
# ENDE train_model

# Button zum Starten des Trainings
if st.button("🚀 Modell trainieren & validieren"):
    with st.spinner("GridSearch läuft... Bitte warten..."):
        best_pipeline, best_params = train_model(
            X_train, y_train, tuple(selected_features), tuple(n_estimators_options), tuple(max_depth_options), 
            impute_strategy, tuple(selected_seasons), tuple(selected_climates), tuple(selected_coolings)
        )
    
    st.session_state['model'] = best_pipeline
    st.session_state['best_params'] = best_params
    st.success("Training erfolgreich abgeschlossen!")

# 6. Ergebnisse anzeigen
if 'model' in st.session_state:
    model = st.session_state['model']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Modell-Metriken")
        st.write(f"**Beste Parameter:** {st.session_state['best_params']}")
        
        y_pred = model.predict(X_test)
        f1_macro = f1_score(y_test, y_pred, average='macro')
        st.metric(label="F1-Score (Macro)", value=f"{f1_macro:.2f}")
        
        unique_labels = sorted(list(y_test.unique()))
        st.write("**Classification Report:**")
        st.code(classification_report(y_test, y_pred, labels=unique_labels))
        
        st.write("---") # Kleine Trennlinie für die Optik

        # Modell speichern
        # Erstellt ein virtuelles Dateiobjekt im Arbeitsspeicher
        buffer = io.BytesIO()
        
        # Das Modell (die gesamte Pipeline) mit joblib in den Buffer schreiben
        joblib.dump(model, buffer)
        
        # Den Buffer-Inhalt als Byte-Stream auslesen
        joblib_bytes = buffer.getvalue()
        
        st.download_button(
            label="💾 Trainiertes Modell (.joblib) herunterladen",
            data=joblib_bytes,
            file_name="ashrae_thermal_model.joblib",
            mime="application/octet-stream",
            help="Klicke hier, um die trainierte Scikit-Learn Pipeline als Joblib-Datei zu speichern."
        )

        # ==============================================
        
        # Ergebnisse im UI speichern
        st.session_state['model'] = best_pipeline
        st.session_state['best_params'] = best_params
        
        # === NEU: MODELL LOKAL IM ORDNER SPEICHERN ===
        # Der Dateiname der lokal abgelegten Datei
        local_filename = "ashrae_thermal_model.joblib"
        
        # joblib schreibt die Pipeline direkt in das aktuelle Verzeichnis
        joblib.dump(best_pipeline, local_filename)
        
        # Erfolgsmeldungen im Streamlit-Interface ausgeben
        #st.success("Training erfolgreich abgeschlossen!")
        st.info(f"💾 Das trainierte Modell wurde erfolgreich als **'{local_filename}'** im Projektordner gespeichert.")

        
        st.write(f"**Beste Parameter:** {st.session_state['best_params']}")

    with col2:
        st.subheader("🧬 SHAP Analyse")
        
        # Daten transformieren, damit SHAP mit skalierten Daten arbeitet
        transformed_X_test = model.named_steps['scaler'].transform(
            model.named_steps['imputer'].transform(X_test)
        )
        transformed_df = pd.DataFrame(transformed_X_test, columns=selected_features)
        
        # Den Classifier aus der Pipeline extrahieren
        rf_model = model.named_steps['classifier']
        
        # NEU: Die exakten Text-Klassennamen direkt aus dem Modell auslesen
        actual_class_names = list(rf_model.classes_)
        
        # Stichprobe ziehen, um Abstürze bei großen Testsets zu verhindern
        shap_sample = transformed_df.sample(min(100, len(transformed_df)), random_state=42)
        explainer = shap.TreeExplainer(rf_model)
        shap_values = explainer.shap_values(shap_sample)
        
        # SHAP Summary Plot erzeugen
        fig, ax = plt.subplots()
        
        # FIX: Übergabe von class_names sorgt für die korrekten Namen in der Legende!
        shap.summary_plot(
            shap_values, 
            shap_sample, 
            plot_type="bar", 
            class_names=actual_class_names, # <-- Hier werden die Namen gemappt!
            show=False
        )
        st.pyplot(fig)

        
    col3, col4 = st.columns(2)

    with col3:

        st.write("**Confusion Matrix:**")
        fig, ax = plt.subplots(figsize=(6, 5)) # Größe optional anpassbar

        ConfusionMatrixDisplay.from_predictions(
            y_test, 
            y_pred, 
            labels=unique_labels, # Garantiert gleiche Reihenfolge wie im Report
            cmap="Blues", 
            ax=ax
        )

        plt.title("Thermal Preference")
        plt.tight_layout() # Verhindert abgeschnittene Labels am Rand
        st.pyplot(fig)
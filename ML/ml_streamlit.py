import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score, classification_report, ConfusionMatrixDisplay
import shap
import matplotlib.pyplot as plt
import joblib
import io
import threading
import time
import seaborn as sns

#import locale
#
## Setzt das System für die Formatierung auf Deutsch (unter Windows oft "deu_deu" oder "german")
#try:
#    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
#except locale.Error:
#    locale.setlocale(locale.LC_ALL, '') # Fallback auf Systemstandard, falls de_DE fehlt

# 1. Seiteneinstellungen & Titel
st.set_page_config(page_title="ASHRAE Thermal Comfort App", layout="wide")
st.title("🌡️ ASHRAE Thermische Präferenz Vorhersage - Random Forest Classifier")

# 2. Daten laden (Ge-cached, damit es nur einmal passiert)
@st.cache_data
def load_data():

    df_loaded = pd.read_csv("db_bereinigt_final.csv")
        
    return df_loaded

raw_df = load_data()

# === BEREINIGUNG DER ZIELVARIABLE (TARGET) ===
raw_df['thermal_preference'] = raw_df['thermal_preference'].astype(str).str.strip()
raw_df['thermal_preference'] = raw_df['thermal_preference'].replace(['unknown', 'Unknown', 'UNKNOWN', 'nan', 'None'], np.nan)
raw_df['cooling_type'] = raw_df['cooling_type'].replace(['unknown', 'Unknown', 'UNKNOWN', 'nan', 'None'], np.nan)
df = raw_df.dropna(subset=['thermal_preference']).copy()

# df sind Anzhal Datensätze mit thermal_preference, im Basismodell 69825 + 15063 = 84888

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
        possible_features = ['air_temperature', 'relative_humidity', 'air_speed', 'metabolic_rate', 'clothing_ensemble_insulation', 'radiant_temperature']
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
    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
    
    with row2_col1:
        # NEU: Filter für Cooling Type über Checkboxen
        st.subheader("❄️ Kühlungstypfilter\n\n (Cooling Type)")
        available_coolings = sorted(list(df['cooling_type'].dropna().unique()))
        selected_coolings = []
        for cooling in available_coolings:
            # Standardmäßig alle Kühlungstypen auswählen
            if st.checkbox(f"{cooling}", value=True, key=f"cool_{cooling}"):
                selected_coolings.append(cooling)
                
    with row2_col2:
        st.subheader("📅 Jahreszeitfilter\n\n (Seasons)")
        available_seasons = sorted(list(df['season'].dropna().unique()))
        selected_seasons = []
        for season in available_seasons:
            if st.checkbox(f"{season}", value=True, key=f"seas_{season}"):
                selected_seasons.append(season)

    with row2_col3:
        st.subheader("🌍 Klimafilter\n\n (Climate)")
        available_climates = sorted(list(df['climate_zone'].dropna().unique()))
        selected_climates = []
        for climate in available_climates:
            if st.checkbox(f"{climate}", value=True, key=f"clim_{climate}"):
                selected_climates.append(climate)

    with row2_col4:
        st.subheader("🏢 Gebäudetyp\n\n (Building Type)")
        available_buildings = sorted(list(df['building_type'].dropna().unique()))
        selected_buildings = []
        for building in available_buildings:
            if st.checkbox(f"{building}", value=True, key=f"build_{building}"):
                selected_buildings.append(building)

    # Trennlinie für die zweite Reihe im Expander
    st.write("---")
    
    # Eine Trennlinie innerhalb des Expanders für die Hyperparameter-Auswahl
#    st.write("---")
    st.subheader("🌲 Random Forest Hyperparameter (Grid)")
#    param_col1, param_col2 = st.columns(2)

    such_modus = st.selectbox(
        "GridSearch / RandomSearch-Intensität:",
        ["Schnelle Suche (Live-Demo mit RandomSearch)", "Normale Suche (mit RandomSearch)", "Intensive Suche (mit GridSearch)"],
    )    

    ######################################################
    ########### Block manuell setzen ##################### # derzeit noch über GUI
    ######################################################

    if such_modus == "Schnelle Suche (Live-Demo mit RandomSearch)":
        # Extrem schlank: Fokus auf die 3 wichtigsten Hebel, minimale Listen
        param = {
        "classifier__max_depth": [5, 10],
        "classifier__n_estimators": [50],
        "classifier__min_samples_leaf": [30],
        "classifier__min_samples_split": [70],
        "classifier__max_features": ["sqrt"],
        #"classifier__class_weight": ["balanced"],
            }
#        #max_depth_options = [3]
#        #n_estimators_options = [100]
        #"classifier__min_samples_leaf":,  # Grober Check gegen Overfitting
        #"class_weight": ["balanced"],

        cv_folds = 3  # Weniger Folds sparen massiv Zeit bei großen Datensätzen
        max_kombinationen = 4   # Hier soagar nur zwei möglich
        use_random_search = True  # Bei so wenigen Kombinationen ist GridSearchCV schneller

    elif such_modus == "Normale Suche (mit RandomSearch)":  # kann auch mal 20 min dauern
        param = {
        "classifier__max_depth": [6, 9, 12],
        "classifier__n_estimators": [100],
        "classifier__min_samples_leaf": [20, 50],
        "classifier__min_samples_split": [50],
        "classifier__max_features": ["sqrt"],
        #"classifier__class_weight": ["balanced"],
            }
#        #max_depth_options = [12]
#        #n_estimators_options = [200]
        #"min_samples_leaf": ,
        #"min_samples_split":,
        #"max_features": ["sqrt"],
        #"class_weight": ["balanced"],

        cv_folds = 5
        max_kombinationen = 6
        use_random_search = True

    else:  # Intensive Suche (Nicht für Live-Vortrag geeignet)
        param = {
        'classifier__n_estimators': [100, 200],
        # Maximale Baumtiefe (Der gesuchte Sweet-Spot zwischen 3 und 16)
        'classifier__max_depth': [6, 9, 12],
        # Mindestanzahl an Datenpunkten pro Endblatt (Schutz vor Rauschen/Overfitting)
        'classifier__min_samples_leaf': [10, 30, 60],
        # Mindestanzahl an Datenpunkten, um einen Knoten überhaupt zu teilen
        'classifier__min_samples_split': [25, 70],
        # Feature-Begrenzung pro Split ('sqrt' nutzt ca. 2 von 5 Features, None nutzt alle 5)
        'classifier__max_features': ['sqrt', None]
            }
#        #max_depth_options = [20]
#        #n_estimators_options = [200]
        #"min_samples_leaf": ,
        #"min_samples_split":,
        #"max_features": ["sqrt"],
        #"class_weight": ["balanced"],

        cv_folds = 5
        max_kombinationen = 0
        use_random_search = False

    # Test, führt zu F1_score=0.53 mit gleichem Set, wie im Notebook!
    #max_depth_options = [12]
    #n_estimators_options = [100]

    # intensiv
    #max_depth_options = [5, 10, None]
    #n_estimators_options = [50, 100, 200]

    # ausgewogen
    #max_depth_options = [5, 10, 12]
    #n_estimators_options = [50, 100, 200]

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

if not selected_buildings:
    st.error("Bitte wähle mindestens einen Gebäudetyp im Gebäudefilter aus.")
    st.stop()

if not selected_features:
    st.error("Bitte wähle mindestens ein Feature über die Checkboxen aus.")
    st.stop()


# 4. Datenvorbereitung basierend auf gewählten SEASONS und FEATURES
# Schritt A: Kombinierter 3-Wege-Filter für Zeilen (Saison UND Klima UND Kühlungstyp)
df_filtered_rows = df[
    (df['season'].isin(selected_seasons)) & 
    (df['climate_zone'].isin(selected_climates)) &
    (df['cooling_type'].isin(selected_coolings)) &
    (df['building_type'].isin(selected_buildings))
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
        value=f"unvollst. Zeilen: {rows_with_missing_values:,} \n\nfehlende Werte: {total_missing_cells:,}"
    )
    if impute_strategy == "Zeilen mit Fehlwerten löschen (dropna)":
        st.caption("🔴 Status: Die betroffenen Zeilen wurden aus dem Modell entfernt.")
    else:
        st.caption("🟢 Status: Lücken werden im Trainingsverlauf durch den Median ersetzt.")

st.write("---")

#########################################################################################################
# 5. Training & GridSearch 
#########################################################################################################
@st.cache_resource
#def train_model(X_tr, y_tr, features, estimators, depths, strategy, seasons, climates, coolings, max_kombinationen, cv_folds):
def train_model(X_tr, y_tr, features, param, strategy, seasons, climates, coolings, buildings, max_kombinationen, cv_folds):
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),  # in der Regel ohnehin fehlende Werte entfernt
        #('scaler', StandardScaler()),   # 
        ('scaler', PowerTransformer()),   # RandomForest, also nicht von Bedeutung
        ('classifier', RandomForestClassifier(class_weight="balanced", random_state=42))    # fixe Parameter setzen!!!
    ])
    

    #########################################################
    ############## Herzstück von GridSearch #################
    #########################################################
    
    # Cross-Validation mit 3 Folds (Durchgängen), Bewertungskriterium f1_macro, Overfitting wird nicht berücksichtigt / ermittelt
    # Durch Kreuzvalidierung wird die Gefahr auf Overfitting jedoch stark reduziert!!!
    
    if (use_random_search):
        param_distributions = param
        #param_distributions = {
        #'classifier__n_estimators': estimators,
        #'classifier__max_depth': depths
        #    }
        #grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='f1_macro', n_jobs=-1)
        grid_search = RandomizedSearchCV(pipeline, param_distributions=param_distributions, cv=cv_folds, n_iter=max_kombinationen, scoring='f1_macro', n_jobs=-1)
        st.write(f"RandomSearch durchgeführt!")
    else:
        param_grid = param
        #param_grid = {
        #'classifier__n_estimators': estimators,
        #'classifier__max_depth': depths
        #    }
        grid_search = GridSearchCV(pipeline, param_grid=param, cv=cv_folds, scoring='f1_macro', n_jobs=-1)
        st.write(f"GridSearch durchgeführt!")
    
    
    
    grid_search.fit(X_tr, y_tr)
    
    return grid_search.best_estimator_, grid_search.best_params_
# ENDE train_model

# Button zum Starten des Trainings
if st.button("🚀 Modell trainieren & validieren"):

    # Container für die Live-Zeitanzeige erstellen
    timer_placeholder = st.empty()

    # Variablen für die Zeitmessung initialisieren
    start_time = time.time()
    suche_aktiv = True

    # Diese Funktion läuft im Hintergrund und aktualisiert den Timer jede Sekunde
    def zeige_live_timer():
        while suche_aktiv:
            vergangene_zeit = time.time() - start_time
            # Zeigt den aktuellen Zwischenstand im Vortrag an
            timer_placeholder.markdown(
                f"⏳ **Berechnung läuft... Aktuelle Dauer:** `{vergangene_zeit:.1f} Sekunden`"
            )
            time.sleep(0.1)

    # Den Live-Timer in einem separaten Hintergrund-Thread starten
    timer_thread = threading.Thread(target=zeige_live_timer)


    if (use_random_search):
        searchtext = 'RandomSearch läuft... Bitte warten...'
    else:
        searchtext = 'GridSearch läuft... Bitte warten...'

    with st.spinner(searchtext):
        timer_thread.start()
        best_pipeline, best_params = train_model(   ################################################################################ Aufruf RANDOM FOREST FUNCTION ##################
            X_train, y_train, tuple(selected_features), param, #tuple(n_estimators_options), tuple(max_depth_options), 
            impute_strategy, tuple(selected_seasons), tuple(selected_climates), tuple(selected_coolings), tuple(selected_buildings), max_kombinationen, cv_folds
        )
    
    # Finale Endzeit berechnen
    end_time = time.time()
    gesamtdauer = end_time - start_time

    # Den provisorischen Timer-Text löschen und durch die Erfolgsmeldung ersetzen
    timer_placeholder.empty()


    st.session_state['model'] = best_pipeline
    st.session_state['best_params'] = best_params
    st.success(f"Training erfolgreich abgeschlossen! Gesamte Rechenzeit: **{gesamtdauer:.2f} Sekunden**")

# 2. Vorhersagen für die Metriken generieren
    y_pred = best_pipeline.predict(X_test)
    unique_labels = sorted(list(y_test.unique()))
    
    # Textbasierten Classification Report als String generieren
    class_report_str = classification_report(y_test, y_pred, labels=unique_labels)
    
    # 3. SHAP-Werte exakt hier EINMAL berechnen
    transformed_X_test = best_pipeline.named_steps['scaler'].transform(
        best_pipeline.named_steps['imputer'].transform(X_test)
    )
    transformed_df = pd.DataFrame(transformed_X_test, columns=selected_features)
    rf_model = best_pipeline.named_steps['classifier']
    
    shap_sample = transformed_df.sample(min(100, len(transformed_df)), random_state=42)
    explainer = shap.TreeExplainer(rf_model)
    shap_values = explainer.shap_values(shap_sample)
    actual_class_names = list(rf_model.classes_)
    
    # 4. Das KOMPLETTE EXPERIMENT-PAKET als Dictionary schnüren
    experiment_data = {
        'pipeline': best_pipeline,
        'best_params': best_params,
        'y_test': y_test,
        'y_pred': y_pred,
        'unique_labels': unique_labels,
        'classification_report': class_report_str, # Der gespeicherte Report
        'shap_values': shap_values,
        'shap_sample': shap_sample,
        'shap_class_names': actual_class_names
    }
    
    # 5. Im Session-State für die UI-Anzeige sichern
    st.session_state['experiment'] = experiment_data
    
    # === MODELL + ERGEBNISSE LOKAL IM ORDNER SPEICHERN ===
    local_filename = "ashrae_thermal_classification_model.joblib"
    joblib.dump(experiment_data, local_filename)
    
    #st.success("Training und Artefakt-Generierung erfolgreich abgeschlossen!")
    st.info(f"💾 Das Gesamtpaket wurde als **'{local_filename}'** im Projektordner gespeichert.")

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

        if 'experiment' in st.session_state:
            exp = st.session_state['experiment']
            # Modell speichern
            # Erstellt ein virtuelles Dateiobjekt im Arbeitsspeicher
            st.write("**Komplettes Experiment-Paket exportieren:**")
            buffer = io.BytesIO()
            # Wir dumpen das geholte 'exp'-Paket in den Speicher-Buffer
            joblib.dump(exp, buffer)
            joblib_bytes = buffer.getvalue()
            
            st.download_button(
                label="📥 Gesamtpaket (.joblib) für Browser herunterladen",
                data=joblib_bytes,
                file_name="ashrae_thermal_classification_bundle.joblib",
                mime="application/octet-stream",
                help="Herunterladen von Pipeline, Parametern, Testdaten, Classification Report und SHAP-Werten."
            )

        # ==============================================
        
        # Ergebnisse im UI speichern
#        st.session_state['model'] = best_pipeline
#        st.session_state['best_params'] = best_params

        with st.spinner("Generiere Pairplot... Bitte warten..."):
            fig_pp = plt.figure(figsize=(12, 10))
            plot_df = df_filtered.dropna()

            if len(plot_df) > 10000:
                plot_df = plot_df.sample(10000, random_state=42)
                st.caption("ℹ️ Hinweis: Der Datensatz ist sehr groß. Es wird eine repräsentative Stichprobe von 10.000 Zeilen visualisiert.")

            sns.pairplot(
               plot_df, 
                hue='thermal_preference', 
                palette='coolwarm', # Schöne Farbpalette für thermischen Komfort
                corner=True # Verhindert doppelte Plots in der oberen Hälfte für bessere Übersicht
            )   

            st.pyplot(plt.gcf()) # plt.gcf() holt sich die aktuelle Seaborn-Grafik
            plt.close('all')

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
        
        with st.spinner("Generiere SHAP-Analyse... Bitte warten..."):
            # Stichprobe ziehen, um Abstürze bei großen Testsets zu verhindern
            shap_sample = transformed_df.sample(min(400, len(transformed_df)), random_state=42) # nur 400 samples!
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

            plt.xlabel("Einfluss auf die Modellvorhersage (Durchschnitt)")
            #plt.ylabel("Features")

            st.pyplot(fig)

        st.write("\n\n")

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


    #col3, col4 = st.columns(2)

    #with col3:


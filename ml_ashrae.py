import streamlit as st

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer, FunctionTransformer, StandardScaler, RobustScaler


st.title("🌡️ Thermal Comfort Modelling")

# Create two tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Auswahl der Parameter", "Logistic Regression", "Decision Tree", "kNN", "Random Forest"])

with tab1: 

    col1_1, col1_2 = st.columns([1, 2])

    with col1_1:

        df = pd.read_csv("db_bereinigt.csv")  
        df_ml = df[['air_temperature','radiant_temperature','air_speed', 'metabolic_rate', 'clothing_ensemble_insulation','thermal_comfort']]

        df_ml_clean = df_ml.dropna()

        code_1='''
        df = pd.read_csv("db_bereinigt.csv")  

        df_ml = df[['air_temperature',
        'radiant_temperature',
        'air_speed', 
        'metabolic_rate', 
        'clothing_ensemble_insulation',
        'thermal_comfort']]

        df_ml_clean = df_ml.dropna()
        '''
        st.code(code_1, language="python")

    with col1_2: 
        st.dataframe(df_ml_clean.head())
        st.write(f"Zeilen: {df_ml_clean.shape[0]} | Spalten: {df_ml_clean.shape[1]}")

        y = df_ml_clean['thermal_comfort']
        X = df_ml_clean.drop(columns=['thermal_comfort'])

        # Display value counts in Streamlit
        # st.write("Target value counts:")
        # st.write(y.value_counts())

        # Plot histogram (numeric) or bar chart (categorical)
        fig, ax = plt.subplots()

        if pd.api.types.is_numeric_dtype(y):
            ax.hist(y, bins=20, color='skyblue', edgecolor='black')
            ax.set_xlabel('Thermal Comfort')
            ax.set_ylabel('Frequency')
        else:
            counts = y.value_counts()
            ax.bar(counts.index.astype(str), counts.values, color='skyblue', edgecolor='black')
            ax.set_xlabel('Thermal Comfort')
            ax.set_ylabel('Count')

        ax.set_title('Thermal Comfort Distribution')

        # Show plot in Streamlit
        st.pyplot(fig)


with tab2:

    st.subheader("Ziel")
    st.subheader("Code")
    st.write("Code für Logistic Regression Model")

    code_2='''
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) # stratify für unbalancing, jedoch keine großen Unterschiede
            
        schiefe_features = ['air_speed', 'metabolic_rate', 'clothing_ensemble_insulation']
        normale_features = ['air_temperature', 'radiant_temperature']

        # StandardScaler für schiefe Features
        schiefe_transformer = Pipeline(steps=[('power_transform', PowerTransformer(method='yeo-johnson'))])

        # Alternativen zum StandardScaler, RobustScaler (bei Ausreißern), MinMaxScaler (gut für neuronale Netze), MaxAbsScaler (für dünnbesetzte Daten)
        # RobustScaler oder StandardScaler hier
        preprocessor = ColumnTransformer(
            transformers=[('schief', schiefe_transformer, schiefe_features),('normal', StandardScaler(), normale_features)  # Normale Spalten werden nur skaliert - hier mit StandardScaler])

        pipeline = Pipeline(steps=[('preprocessor', preprocessor),('classifier', LogisticRegression(max_iter=100))])
    

        # 4. Pipeline trainieren (skaliert X_train intern und trainiert das Modell)
        pipeline.fit(X_train, y_train)

        # 5. Vorhersagen treffen (skaliert X_test intern mit den Werten aus dem Training)
        y_pred = pipeline.predict(X_test)
        '''
    st.code(code_2, language="python")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) # stratify für unbalancing, jedoch keine großen Unterschiede

    col2_1, col2_2 = st.columns([1,1])

    with col2_1:

        schiefe_features = ['air_speed', 'metabolic_rate', 'clothing_ensemble_insulation']
        normale_features = ['air_temperature', 'radiant_temperature']

        # StandardScaler für schiefe Features
        schiefe_transformer = Pipeline(steps=[('power_transform', PowerTransformer(method='yeo-johnson')) ])

        # Alternativ mit Robust, Scaler statt StandardScaler
        #schiefe_pipeline = Pipeline(steps=[
        #    # Wichtig: standardize=False schaltet das automatische 'StandardScaler'-Verhalten aus
        #    ('power', PowerTransformer(method='yeo-johnson', standardize=False)), 
        #    # Jetzt skaliert der RobustScaler die transformierten Daten ausreißersicher
        #    ('robust_scale', RobustScaler()) 
        #])

        # Alternativen zum StandardScaler, RobustScaler (bei Ausreißern), MinMaxScaler (gut für neuronale Netze), MaxAbsScaler (für dünnbesetzte Daten)
        # RobustScaler oder StandardScaler hier
        preprocessor = ColumnTransformer(
            transformers=[
                ('schief', schiefe_transformer, schiefe_features),
                ('normal', StandardScaler(), normale_features)  # Normale Spalten werden nur skaliert - hier mit StandardScaler
                #('normal', RobustScaler(), normale_features) # Alternative zu StandardScaler der RobustScaler - Nachteile bei logReg, man verliert Infos zu Ausreißern auch wenn er dafür besser ist, hohe Anfälligkeit bei wenig Daten
            ]
        )

        pipeline = Pipeline(steps=[('preprocessor', preprocessor),('classifier', LogisticRegression(max_iter=100))])
        ##################################################################################################

        ###########################################################################
        # allgemeine Pipeline ohne log
        #pipeline = Pipeline([
        #    ('scaler', StandardScaler()),
        #    ('classifier', LogisticRegression(max_iter=100))
        #])
        ###########################################################################

        # 4. Pipeline trainieren (skaliert X_train intern und trainiert das Modell)
        pipeline.fit(X_train, y_train)

        # 5. Vorhersagen treffen (skaliert X_test intern mit den Werten aus dem Training)
        y_pred = pipeline.predict(X_test)


        # 6. Bewertung
        st.subheader("Bewertung: Logistische Regression")

        accuracy = accuracy_score(y_test, y_pred)
        st.write(f"**Genauigkeit mit Pipeline:** {accuracy:.2f}")

        st.markdown("**Detaillierter Klassifikationsbericht:**")
        report = classification_report(y_test, y_pred, output_dict=False)
        st.text(report)


        report_dict = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report_dict).transpose()

        st.dataframe(report_df.style.format({
            'precision': "{:.2f}",
            'recall': "{:.2f}",
            'f1-score': "{:.2f}",
            'support': "{:.0f}"
        }))

        

    with col2_2:
        # confusion matrix
        st.subheader("Confusion Matrix")

        fig, ax = plt.subplots()
        ConfusionMatrixDisplay.from_predictions(y_test, y_pred, cmap="Blues", ax=ax)
        ax.set_title("Logistische Regression")
        st.pyplot(fig)












































with tab3:
    st.write("Decision Tree")



with tab4:
    st.write("kNN")


with tab5:
    st.write("Random Forest")


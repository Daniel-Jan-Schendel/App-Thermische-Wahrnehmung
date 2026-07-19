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

EXCEL_FILE = "ML/Ergebnisse_ASHRAE_ML.xlsx"

@st.cache_data
def get_sheet(sheet_name):
    # Liest genau den gewünschten Reiter aus der Excel-Datei
    return pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)

st.title(":material/smart_toy: Machine Learning")

# Create two tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Bearbeitete Themen", "Subjektive Komfortbewertungen", "Decision Tree", "kNN", "Anomaliebetrachtungen"])


FONT_SIZE_TEXT = "24px"
FONT_SIZE_BULLET = "34px"
BULLET_COLOR = "#ff4b4b"
TEXT_COLOR = "#31333F"

SMALL_FONT_SIZE_TEXT = "16px"
SMALL_FONT_SIZE_BULLET = "24px"
SMALL_BULLET_COLOR = "#7f8c8d"
INDENT_WIDTH = "40px"

def slide_point(text):
    return f"""
    <div style='font-size: {FONT_SIZE_TEXT}; color: {TEXT_COLOR}; line-height: 1.6; margin-bottom: 12px; display: flex; align-items: center;'>
        <span style='font-size: {FONT_SIZE_BULLET}; color: {BULLET_COLOR}; margin-right: 15px;'>•</span> 
        <div>{text}</div>
    </div>
    """

def slide_smallpoint(text):
    return f"""
    <div style='font-size: {SMALL_FONT_SIZE_TEXT}; color: {TEXT_COLOR}; line-height: 1.6; margin-bottom: 8px; margin-left: {INDENT_WIDTH}; display: flex; align-items: center;'>
        <span style='font-size: {SMALL_FONT_SIZE_BULLET}; color: {SMALL_BULLET_COLOR}; margin-right: 12px;'>–</span><div>{text}</div>
    </div>
    """

with tab1: 
    bullet_points, bullet_images = st.columns([3,1])
    with bullet_points:
        st.header('Bearbeitete Themengebiete:')

        FONT_SIZE_TEXT = "24px"
        FONT_SIZE_BULLET = "34px"
        BULLET_COLOR = "#ff4b4b"  # Streamlit-Rot
        TEXT_COLOR = "#31333F"  # Schönes Dunkelgrau

        st.write("\n")

        st.write("\n")
        st.html(slide_point("Untersuchungen zur Vorhersage der subjektive Komfortbewertungen (Klassifizierung)"))

        st.write("\n")
        st.html(slide_point("Untersuchungen zur Vorhersage der Kühlungsart (Cooling Type) (Klassifizierung)"))

        st.write("\n")
        st.html(slide_point("Untersuchungen zur Vorhersage der der Bekleidungsisolationswertes (clothing_ensemble_insulation) (Regression)"))

        st.write("\n")
        st.html(slide_point("Anomaliebetrachtungen"))
    
    with bullet_images:
        st.write("BILDER")

with tab2:

    st.subheader("Subjektive Komfortbewertungen")

    st.html(slide_point("Idee: Vorhersage der subjektiven Komfortbewertungen (...) mit Hilfe von Featuren wie, ..."))


    st.subheader("Aufgetrendende Probleme")

    st.html(slide_point("Label Noise"))
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp; - Die gleichen Bedingungen führen zu subjektiv unterschiedlichen Ergebnisse.")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp; - Es bilden sich keine klassischen Cluster oder Möglichkeiten für einen Classifier für Unterscheidungen.")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp; - Klassifizierungen erzielen eine Genauigkeit die kaum Mehrwert bietet.")

    st.write("PAIRPLOT")

    st.subheader("Versuchte Gegenmaßnahmen")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp; - Kleinere Datensätze mit Filterung für homogenere Datensätze.")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp; - Reduzierung der Klassen des Targets.")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp; - Einsatz von TomekLink Filtern und SMOTE")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp; - Aufbau eines Dashboards zum schnellen Untersuchen möglicher Modelle.")

    st.html(slide_point("Auf Grund der Daten lassen sich keine verlässlichen Vorhersagen bezüglich der subjektiven Komfortbewertungen treffen."))

    df_thermal_clf = get_sheet("thermal_clf")
    st.table(df_thermal_clf)

with tab3:
    st.write("Decision Tree")



with tab4:
    st.write("kNN")


with tab5:
    st.write("Anomaliebetrachtungen")


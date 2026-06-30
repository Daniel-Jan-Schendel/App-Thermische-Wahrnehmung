import streamlit as st
import sklearn
import matplotlib.pyplot as pd

import streamlit.components.v1 as components
import os
import nbformat
from nbconvert import HTMLExporter

st.set_page_config(page_title="Machine Learning - ASHRAE", layout="wide",initial_sidebar_state="expanded")

tab_description,  tab_Notebook = st.tabs(
    ["📘 Description", "📄 Notebook"]
)

with tab_description:

    st.header("Machine Learning Applications")

    st.write("""
    This section explores how machine learning techniques can be applied to the 
    Global Thermal Comfort Database to identify patterns, predict comfort responses, 
    and support data‑driven decision‑making in building performance analysis.

    By leveraging environmental measurements (such as air temperature, humidity, 
    air speed, and radiant temperature) together with occupant feedback, machine 
    learning models can help estimate thermal sensation, predict comfort votes, 
    and classify indoor environmental conditions according to ASHRAE standards.
    """)

    st.subheader("What We Aim to Achieve")

    st.write("""
    The goal of this module is to demonstrate how supervised learning algorithms 
    — such as regression models, decision trees, random forests, or neural networks — 
    can be trained using selected variables from the database. These models can be 
    used to:

    - Predict thermal sensation votes (TSV)
    - Estimate PMV/PPD values from raw measurements
    - Classify comfort categories based on environmental conditions
    - Identify the most influential variables affecting comfort perception

    These predictive tools can support researchers and practitioners in evaluating 
    indoor environments, optimizing HVAC operation, and improving occupant comfort.
    """)

with tab_Notebook:
    notebook_pfad = "test_notebook.ipynb"

    if not os.path.exists(notebook_pfad):
        st.error(f"❌ Die Datei '{notebook_pfad}' wurde im Ordner nicht gefunden!")
    else:
        try:
            with st.spinner("Notebook wird eingelesen und konvertiert..."):
                # 1. Notebook-Datei im JSON-Format einlesen
                with open(notebook_pfad, "r", encoding="utf-8") as f:
                    notebook_node = nbformat.read(f, as_version=4)
                
                # 2. Den HTML-Exporter konfigurieren
                html_exporter = HTMLExporter()
                
                # 3. Direkt in HTML-Inhalt umwandeln (ohne subprocess!)
                (html_body, resources) = html_exporter.from_notebook_node(notebook_node)
                
            #st.success("✅ Notebook erfolgreich geladen!")
            
            # 4. Das HTML direkt in Streamlit anzeigen
            components.html(html_body, height=900, scrolling=True)
            
        except Exception as e:
            st.error("❌ Fehler bei der Konvertierung innerhalb von Python:")
            st.exception(e)
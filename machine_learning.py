import streamlit as st
import sklearn
import matplotlib.pyplot as pd

st.set_page_config(page_title="Machine Learning - ASHRAE", layout="wide",initial_sidebar_state="expanded")

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
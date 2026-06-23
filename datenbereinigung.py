import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Datenbereinigung - ASHRAE", layout="wide",initial_sidebar_state="expanded")

st.header("📊 Inspektion des Datensatzes")

# --- Datei direkt laden ---
CSV_PATH = "db_measurements_v210.csv"

try:
    df = pd.read_csv(CSV_PATH)
    st.success(f"Datei '{CSV_PATH}' erfolgreich geladen!")
except FileNotFoundError:
    st.error(f"Die Datei '{CSV_PATH}' wurde nicht gefunden. Bitte sicherstellen, dass sie im gleichen Ordner liegt.")
    st.stop()

# --- Mostrar el código usado ---
st.subheader("📌 Verwendeter Python-Code für die Dateninspektion")

st.code("""
import pandas as pd

df = pd.read_csv("db_measurements_v210.csv")
df.info()
df.describe()
df.shape
duplicates = df[df.duplicated()]
df_clean = df.drop_duplicates()
""", language="python")

# --- Original anzeigen ---
st.subheader("📁 Originaler Datensatz (vor der Reinigung)")
st.dataframe(df)

# --- Dimensionen vor der Reinigung ---
st.write("## 📏 Dimensionen vor der Reinigung")
st.write(f"**Zeilen:** {df.shape[0]}")
st.write(f"**Spalten:** {df.shape[1]}")

# --- Erste Untersuchung ---
st.subheader("🔍 Erste Untersuchung des Datensatzes")

st.write("**Erste Zeilen:**")
st.dataframe(df.head())

st.write("**Datenstruktur:**")
buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())

st.write("**Statistische Übersicht:**")
st.dataframe(df.describe(include="all"))

# --- Duplikate ---
st.subheader("🧩 Duplizierte Zeilen")
duplicates = df[df.duplicated()]
st.write(f"Anzahl duplizierter Zeilen: {duplicates.shape[0]}")
st.dataframe(duplicates)

# --- Reinigung ---
st.subheader("🧹 Datensatz nach der Reinigung")
df_clean = df.drop_duplicates()
st.dataframe(df_clean)

# --- Dimensionen nach der Reinigung ---
st.write("### 📏 Dimensionen nach der Reinigung")
st.write(f"**Zeilen:** {df_clean.shape[0]}")
st.write(f"**Spalten:** {df_clean.shape[1]}")

# --- Vergleich ---
st.subheader("📌 Vergleich: Vorher vs. Nachher")

col1, col2 = st.columns(2)

with col1:
    st.write("**Vorher (Original):**")
    st.write(f"{df.shape[0]} Zeilen, {df.shape[1]} Spalten")

with col2:
    st.write("**Nachher (Clean):**")
    st.write(f"{df_clean.shape[0]} Zeilen, {df_clean.shape[1]} Spalten")

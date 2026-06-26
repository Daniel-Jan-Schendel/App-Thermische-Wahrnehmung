import streamlit as st
import pandas as pd

st.set_page_config(page_title="ASHRAE Analytics", layout="wide", initial_sidebar_state="expanded")

df_bereinigt = pd.read_csv("db_bereinigt.csv")

st.title("ASHRAE Analytics")
#st.line_chart(df_bereinigt["DB"])
st.dataframe(df_bereinigt)
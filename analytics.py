import streamlit as st
import pandas as pd

st.set_page_config(page_title="ASHRAE Analytics", layout="wide", initial_sidebar_state="expanded")

df = pd.read_csv("db_measurements_v210.csv")


def main(df):
    st.title("ASHRAE Analytics")
    st.line_chart(df["DB"])
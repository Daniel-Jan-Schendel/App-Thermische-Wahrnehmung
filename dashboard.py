import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

# st.title("SmartBuilding-Analytics")
# st.subheader("Datenarchitektur zur Optimierung klimatisierter Gebäudeinfrastrukturen")
# st.write("Dashboard with two sections: Dataset Overview and Data Explorer.")

st.title("SmartBuilding-Analytics Dashboard")


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("db_measurements_v210.csv")

df = load_data()



# Create two tabs
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📄 KPI", "📊 Statistics"])

# ---------------------------------------------------------
# TAB 1 — Dataset Overview
# ---------------------------------------------------------
# with tab1:
#     st.header("Dataset Overview")

#     if show_info:
#         st.subheader("Preview of the dataset")
#         st.dataframe(df.head())

#         st.subheader("Dataset shape")
#         st.write(f"Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")

#         st.subheader("Column names")
#         st.write(list(df.columns))

# # ---------------------------------------------------------
# # TAB 2 — Data Explorer
# # ---------------------------------------------------------
# with tab2:
#     st.header("Data Explorer")

#     st.subheader("Select a column to analyze")
#     column = st.selectbox("Choose a column:", df.columns)

#     st.subheader("Summary statistics")
#     st.write(df[column].describe())

#     # Numeric filtering
#     if pd.api.types.is_numeric_dtype(df[column]):
#         st.subheader("Filter by numeric range")

#         min_val = float(df[column].min())
#         max_val = float(df[column].max())

#         selected_range = st.slider(
#             "Select value range:",
#             min_value=min_val,
#             max_value=max_val,
#             value=(min_val, max_val)
#         )

#         filtered_df = df[
#             (df[column] >= selected_range[0]) &
#             (df[column] <= selected_range[1])
#         ]

#         st.write("Filtered results:")
#         st.dataframe(filtered_df.head())

#     # Categorical filtering
#     else:
#         st.subheader("Filter by category")

#         unique_values = df[column].dropna().unique()
#         selected_value = st.selectbox("Select a value:", unique_values)

#         filtered_df = df[df[column] == selected_value]

#         st.write("Filtered results:")
#         st.dataframe(filtered_df.head())

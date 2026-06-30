import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="ASHRAE Analytics", layout="wide", initial_sidebar_state="expanded")

df_bereinigt = pd.read_csv("db_bereinigt.csv")

st.title("ASHRAE Analytics")
#st.line_chart(df_bereinigt["DB"])
st.dataframe(df_bereinigt)



# Copy dataframe
df = df_bereinigt.copy()

# Rename columns if needed
df = df.rename(columns={
    "latitud": "latitude",
    "longitud": "longitude"
})

# Convert to numeric
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

# Create a reduced table with unique combinations
df_list = df[["city", "country", "region", "latitude", "longitude"]].drop_duplicates()


# Create a map

regions = df_list["region"].unique()
color_map = {
    region: [int(i*60) % 255, int(i*120) % 255, int(i*180) % 255]
    for i, region in enumerate(regions)
}

df_list["color"] = df_list["region"].map(color_map)

layer = pdk.Layer(
    "ScatterplotLayer",
    df_list,
    get_position='[longitude, latitude]',
    get_fill_color='color',
    get_radius=50000,
)

view_state = pdk.ViewState(
    latitude=df_list["latitude"].mean(),
    longitude=df_list["longitude"].mean(),
    zoom=1.5
)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state
    )
)
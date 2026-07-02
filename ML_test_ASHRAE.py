import streamlit as st
import numpy as np
import pickle

st.title("🌡️ ASHRAE Thermal Comfort Predictor")

# Load model
with open("model_ashrae.pkl", "rb") as file:
    model = pickle.load(file)

st.write("Enter Ambiental Conditions:")

#air_temp = st.slider("Air Temperature (°C)", 10.0, 40.0, 22.0)
humidity = st.slider("Relative Humidity (%)", 10.0, 100.0, 50.0)
air_vel = st.slider("Air Velocity (m/s)", 0.0, 2.0, 0.2)
mrt = st.slider("Mean Radiant Temperature (°C)", 10.0, 40.0, 22.0)
met = st.slider("Metabolic Rate", 0.8, 2.0, 1.2)
clo = st.slider("Clothing Insulation (clo)", 0.1, 1.5, 0.5)

if st.button("Predict Thermal Comfort"):
    input_data = np.array([[
    float("relative_humidity"),
    float("air_speed"),
    float("radiant_temperature"),
    float("metabolic_rate"),
    float("clothing_ensemble_insulation")
    ]])

    prediction = model.predict(input_data)

    st.success(f"Thermal Sensation: {prediction[0]:.2f}")

    st.info("(-3 cold → 0 neutral → +3 hot)")


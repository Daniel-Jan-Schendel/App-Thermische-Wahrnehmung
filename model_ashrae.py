# model_ashrae.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load data ASHRAE
df = pd.read_csv("db_bereinigt.csv")

# -----------------------------
# CLEANING 
# -----------------------------

features = [
    "air_temperature",
    "relative_humidity",
    "air_speed",
    "radiant_temperature",
    "metabolic_rate",
    "clothing_ensemble_insulation"
]

target = "thermal_sensation"

# remove rows with NaN in features or target
df = df.dropna(subset=features + [target])

# Separate X and y
X = df[features]
y = df[target]

# optional
X = X.reset_index(drop=True)
y = y.reset_index(drop=True)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save model
with open("model_ashrae.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model ASHRAE saved successfully")
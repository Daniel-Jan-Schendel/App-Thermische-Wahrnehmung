from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import  datasets
import pandas as pd
import numpy as np
import pickle

# Load the Iris dataset
df = datasets.load_iris()
X, y = df.data, df.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model save as model.pkl")

# to generate model.pkl python model_iris.py
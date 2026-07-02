import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app UI
st.title("Iris Species Predictor")

# Load model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Create two tabs
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["Code", "Visualisierung"])

with tab1:

    st.write("Model")
    code_1 = '''
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
    '''
    st.code(code_1, language="python")
 
with tab2:

    st.write("Enter flower measurements to predict its species.")

    # Input sliders for user data
    sepal_length = st.slider("Sepal Length (cm)", 4.0, 8.0, step=0.1)
    sepal_width = st.slider("Sepal Width (cm)", 2.0, 5.0, step=0.1)
    petal_length = st.slider("Petal Length (cm)", 1.0, 7.0, step=0.1)
    petal_width = st.slider("Petal Width (cm)", 0.1, 2.5, step=0.1)

    # Predict button
    if st.button("Predict"):
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        prediction = model.predict(features)
        st.write(f"Predicted Species: **{prediction[0]}**")

    if st.checkbox("Show Feature Importance"):
        importance = model.feature_importances_
        features = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
        plt.barh(features, importance)
        st.pyplot(plt)
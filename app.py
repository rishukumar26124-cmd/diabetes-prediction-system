
import streamlit as st
import requests

st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Diabetes Prediction System")
st.write("Enter patient information to predict diabetes.")

st.divider()
st.subheader("Patient Details")

col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies", 0, 20, 2)
    glucose = st.number_input("Glucose", 0, 300, 120)
    blood_pressure = st.number_input("Blood Pressure", 0, 200, 70)
    skin_thickness = st.number_input("Skin Thickness", 0, 100, 25)

with col2:
    insulin = st.number_input("Insulin", 0, 900, 80)
    bmi = st.number_input("BMI", 0.0, 70.0, 28.5)
    diabetes_pedigree = st.number_input(
        "Diabetes Pedigree Function", 0.0, 3.0, 0.5
    )
    age = st.number_input("Age", 1, 120, 35)

st.divider()

if st.button("Predict Diabetes", type="primary", use_container_width=True):

    input_data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetes_pedigree,
        "Age": age
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=input_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()["prediction"]

            st.subheader("Prediction Result")

            if result == "Diabetes":
                st.error("Model prediction: Diabetes")
            else:
                st.success("Model prediction: No Diabetes")

            st.caption(
                "This is an ML model prediction, not a medical diagnosis."
            )

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI. Please start the backend.")

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

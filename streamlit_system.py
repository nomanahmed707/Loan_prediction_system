import streamlit as st
import numpy as np
import joblib

# Load trained model
model = joblib.load("tuned_random_forest_model.pkl")

# Page config
st.set_page_config(page_title="Loan Approval App", layout="centered")

# Correctly scoped background & style
st.markdown("""
    <style>
        /* Apply background to the app */
        [data-testid="stAppViewContainer"] {
            background-image: url("https://images.unsplash.com/photo-1642240251149-bcccea43798d?q=80&w=464&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* Make all labels larger and white */
        label, .stSelectbox label, .stNumberInput label, .stSlider label {
            font-size: 1.25rem !important;
            color: white !important;
            font-weight: 600;
        }

        /* Input box font size */
        .stTextInput input, .stNumberInput input, .stSelectbox div, .stSlider div {
            font-size: 1.1rem !important;
        }

        /* Buttons */
        .stButton>button {
            font-size: 1.2rem;
            background-color: #28a745;
            color: white;
            padding: 10px 24px;
            border-radius: 6px;
            border: none;
        }

        .stButton>button:hover {
            background-color: #218838;
        }

        /* Center title and subtitle */
        .custom-title {
            font-size: 2.5rem;
            text-align: center;
            color: white;
            margin-bottom: 0.3em;
        }

        .custom-subtitle {
            font-size: 1.3rem;
            text-align: center;
            color: #eeeeee;
            margin-bottom: 2em;
        }

        .result-text {
            font-size: 1.8rem;
            text-align: center;
            color: white;
            margin-top: 1.5em;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown("<div class='custom-title'>🏦 Loan Approval Prediction System</div>", unsafe_allow_html=True)
st.markdown("<div class='custom-subtitle'>Fill in the details below to predict loan approval.</div>", unsafe_allow_html=True)

# UI Inputs
gender = st.selectbox("Gender", ['Male', 'Female'])
married = st.selectbox("Married", ['Yes', 'No'])
dependents = st.selectbox("Number of Dependents", ['0', '1', '2', '3+'])
education = st.selectbox("Education", ['Graduate', 'Not Graduate'])
self_employed = st.selectbox("Self Employed", ['Yes', 'No'])
applicant_income = st.number_input("Applicant Income", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
loan_amount = st.slider("Loan Amount (in 1000s)", 10, 600, step=10)
loan_term = st.selectbox("Loan Term (months)", [360, 180, 120, 60, 12])
credit_history = st.selectbox("Credit History", [1.0, 0.0])
property_area = st.selectbox("Property Area", ['Urban', 'Semiurban', 'Rural'])

# Encode categorical
gender = 1 if gender == 'Male' else 0
married = 1 if married == 'Yes' else 0
dependents = 3 if dependents == '3+' else int(dependents)
education = 1 if education == 'Graduate' else 0
self_employed = 1 if self_employed == 'Yes' else 0
property_area_semiurban = 1 if property_area == 'Semiurban' else 0
property_area_urban = 1 if property_area == 'Urban' else 0

features = np.array([[gender, married, dependents, education, self_employed,
                      applicant_income, coapplicant_income, loan_amount,
                      loan_term, credit_history, property_area_semiurban, property_area_urban]])

# Prediction
if st.button("Predict"):
    prediction = model.predict(features)
    result = "🎉 Congratulations! Your loan is approved ✅" if prediction[0] == 1 else "🔁 Loan not approved. You can try again later"
    st.markdown(f"<div class='result-text'>{result}</div>", unsafe_allow_html=True)

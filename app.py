import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("customer_churn_model.pkl")

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊"
)

st.sidebar.title("About")
st.sidebar.info(
    """
    Customer Churn Prediction App

    Model: Random Forest Classifier

    Features:
    - Age
    - Tenure
    - Monthly Charges
    - Total Charges
    - Contract Type
    - Internet Service
    - Tech Support
    """
)

st.sidebar.success("""
Model Performance

Accuracy: 99.95%
ROC-AUC: 0.997
""")

st.title("📊 Customer Churn Prediction")
st.write("Predict whether a customer is likely to churn.")

st.markdown("""
This application predicts whether a customer is likely to churn based on
customer demographics, subscription details, and support information.

**Best Model:** Random Forest Classifier
""")

# User Inputs

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=35
)

tenure = st.number_input(
    "Tenure (Months)",
    min_value=0,
    max_value=150,
    value=24
)

monthly_charges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    max_value=500.0,
    value=75.0
)

total_charges = st.number_input(
    "Total Charges",
    min_value=0.0,
    max_value=20000.0,
    value=1800.0
)

gender = st.selectbox(
    "Gender",
    ["Female", "Male"]
)

contract = st.selectbox(
    "Contract Type",
    ["Month-to-Month", "One-Year", "Two-Year"]
)

internet_service = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber Optic", "None"]
)

tech_support = st.selectbox(
    "Tech Support",
    ["No", "Yes"]
)

if st.button("Predict Churn"):

    # Create input dataframe
    input_data = pd.DataFrame({
        "Age": [age],
        "Tenure": [tenure],
        "MonthlyCharges": [monthly_charges],
        "TotalCharges": [total_charges],
        "Gender_Male": [1 if gender == "Male" else 0],
        "ContractType_One-Year": [1 if contract == "One-Year" else 0],
        "ContractType_Two-Year": [1 if contract == "Two-Year" else 0],
        "InternetService_Fiber Optic": [1 if internet_service == "Fiber Optic" else 0],
        "InternetService_None": [1 if internet_service == "None" else 0],
        "TechSupport_Yes": [1 if tech_support == "Yes" else 0]
    })

    # Prediction
    prediction = model.predict(input_data)[0]

    # Probability
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error(
            f"⚠️ Customer is likely to churn.\n\nChurn Probability: {probability:.2%}"
        )
    else:
        st.success(
            f"✅ Customer is likely to stay.\n\nRetention Probability: {(1-probability):.2%}"
        )

    st.subheader("Prediction Probability")

    st.progress(float(probability))

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Churn Probability",
            f"{probability:.2%}"
        )

    with col2:
        st.metric(
            "Retention Probability",
            f"{1-probability:.2%}"
        )

    if probability > 0.8:
        st.warning("High churn risk customer")
    elif probability > 0.5:
        st.info("Moderate churn risk customer")
    else:
        st.success("Low churn risk customer")
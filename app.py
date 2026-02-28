
import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("aml_model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

st.title("Anti-Money Laundering Predictor")

st.write("Enter transaction details")

# Inputs
amount = st.number_input("Amount", 0.0)

payment_type = st.selectbox(
    "Payment Type",
    ["Credit card", "Cash Deposit", "Cross-border", "Wire"]
)

sender_location = st.selectbox(
    "Sender Location",
    ["USA", "UK", "India", "Germany", "France"]
)

receiver_location = st.selectbox(
    "Receiver Location",
    ["USA", "UK", "India", "Germany", "France"]
)

hour = st.slider("Hour", 0, 23)

# Predict button
if st.button("Predict"):

    # Create dataframe
    data = pd.DataFrame({
        "Amount": [amount],
        "Payment_type": [payment_type],
        "Sender_bank_location": [sender_location],
        "Receiver_bank_location": [receiver_location],
        "Hour": [hour],
        "Minute": [0],
        "Payment_currency": ["USD"],
        "Received_currency": ["USD"]
    })

    # Feature engineering
    data["is_cross_border"] = (
        data["Sender_bank_location"] != data["Receiver_bank_location"]
    ).astype(int)

    data["currency_mismatch"] = 0

    # One hot encoding
    data = pd.get_dummies(data)

    # Match training columns
    data = data.reindex(columns=model_columns, fill_value=0)

    # Prediction
    pred = model.predict(data)[0]

    if pred == 1:
        st.error("⚠️ Laundering Transaction")
    else:
        st.success("✅ Legit Transaction")
import streamlit as st
import numpy as np
import pickle
import random

# Load the AI model
try:
    with open("Diabetesmodel.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    model = None
    st.error("Model file not loaded.")

# Chatbot responses
tips_positive = [
    "Consider monitoring your blood sugar regularly.",
    "A balanced diet low in refined sugar can help manage diabetes.",
    "Try to incorporate 30 minutes of light exercise daily.",
    "Discuss medication options with a healthcare provider."
]

tips_negative = [
    "Maintain healthy habits to reduce future risk.",
    "Keep up with regular health checkups.",
    "Stay active and eat whole foods where possible.",
    "Drink plenty of water and watch your stress levels."
]

# Sidebar
with st.sidebar:
    st.header("About this App")
    st.write("This app predicts your risk of diabetes using a machine learning model.")
    st.write("Created with 💻 by Jocelyn.")
    st.markdown("---")
    st.info("Remember: This is not a diagnostic tool. Always consult a healthcare professional.")

# App layout
st.title("🧠 AI Diabetes Risk + Wellness Chatbot")
st.write("Fill in your health information to get a prediction and lifestyle tips.")

# Input form
with st.form("health_form"):
    glucose = st.number_input("🧪 Glucose Level", min_value=0.0, format="%.2f")
    bp = st.number_input("💓 Blood Pressure", min_value=0.0, format="%.2f")
    bmi = st.number_input("⚖️ BMI", min_value=0.0, format="%.2f")
    age = st.number_input("📅 Age", min_value=0, step=1)

    submitted = st.form_submit_button("Predict")

if submitted:
    if model is None:
        st.error("❌ Model file not loaded.")
    else:
        try:
            input_data = np.array([[glucose, bp, bmi, age]])
            prediction = model.predict(input_data)

            # Display user inputs
            st.subheader("📝 Your Input Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Glucose", glucose)
                st.metric("BMI", bmi)
            with col2:
                st.metric("Blood Pressure", bp)
                st.metric("Age", age)

            st.markdown("---")

            # Prediction results
            if prediction[0] == 1:
                st.warning("⚠️ You are likely to have diabetes.")
                st.chat_message("bot").write(random.choice(tips_positive))

                if glucose > 150:
                    st.info("Your glucose level is quite high. It might be worth scheduling a check-up.")
            else:
                st.success("✅ You are not likely to have diabetes.")
                st.chat_message("bot").write(random.choice(tips_negative))

                if age < 30 and bmi < 25:
                    st.info("Your overall health profile looks good. Keep it up!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
import requests
import streamlit as st

# Streamlit Configuration
st.set_page_config(
    page_title="EPC Energy Rating Predictor",
    layout="centered")
st.title("EPC Energy Rating Predictor (JWT Secured)")

# Sidebar Login Panel
st.sidebar.header("User Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

# Session token management
if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Authenticate with FastAPI
if login_button:
    login_url = "http://localhost:8000/login"
    try:
        response = requests.post(
            login_url, data={"username": username, "password": password}
        )
        if response.status_code == 200:
            st.session_state.access_token = response.json()["access_token"]
            st.sidebar.success("Login successful.")
        else:
            error_message = response.json().get("detail", "Unknown error")
            st.sidebar.error(f"Login failed: {error_message}")
    except Exception as e:
        st.sidebar.error(f"Login error: {e}")

# Block further interaction until logged in
if not st.session_state.access_token:
    st.warning("Please log in using the sidebar to access the model.")
    st.stop()

# Model Options
model_list = [
    "Random Forest",
    "XGBoost",
    "Logistic Regression",
    "MLPClassifier"
]

st.markdown(
    """
**Best Performing Model:** Random Forest  
**F1 Macro Score:** 0.6803  
**Accuracy:** 79.08%
"""
)

# Model Selection
model_choice = st.selectbox(
    "Choose a model:",
    model_list,
    index=model_list.index("Random Forest"))

# User Search Mode
search_mode = st.radio("Search by:", ["LMK_KEY", "Property Address"])

# Input Area
if search_mode == "LMK_KEY":
    input_value = st.text_input("Enter LMK_KEY:")
else:
    input_value = st.text_input("Enter Property Address:")

# Prediction Button
if st.button("Predict Energy Rating"):
    if not input_value.strip():
        st.warning("Please enter a valid search value to continue.")
    else:
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}

        # Select model
        select_url = "http://localhost:8000/select_model"
        select_response = requests.post(
            select_url, json={"model_name": model_choice}, headers=headers
        )

        if select_response.status_code != 200:
            st.error(f"Model selection failed: {select_response.json().get('detail')}")
            st.stop()

        # Predict
        endpoint = "/predict/by-lmk" if search_mode == "LMK_KEY" else "/predict/by-address"
        predict_url = f"http://localhost:8000{endpoint}"
        input_field = "lmk_key" if search_mode == "LMK_KEY" else "address"

        predict_response = requests.post(
            predict_url, json={input_field: input_value}, headers=headers
        )

        if predict_response.status_code == 200:
            result = predict_response.json()
            if 'error' in result:
                st.error(f"Prediction failed: {result['error']}")
            else:
                st.success(
                    f"**Prediction for:** `{result['property_address']}`  \n"
                    f"**LMK_KEY:** `{result['lmk_key']}`  \n\n"
                    f"**Predicted Potential Energy Rating:** **{result['predicted_rating_letter']}**"
                )
        else:
            try:
                error_detail = predict_response.json().get("detail", "Unknown error")
            except Exception:
                error_detail = predict_response.text
            st.error(f"Prediction failed: {error_detail}")

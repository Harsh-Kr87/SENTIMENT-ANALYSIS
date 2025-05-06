import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Flask API endpoint
prediction_endpoint = "http://127.0.0.1:5000/predict"

# Set page configuration
st.set_page_config(page_title="Sentiment Predictor", page_icon="🔍", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .header {
            background-color: #004aad;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
        }
        .footer {
            background-color: #2c3e50;
            padding: 10px;
            color: white;
            text-align: center;
            border-radius: 10px;
            margin-top: 30px;
        }
        .stButton>button {
            background-color: #004aad !important;
            color: white !important;
            font-size: 16px !important;
            padding: 10px !important;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown(
    """
    <div class="header">
        <h1>🔍 Text Sentiment Predictor</h1>
        <p>Analyze the sentiment of text using AI-powered predictions</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Image (Replace with your own image link)
st.image("https://source.unsplash.com/1600x400/?technology,ai", use_column_width=True)

# Upload & Text Input Section
st.write("## Upload a CSV file or enter text for sentiment prediction")

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader(
        "Upload a CSV file for bulk prediction:",
        type="csv",
    )

with col2:
    user_input = st.text_input("Enter text and click on Predict", "")

# Prediction on single sentence
if st.button("Predict"):
    if uploaded_file is not None:
        response = requests.post(prediction_endpoint, files={"file": uploaded_file})
        
        if response.status_code == 200:
            response_bytes = BytesIO(response.content)
            response_df = pd.read_csv(response_bytes)

            # Provide download button for predictions
            st.download_button(
                label="📥 Download Predictions",
                data=response_bytes,
                file_name="Predictions.csv",
                key="result_download_button",
            )
        else:
            st.error(f"⚠️ Error processing the uploaded file. Server response: {response.text}")

    else:
        if user_input.strip():  
            response = requests.post(prediction_endpoint, json={"text": user_input})
            
            if response.status_code == 200:
                try:
                    response_data = response.json()

                    if "prediction" in response_data:
                        st.success(f"✅ **Predicted Sentiment:** {response_data['prediction']}")
                    else:
                        st.error(f"⚠️ Unexpected response from API: {response_data}")

                except Exception as e:
                    st.error(f"⚠️ Error parsing response: {str(e)}")

            else:
                st.error(f"⚠️ Error in prediction. Server response: {response.text}")

        else:
            st.warning("⚠️ Please enter text for prediction.")

# Footer Section
st.markdown(
    """
    <div class="footer">
        <p><b>A Team Effort Towards Innovation</b> | 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)

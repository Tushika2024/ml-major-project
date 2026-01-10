import streamlit as st
import requests
from src.exception import CustomException
import sys

# 1. Page Config
st.set_page_config(page_title="ML Connector", layout="centered")

# 2. Custom CSS Injection (Modified for high visibility)
st.markdown("""
    <style>
    /* Force background color of the whole page */
    .stApp {
        background-color: #f0f2f6 !important;
    }

    /* Style the Form - Added a border to make it visible */
    [data-testid="stForm"] {
        background-color: #ffffff !important;
        padding: 40px !important;
        border-radius: 20px !important;
        border: 2px solid #1e3a8a !important; /* Blue border to prove styling works */
        box-shadow: 10px 10px 30px rgba(0, 0, 0, 0.1) !important;
    }

    /* Style the Button */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #1e3a8a, #3b82f6) !important;
        color: white !important;
        border: none !important;
        height: 50px !important;
        font-size: 20px !important;
    }
    
    /* Center text for headers */
    .stMarkdown h1, .stMarkdown h5 {
        text-align: center;
        color: #1e3a8a;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Caching Function
@st.cache_data(show_spinner=False)
def get_prediction(payload):
    try:
        response = requests.post("http://127.0.0.1:5000/predictdata", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Server error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# 4. UI
st.title("🎓 Student Performance Predictor")

with st.form("ml_form"):
    st.markdown("##### 📝 Enter Academic Records")

    gender = st.selectbox('Gender', ['Male', 'Female'])
    ethnicity = st.selectbox('Ethnicity', ['group A', 'group B', 'group C', 'group D', 'group E'])
    parent_ed = st.selectbox('Parental Education', ['High School', "Associate's Degree", "Bachelor's Degree", "Master's Degree", 'Some College', 'Some High School'])
    lunch = st.selectbox('Lunch Type', ['Standard', 'Free/Reduced'])
    test_prep = st.selectbox('Test Preparation', ['None', 'Completed'])
    reading_score = st.number_input('Reading Score', 0.0, 100.0, 50.0)
    writing_score = st.number_input('Writing Score', 0.0, 100.0, 50.0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("PREDICT SCORE")

    if submitted:
        payload = {
            "gender": gender.lower(),
            "ethnicity": ethnicity,
            "parental_level_of_education": parent_ed.lower(),
            "lunch": lunch.lower(),
            "test_preparation_course": test_prep.lower(),
            "reading_score": reading_score,
            "writing_score": writing_score
        }
        
        with st.spinner("Predicting the score..."):
            # IMPORTANT: Call the cached function here!
            res_data = get_prediction(payload)
            
            if "error" in res_data:
                st.error(res_data["error"])
            else:
                st.divider()
                st.success("Analysis Complete!")
                st.metric(label="Predicted Math Score", value=res_data['result'])
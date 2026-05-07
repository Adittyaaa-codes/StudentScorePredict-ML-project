import streamlit as st
import requests

st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
    .main { padding: 1rem; }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 1.1rem;
        padding: 0.6rem;
        border-radius: 8px;
        border: none;
        margin-top: 1rem;
    }
    .stButton > button:hover { background-color: #45a049; }
    .result-box {
        background-color: #f0f9ff;
        border-left: 5px solid #4CAF50;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1.5rem;
    }
    @media (max-width: 768px) {
        .main { padding: 0.5rem; }
        h1 { font-size: 1.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Student Score Predictor")
st.markdown("Fill in the details below to predict the exam score.")

st.subheader("📋 Personal Info")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=15, max_value=35, value=20)
with col2:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

gender_Male = 1 if gender == "Male" else 0
gender_Other = 1 if gender == "Other" else 0

col3, col4 = st.columns(2)
with col3:
    part_time_job_input = st.selectbox("Part-Time Job", ["No", "Yes"])
with col4:
    extracurricular_input = st.selectbox("Extracurricular Activities", ["No", "Yes"])

part_time_job = 1 if part_time_job_input == "Yes" else 0
extracurricular_participation_Yes = 1 if extracurricular_input == "Yes" else 0

st.subheader("📚 Study Habits")
col5, col6 = st.columns(2)
with col5:
    study_hours_per_day = st.slider("Study Hours / Day", 0.0, 12.0, 5.0, step=0.5)
with col6:
    attendance_percentage = st.slider("Attendance %", 0.0, 100.0, 80.0, step=1.0)

col7, col8 = st.columns(2)
with col7:
    social_media_hours = st.slider("Social Media Hours / Day", 0.0, 10.0, 2.0, step=0.5)
with col8:
    netflix_hours = st.slider("Netflix Hours / Day", 0.0, 10.0, 1.5, step=0.5)

st.subheader("🏃 Lifestyle")
col9, col10 = st.columns(2)
with col9:
    sleep_hours = st.slider("Sleep Hours / Day", 3.0, 12.0, 7.0, step=0.5)
with col10:
    exercise_frequency = st.slider("Exercise Days / Week", 0, 7, 3)

col11, col12 = st.columns(2)
with col11:
    mental_health_rating = st.slider("Mental Health Rating (1-10)", 1, 10, 7)
with col12:
    diet_quality_input = st.selectbox("Diet Quality", ["Poor", "Fair", "Good"])

diet_map = {"Poor": 0, "Fair": 1, "Good": 2}
diet_quality = diet_map[diet_quality_input]

st.subheader("🏠 Background")
col13, col14 = st.columns(2)
with col13:
    parental_edu_input = st.selectbox(
        "Parental Education",
        ["High School", "Bachelor", "Master"]
    )
with col14:
    internet_input = st.selectbox("Internet Quality", ["Poor", "Average", "Good"])

edu_map = {"High School": 0, "Bachelor": 1, "Master": 2}
internet_map = {"Poor": 0, "Average": 1, "Good": 2}
parental_education_level = edu_map[parental_edu_input]
internet_quality = internet_map[internet_input]

if st.button("🔮 Predict Score"):
    payload = {
        "age": age,
        "study_hours_per_day": study_hours_per_day,
        "social_media_hours": social_media_hours,
        "netflix_hours": netflix_hours,
        "part_time_job": part_time_job,
        "attendance_percentage": attendance_percentage,
        "sleep_hours": sleep_hours,
        "diet_quality": diet_quality,
        "exercise_frequency": float(exercise_frequency),
        "parental_education_level": parental_education_level,
        "internet_quality": internet_quality,
        "mental_health_rating": float(mental_health_rating),
        "gender_Male": gender_Male,
        "gender_Other": gender_Other,
        "extracurricular_participation_Yes": extracurricular_participation_Yes
    }

    try:
        response = requests.post("https://studentscorepredict-ml-project-2.onrender.com/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            score = result["predicted_exam_score"]
            grade = result["grade"]
            interpretation = result["interpretation"]

            st.markdown(f"""
            <div class="result-box">
                <h2>📊 Prediction Result</h2>
                <h1 style="color:#4CAF50; font-size:3rem;">{score}</h1>
                <p style="font-size:1.2rem;">Grade: <strong>{grade}</strong></p>
                <p style="color:#555;">{interpretation}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Server error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the prediction server. Make sure it's accessible at https://studentscorepredict-ml-project-2.onrender.com")
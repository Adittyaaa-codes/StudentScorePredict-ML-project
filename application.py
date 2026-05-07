from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import pickle
import numpy as np

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, scaler
    with open("models/linreg.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    yield


application = FastAPI(
    title="Student Score Predictor",
    description="Predict exam score based on student habits",
    version="1.0.0",
    lifespan=lifespan
)

app = application

class StudentInput(BaseModel):
    age: float
    study_hours_per_day: float
    social_media_hours: float
    netflix_hours: float
    part_time_job: int                    
    attendance_percentage: float
    sleep_hours: float
    diet_quality: int                     
    exercise_frequency: float
    parental_education_level: int         
    internet_quality: int                 
    mental_health_rating: float
    gender_Male: int                     
    gender_Other: int                     
    extracurricular_participation_Yes: int  


@app.get("/")
def root():
    return {"message": "Student Score Predictor is running 🎓"}

@app.post("/predict")
def predict(data: StudentInput):
    features = np.array([[
        data.age,
        data.study_hours_per_day,
        data.social_media_hours,
        data.netflix_hours,
        data.part_time_job,
        data.attendance_percentage,
        data.sleep_hours,
        data.diet_quality,
        data.exercise_frequency,
        data.parental_education_level,
        data.internet_quality,
        data.mental_health_rating,
        data.gender_Male,
        data.gender_Other,
        data.extracurricular_participation_Yes
    ]])

    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    prediction = float(np.clip(prediction, 0, 100))

    return {
        "predicted_exam_score": round(float(prediction), 2),
        "grade": get_grade(prediction),
        "interpretation": get_interpretation(prediction)
    }

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

def get_grade(score: float) -> str:
    if score >= 90: return "A"
    elif score >= 75: return "B"
    elif score >= 60: return "C"
    elif score >= 45: return "D"
    else: return "F"

def get_interpretation(score: float) -> str:
    if score >= 90: return "Excellent performance"
    elif score >= 75: return "Good performance"
    elif score >= 60: return "Average performance"
    elif score >= 45: return "Below average"
    else: return "Needs significant improvement"
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

model = joblib.load(os.path.join("model", "model.pkl"))

# Initialize FastAPI app
app = FastAPI(title="Housing Price Predictor")

# Input schema
class PredictionInput(BaseModel):
    area: float

# Health check endpoint
@app.get("/")
def home():
    return {"message": "FastAPI server is running!"}

# Prediction endpoint
@app.post("/predict")
def predict(data: PredictionInput):
    area = data.area
    prediction = model.predict([[area]])[0]
    return {"prediction": round(prediction, 2)}  # rounded for readability

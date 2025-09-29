from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import logging

# Load ML model
model = joblib.load(os.path.join("model", "model.pkl"))

# Initialize FastAPI app
app = FastAPI(title="Housing Price Predictor")

# Setup logging
logging.basicConfig(
    filename="predictions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
    
    # Log the input and prediction
    logging.info(f"Input: {data.dict()}, Prediction: {prediction}")
    
    return {"prediction": round(prediction, 2)}

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from model import AnomalyDetector
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(filename='anomalies.log', level=logging.INFO)

app = FastAPI()

# CORS middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = AnomalyDetector()

class Query(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    """
    Train the model on startup.
    In a real-world scenario, this would be a separate, offline process.
    """
    detector.train()

@app.post("/predict")
async def predict(query: Query):
    """
    Predict if a query is an anomaly.
    """
    feature = np.array([[len(query.query)]])
    is_anomaly = detector.predict(feature)
    if is_anomaly:
        logging.info(f"Anomalous query detected: {query.query}")
    return {"query": query.query, "is_anomaly": bool(is_anomaly)}

@app.get("/anomalies")
async def get_anomalies():
    """
    Retrieve the list of detected anomalies.
    """
    try:
        with open("anomalies.log", "r") as f:
            anomalies = f.readlines()
        return {"anomalies": anomalies}
    except FileNotFoundError:
        return {"anomalies": []}

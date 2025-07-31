from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import logging
import requests
import json
from typing import List, Dict, Any

# --- Configuration ---
logging.basicConfig(filename='anomalies.log', level=logging.INFO)
POLICY_SERVICE_URL = "http://localhost:8005"

# --- In-Memory Storage ---
anomalies_store: List[dict] = []
policies_store: Dict[str, dict] = {}

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Anomaly Detection Service",
    description="Uses vector search and a policy engine to detect anomalous events."
)

# --- CORS Middleware ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ML Model and Vector DB Initialization ---
model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="events")

# --- Pydantic Models ---
class GenericEvent(BaseModel):
    user_id: str
    timestamp: str
    event_type: str
    data: Dict[str, Any]

class HistoricalData(BaseModel):
    events: list[GenericEvent]

# --- WebSocket Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# --- Helper Functions ---
def event_to_string(event: GenericEvent) -> str:
    data_str = ", ".join([f"{k}: {v}" for k, v in event.data.items()])
    return f"User {event.user_id} triggered a {event.event_type} event with data: {data_str}"

async def load_policies():
    """Loads policies from the policy service."""
    try:
        response = requests.get(f"{POLICY_SERVICE_URL}/policies")
        response.raise_for_status()
        policies = response.json()
        for policy in policies:
            policies_store[policy['id']] = policy
        logging.info(f"Successfully loaded {len(policies)} policies.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to load policies: {e}")

# --- API Endpoints ---
@app.on_event("startup")
async def startup_event():
    await load_policies()

@app.post("/load-historical-data")
def load_historical_data(data: HistoricalData):
    try:
        collection.add(
            embeddings=model.encode([event_to_string(e) for e in data.events]).tolist(),
            documents=[event_to_string(e) for e in data.events],
            metadatas=[e.dict() for e in data.events],
            ids=[f"{e.user_id}-{e.timestamp}-{i}" for i, e in enumerate(data.events)]
        )
        return {"message": f"Successfully loaded {len(data.events)} historical records."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-event")
async def check_event(event: GenericEvent):
    is_anomaly = False
    reason = ""

    # 1. Vector Search for similar past events
    try:
        query_embedding = model.encode(event_to_string(event)).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={"user_id": event.user_id, "event_type": event.event_type}
        )
        distances = results['distances'][0]
        if not distances or np.mean(distances) > 0.4: # Higher threshold for general deviation
            is_anomaly = True
            reason = "Event deviates significantly from user's past behavior."

    except Exception as e:
        logging.warning(f"Vector search failed for user {event.user_id}: {e}")

    # 2. Policy-based checks
    for policy in policies_store.values():
        if policy['data_type'] == event.event_type:
            for rule in policy['rules']:
                field = rule['field']
                operator = rule['operator']
                value = rule['value']
                
                if field in event.data:
                    event_value = event.data[field]
                    if operator == ">" and event_value > value:
                        is_anomaly = True
                        reason = f"Policy Violated: {policy['name']} - {field} ({event_value}) > {value}."
                    elif operator == "<" and event_value < value:
                        is_anomaly = True
                        reason = f"Policy Violated: {policy['name']} - {field} ({event_value}) < {value}."

    if is_anomaly:
        anomaly_data = {"event": event.dict(), "reason": reason}
        anomalies_store.append(anomaly_data)
        logging.info(json.dumps(anomaly_data))
        await manager.broadcast(json.dumps(anomaly_data))
        try:
            # Assuming compliance service is updated to handle generic events
            requests.post("http://localhost:8002/report_anomaly", json=anomaly_data)
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to report anomaly: {e}")
        return {"is_anomaly": True, **anomaly_data}
        
    return {"is_anomaly": False, "event": event.dict()}

@app.get("/anomalies")
async def get_anomalies():
    return {"anomalies": anomalies_store}

@app.websocket("/ws/anomalies")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
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

# --- In-Memory Storage ---
anomalies_store: List[dict] = []

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Anomaly Detection Service",
    description="Uses vector search and simulated RAG to detect anomalous banking transactions and loan applications."
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
collection = chroma_client.get_or_create_collection(name="transactions")

# --- Pydantic Models ---
class GenericTransaction(BaseModel):
    user_id: str
    timestamp: str
    data: Dict[str, Any]

class HistoricalData(BaseModel):
    transactions: list[GenericTransaction]

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
def transaction_to_string(transaction: GenericTransaction) -> str:
    data_str = ", ".join([f"{k}: {v}" for k, v in transaction.data.items()])
    return f"User {transaction.user_id} performed an action with the following data: {data_str}"

# --- API Endpoints ---
@app.post("/load-historical-data")
def load_historical_data(data: HistoricalData):
    try:
        collection.add(
            embeddings=model.encode([transaction_to_string(t) for t in data.transactions]).tolist(),
            documents=[transaction_to_string(t) for t in data.transactions],
            metadatas=[t.dict() for t in data.transactions],
            ids=[f"{t.user_id}-{t.timestamp}-{i}" for i, t in enumerate(data.transactions)]
        )
        return {"message": f"Successfully loaded {len(data.transactions)} historical records."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-transaction")
async def check_transaction(transaction: GenericTransaction):
    try:
        query_embedding = model.encode(transaction_to_string(transaction)).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={"user_id": transaction.user_id}
        )
        
        distances = results['distances'][0]
        retrieved_docs = results['metadatas'][0]
        
        is_anomaly = False
        reason = ""

        if not distances or np.mean(distances) > 0.3:
            is_anomaly = True
            if not retrieved_docs:
                reason = "No historical data found for this user."
            else:
                # Generic RAG-style reasoning
                reason = "Action deviates significantly from user's established patterns."

    except Exception as e:
        is_anomaly = True
        reason = f"Error during analysis: {e}"

    if is_anomaly:
        anomaly_data = {"transaction": transaction.dict(), "reason": reason}
        anomalies_store.append(anomaly_data)
        logging.info(json.dumps(anomaly_data))
        await manager.broadcast(json.dumps(anomaly_data))
        try:
            requests.post("http://localhost:8002/report_anomaly", json=anomaly_data)
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to report anomaly: {e}")
        return {"is_anomaly": True, **anomaly_data}
        
    return {"is_anomaly": False, "transaction": transaction.dict()}

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
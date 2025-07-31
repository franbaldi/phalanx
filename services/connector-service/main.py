
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json
import os
from fastapi.middleware.cors import CORSMiddleware

# --- Configuration ---
DB_FILE = "connectors.json"

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Connector Service",
    description="Manages data source connector configurations for the Phalanx platform."
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

# --- Pydantic Models ---
class Connector(BaseModel):
    id: str
    name: str
    type: str # e.g., "mongodb", "postgresql"
    connection_string: str

# --- Helper Functions ---
def load_connectors() -> Dict[str, Connector]:
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        data = json.load(f)
        return {item['id']: Connector(**item) for item in data}

def save_connectors(connectors: Dict[str, Connector]):
    with open(DB_FILE, "w") as f:
        json.dump([c.dict() for c in connectors.values()], f, indent=2)

# --- API Endpoints ---
@app.get("/connectors", response_model=List[Connector])
def get_connectors():
    """Retrieves a list of all configured connectors."""
    connectors = load_connectors()
    return list(connectors.values())

@app.post("/connectors", response_model=Connector)
def create_connector(connector: Connector):
    """Creates a new data source connector."""
    connectors = load_connectors()
    if connector.id in connectors:
        raise HTTPException(status_code=400, detail="Connector with this ID already exists.")
    connectors[connector.id] = connector
    save_connectors(connectors)
    return connector

@app.delete("/connectors/{connector_id}", status_code=204)
def delete_connector(connector_id: str):
    """Deletes a connector by its ID."""
    connectors = load_connectors()
    if connector_id not in connectors:
        raise HTTPException(status_code=404, detail="Connector not found.")
    del connectors[connector_id]
    save_connectors(connectors)
    return


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os
from fastapi.middleware.cors import CORSMiddleware

# --- Configuration ---
DB_FILE = "policies.json"

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Policy Service",
    description="Manages and evaluates DORA-compliant policies for the Phalanx platform."
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
class Policy(BaseModel):
    id: str
    name: str
    description: str
    data_type: str # e.g., "transaction", "loan_application"
    rules: List[Dict[str, Any]]

# --- Helper Functions ---
def load_policies() -> Dict[str, Policy]:
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        data = json.load(f)
        return {item['id']: Policy(**item) for item in data}

def save_policies(policies: Dict[str, Policy]):
    with open(DB_FILE, "w") as f:
        json.dump([p.dict() for p in policies.values()], f, indent=2)

# --- API Endpoints ---
@app.get("/policies", response_model=List[Policy])
def get_policies():
    """Retrieves a list of all configured policies."""
    policies = load_policies()
    return list(policies.values())

@app.post("/policies", response_model=Policy)
def create_policy(policy: Policy):
    """Creates a new policy."""
    policies = load_policies()
    if policy.id in policies:
        raise HTTPException(status_code=400, detail="Policy with this ID already exists.")
    policies[policy.id] = policy
    save_policies(policies)
    return policy

@app.delete("/policies/{policy_id}", status_code=204)
def delete_policy(policy_id: str):
    """Deletes a policy by its ID."""
    policies = load_policies()
    if policy_id not in policies:
        raise HTTPException(status_code=404, detail="Policy not found.")
    del policies[policy_id]
    save_policies(policies)
    return

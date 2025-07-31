#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Helper Functions ---
kill_process_on_port() {
  PORT=$1
  echo "Checking for process on port $PORT..."
  PID=$(lsof -t -i:$PORT)
  if [ -n "$PID" ]; then
    echo "Killing process $PID on port $PORT..."
    kill -9 $PID
  else
    echo "No process found on port $PORT."
  fi
}

install_python_dependencies() {
  if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
  fi
  echo "Activating virtual environment and installing dependencies..."
  source .venv/bin/activate
  pip install -r requirements.txt
  deactivate
}

wait_for_service() {
  URL=$1
  echo "Waiting for service at $URL to be ready..."
  until curl -s -f -o /dev/null "$URL"
  do
    echo "Service not yet available, waiting..."
    sleep 5
  done
  echo "Service is ready!"
}

wait_for_mongo() {
  HOST=$1
  PORT=$2
  echo "Waiting for MongoDB at $HOST:$PORT to be ready..."
  until python3 -c "
import socket
import sys
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('$HOST', $PORT))
    s.close()
    sys.exit(0)
except socket.error:
    sys.exit(1)
" > /dev/null 2>&1
  do
    echo "MongoDB not yet available, waiting..."
    sleep 5
  done
  echo "MongoDB is ready!"
}

populate_mongodb() {
  echo "Populating MongoDB with dummy data..."
  python3 -c '''
from pymongo import MongoClient
import datetime
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["phalanx_db"]

# Transactions Collection
transactions = db["transactions"]
transactions.drop()
for i in range(100):
    transactions.insert_one({
        "user_id": f"user_{random.randint(1, 10)}",
        "amount": round(random.uniform(10, 1000), 2),
        "currency": random.choice(["USD", "EUR", "GBP"]),
        "recipient": f"merchant_{random.randint(1, 20)}",
        "country": random.choice(["USA", "GBR", "DEU", "FRA"]),
        "timestamp": datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
    })
print(f"Inserted {transactions.count_documents({})} transactions.")

# Loan Applications Collection
loan_applications = db["loan_applications"]
loan_applications.drop()
for i in range(50):
    loan_applications.insert_one({
        "user_id": f"user_{random.randint(1, 10)}",
        "loan_amount": round(random.uniform(5000, 100000), 2),
        "credit_score": random.randint(300, 850),
        "timestamp": datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
    })
print(f"Inserted {loan_applications.count_documents({})} loan applications.")

client.close()
'''
}

# --- Frontend ---
echo "--- Setting up Dashboard Frontend ---"
kill_process_on_port 3000
cd dashboard-frontend
echo "Installing frontend dependencies..."
npm install
echo "Starting frontend development server..."
npm start &
cd ..

# --- Anomaly Detection Service ---
echo "--- Setting up Anomaly Detection Service ---"
kill_process_on_port 8000
cd services/anomaly-detection-service
install_python_dependencies
echo "Starting anomaly detection service..."
source .venv/bin/activate
uvicorn main:app --reload --port 8000 &
sleep 5
cd ../..

# --- Database Integration Service ---
echo "--- Setting up Database Integration Service ---"
kill_process_on_port 8001
cd services/database-integration-service
install_python_dependencies
echo "Starting database integration service..."
source .venv/bin/activate
uvicorn main:app --reload --port 8001 &
sleep 5
cd ../..

# --- Compliance Automation Service ---
echo "--- Setting up Compliance Automation Service ---"
kill_process_on_port 8002
cd services/compliance-automation-service
install_python_dependencies
echo "Starting compliance automation service..."
source .venv/bin/activate
uvicorn main:app --reload --port 8002 &
sleep 5
cd ../..

# --- Connector Service ---
echo "--- Setting up Connector Service ---"
kill_process_on_port 8004
cd services/connector-service
install_python_dependencies
echo "Starting connector service..."
source .venv/bin/activate
uvicorn main:app --reload --port 8004 &
sleep 5
cd ../..

# --- Policy Service ---
echo "--- Setting up Policy Service ---"
kill_process_on_port 8005
cd services/policy-service
install_python_dependencies
echo "Starting policy service..."
source .venv/bin/activate
uvicorn main:app --reload --port 8005 &
cd ../..

# --- Database Provisioning Service ---
echo "--- Setting up Database Provisioning Service ---
kill_process_on_port 8003
cd services/database-provisioning-service
echo "Building and running database provisioning service container..."
docker build -t database-provisioning-service .
docker rm -f database-provisioning-service || true
docker run -d --name database-provisioning-service -p 8003:8003 -v /var/run/docker.sock:/var/run/docker.sock database-provisioning-service
cd ../..

# --- MongoDB Service ---
echo "--- Setting up MongoDB Service ---"
kill_process_on_port 27017
docker rm -f phalanx-mongodb || true
docker run -d --name phalanx-mongodb -p 27017:27017 mongo:latest

echo "--- All services are starting up ---"

# Wait for MongoDB to be ready
wait_for_mongo "localhost" 27017

# Populate MongoDB with dummy data
populate_mongodb

# Wait for all services to be ready
wait_for_service "http://localhost:8000/docs"
wait_for_service "http://localhost:8001/docs"
wait_for_service "http://localhost:8002/docs"
wait_for_service "http://localhost:8004/docs"
wait_for_service "http://localhost:8005/docs"

echo "--- Running DORA Incident Simulator ---"
cd services/anomaly-detection-service
source .venv/bin/activate
python3 dora_incident_simulator.py
cd ../..

echo "--- Simulation finished ---"

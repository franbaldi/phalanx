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
cd ../..

# --- Database Integration Service ---
echo "--- Setting up Database Integration Service ---"
kill_process_on_port 8001
cd services/database-integration-service
install_python_dependencies
echo "Starting database integration service..."
source .venv/bin/activate
uvicorn main:app --reload --port 8001 &
cd ../..

# --- Compliance Automation Service ---
echo "--- Setting up Compliance Automation Service ---"
kill_process_on_port 8002
cd services/compliance-automation-service
install_python_dependencies
echo "Starting compliance automation service..."
source .venv/bin/activate
uvicorn main:app --reload --port 8002 &
cd ../..

# --- Connector Service ---
echo "--- Setting up Connector Service ---"
kill_process_on_port 8004
cd services/connector-service
install_python_dependencies
echo "Starting connector service..."
source .venv/bin/activate
uvicorn main:app --reload --port 8004 &
cd ../..

# --- Database Provisioning Service ---
echo "--- Setting up Database Provisioning Service ---"
kill_process_on_port 8003
cd services/database-provisioning-service
echo "Building and running database provisioning service container..."
docker build -t database-provisioning-service .
docker rm -f database-provisioning-service || true
docker run -d --name database-provisioning-service -p 8003:8003 -v /var/run/docker.sock:/var/run/docker.sock database-provisioning-service
cd ../..

echo "--- All services are starting up ---"

# --- Run DORA Incident Simulator ---
wait_for_service "http://localhost:8000/docs"

echo "--- Running DORA Incident Simulator ---"
cd services/anomaly-detection-service
source .venv/bin/activate
python3 dora_incident_simulator.py
cd ../..

echo "--- Simulation finished ---"

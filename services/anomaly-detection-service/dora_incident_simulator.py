import requests
import time

# --- Configuration ---
DB_INTEGRATION_API_URL = "http://localhost:8001"
COMPLIANCE_API_URL = "http://localhost:8002"

# --- Main Simulation Logic ---
def run_simulation():
    """Runs the DORA incident simulation."""
    print("--- Starting DORA Incident Simulation ---")

    # 1. Connect to MongoDB for transactions
    print("\nConnecting to MongoDB for transaction data...")
    transaction_db_connection = {
        "db_type": "mongodb",
        "host": "localhost",
        "port": 27017,
        "user": "",
        "password": "",
        "dbname": "phalanx_db",
        "collection_name": "transactions"
    }
    try:
        response = requests.post(f"{DB_INTEGRATION_API_URL}/connect", json=transaction_db_connection)
        response.raise_for_status()
        print(response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to MongoDB for transactions: {e}")

    # 2. Connect to MongoDB for loan applications
    print("\nConnecting to MongoDB for loan application data...")
    loan_app_db_connection = {
        "db_type": "mongodb",
        "host": "localhost",
        "port": 27017,
        "user": "",
        "password": "",
        "dbname": "phalanx_db",
        "collection_name": "loan_applications"
    }
    try:
        response = requests.post(f"{DB_INTEGRATION_API_URL}/connect", json=loan_app_db_connection)
        response.raise_for_status()
        print(response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to MongoDB for loan applications: {e}")

    # 3. Generate monthly report
    print("\nGenerating monthly DORA report...")
    try:
        response = requests.post(f"{COMPLIANCE_API_URL}/generate_monthly_report")
        response.raise_for_status()
        print(response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error generating monthly report: {e}")

    print("--- Simulation finished ---")

if __name__ == "__main__":
    run_simulation()

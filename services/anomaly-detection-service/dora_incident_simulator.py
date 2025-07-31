

import requests
import random
import time
from datetime import datetime, timedelta

# --- Configuration ---
API_URL = "http://localhost:8000"

# --- Helper Functions ---
def generate_normal_transaction(user_id):
    """Generates a typical, non-anomalous transaction."""
    return {
        "user_id": user_id,
        "amount": round(random.uniform(10, 200), 2),
        "currency": "USD",
        "recipient": f"Merchant_{random.randint(1, 10)}",
        "country": "USA",
        "timestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
    }

def generate_anomalous_transaction(user_id):
    """Generates a transaction that should be flagged as an anomaly."""
    return {
        "user_id": user_id,
        "amount": round(random.uniform(5000, 10000), 2), # Unusually large amount
        "currency": "EUR",
        "recipient": "Offshore_Account_123",
        "country": "Cayman Islands", # Suspicious location
        "timestamp": datetime.now().isoformat()
    }

# --- Main Simulation Logic ---
def run_simulation():
    """Runs the DORA incident simulation."""
    print("--- Starting DORA Incident Simulation ---")

    # 1. Load historical data for two users
    print("Loading historical transaction data...")
    historical_data = {
        "transactions": [generate_normal_transaction("user_123") for _ in range(50)] + \
                        [generate_normal_transaction("user_456") for _ in range(50)]
    }
    try:
        response = requests.post(f"{API_URL}/load-historical-data", json=historical_data)
        response.raise_for_status()
        print(response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error loading historical data: {e}")
        return

    # 2. Simulate new transactions
    print("\n--- Simulating New Transactions ---")
    for i in range(10):
        # A normal transaction for user_123
        normal_transaction = generate_normal_transaction("user_123")
        print(f"Sending normal transaction for user_123: {normal_transaction['amount']} USD")
        response = requests.post(f"{API_URL}/check-transaction", json=normal_transaction)
        print(f"-> Response: {response.json()}")
        time.sleep(2)

        # An anomalous transaction for user_456
        if i % 3 == 0:
            anomalous_transaction = generate_anomalous_transaction("user_456")
            print(f"Sending ANOMALOUS transaction for user_456: {anomalous_transaction['amount']} EUR to {anomalous_transaction['country']}")
            response = requests.post(f"{API_URL}/check-transaction", json=anomalous_transaction)
            print(f"-> Response: {response.json()}")
            time.sleep(2)

if __name__ == "__main__":
    run_simulation()


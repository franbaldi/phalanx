

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

def generate_normal_loan_application(user_id):
    """Generates a typical, non-anomalous loan application."""
    return {
        "user_id": user_id,
        "loan_amount": round(random.uniform(10000, 50000), 2),
        "property_value": round(random.uniform(100000, 500000), 2),
        "credit_score": random.randint(650, 850),
        "timestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
    }

def generate_anomalous_loan_application(user_id):
    """Generates a loan application that should be flagged as an anomaly."""
    return {
        "user_id": user_id,
        "loan_amount": round(random.uniform(200000, 500000), 2), # Unusually high loan amount
        "property_value": round(random.uniform(100000, 200000), 2),
        "credit_score": random.randint(300, 600), # Low credit score
        "timestamp": datetime.now().isoformat()
    }

# --- Main Simulation Logic ---
def run_simulation():
    """Runs the DORA incident simulation."""
    print("--- Starting DORA Incident Simulation ---")

    # 1. Load historical data for two users
    print("Loading historical transaction data...")
    historical_transactions = {
        "transactions": [generate_normal_transaction("user_123") for _ in range(50)] + \
                        [generate_normal_transaction("user_456") for _ in range(50)]
    }
    try:
        response = requests.post(f"{API_URL}/load-historical-data", json=historical_transactions)
        response.raise_for_status()
        print(response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error loading historical transaction data: {e}")
        return

    print("Loading historical loan application data...")
    historical_loan_applications = {
        "transactions": [generate_normal_loan_application("user_789") for _ in range(50)]
    }
    try:
        response = requests.post(f"{API_URL}/load-historical-data", json=historical_loan_applications)
        response.raise_for_status()
        print(response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error loading historical loan application data: {e}")
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

        # A normal loan application for user_789
        normal_loan_application = generate_normal_loan_application("user_789")
        print(f"Sending normal loan application for user_789: {normal_loan_application['loan_amount']} USD")
        response = requests.post(f"{API_URL}/check-transaction", json=normal_loan_application)
        print(f"-> Response: {response.json()}")
        time.sleep(2)

        # An anomalous loan application for user_789
        if i % 3 == 0:
            anomalous_loan_application = generate_anomalous_loan_application("user_789")
            print(f"Sending ANOMALOUS loan application for user_789: {anomalous_loan_application['loan_amount']} USD")
            response = requests.post(f"{API_URL}/check-transaction", json=anomalous_loan_application)
            print(f"-> Response: {response.json()}")
            time.sleep(2)

if __name__ == "__main__":
    run_simulation()


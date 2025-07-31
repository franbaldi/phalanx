import requests
import time
import random
from datetime import datetime, timedelta

# --- Configuration ---
DB_INTEGRATION_API_URL = "http://localhost:8001"
COMPLIANCE_API_URL = "http://localhost:8002"
ANOMALY_DETECTION_API_URL = "http://localhost:8000"
POLICY_SERVICE_URL = "http://localhost:8005"

# --- Helper Functions for generating new event types ---
def generate_data_record(user_id, age_in_years):
    return {
        "user_id": user_id,
        "timestamp": (datetime.now() - timedelta(days=age_in_years * 365)).isoformat(),
        "event_type": "data_record",
        "data": {
            "record_id": f"rec_{random.randint(1000, 9999)}",
            "data_type": "customer_info",
            "age_in_years": age_in_years
        }
    }

def generate_system_config_change(user_id, authorized=True, change_type="minor"):
    return {
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "event_type": "system_config",
        "data": {
            "config_item": f"cfg_{random.randint(100, 999)}",
            "change_description": "System parameter update",
            "authorized_approver": authorized,
            "change_type": change_type
        }
    }

# --- Main Simulation Logic ---
def run_simulation():
    """Runs the DORA incident simulation."""
    print("--- Starting DORA Incident Simulation ---")

    # 0. Create policies (ensure they are loaded in policy service)
    print("Creating example policies...")
    policies_to_create = [
        {
            "id": "data-retention-policy",
            "name": "Data Retention Policy",
            "description": "Flags data older than 7 years for GDPR compliance.",
            "data_type": "data_record",
            "rules": [
                {
                    "field": "age_in_years",
                    "operator": ">",
                    "value": 7
                }
            ]
        },
        {
            "id": "unauthorized-config-change",
            "name": "Unauthorized Configuration Change Policy",
            "description": "Flags any unauthorized changes to critical system configurations.",
            "data_type": "system_config",
            "rules": [
                {
                    "field": "authorized_approver",
                    "operator": "==",
                    "value": False
                },
                {
                    "field": "change_type",
                    "operator": "==",
                    "value": "critical"
                }
            ]
        }
    ]
    for policy_data in policies_to_create:
        try:
            response = requests.post(f"{POLICY_SERVICE_URL}/policies", json=policy_data)
            response.raise_for_status()
            print(f"Policy '{policy_data['name']}' created/updated successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error creating/updating policy '{policy_data['name']}': {e}")

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

    # 3. Simulate new data_record events
    print("\n--- Simulating Data Record Events ---")
    for i in range(5):
        # Normal data record
        normal_record = generate_data_record("user_data_1", random.randint(1, 5))
        print(f"Sending normal data record for user_data_1 (age: {normal_record['data']['age_in_years']} years)")
        requests.post(f"{ANOMALY_DETECTION_API_URL}/check-event", json=normal_record)
        time.sleep(1)

        # Anomalous data record (older than 7 years)
        if i == 2:
            anomalous_record = generate_data_record("user_data_2", random.randint(8, 15))
            print(f"Sending ANOMALOUS data record for user_data_2 (age: {anomalous_record['data']['age_in_years']} years)")
            requests.post(f"{ANOMALY_DETECTION_API_URL}/check-event", json=anomalous_record)
            time.sleep(1)

    # 4. Simulate new system_config events
    print("\n--- Simulating System Configuration Change Events ---")
    for i in range(5):
        # Normal config change
        normal_config = generate_system_config_change("admin_1", authorized=True, change_type="minor")
        print(f"Sending normal config change for admin_1 (authorized: {normal_config['data']['authorized_approver']})")
        requests.post(f"{ANOMALY_DETECTION_API_URL}/check-event", json=normal_config)
        time.sleep(1)

        # Anomalous config change (unauthorized critical change)
        if i == 3:
            anomalous_config = generate_system_config_change("admin_2", authorized=False, change_type="critical")
            print(f"Sending ANOMALOUS config change for admin_2 (authorized: {anomalous_config['data']['authorized_approver']}, type: {anomalous_config['data']['change_type']})")
            requests.post(f"{ANOMALY_DETECTION_API_URL}/check-event", json=anomalous_config)
            time.sleep(1)

    # 5. Generate monthly report
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
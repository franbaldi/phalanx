# Phalanx AI

Phalanx AI is a comprehensive security solution that uses machine learning to detect and report anomalies in database queries. It features a microservices-based architecture with a React-based frontend for monitoring and visualization.

## Architecture

The project is composed of the following main components:

- **Dashboard Frontend**: A React application that provides a user interface for monitoring and visualizing database security anomalies.
- **Backend Services**: A set of Python-based microservices that handle anomaly detection, compliance reporting, and database integration.

### Services

- **Anomaly Detection Service**: A FastAPI service that uses a machine learning model and a policy engine to detect anomalous events, including transactions, loan applications, data records, and system configuration changes.
- **Compliance Automation Service**: A FastAPI service that generates monthly DORA compliance reports based on collected anomalies, providing insights and remediation suggestions.
- **Database Integration Service**: A FastAPI service that connects to various databases (e.g., MongoDB) to ingest data and forward it as events to the Anomaly Detection Service.
- **Policy Service**: A FastAPI service that manages and evaluates DORA-compliant policies.
- **Connector Service**: A FastAPI service for managing external data source connections.

## Getting Started

To run the complete Phalanx AI project, use the provided `start_phalanx.sh` script. This script will:

- Kill any processes running on the required ports.
- Set up and start the Dashboard Frontend.
- Set up and start all Backend Services (Anomaly Detection, Compliance Automation, Database Integration, Policy, and Connector Services).
- Start a local MongoDB Docker container.
- Run the DORA Incident Simulator to generate sample data and trigger anomalies.

### Prerequisites

- Node.js and npm (for the frontend)
- Python 3.13 and pip (for the backend services)
- Docker (for MongoDB and Database Provisioning Service)

### Installation and Running

1.  **Make the startup script executable:**
    ```bash
    chmod +x start_phalanx.sh
    ```

2.  **Run the startup script:**
    ```bash
    ./start_phalanx.sh
    ```

    This script will start all necessary components. The Dashboard Frontend will be available at [http://localhost:3000](http://localhost:3000).

## Usage

Once all services and the frontend are running via `start_phalanx.sh`:

1.  **View Anomalies**: Open your browser to [http://localhost:3000](http://localhost:3000) to see detected anomalies in real-time.
2.  **Policy Management**: Navigate to the "Policies" section in the dashboard to view and manage DORA compliance policies.
3.  **Monthly Reports**: The `dora_incident_simulator.py` script will automatically trigger the generation of monthly DORA compliance reports. These reports provide a summary of anomalies, identified problems, and suggestions for remediation.
4.  **Data Ingestion**: The Database Integration Service connects to a local MongoDB instance (`phalanx_db`) and ingests data from `transactions` and `loan_applications` collections, forwarding them as events for anomaly detection.

## Extending Use Cases for DORA Compliance

Phalanx AI is designed to be extensible for various DORA compliance requirements. Here are some areas where you can further extend its capabilities:

-   **New Policy Types**: Define new policy types in `services/policy-service/policies.json` to cover additional compliance areas (e.g., access control, data encryption, third-party risk management).
-   **Enhanced Anomaly Detection**: Integrate more sophisticated machine learning models or external threat intelligence feeds into the Anomaly Detection Service (`services/anomaly-detection-service/main.py`) to identify complex attack patterns or compliance breaches.
-   **Business Continuity and Disaster Recovery (BCP/DR) Simulation**: Develop modules to simulate BCP/DR scenarios and assess the system's resilience. This could involve:
    -   **Automated Failover Testing**: Simulate primary system failures and verify failover to backup systems.
    -   **Data Recovery Verification**: Test data restoration processes and integrity checks.
    -   **Reporting on RTO/RPO**: Generate reports on Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) based on simulation results.
-   **Automated Remediation**: Implement automated or semi-automated remediation actions for detected anomalies or policy violations (e.g., blocking suspicious IP addresses, isolating compromised accounts).
-   **Integration with GRC Tools**: Connect Phalanx AI with existing Governance, Risk, and Compliance (GRC) platforms for centralized risk management and reporting.
-   **Audit Trail and Evidence Collection**: Enhance logging and data collection to provide comprehensive audit trails for regulatory compliance and forensic analysis.
-   **User Behavior Analytics (UBA)**: Implement UBA to detect anomalous user activities, such as unusual login times, access patterns, or data exfiltration attempts.
-   **Supply Chain Risk Management**: Extend monitoring to third-party service providers and their compliance posture, as required by DORA.

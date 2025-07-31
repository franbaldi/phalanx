# Phalanx AI

Phalanx AI is a comprehensive security solution that uses machine learning to detect and report anomalies in database queries. It features a microservices-based architecture with a React-based frontend for monitoring and visualization.

## Architecture

The project is composed of the following main components:

- **Dashboard Frontend**: A React application that provides a user interface for monitoring and visualizing database security anomalies.
- **Backend Services**: A set of Python-based microservices that handle anomaly detection, compliance reporting, and database integration.

### Services

- **Anomaly Detection Service**: A FastAPI service that uses a machine learning model to predict whether a given database query is an anomaly.
- **Compliance Automation Service**: A FastAPI service that generates compliance reports (e.g., DORA) based on the detected anomalies.
- **Database Integration Service**: A FastAPI service that simulates connections to various databases, captures queries, and forwards them to the Anomaly Detection Service.

## Getting Started

To run the complete Phalanx AI project, you will need to run each of the backend services and the frontend application.

### Prerequisites

- Node.js and npm (for the frontend)
- Python 3.13 and pip (for the backend services)

### Installation and Running

Below are the instructions for running each part of the project.

#### 1. Dashboard Frontend

The frontend is a React application.

1.  **Navigate to the frontend directory:**
    ```bash
    cd dashboard-frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm start
    ```
    The application will be available at [http://localhost:3000](http://localhost:3000).

#### 2. Backend Services

Each backend service is a self-contained FastAPI application. You will need to run each service in a separate terminal.

##### a. Anomaly Detection Service

This service detects anomalies in database queries.

1.  **Navigate to the service directory:**
    ```bash
    cd services/anomaly-detection-service
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the service:**
    ```bash
    uvicorn main:app --reload
    ```
    The service will run on `http://localhost:8000`.

##### b. Database Integration Service

This service captures and forwards database queries.

1.  **Navigate to the service directory:**
    ```bash
    cd services/database-integration-service
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the service:**
    ```bash
    uvicorn main:app --reload --port 8001
    ```
    The service will run on `http://localhost:8001`.

##### c. Compliance Automation Service

This service generates compliance reports.

1.  **Navigate to the service directory:**
    ```bash
    cd services/compliance-automation-service
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the service:**
    ```bash
    uvicorn main:app --reload --port 8002
    ```
    The service will run on `http://localhost:8002`.

## Usage

Once all the services and the frontend are running, you can use the application as follows:

1.  **Connect to a "database"** using the Database Integration Service endpoint (e.g., via a tool like `curl` or Postman).
2.  **Send "queries"** to the Database Integration Service. These queries will be analyzed by the Anomaly Detection Service.
3.  **View the results** in the Dashboard Frontend, which will display whether the queries are considered anomalies.
4.  If an anomaly is detected, the **Compliance Automation Service** will be notified to generate a report.

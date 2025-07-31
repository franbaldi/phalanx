# Compliance Automation Service

This service is responsible for generating compliance reports, such as DORA incident reports, based on detected anomalies.

## Running the service

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the service:
   ```
   uvicorn main:app --reload --port 8002
   ```

## API

### POST /report_anomaly

Receives an anomaly and generates a DORA incident report.

**Request body:**

```json
{
  "query": "DELETE FROM customers WHERE id = 1; DROP TABLE users;",
  "timestamp": "2025-07-26 10:00:00"
}
```

**Response:**

```json
{
  "message": "DORA report generated successfully."
}
```

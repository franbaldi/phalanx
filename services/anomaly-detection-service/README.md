# Anomaly Detection Service

This service provides a RESTful API for detecting anomalies in database queries.

## Running the service

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the service:
   ```
   uvicorn main:app --reload
   ```

## API

### POST /predict

Predicts if a query is an anomaly.

**Request body:**

```json
{
  "query": "SELECT * FROM users WHERE id = 1"
}
```

**Response:**

```json
{
  "query": "SELECT * FROM users WHERE id = 1",
  "is_anomaly": false
}
```

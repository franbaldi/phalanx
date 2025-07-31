# Database Integration Service

This service is responsible for connecting to various databases, capturing query/transaction logs, and forwarding them to the `anomaly-detection-service` for analysis.

## Running the service

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the service:
   ```
   uvicorn main:app --reload --port 8001
   ```

## API

### POST /connect

Simulates connecting to a database and starts capturing queries.

**Request body:**

```json
{
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "user": "user",
  "password": "password",
  "dbname": "mydb"
}
```

**Response:**

```json
{
  "message": "Successfully connected to postgresql at localhost"
}
```

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import httpx
import asyncio
import datetime

app = FastAPI()

class DBConnection(BaseModel):
    db_type: str
    host: str
    port: int
    user: str
    password: str
    dbname: str

async def forward_query(query: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://127.0.0.1:8000/predict", json={"query": query})
            response.raise_for_status()  # Raise an exception for bad status codes
            
            prediction = response.json()
            if prediction.get("is_anomaly"):
                await client.post(
                    "http://127.0.0.1:8002/report_anomaly",
                    json={
                        "query": query,
                        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    },
                )
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


async def simulate_queries(background_tasks: BackgroundTasks):
    queries = [
        "SELECT * FROM users WHERE id = 1",
        "SELECT * FROM products WHERE category = 'electronics'",
        "INSERT INTO orders (customer_id, product_id, quantity) VALUES (1, 2, 3)",
        "DELETE FROM customers WHERE id = 1; DROP TABLE users;"
    ]
    for query in queries:
        background_tasks.add_task(forward_query, query)
        await asyncio.sleep(5)

@app.post("/connect")
async def connect_to_db(db_connection: DBConnection, background_tasks: BackgroundTasks):
    """
    Simulates connecting to a database and capturing queries.
    """
    # In a real implementation, this would establish a connection
    # and start monitoring the database.
    background_tasks.add_task(simulate_queries, background_tasks)
    return {"message": f"Successfully connected to {db_connection.db_type} at {db_connection.host}"}

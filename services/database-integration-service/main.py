from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import Optional, Dict, Any
import httpx
import asyncio
from bson import json_util
import json

app = FastAPI()

class DBConnection(BaseModel):
    db_type: str
    host: str
    port: int
    user: Optional[str] = None
    password: Optional[str] = None
    dbname: str
    collection_name: str

@app.post("/connect")
async def connect_to_db(db_connection: DBConnection):
    """
    Connects to a MongoDB database, fetches data from a specified collection,
    and sends each document as an event to the anomaly detection service.
    """
    if db_connection.db_type != "mongodb":
        raise HTTPException(status_code=400, detail="Only MongoDB is supported at the moment.")

    try:
        # Construct MongoDB connection string
        if db_connection.user and db_connection.password:
            mongo_uri = f"mongodb://{db_connection.user}:{db_connection.password}@{db_connection.host}:{db_connection.port}/"
        else:
            mongo_uri = f"mongodb://{db_connection.host}:{db_connection.port}/"

        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Check if the server is available
        client.admin.command('ping')

        db = client[db_connection.dbname]
        collection = db[db_connection.collection_name]

        # Fetch data from the collection and serialize using bson.json_util
        documents = json.loads(json_util.dumps(collection.find()))

        if not documents:
            return {"message": f"No documents found in collection {db_connection.collection_name}."}

        # Send each document as an event to the anomaly detection service
        async with httpx.AsyncClient() as http_client:
            for doc in documents:
                event_data = {
                    "user_id": doc.get("user_id", "unknown"),
                    "timestamp": doc.get("timestamp", ""),
                    "event_type": db_connection.collection_name,
                    "data": doc
                }
                try:
                    response = await http_client.post("http://localhost:8000/check-event", json=event_data)
                    response.raise_for_status()
                    print(f"Sent event to anomaly detection: {event_data}")
                except httpx.RequestError as exc:
                    print(f"Error sending event to anomaly detection: {exc.request.url!r} - {exc}")
                except Exception as e:
                    print(f"Unexpected error sending event: {e}")

        return {"message": f"Successfully connected to MongoDB and processed {len(documents)} documents from {db_connection.collection_name}."}

    except ConnectionFailure as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to MongoDB: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect or process data: {e}")

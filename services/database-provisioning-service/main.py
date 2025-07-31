
from fastapi import FastAPI, HTTPException
import docker

app = FastAPI()
client = docker.from_env()

@app.post("/provision-mongodb")
def provision_mongodb():
    """
    Provisions a new MongoDB container with sample data.
    """
    try:
        container = client.containers.run(
            "mongo",
            detach=True,
            ports={'27017/tcp': 27017},
            environment=[
                "MONGO_INITDB_ROOT_USERNAME=admin",
                "MONGO_INITDB_ROOT_PASSWORD=password",
            ],
        )
        return {"message": f"MongoDB container {container.id} created successfully."}
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=f"Failed to create MongoDB container: {e}")

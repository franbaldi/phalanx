
# Database Provisioning Service

This service is responsible for provisioning and managing local database instances for testing and evaluation purposes.

## Running the service

1. **Build the Docker image:**
   ```bash
   docker build -t database-provisioning-service .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -d -p 8003:8003 -v /var/run/docker.sock:/var/run/docker.sock database-provisioning-service
   ```

## API

### POST /provision-mongodb

Provisions a new MongoDB container.

**Response:**

```json
{
  "message": "MongoDB container <container_id> created successfully."
}
```

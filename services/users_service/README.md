# Users Service – FastAPI + Docker

This document explains the architecture of the Users Service, details the provided Dockerfile, and lists common Python and Docker commands for development and deployment.


## Architecture Overview

- **Framework:** FastAPI (Python 3.12)
- **Database:** MySQL (configured via Docker Compose)
- **ORM:** SQLAlchemy
- **Environment Management:** python-dotenv
- **Web Server:** Uvicorn

### Key Files

- [`app/main.py`](app/main.py): Main FastAPI entry point.
- [`app/database.py`](app/database.py): Database connection and session management.
- [`app/routes/`](app/routes/): API route definitions.
- [`requirements.txt`](requirements.txt): Python dependencies.
- [`Dockerfile`](Dockerfile): Docker build instructions.


## Dockerfile Explained

The Dockerfile builds a production-ready image for the FastAPI app.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install build tools for compiling dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Steps

1. **Base Image:** Uses a slim Python 3.12 image.
2. **Install Build Tools:** Installs `build-essential` for compiling Python packages with C extensions.
3. **Install Dependencies:** Installs Python packages from `requirements.txt`.
4. **Copy Code:** Copies the FastAPI app code into the container.
5. **Expose Port:** Exposes port 8000 for the API.
6. **Run Server:** Starts the app with Uvicorn.


## Project Structure

- **app/**: Application code (routes, models, database, etc.)
- **requirements.txt**: Python dependencies.
- **Dockerfile**: Container build instructions.


## Common Docker Commands

| Command                                      | Description                                 |
|-----------------------------------------------|---------------------------------------------|
| `docker build -t users-service .`             | Build the Docker image                      |
| `docker run -p 8001:8000 users-service`       | Run the container, mapping port 8000 to 8001|
| `docker compose up --build`                   | Start all services with Docker Compose      |
| `docker compose logs users_service`           | View logs for the users_service container   |


## Common FastAPI Development Commands

| Command                                      | Description                                 |
|-----------------------------------------------|---------------------------------------------|
| `uvicorn app.main:app --reload`               | Run with hot reload (for local dev)         |
| `pytest`                                      | Run tests (if tests are present)            |
| `pip install -r requirements.txt`             | Install dependencies locally                |


## Environment Configuration

- **Database URL:** Set via `.env` file or environment variable `DATABASE_URL`.
- **Other settings:** See [`app/database.py`](app/database.py) for details.

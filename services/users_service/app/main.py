from fastapi import FastAPI
from app.routes.health import router as health_router

app = FastAPI()

# Register routes
app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "Users Service Running"}

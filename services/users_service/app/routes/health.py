from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text  # <-- Add this import
from app.database import get_db

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """
    Health Check API
    1. Establishes DB connection
    2. Performs a lightweight query (SELECT 1)
    3. If DB is reachable → 200 OK
    """

    try:
        db.execute(text("SELECT 1"))  # <-- Wrap SQL in text()
        return {"status": "OK", "database": "connected"}
    except Exception as ex:
        # Service is up but DB is unreachable → report cleanly
        return {"status": "ERROR", "database": "unreachable", "details": str(ex)}
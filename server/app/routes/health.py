from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint verifying API status and database connectivity.
    """
    db_status = "unhealthy"
    try:
        # Execute a simple lightweight query to verify DB connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    if "unhealthy" in db_status:
        # We can either return 200 with degraded status or 503 Service Unavailable
        return {
            "status": "degraded",
            "database": db_status,
            "message": "API is online but Database connection failed."
        }

    return {
        "status": "healthy",
        "database": "connected",
        "message": "API and Database are operational."
    }

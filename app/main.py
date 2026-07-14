from fastapi import FastAPI

from app.core.config import settings

from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.session import get_db
from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import configure_logging, get_logger
from app.api import auth
from app.routers import documents

configure_logging()

logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

logger.info("Application started successfully.")

app.include_router(
    auth.router,
    prefix="/api/v1"
)

app.include_router(
    documents.router,
    prefix="/api/v1"
)

@app.get("/")
def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }

@app.get("/version")
def version():
    return {
        "version": settings.app_version,
    }
    
@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"message": "Database connection successful"}

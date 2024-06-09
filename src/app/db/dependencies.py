from src.app.db.database import SessionLocal


def get_db():
    """
    Get database session dependency for FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

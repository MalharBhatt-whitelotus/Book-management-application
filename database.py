from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

# SQLite needs this connect arg for multithreaded FastAPI usage
engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency for database session
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
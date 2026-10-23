from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Engine: Database bilan ulanishni boshqaradi
# DATABASE_URL dan o'qiydi (config.py dan)
engine = create_engine(settings.DATABASE_URL)

# SessionLocal: Har bir request uchun yangi session yaratadi
# Bu pattern FastAPI'da dependency injection uchun ishlatiladi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Barcha modellar uchun asos (inheritance uchun)
# Har model Base'dan inherit qiladi
Base = declarative_base()


# Dependency: FastAPI endpointlarida ishlatiladi
# Har requestda yangi session ochiladi, request tugagach yopiladi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

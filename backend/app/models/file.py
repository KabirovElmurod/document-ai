from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    stored_path = Column(String(500), nullable=False)  # Diskdagi to'liq yo'l
    content_type = Column(String(100), nullable=False)  # MIME type (pdf, docx, xlsx, png, jpg)
    size = Column(Integer, nullable=False)  # Baytlarda
    created_at = Column(DateTime(timezone=True), server_default=func.now())

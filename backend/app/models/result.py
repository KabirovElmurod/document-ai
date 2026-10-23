from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=True)  # Ajratilgan matn
    summary = Column(Text, nullable=True)  # AI tomonidan yaratilgan xulosa
    data = Column(JSON, nullable=True)  # Qo'shimcha ma'lumotlar (jadvallar, metadata, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship: Result -> File
    file = relationship("File", backref="results")

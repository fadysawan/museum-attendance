from .base import Base
from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime

class MuseumAttributes(Base):
    __tablename__ = "museum_attributes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    museum_id: Mapped[int] = mapped_column(ForeignKey("museum.id"), nullable=False)
    attribute_key: Mapped[str] = mapped_column(String(100), nullable=False)
    attribute_value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    museum: Mapped["Museum"] = relationship("Museum", back_populates="museum_attributes")

    def __repr__(self) -> str:
        return f"<MuseumAttributes(id={self.id}, museum_id={self.museum_id}, attribute_name='{self.attribute_name}')>"
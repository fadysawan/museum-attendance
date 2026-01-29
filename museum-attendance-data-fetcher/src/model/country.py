from .base import Base
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    cities: Mapped[List["City"]] = relationship("City", back_populates="country")

    def __repr__(self) -> str:
        return f"<Country(id={self.id}, name='{self.name}')>"
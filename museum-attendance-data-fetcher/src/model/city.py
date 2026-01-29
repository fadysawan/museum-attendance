from .base import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime

class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reference_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("country.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    country: Mapped["Country"] = relationship("Country", back_populates="cities")
    museums: Mapped[List["Museum"]] = relationship("Museum", back_populates="city")

    def __repr__(self) -> str:
        return f"<City(id={self.id}, name='{self.name}', country_id={self.country_id})>"
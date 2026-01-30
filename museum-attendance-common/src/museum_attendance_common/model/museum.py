from __future__ import annotations
from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime

if TYPE_CHECKING:
    from .museum_attributes import MuseumAttributes
    from .city import City

class Museum(Base):
    __tablename__ = "museum"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    reference_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), nullable=False)
    museum_attributes: Mapped[List["MuseumAttributes"]] = relationship("MuseumAttributes", back_populates="museum")
    city: Mapped["City"] = relationship("City", back_populates="museums")
    number_of_visitors: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    city: Mapped["City"] = relationship("City", back_populates="museums")

    def __repr__(self) -> str:
        return f"<Museum(id={self.id}, name='{self.name}', city_id={self.city_id})>"
    
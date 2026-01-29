from model import Country
from sqlalchemy.orm import Session
from utils import get_logger
from typing import Tuple

logger = get_logger(__name__)

class CountryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Country:
        return self.session.query(Country).filter(Country.name == name).first()

    def add(self, name: str) -> Tuple[Country, bool, bool]:
        country = self.get_by_name(name)
        if country:
            logger.warning(f"Country with name '{name}' already exists.")
            return country, False, False
        country = Country(name=name)
        self.session.add(country)
        self.session.flush()
        return country, True, False
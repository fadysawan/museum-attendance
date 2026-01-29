from model import City, Country
from utils import get_logger
from typing import Tuple

logger = get_logger(__name__)

class CityRepository:
    def __init__(self, session):
        self.session = session

    def get_by_name(self, name: str) -> City:
        return self.session.query(City).filter(City.name == name).first()

    def persist(self, name: str, population: int, reference_url: str, country: Country) -> Tuple[City, bool, bool]:
        """Persists a city in the database."""
        city = self.get_by_name(name)
        if city:
            city.population = population
            city.reference_url = reference_url
            self.session.flush()
            return city, False, True
        city = City(name=name, population=population, reference_url=reference_url, country_id=country.id)
        self.session.add(city)
        self.session.flush()
        return city, True, False
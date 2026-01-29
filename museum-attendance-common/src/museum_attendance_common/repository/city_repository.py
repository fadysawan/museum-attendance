from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from museum_attendance_common.model import City, Country
from museum_attendance_common.utils import get_logger
from typing import Tuple
from museum_attendance_common.exceptions import DatabaseError

logger = get_logger(__name__)

class CityRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_name(self, name: str) -> City | None:
        try:
            return self.session.query(City).filter(City.name == name).first()
        except SQLAlchemyError as e:
            logger.error(f"Error querying city '{name}': {str(e)}")
            raise DatabaseError(f"Failed to query city: {str(e)}", entity_type="City", entity_id=name) from e

    def persist(self, name: str, population: int | None, reference_url: str | None, country: Country) -> Tuple[City, bool, bool]:
        """Persists a city in the database."""
        try:
            city = self.get_by_name(name)
            if city:
                city.population = population
                city.reference_url = reference_url
                self.session.flush()
                logger.debug(f"Updated city: {name}")
                return city, False, True
            
            city = City(name=name, population=population, reference_url=reference_url, country_id=country.id)
            self.session.add(city)
            self.session.flush()
            logger.debug(f"Created city: {name}")
            return city, True, False
            
        except SQLAlchemyError as e:
            logger.error(f"Error persisting city '{name}': {str(e)}")
            raise DatabaseError(f"Failed to persist city: {str(e)}", entity_type="City", entity_id=name, operation="persist") from e
from museum_attendance_common.model import Country
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from museum_attendance_common.utils import get_logger
from typing import Tuple
from museum_attendance_common.exceptions import DatabaseError

logger = get_logger(__name__)

class CountryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Country | None:
        try:
            return self.session.query(Country).filter(Country.name == name).first()
        except SQLAlchemyError as e:
            logger.error(f"Error querying country '{name}': {str(e)}")
            raise DatabaseError(f"Failed to query country: {str(e)}", entity_type="Country", entity_id=name) from e

    def add(self, name: str) -> Tuple[Country, bool, bool]:
        try:
            country = self.get_by_name(name)
            if country:
                logger.debug(f"Country '{name}' already exists")
                return country, False, False
            
            country = Country(name=name)
            self.session.add(country)
            self.session.flush()
            logger.debug(f"Created country: {name}")
            return country, True, False
            
        except SQLAlchemyError as e:
            logger.error(f"Error adding country '{name}': {str(e)}")
            raise DatabaseError(f"Failed to add country: {str(e)}", entity_type="Country", entity_id=name, operation="add") from e
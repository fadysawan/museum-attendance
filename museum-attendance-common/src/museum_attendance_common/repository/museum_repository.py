from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from museum_attendance_common.model import Museum, City
from museum_attendance_common.utils import get_logger
from typing import Tuple
from museum_attendance_common.exceptions import DatabaseError

logger = get_logger(__name__)

class MuseumRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Museum | None:
        try:
            return self.session.query(Museum).filter(Museum.name == name).first()
        except SQLAlchemyError as e:
            logger.error(f"Error querying museum '{name}': {str(e)}")
            raise DatabaseError(f"Failed to query museum: {str(e)}", entity_type="Museum", entity_id=name) from e

    def persist(self, name: str, number_of_visitors: int, reference_url: str, city: City) -> Tuple[Museum, bool, bool]:
        try:
            museum = self.get_by_name(name)
            if museum:
                museum.number_of_visitors = number_of_visitors
                self.session.flush()
                logger.debug(f"Updated museum: {name}")
                return museum, False, True
            
            museum = Museum(name=name, number_of_visitors=number_of_visitors, reference_url=reference_url, city_id=city.id)
            self.session.add(museum)
            self.session.flush()
            logger.debug(f"Created museum: {name}")
            return museum, True, False
            
        except SQLAlchemyError as e:
            logger.error(f"Error persisting museum '{name}': {str(e)}")
            raise DatabaseError(f"Failed to persist museum: {str(e)}", entity_type="Museum", entity_id=name, operation="persist") from e
        
    def get_museums(self, include_attributes: bool = False) -> list[Museum]:
        try:
            query = self.session.query(Museum).options(joinedload(Museum.city))
            if include_attributes:
                query = query.options(joinedload(Museum.museum_attributes))
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error querying museums: {str(e)}")
            raise DatabaseError(f"Failed to query museums: {str(e)}", entity_type="Museum") from e
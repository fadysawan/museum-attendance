from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from museum_attendance_common.model import MuseumAttributes, Museum
from typing import Tuple
from museum_attendance_common.utils import get_logger
from museum_attendance_common.exceptions import DatabaseError

logger = get_logger(__name__)

class MuseumAttributesRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_museum_and_key(self, museum: Museum, attribute_key: str) -> MuseumAttributes | None:
        try:
            return (
                self.session.query(MuseumAttributes)
                .filter(
                    MuseumAttributes.museum_id == museum.id,
                    MuseumAttributes.attribute_key == attribute_key
                )
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error querying museum attribute '{attribute_key}' for museum {museum.id}: {str(e)}")
            raise DatabaseError(f"Failed to query museum attribute: {str(e)}", entity_type="MuseumAttributes") from e

    def persist(self, museum: Museum, attribute_key: str, attribute_value: str) -> Tuple[MuseumAttributes, bool, bool]:
        try:
            museum_attribute = self.get_by_museum_and_key(museum, attribute_key)
            if museum_attribute:
                museum_attribute.attribute_value = attribute_value
                self.session.flush()
                logger.debug(f"Updated attribute '{attribute_key}' for museum {museum.id}")
                return museum_attribute, False, True
            
            museum_attribute = MuseumAttributes(
                museum_id=museum.id,
                attribute_key=attribute_key,
                attribute_value=attribute_value
            )
            self.session.add(museum_attribute)
            self.session.flush()
            logger.debug(f"Created attribute '{attribute_key}' for museum {museum.id}")
            return museum_attribute, True, False
            
        except SQLAlchemyError as e:
            logger.error(f"Error persisting museum attribute '{attribute_key}': {str(e)}")
            raise DatabaseError(f"Failed to persist museum attribute: {str(e)}", entity_type="MuseumAttributes", operation="persist") from e
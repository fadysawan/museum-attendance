from sqlalchemy.orm import Session
from model import MuseumAttributes, Museum
from typing import Tuple


class MuseumAttributesRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_museum_and_key(self, museum: Museum, attribute_key: str) -> MuseumAttributes:
        return (
            self.session.query(MuseumAttributes)
            .filter(
                MuseumAttributes.museum_id == museum.id,
                MuseumAttributes.attribute_key == attribute_key
            )
            .first()
        )

    def persist(self, museum: Museum, attribute_key: str, attribute_value: str) -> Tuple[MuseumAttributes, bool, bool]:
        museum_attribute = self.get_by_museum_and_key(museum, attribute_key)
        if museum_attribute:
            museum_attribute.attribute_value = attribute_value
            self.session.flush()
            return museum_attribute, False, True
        
        museum_attribute = MuseumAttributes(
            museum_id=museum.id,
            attribute_key=attribute_key,
            attribute_value=attribute_value
        )
        self.session.add(museum_attribute)
        self.session.flush()
        return museum_attribute, True, False
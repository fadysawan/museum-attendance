from sqlalchemy.orm import Session
from model import Museum, City
from utils import get_logger
from typing import Tuple

logger = get_logger(__name__)

class MuseumRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Museum:
        return self.session.query(Museum).filter(Museum.name == name).first()

    def persist(self, name: str, number_of_visitors: int, reference_url: str, city: City) -> Tuple[Museum, bool, bool]:
        museum = self.get_by_name(name)
        if museum:
            museum.number_of_visitors = number_of_visitors
            self.session.flush()
            return museum, False, True
        museum = Museum(name=name, number_of_visitors=number_of_visitors, reference_url=reference_url, city_id=city.id)
        self.session.add(museum)
        self.session.flush()
        return museum, True, False
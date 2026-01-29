

from museum_attendance_common.repository import CityRepository, CountryRepository, MuseumRepository, MuseumAttributesRepository
from museum_attendance_common.model import Museum, City, Country
from museum_attendance_common.utils import get_logger
from museum_attendance_common.exceptions import DatabaseError
from dto import Museum as MuseumDTO
from typing import Tuple
from exceptions import DataProcessingError

logger = get_logger(__name__)

class PersistenceService:
    museum_repository: MuseumRepository
    city_repository: CityRepository
    country_repository: CountryRepository
    museum_attributes_repository: MuseumAttributesRepository

    def __init__(self, museum_repository: MuseumRepository, country_repository: CountryRepository, museum_attributes_repository: MuseumAttributesRepository, city_repository: CityRepository) -> None:
        self.museum_repository = museum_repository
        self.country_repository = country_repository
        self.museum_attributes_repository = museum_attributes_repository
        self.city_repository = city_repository

    def persist_country(self, country_name: str) -> Tuple[Country, bool, bool]:
        if not country_name:
            logger.error("Country name cannot be empty")
            raise DataProcessingError("Country name cannot be empty", field="country_name", value=country_name)
        
        try:
            country, inserted, updated = self.country_repository.add(country_name)
            logger.debug(f"Country persisted: {country_name} (inserted={inserted}, updated={updated})")
            return country, inserted, updated
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error persisting country '{country_name}': {str(e)}")
            raise DataProcessingError(f"Failed to persist country: {str(e)}", field="country_name", value=country_name) from e

    def persist_city(self, museum_dto: MuseumDTO, country: Country) -> Tuple[City, bool, bool]:
        city_name = museum_dto.get_city()
        if not city_name:
            logger.error("City name cannot be empty")
            raise DataProcessingError("City name cannot be empty", field="city", value=city_name)
        
        try:
            city, inserted, updated = self.city_repository.persist(
                museum_dto.get_city(), 
                museum_dto.get_city_population(), 
                museum_dto.get_city_reference_url(), 
                country
            )
            logger.debug(f"City persisted: {city_name} (inserted={inserted}, updated={updated})")
            return city, inserted, updated
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error persisting city '{city_name}': {str(e)}")
            raise DataProcessingError(f"Failed to persist city: {str(e)}", field="city", value=city_name) from e
    
    def persist_museum(self, museum_dto: MuseumDTO, city: City) -> Tuple[Museum, bool, bool]:
        if not museum_dto.name:
            logger.error("Museum name cannot be empty")
            raise DataProcessingError("Museum name cannot be empty", field="museum_name", value=museum_dto.name)
        
        try:
            museum, inserted, updated = self.museum_repository.persist(
                name=museum_dto.name,
                number_of_visitors=museum_dto.get_museum_visitor_count(),
                reference_url=museum_dto.get_museum_reference_url(),
                city=city
            )
            logger.debug(f"Museum persisted: {museum_dto.name} (inserted={inserted}, updated={updated})")
            return museum, inserted, updated
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error persisting museum '{museum_dto.name}': {str(e)}")
            raise DataProcessingError(f"Failed to persist museum: {str(e)}", field="museum_name", value=museum_dto.name) from e

    def persist_museum_attributes(self, attributes: dict[str, str], museum: Museum) -> Tuple[int, int]:
        inserted_count = 0
        updated_count = 0
        
        try:
            for museum_attribute_key, museum_attribute_value in attributes.items():
                museum_attribute, inserted, updated = self.museum_attributes_repository.persist(
                    museum=museum,
                    attribute_key=museum_attribute_key,
                    attribute_value=museum_attribute_value
                )
                if inserted:
                    inserted_count += 1
                if updated:
                    updated_count += 1
            
            logger.debug(f"Museum attributes persisted for museum {museum.id}: {inserted_count} inserted, {updated_count} updated")
            return inserted_count, updated_count
            
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error persisting museum attributes for museum {museum.id}: {str(e)}")
            raise DataProcessingError(f"Failed to persist museum attributes: {str(e)}") from e
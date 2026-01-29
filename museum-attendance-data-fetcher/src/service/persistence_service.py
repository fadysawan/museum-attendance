

from repository import CityRepository, CountryRepository, MuseumRepository, MuseumAttributesRepository
from model import Museum, City, Country
from dto import Museum as MuseumDTO
from typing import Tuple

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
            raise ValueError("Country name cannot be empty")
        return self.country_repository.add(country_name)

    def persist_city(self, museum_dto: MuseumDTO, country: Country) -> Tuple[City, bool, bool]:
        if not museum_dto.get_city():
            raise ValueError("City name cannot be empty")
        return self.city_repository.persist(museum_dto.get_city(), museum_dto.get_city_population(), museum_dto.get_city_reference_url(), country)
    
    def persist_museum(self, museum_dto: MuseumDTO, city: City) -> Tuple[Museum, bool, bool]:
        if not museum_dto.name:
            raise ValueError("Museum name cannot be empty")
        return self.museum_repository.persist(
            name=museum_dto.name,
            number_of_visitors=museum_dto.get_museum_visitor_count(),
            reference_url=museum_dto.get_museum_reference_url(),
            city=city
        )

    def persist_museum_attributes(self, attributes: dict[str, str], museum: Museum) -> Tuple[int, int]:
        inserted_count = 0
        updated_count = 0
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
        return inserted_count, updated_count
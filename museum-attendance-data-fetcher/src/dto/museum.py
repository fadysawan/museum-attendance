from dataclasses import dataclass
from .city import City
from enumeration import GlobalEnum

@dataclass
class Museum:
    name: str
    visitor_count: int
    city: str
    wikipedia_city_details_page_title: str
    wikipedia_city_details: City
    country: str
    wikipedia_museum_details_page_title: str
    wikipedia_museum_attributes: dict[str, str]

    def get_country(self) -> str:
        if self.wikipedia_city_details and self.wikipedia_city_details.country and self.wikipedia_city_details.country != GlobalEnum.NA.value:
            return self.wikipedia_city_details.country
        return self.country
    
    def get_city(self) -> str:
        if self.wikipedia_city_details and self.wikipedia_city_details.name and self.wikipedia_city_details.name != GlobalEnum.NA.value:
            return self.wikipedia_city_details.name
        return self.city
    
    def get_city_population(self) -> int | None:
        if self.wikipedia_city_details:
            return self.wikipedia_city_details.population
        return None
    
    def get_city_reference_url(self) -> str | None:
        return self.wikipedia_city_details_page_title
    
    def get_museum_attributes(self) -> dict[str, str]:
        return self.wikipedia_museum_attributes
    
    def get_museum_reference_url(self) -> str:
        return self.wikipedia_museum_details_page_title
    
    def get_museum_name(self) -> str:
        return self.name
    
    def get_museum_visitor_count(self) -> int:
        return self.visitor_count
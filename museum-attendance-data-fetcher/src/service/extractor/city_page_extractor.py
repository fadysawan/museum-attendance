from .abstract_wikipedia_page_extractor import AbstractWikipediaPageExtractor
from bs4 import BeautifulSoup
from dto import City
from utils import get_logger
from quantulum3 import parser
from enumeration import GlobalEnum

logger = get_logger(__name__)

class CityPageExtractor(AbstractWikipediaPageExtractor[City]):
    def extract_data(self, soup: BeautifulSoup) -> dict:
        """Extract city data from the infobox."""
        infobox = soup.find("table", {"class": "infobox"})
        if not infobox:
            logger.warning("No infobox found on the city page.")
            return {}

        city_data = {}

        # Extract city name
        title_tag = soup.find("div", {"class": "fn org"})
        city_name = title_tag.text.strip() if title_tag else GlobalEnum.NA.value
        city_data["name"] = city_name

        # Extract country
        country = self.__extract_infobox_value(infobox, "Country")
        city_data["country"] = country if country else GlobalEnum.NA.value

        # Extract population
        population_text = self.__extract_infobox_population_total(infobox)
        population = self.__parse_population(population_text) if population_text else None
        if population == 0 or not population:
            logger.debug(f"Population for city {city_name} is zero or could not be parsed.")
            population = None
        city_data["population"] = population

        return city_data

    def to_dto(self) -> City:
        data = self.get_data()
        return City(**data)
    
    def __extract_infobox_value(self, infobox: BeautifulSoup, label: str) -> str | None:
        """Extract a value from the infobox based on the label."""
        row = infobox.find("th", string=lambda text: text and label in text)
        if row:
            value_cell = row.find_next_sibling("td")
            if value_cell:
                return value_cell.get_text(strip=True)
        return None
    
    def __extract_infobox_population_total(self, infobox: BeautifulSoup) -> str | None:
        """Extract the total population from the infobox."""
        row = infobox.find("tr")
        while row:
            header = row.find("th")
            header_text = header.get_text() if header else ""
            if header and "Population" in header.get_text():
                break
            row = row.find_next_sibling("tr")
        if row:
            value_cell = row.find_next("td")
            if value_cell:
                return value_cell.get_text(strip=True)
        return None

    def __parse_population(self, population_text: str) -> int | None:
        """Parse the population text to extract the number."""
        quantities = parser.parse(population_text)
        if quantities:
            return int(quantities[0].value)
        return None
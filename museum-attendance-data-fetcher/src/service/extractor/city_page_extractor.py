from .abstract_wikipedia_page_extractor import AbstractWikipediaPageExtractor
from bs4 import BeautifulSoup, Tag
from dto import City
from museum_attendance_common.utils import get_logger
from quantulum3 import parser
from enumeration import GlobalEnum
from exceptions import DataProcessingError

logger = get_logger(__name__)

class CityPageExtractor(AbstractWikipediaPageExtractor[City]):
    def extract_data(self, soup: BeautifulSoup) -> dict:
        """Extract city data from the infobox."""
        try:
            infobox = soup.find("table", {"class": "infobox"})
            if not infobox:
                logger.warning("No infobox found on the city page")
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
                logger.debug(f"Population for city {city_name} is zero or could not be parsed")
                population = None
            city_data["population"] = population

            return city_data
            
        except AttributeError as e:
            logger.error(f"HTML structure error in city infobox: {str(e)}")
            raise DataProcessingError(f"Failed to parse city infobox: {str(e)}", element="infobox") from e
        except Exception as e:
            logger.error(f"Unexpected error extracting city data: {str(e)}")
            raise DataProcessingError(f"Failed to extract city data: {str(e)}") from e

    def to_dto(self) -> City:
        data = self.get_data()
        return City(**data)
    
    def __extract_infobox_value(self, infobox: Tag, label: str) -> str | None:
        """Extract a value from the infobox based on the label."""
        # Find all th elements and check their text content
        for th in infobox.find_all("th"):
            th_text = th.get_text(strip=True)
            if label in th_text:
                value_cell = th.find_next_sibling("td")
                if value_cell:
                    result = value_cell.get_text(strip=True)
                    return str(result) if result else None
        return None
    
    def __extract_infobox_population_total(self, infobox: Tag) -> str | None:
        """Extract the total population from the infobox."""
        row = infobox.find("tr")
        while row:
            header = row.find("th")
            if header and "Population" in header.get_text():
                break
            row = row.find_next_sibling("tr")
        if row:
            value_cell = row.find_next("td")
            if value_cell:
                return value_cell.get_text(strip=True)

    def __parse_population(self, population_text: str) -> int | None:
        """Parse the population text to extract the number."""
        try:
            quantities = parser.parse(population_text)
            if quantities:
                return int(quantities[0].value)
            return None
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse population '{population_text}': {str(e)}")
            return None
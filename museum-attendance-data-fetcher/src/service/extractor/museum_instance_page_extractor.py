from .abstract_wikipedia_page_extractor import AbstractWikipediaPageExtractor
from bs4 import BeautifulSoup
from museum_attendance_common.utils import get_logger
from exceptions import DataProcessingError

logger = get_logger(__name__)

class MuseumInstancePageExtractor(AbstractWikipediaPageExtractor[dict[str, str]]):
    def extract_data(self, soup: BeautifulSoup) -> dict:
        try:
            info_box = soup.find('table', {'class': 'infobox'})
            if not info_box:
                logger.warning("No infobox found on the page")
                return {}

            data = {}
            rows = info_box.find_all('tr')
            for row in rows:
                try:
                    header = row.find('th')
                    value = row.find('td')
                    if header and value:
                        key = header.get_text(strip=True).lower().replace(' ', '_')
                        data[key] = value.get_text(strip=True)
                except AttributeError:
                    continue

            return data
            
        except AttributeError as e:
            logger.error(f"HTML structure error in museum infobox: {str(e)}")
            raise DataProcessingError(f"Failed to parse museum infobox: {str(e)}", element="infobox") from e
        except Exception as e:
            logger.error(f"Unexpected error extracting museum data: {str(e)}")
            raise DataProcessingError(f"Failed to extract museum data: {str(e)}") from e

    def to_dto(self) -> dict[str, str]:
        data = self.get_data()
        return data
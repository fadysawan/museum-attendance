from .abstract_wikipedia_page_extractor import AbstractWikipediaPageExtractor
from bs4 import BeautifulSoup
from utils import get_logger

logger = get_logger(__name__)

class MuseumInstancePageExtractor(AbstractWikipediaPageExtractor[dict[str, str]]):
    def extract_data(self, soup: BeautifulSoup) -> dict:
        info_box = soup.find('table', {'class': 'infobox'})
        if not info_box:
            logger.warning("No infobox found on the page.")
            return {}

        data = {}
        rows = info_box.find_all('tr')
        for row in rows:
            header = row.find('th')
            value = row.find('td')
            if header and value:
                key = header.get_text(strip=True).lower().replace(' ', '_')
                data[key] = value.get_text(strip=True)

        return data

    def to_dto(self) -> dict[str, str]:
        data = self.get_data()
        return data
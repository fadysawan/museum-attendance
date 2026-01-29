from dataclasses import dataclass
from .abstract_wikipedia_page_extractor import AbstractWikipediaPageExtractor
from dto import Museum
from bs4 import BeautifulSoup
from enumeration import GlobalEnum, MuseumTableHeader
from quantulum3 import parser
from typing import Tuple
from utils import get_logger

logger = get_logger(__name__)

@dataclass 
class MuseumListPageExtractor(AbstractWikipediaPageExtractor[Museum]):
    def extract_data(self, soup: BeautifulSoup) -> dict:
        """Extract museum list data from the table."""
        museums = {}
        
        table = soup.find('table', class_='wikitable sortable')
        if not table:
            logger.warning("No museum table found on the page.")
            return museums
        
        rows = table.find('tbody').find_all('tr')[1:]
        
        for _, row in enumerate(rows, start=1):
            cells = row.find_all('td')
            if len(cells) == 4:
                museum_name, museum_page_title = self.__get_data_from_row(row, self.__get_column_index(table, MuseumTableHeader.NAME.value))
                if museum_name == GlobalEnum.NA.value:
                    logger.debug(f"Skipping row {row} due to missing museum name.")
                    continue
                city, city_page_title = self.__get_data_from_row(row, self.__get_column_index(table, MuseumTableHeader.CITY.value))
                if city == GlobalEnum.NA.value:
                    logger.debug(f"Skipping row {row} due to missing city name.")
                    continue
                country, _ = self.__get_data_from_row(row, self.__get_column_index(table, MuseumTableHeader.COUNTRY.value))
                visitors_text, _ = self.__get_data_from_row(row, self.__get_column_index(table, MuseumTableHeader.VISITORS.value))
                logger.debug(f"Extracted data - Museum: {museum_name}, City: {city}, Country: {country}, Visitors: {visitors_text}")
                museums[museum_name] = {
                    'name': museum_name,
                    'visitor_count': self.__parse_visitors(visitors_text),
                    'city': city,
                    'wikipedia_city_details': None,
                    'wikipedia_city_details_page_title': city_page_title,
                    'wikipedia_museum_attributes': None,
                    'wikipedia_museum_details_page_title': museum_page_title,
                    'country': country,
                }
            else:
                logger.debug(f"Skipping row {row} due to unexpected number of cells: {len(cells)}")
        
        return museums
    
    def to_dto(self) -> list[Museum]:
        data = self.get_data()
        return [Museum(**museum_data) for museum_data in data.values()]

    def __parse_visitors(self, visitors_text: str) -> int | None:
        """Parse the visitors text to extract number and year."""
        logger.debug(f"Parsing visitors text: {visitors_text}")
        quantities = parser.parse(visitors_text)
        if quantities:
            logger.debug(f"Extracted visitor count: {quantities[0].value}")
            return int(quantities[0].value)
        return None

    def __get_data_from_row(self, row: BeautifulSoup, column_index: int) -> Tuple[str, str]:
        """Extract the museum name from the row."""
        if len(row.find_all('td')) <= column_index or column_index == -1:
            raise IndexError("Column index out of range")
        name_cell = row.find_all('td')[column_index]
        if not name_cell:
            logger.warning("Name cell is missing in the row.")
            return GlobalEnum.NA.value, GlobalEnum.NA.value
        
        page_title = GlobalEnum.NA.value
        link = name_cell.find('a')
        if link and 'href' in link.attrs:
            page_title = link['href'].split('/')[-1]

        return name_cell.get_text(strip=True), page_title


    def __get_column_index(self, table: BeautifulSoup, column_name: str) -> int:
        """Get the index of the specified column in the table."""
        header_row = table.find('tr')
        headers = header_row.find_all(['th', 'td'])
        for index, header in enumerate(headers):
            if column_name in header.get_text(strip=True):
                return index
        return -1

from abc import abstractmethod, ABC
from dataclasses import dataclass
from bs4 import BeautifulSoup
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class AbstractWikipediaPageExtractor(ABC, Generic[T]):
    _html_content: str

    def get_html_content(self) -> str:
        return self._html_content
    
    def parse_html(self) -> BeautifulSoup:
        return BeautifulSoup(self._html_content, 'html.parser')
    
    @abstractmethod
    def extract_data(self, soup: BeautifulSoup) -> dict:
        """Abstract method to extract data from the HTML content."""
        pass

    def get_data(self) -> dict:
        """Get the extracted data as a dictionary."""
        soup = self.parse_html()
        return self.extract_data(soup)
    
    @abstractmethod
    def to_dto(self) -> T | list[T]:
        """Convert the extracted data to a DTO of type T."""
        pass


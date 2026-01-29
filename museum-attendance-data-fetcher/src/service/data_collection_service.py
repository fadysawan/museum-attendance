from bs4 import BeautifulSoup
from quantulum3 import parser
from museum_attendance_common.utils import get_logger
from museum_attendance_common.config import Settings
from dto import MostVisitedMuseumList, Museum, City
from service.extractor import MuseumListPageExtractor, MuseumInstancePageExtractor, CityPageExtractor
from service.api import wikipedia_service
from concurrent.futures import ThreadPoolExecutor, as_completed


logger = get_logger(__name__)
settings = Settings()

class DataCollectionService:
    @staticmethod
    def collect_data(master_page_title: str) -> MostVisitedMuseumList:
        most_visited_museums_html_content = wikipedia_service.get_page_html(master_page_title)
        museum_list_page_extractor: MuseumListPageExtractor = MuseumListPageExtractor(_html_content=most_visited_museums_html_content)
        data = museum_list_page_extractor.to_dto()
        
        with ThreadPoolExecutor(max_workers=settings.max_workers) as executor:
            museum_details_futures = [executor.submit(DataCollectionService.fetch_museum_details, museum) for museum in data]
            for future in as_completed(museum_details_futures):
                museum = future.result()
                logger.info(f"Completed data collection for museum: {museum.name}")

            city_details_futures = [executor.submit(DataCollectionService.fetch_city_details, museum) for museum in data if museum.wikipedia_city_details_page_title != "N/A"]
            for future in as_completed(city_details_futures):
                museum = future.result()
                logger.info(f"Completed data collection for city: {museum.city}")

        return MostVisitedMuseumList(wikipedia_museum_instance_list=data)
    
    @staticmethod
    def fetch_museum_details(museum: Museum) -> Museum:
        try:
            logger.info(f"Collecting data for museum: {museum.name}")
            museum_instance_html_content = wikipedia_service.get_page_html(museum.wikipedia_museum_details_page_title)
            museum_instance_page_extractor = MuseumInstancePageExtractor(_html_content=museum_instance_html_content)
            museum.wikipedia_museum_attributes = museum_instance_page_extractor.extract_data(BeautifulSoup(museum_instance_html_content, 'html.parser'))
            return museum
        except Exception as e:
            logger.error(f"Error fetching data for {museum.name}: {e}")
            return museum

    @staticmethod
    def fetch_city_details(museum: Museum) -> Museum:
        try:
            logger.info(f"Collecting data for city: {museum.city}")
            city_html_content = wikipedia_service.get_page_html(museum.wikipedia_city_details_page_title)
            city_page_extractor = CityPageExtractor(_html_content=city_html_content)
            museum.wikipedia_city_details = city_page_extractor.to_dto()
            return museum
        except Exception as e:
            logger.error(f"Error fetching data for city {museum.city}: {e}")
            return museum

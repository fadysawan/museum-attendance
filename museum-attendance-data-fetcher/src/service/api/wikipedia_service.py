from ratelimit import limits, sleep_and_retry
import requests
import os
from utils import get_logger
from config.settings import Settings

logger = get_logger(__name__)

class WikipediaService:
    def __init__(self):
        self.__access_token = None

    def authenticate(self):
        settings = Settings()
        response = requests.post(
            settings.wikipedia_auth_url,
            data={
                "client_id": settings.wikipedia_client_id,
                "client_secret": settings.wikipedia_client_secret,
                "grant_type": "client_credentials"
            },
            headers={
                "User-Agent": "MuseumAttendanceDataFetcher/1.0 (contact: fady.sawan@gmail.com)"
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        self.__access_token = data.get("access_token")
    
    def __get_access_token(self) -> str:
        if not self.__access_token:
            self.authenticate()
        return self.__access_token

    @sleep_and_retry
    @limits(calls=2, period=1)
    def get_page_html(self, page_title: str) -> str:
        settings = Settings()
        response = requests.get(
            f"{settings.wikipedia_api_url}page/html/{page_title}",
            headers={
                "Authorization": f"Bearer {self.__get_access_token()}",
                "User-Agent": "MuseumAttendanceDataFetcher/1.0 (contact: fady.sawan@gmail.com)"
            },
            timeout=30
        )
        response.raise_for_status()
        # write the content into a file
        if settings.keep_html_files:
            self.save_file(page_title, response.text)
        return response.text

    def save_file(self, page_title: str, content: str):
        if not os.path.exists("assets"):
            os.makedirs("assets")
        with open(f"assets/{page_title}.html", "w", encoding="utf-8") as file:
            file.write(content)
wikipedia_service = WikipediaService()
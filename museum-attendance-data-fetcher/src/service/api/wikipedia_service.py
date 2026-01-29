from ratelimit import limits, sleep_and_retry
import requests
import os
import time
from requests.exceptions import RequestException, HTTPError
from museum_attendance_common.utils import get_logger
from museum_attendance_common.config import Settings
from exceptions import APIError

logger = get_logger(__name__)


class WikipediaService:
    def __init__(self) -> None:
        self.__access_token: str | None = None
        self.__settings = Settings()

    def authenticate(self) -> None:
        """Authenticate with Wikipedia API and obtain access token.

        Raises:
            APIError: If authentication fails
        """
        logger.info("Attempting to authenticate with Wikipedia API")

        try:
            start_time = time.time()
            response = requests.post(
                self.__settings.wikipedia_auth_url,
                data={
                    "client_id": self.__settings.wikipedia_client_id,
                    "client_secret": self.__settings.wikipedia_client_secret,
                    "grant_type": "client_credentials",
                },
                headers={"User-Agent": "MuseumAttendanceDataFetcher/1.0 (contact: fady.sawan@gmail.com)"},
                timeout=30,
            )
            elapsed_time = time.time() - start_time

            response.raise_for_status()
            data = response.json()
            self.__access_token = data.get("access_token")

            if not self.__access_token:
                raise APIError("No access token in authentication response", url=self.__settings.wikipedia_auth_url)

            logger.info(f"Successfully authenticated with Wikipedia API (took {elapsed_time:.2f}s)")

        except (HTTPError, RequestException) as e:
            status_code = getattr(getattr(e, "response", None), "status_code", None)
            logger.error(f"Authentication failed: {str(e)}")
            raise APIError(f"Authentication failed: {str(e)}", status_code=status_code, url=self.__settings.wikipedia_auth_url) from e
    
    def __get_access_token(self) -> str:
        """Get access token, authenticating if necessary.

        Returns:
            str: Valid access token

        Raises:
            APIError: If authentication fails
        """
        if not self.__access_token:
            self.authenticate()
        assert self.__access_token is not None  # For mypy
        return self.__access_token

    @sleep_and_retry
    @limits(calls=2, period=1)
    def get_page_html(self, page_title: str) -> str:
        """Fetch HTML content for a Wikipedia page.

        Args:
            page_title: Title of the Wikipedia page to fetch

        Returns:
            str: HTML content of the page

        Raises:
            APIError: If API request fails
        """
        url = f"{self.__settings.wikipedia_api_url}page/html/{page_title}"

        logger.info(f"Fetching Wikipedia page: {page_title}")

        try:
            start_time = time.time()
            response = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {self.__get_access_token()}",
                    "User-Agent": "MuseumAttendanceDataFetcher/1.0 (contact: fady.sawan@gmail.com)",
                },
                timeout=30,
            )
            elapsed_time = time.time() - start_time

            response.raise_for_status()

            logger.info(f"Successfully fetched page: {page_title} (took {elapsed_time:.2f}s)")

            # Save HTML file if configured
            if self.__settings.keep_html_files:
                self.save_file(page_title, response.text)

            html_content: str = response.text
            return html_content

        except HTTPError as e:
            if e.response.status_code in (401, 403):
                self.__access_token = None  # Force re-authentication

            logger.error(f"HTTP {e.response.status_code} error fetching page: {page_title}")
            raise APIError(f"HTTP {e.response.status_code} error fetching {page_title}", status_code=e.response.status_code, url=url) from e

        except RequestException as e:
            logger.error(f"Request error fetching page {page_title}: {str(e)}")
            raise APIError(f"Request error when fetching {page_title}: {str(e)}", url=url) from e

    def save_file(self, page_title: str, content: str) -> None:
        """Save HTML content to a file.

        Args:
            page_title: Title of the page (used as filename)
            content: HTML content to save

        Raises:
            APIError: If file save operation fails
        """
        try:
            if not os.path.exists("assets"):
                os.makedirs("assets")

            filepath = f"assets/{page_title}.html"
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)

            logger.debug(f"Saved HTML file: {filepath}")

        except Exception as e:
            logger.error(f"Failed to save HTML file for {page_title}: {str(e)}")
            raise APIError(f"Failed to save HTML file for {page_title}") from e

wikipedia_service = WikipediaService()
"""Tests for WikipediaService."""
import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from requests.exceptions import HTTPError, RequestException
import os

from service.api.wikipedia_service import WikipediaService
from exceptions import APIError


class TestWikipediaService:
    """Test suite for WikipediaService."""

    @pytest.fixture
    def wiki_service(self):
        """Create a WikipediaService instance for testing."""
        with patch('service.api.wikipedia_service.Settings') as mock_settings:
            mock_settings_instance = Mock()
            mock_settings_instance.wikipedia_auth_url = "https://api.wikimedia.org/oauth2/token"
            mock_settings_instance.wikipedia_client_id = "test_client_id"
            mock_settings_instance.wikipedia_client_secret = "test_client_secret"
            mock_settings_instance.wikipedia_api_url = "https://api.wikimedia.org/core/v1/wikipedia/en/"
            mock_settings_instance.keep_html_files = False
            mock_settings.return_value = mock_settings_instance
            
            service = WikipediaService()
            return service

    @patch('service.api.wikipedia_service.requests.post')
    @patch('service.api.wikipedia_service.time.time')
    def test_authenticate_success(self, mock_time, mock_post, wiki_service):
        """Test successful authentication."""
        mock_time.side_effect = [100.0, 100.5]  # start and end time
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_token_123"}
        mock_post.return_value = mock_response
        
        wiki_service.authenticate()
        
        # Verify token was set
        assert wiki_service._WikipediaService__access_token == "test_token_123"
        
        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args[1]
        assert "client_id" in call_kwargs["data"]
        assert "client_secret" in call_kwargs["data"]
        assert "grant_type" in call_kwargs["data"]

    @patch('service.api.wikipedia_service.requests.post')
    def test_authenticate_no_token_in_response(self, mock_post, wiki_service):
        """Test authentication with no token in response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response
        
        with pytest.raises(APIError) as exc_info:
            wiki_service.authenticate()
        
        assert "No access token" in str(exc_info.value)

    @patch('service.api.wikipedia_service.requests.post')
    def test_authenticate_http_error(self, mock_post, wiki_service):
        """Test authentication with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_post.return_value = mock_response
        
        with pytest.raises(APIError) as exc_info:
            wiki_service.authenticate()
        
        assert "Authentication failed" in str(exc_info.value)

    @patch('service.api.wikipedia_service.requests.post')
    def test_authenticate_request_exception(self, mock_post, wiki_service):
        """Test authentication with request exception."""
        mock_post.side_effect = RequestException("Connection error")
        
        with pytest.raises(APIError) as exc_info:
            wiki_service.authenticate()
        
        assert "Authentication failed" in str(exc_info.value)

    @patch('service.api.wikipedia_service.requests.get')
    @patch('service.api.wikipedia_service.time.time')
    def test_get_page_html_success(self, mock_time, mock_get, wiki_service):
        """Test successful page fetch."""
        mock_time.side_effect = [200.0, 200.8]
        wiki_service._WikipediaService__access_token = "test_token"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test content</body></html>"
        mock_get.return_value = mock_response
        
        html = wiki_service.get_page_html("Test_Page")
        
        assert html == "<html><body>Test content</body></html>"
        mock_get.assert_called_once()
        
        call_kwargs = mock_get.call_args[1]
        assert "Authorization" in call_kwargs["headers"]
        assert "Bearer test_token" in call_kwargs["headers"]["Authorization"]

    @patch('service.api.wikipedia_service.requests.get')
    def test_get_page_html_with_save_file(self, mock_get, wiki_service):
        """Test page fetch with file saving enabled."""
        wiki_service._WikipediaService__access_token = "test_token"
        wiki_service._WikipediaService__settings.keep_html_files = True
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>Content</html>"
        mock_get.return_value = mock_response
        
        with patch.object(wiki_service, 'save_file') as mock_save:
            html = wiki_service.get_page_html("Test_Page")
            
            assert html == "<html>Content</html>"
            mock_save.assert_called_once_with("Test_Page", "<html>Content</html>")

    @patch('service.api.wikipedia_service.requests.get')
    def test_get_page_html_http_401_clears_token(self, mock_get, wiki_service):
        """Test that 401 error clears access token."""
        wiki_service._WikipediaService__access_token = "test_token"
        
        mock_response = Mock()
        mock_response.status_code = 401
        http_error = HTTPError(response=mock_response)
        http_error.response = mock_response
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response
        
        with pytest.raises(APIError):
            wiki_service.get_page_html("Test_Page")
        
        assert wiki_service._WikipediaService__access_token is None

    @patch('service.api.wikipedia_service.requests.get')
    def test_get_page_html_http_error(self, mock_get, wiki_service):
        """Test page fetch with HTTP error."""
        wiki_service._WikipediaService__access_token = "test_token"
        
        mock_response = Mock()
        mock_response.status_code = 404
        http_error = HTTPError(response=mock_response)
        http_error.response = mock_response
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response
        
        with pytest.raises(APIError) as exc_info:
            wiki_service.get_page_html("Nonexistent_Page")
        
        assert exc_info.value.status_code == 404

    @patch('service.api.wikipedia_service.requests.get')
    def test_get_page_html_request_exception(self, mock_get, wiki_service):
        """Test page fetch with request exception."""
        wiki_service._WikipediaService__access_token = "test_token"
        mock_get.side_effect = RequestException("Network error")
        
        with pytest.raises(APIError) as exc_info:
            wiki_service.get_page_html("Test_Page")
        
        assert "Request error" in str(exc_info.value)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_save_file_creates_directory(self, mock_makedirs, mock_exists, mock_file, wiki_service):
        """Test that save_file creates assets directory if it doesn't exist."""
        mock_exists.return_value = False
        
        wiki_service.save_file("Test_Page", "<html>content</html>")
        
        mock_makedirs.assert_called_once_with("assets")
        mock_file.assert_called_once_with("assets/Test_Page.html", "w", encoding="utf-8")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_save_file_writes_content(self, mock_exists, mock_file, wiki_service):
        """Test that save_file writes content correctly."""
        mock_exists.return_value = True
        content = "<html><body>Test</body></html>"
        
        wiki_service.save_file("Test_Page", content)
        
        mock_file.assert_called_once_with("assets/Test_Page.html", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with(content)

    @patch('builtins.open')
    @patch('os.path.exists')
    def test_save_file_handles_error(self, mock_exists, mock_open_func, wiki_service):
        """Test that save_file handles errors properly."""
        mock_exists.return_value = True
        mock_open_func.side_effect = IOError("Disk full")
        
        with pytest.raises(APIError) as exc_info:
            wiki_service.save_file("Test_Page", "<html>content</html>")
        
        assert "Failed to save HTML file" in str(exc_info.value)

    def test_get_access_token_authenticates_if_needed(self, wiki_service):
        """Test that __get_access_token calls authenticate if no token exists."""
        wiki_service._WikipediaService__access_token = None
        
        def set_token():
            wiki_service._WikipediaService__access_token = "new_token"
        
        with patch.object(wiki_service, 'authenticate', side_effect=set_token) as mock_auth:
            token = wiki_service._WikipediaService__get_access_token()
            
            assert token == "new_token"
            mock_auth.assert_called_once()

    def test_get_access_token_returns_existing_token(self, wiki_service):
        """Test that __get_access_token returns existing token without authenticating."""
        wiki_service._WikipediaService__access_token = "existing_token"
        
        with patch.object(wiki_service, 'authenticate') as mock_auth:
            token = wiki_service._WikipediaService__get_access_token()
            
            assert token == "existing_token"
            mock_auth.assert_not_called()

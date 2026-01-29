"""Tests for logging utilities."""
import logging
import json
from io import StringIO
from museum_attendance_common.utils.logging import JsonFormatter, setup_logging, get_logger


class TestJsonFormatter:
    """Tests for JsonFormatter class."""

    def test_format_basic_log(self):
        """Test basic log message formatting."""
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        
        formatted = formatter.format(record)
        log_data = json.loads(formatted)

        assert log_data["level"] == "INFO"
        assert log_data["logger"] == "test_logger"
        assert log_data["message"] == "Test message"
        assert log_data["module"] == "test"
        assert "function" in log_data  # Function field exists
        assert log_data["line"] == 10
        assert "timestamp" in log_data

    def test_format_with_extra_fields(self):
        """Test log formatting with extra fields."""
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test_logger",
            level=logging.WARNING,
            pathname="test.py",
            lineno=20,
            msg="Warning message",
            args=(),
            exc_info=None,
        )
        record.user_id = "12345"
        record.request_id = "abc-def"
        
        formatted = formatter.format(record)
        log_data = json.loads(formatted)
        
        assert log_data["user_id"] == "12345"
        assert log_data["request_id"] == "abc-def"
        assert log_data["message"] == "Warning message"

    def test_format_with_exception(self):
        """Test log formatting with exception info."""
        formatter = JsonFormatter()
        try:
            raise ValueError("Test error")
        except ValueError:
            import sys
            exc_info = sys.exc_info()
            record = logging.LogRecord(
                name="test_logger",
                level=logging.ERROR,
                pathname="test.py",
                lineno=30,
                msg="Error occurred",
                args=(),
                exc_info=exc_info,
            )
            
            formatted = formatter.format(record)
            log_data = json.loads(formatted)
            
            assert log_data["level"] == "ERROR"
            assert log_data["message"] == "Error occurred"
            assert "exception" in log_data
            assert "ValueError: Test error" in log_data["exception"]


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_default_level(self):
        """Test setup_logging with default INFO level."""
        setup_logging()
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
        
        # Check that JsonFormatter is installed
        handlers = root_logger.handlers
        assert len(handlers) > 0
        assert isinstance(handlers[0].formatter, JsonFormatter)

    def test_setup_logging_debug_level(self):
        """Test setup_logging with DEBUG level."""
        setup_logging(log_level="DEBUG")
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_setup_logging_warning_level(self):
        """Test setup_logging with WARNING level."""
        setup_logging(log_level="WARNING")
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.WARNING

    def test_setup_logging_error_level(self):
        """Test setup_logging with ERROR level."""
        setup_logging(log_level="ERROR")
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.ERROR


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a Logger instance."""
        logger = get_logger("test_module")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_get_logger_different_names(self):
        """Test that get_logger returns different loggers for different names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1 is not logger2
        assert logger1.name == "module1"
        assert logger2.name == "module2"

    def test_get_logger_same_name_returns_same_instance(self):
        """Test that get_logger returns the same instance for the same name."""
        logger1 = get_logger("test_module")
        logger2 = get_logger("test_module")
        
        assert logger1 is logger2

    def test_logger_can_log_messages(self):
        """Test that logger can log messages with JSON formatting."""
        setup_logging(log_level="INFO")
        
        # Capture log output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(JsonFormatter())
        
        logger = get_logger("test_logger")
        logger.handlers = [handler]
        logger.setLevel(logging.INFO)
        
        logger.info("Test info message")
        
        output = stream.getvalue()
        log_data = json.loads(output.strip())
        
        assert log_data["level"] == "INFO"
        assert log_data["message"] == "Test info message"
        assert log_data["logger"] == "test_logger"

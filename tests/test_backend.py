import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.exceptions import ConfigurationError, ParserFailureError
from src.config import get_settings
from src.parsers import IngestionRouter

def test_config_loads_safely():
    # Test that get_settings works when .env is present
    settings = get_settings()
    assert settings.sqlite_db_path == "local_chronicle.db"
    assert settings.log_level == "INFO"

@patch('src.parsers.Path.exists', return_value=False)
def test_ingestion_router_missing_file(mock_exists):
    # Test that routing a missing file throws our custom Exception, not a raw FileNotFoundError
    with pytest.raises(ParserFailureError):
        IngestionRouter.process_file("missing_file.pdf")

@patch('src.parsers.Path.exists', return_value=True)
@patch('src.parsers.Path.read_text', return_value="Hello World")
def test_ingestion_router_text_file(mock_read, mock_exists):
    # Test that a text file is simply read
    text = IngestionRouter.process_file("test.txt")
    assert text == "Hello World"

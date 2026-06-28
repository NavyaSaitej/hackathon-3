import pytest
from backend.parsers import IngestionRouter
from backend.exceptions import ParserFailureError

def test_parse_txt():
    text = IngestionRouter.process_file("local_assets/dummy_files/test.txt")
    assert "Hello from txt" in text

def test_parse_md():
    text = IngestionRouter.process_file("local_assets/dummy_files/test.md")
    assert "Hello from md" in text

def test_parse_docx():
    text = IngestionRouter.process_file("local_assets/dummy_files/test.docx")
    assert "Hello from docx" in text

def test_parse_pptx():
    text = IngestionRouter.process_file("local_assets/dummy_files/test.pptx")
    assert "Hello from pptx" in text

def test_parse_xlsx():
    text = IngestionRouter.process_file("local_assets/dummy_files/test.xlsx")
    assert "Hello from xlsx" in text

def test_parse_pdf():
    text = IngestionRouter.process_file("local_assets/dummy_files/test.pdf")
    assert "Hello from pdf" in text

def test_parse_missing_audio_deps():
    with pytest.raises(ParserFailureError, match="Parsing failed for local_assets/dummy_files/test.wav"):
        IngestionRouter.process_file("local_assets/dummy_files/test.wav")

def test_parse_missing_image_deps():
    with pytest.raises(ParserFailureError, match="Parsing failed for local_assets/dummy_files/test.png"):
        IngestionRouter.process_file("local_assets/dummy_files/test.png")

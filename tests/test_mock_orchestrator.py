import pytest
from unittest.mock import patch, MagicMock
from backend.orchestrator import process_file_offline

@patch('backend.orchestrator.LLMExtractor')
@patch('backend.orchestrator.IngestionRouter.process_file')
def test_full_pipeline_mock(mock_process_file, mock_extractor_class):
    mock_process_file.return_value = "This is a test document about Project X."
    
    mock_extractor = MagicMock()
    mock_extractor.extract.return_value = {
        "summary": "Project X mock summary.",
        "action_items": ["Action 1"],
        "key_entities": ["Project X"]
    }
    mock_extractor_class.return_value = mock_extractor
    
    # Run Orchestrator Pipeline
    result = process_file_offline("dummy_files/test.pdf")
    
    # Assert
    assert result["summary"] == "Project X mock summary."
    assert "Project X" in result["key_entities"]
    
    # Check Database via SQLModel
    from sqlmodel import Session, select
    from backend.database import get_engine, ChronicleNote
    
    engine = get_engine()
    with Session(engine) as session:
        statement = select(ChronicleNote).where(ChronicleNote.filename == "dummy_files/test.pdf")
        note = session.exec(statement).first()
        
        assert note is not None
        assert note.filename == "dummy_files/test.pdf"
        assert note.summary == "Project X mock summary."

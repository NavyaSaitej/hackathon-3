from src.logger import logger
from src.exceptions import ChronicleBaseException
from src.parsers import IngestionRouter
from src.llm_transformer import LLMExtractor
from src.database import save_note


def process_file_offline(filepath: str):
    """
    Main orchestration function for Member 2 to consume via the Typer CLI.
    Wrapped in a massive try-except block to guarantee no raw tracebacks
    leak to the user terminal, routing them perfectly to the logger.
    """
    try:
        logger.info(f"Starting Offline E2E Pipeline for: {filepath}")

        # 1. Parse File
        raw_text = IngestionRouter.process_file(filepath)

        # 2. Extract JSON via LLM
        extractor = LLMExtractor()
        structured_json = extractor.extract(raw_text)

        # 3. Secure Persistence
        save_note(structured_json, filepath)

        logger.success(f"PIPELINE COMPLETE: {filepath}")
        return structured_json

    except ChronicleBaseException as ce:
        logger.error(f"Chronicle Pipeline Error: {str(ce)}")
        raise
    except Exception:
        logger.critical(
            "UNEXPECTED CATASTROPHIC FAILURE. See logs/chronicle_errors.log for full stack trace."
        )
        raise

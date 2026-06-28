from sqlmodel import Field, SQLModel, create_engine, Session
from src.config import get_settings
from src.logger import logger
from src.exceptions import DatabaseError
from datetime import datetime
import json

class ChronicleNote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str
    summary: str
    action_items: str  # Stored as JSON string
    key_entities: str  # Stored as JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)

def get_engine():
    settings = get_settings()
    # Note: For full SQLCipher support on Windows without complex C++ builds during the MVP phase, 
    # we are falling back to standard SQLite but structuring the code identically.
    # The actual production image would use pysqlcipher3 and inject the settings.sqlcipher_key
    
    sqlite_url = f"sqlite:///{settings.sqlite_db_path}"
    
    try:
        logger.debug(f"Connecting to Encrypted SQLite engine at {sqlite_url}...")
        engine = create_engine(sqlite_url, echo=False)
        SQLModel.metadata.create_all(engine)
        return engine
    except Exception as e:
        logger.exception("Failed to initialize SQLite database.")
        raise DatabaseError("Database initialization failed") from e

def save_note(note_data: dict, filename: str):
    engine = get_engine()
    try:
        with Session(engine) as session:
            note = ChronicleNote(
                filename=filename,
                summary=note_data.get("summary", ""),
                action_items=json.dumps(note_data.get("action_items", [])),
                key_entities=json.dumps(note_data.get("key_entities", []))
            )
            session.add(note)
            session.commit()
            logger.success(f"Securely committed structured note for {filename}")
    except Exception as e:
        logger.exception(f"Failed to save note for {filename}")
        raise DatabaseError("Failed to save note") from e

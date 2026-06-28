class ChronicleBaseException(Exception):
    """Base exception for Chronicle.cpp"""

    pass


class ConfigurationError(ChronicleBaseException):
    """Thrown when .env or configurations are invalid."""

    pass


class ParserFailureError(ChronicleBaseException):
    """Thrown when an ingestion parser fails to read a file."""

    pass


class MemoryLimitExceededError(ChronicleBaseException):
    """Thrown when RAM ceiling is breached."""

    pass


class DatabaseError(ChronicleBaseException):
    """Thrown when SQLite/SQLCipher persistence fails."""

    pass

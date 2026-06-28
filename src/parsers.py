import gc
from pathlib import Path
from src.logger import logger
from src.exceptions import ParserFailureError

class IngestionRouter:
    """Routes files to the correct offline parser based on extension."""
    
    @staticmethod
    def process_file(filepath: str) -> str:
        path = Path(filepath)
        if not path.exists():
            logger.error(f"File not found: {filepath}")
            raise ParserFailureError(f"File not found: {filepath}")
            
        ext = path.suffix.lower()
        try:
            logger.info(f"Routing {filepath} to parser for extension '{ext}'")
            
            if ext == '.pdf':
                text = IngestionRouter._parse_pdf(path)
            elif ext in ['.txt', '.md']:
                text = path.read_text(encoding='utf-8')
            elif ext in ['.wav', '.mp3']:
                text = IngestionRouter._parse_audio(path)
            elif ext in ['.png', '.jpg']:
                text = IngestionRouter._parse_image(path)
            else:
                logger.warning(f"Unsupported file type: {ext}. Attempting raw string extraction.")
                text = path.read_text(encoding='utf-8', errors='ignore')
                
            logger.info(f"Successfully extracted {len(text)} characters.")
            return text
            
        except Exception as e:
            logger.exception(f"Failed to parse {filepath}")
            raise ParserFailureError(f"Parsing failed for {filepath}") from e
        finally:
            logger.debug("Enforcing Garbage Collection after parser phase...")
            gc.collect()

    @staticmethod
    def _parse_pdf(path: Path) -> str:
        import fitz  # PyMuPDF
        logger.debug("Loading PyMuPDF...")
        doc = fitz.open(str(path))
        text = "".join([page.get_text() + "\n" for page in doc])
        return text

    @staticmethod
    def _parse_audio(path: Path) -> str:
        logger.debug("Loading faster-whisper...")
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            logger.error("faster-whisper not installed.")
            raise ParserFailureError("Audio dependencies missing.")
        
        # Audio normalization via ffmpeg would go here in production
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(path), beam_size=5)
        text = " ".join([segment.text for segment in segments])
        
        # Explicitly delete model to free RAM
        del model
        return text

    @staticmethod
    def _parse_image(path: Path) -> str:
        logger.debug("Loading rapidocr_onnxruntime...")
        try:
            from rapidocr_onnxruntime import RapidOCR
        except ImportError:
            logger.error("rapidocr_onnxruntime not installed.")
            raise ParserFailureError("Image dependencies missing.")
            
        engine = RapidOCR()
        result, _ = engine(str(path))
        if result:
            text = " ".join([res[1] for res in result])
        else:
            text = ""
            
        # Explicitly delete engine
        del engine
        return text

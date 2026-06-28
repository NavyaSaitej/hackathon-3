# Task List

> *Aligned with GitLab Issues Tracker*

## Member 1: AI Core & Omni-Modal Data Pipeline (5 Tasks)

### 1. Diagnostics & Configuration Management
- [ ] Implement `src/config.py` using `pydantic-settings` to validate `.env`.
- [ ] Implement `src/logger.py` using `loguru` to capture traces to terminal and `logs/chronicle_errors.log`.
- [ ] Define custom hierarchy in `src/exceptions.py`.

### 2. Unified Ingestion Router (Audio, OCR, Docs)
- [ ] Implement `src/parsers.py`. Abstract `faster-whisper`, `rapidocr`, `PyMuPDF`, and `python-docx`.
- [ ] Wrap all parsers in `try...except` throwing custom exceptions for `loguru` to catch.
- [ ] Add `ffmpeg-python` step to normalize audio inputs to 16kHz mono before Whisper processing.

### 3. LLM JSON Extraction & Memory Management
- [ ] Implement `src/llm_transformer.py`.
- [ ] Load GGUF model via `llama-cpp-python`.
- [ ] **Critical**: Implement explicit `del model; gc.collect()` logic inside a `finally:` block.

### 4. Encrypted SQLite Storage (SQLCipher)
- [ ] Implement `src/database.py` using `sqlmodel` (wrapping SQLite).
- [ ] Inject `SQLCIPHER_KEY` from `src/config.py`.
- [ ] Define `JSON` column in `sqlmodel` for the raw schema output.

### 5. Air-Gap Validation (Backend & Diagnostics)
- [ ] Inject a complex PDF and a Whiteboard image offline. Assert output is valid JSON.
- [ ] Inject a corrupted file to verify `loguru` accurately logs the trace offline.

---

## Member 2: CLI, UX & DevOps (4 Tasks)
*(CLI Tasks remain unchanged)*

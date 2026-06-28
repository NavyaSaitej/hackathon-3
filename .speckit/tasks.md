# Task List

> *Aligned with GitLab Issues Tracker*

## Member 1: AI Core & Omni-Modal Data Pipeline (4 Tasks)

### 1. Unified Ingestion Router (Audio, OCR, Docs)
- [ ] Implement `src/parsers.py`. Abstract `faster-whisper`, `rapidocr`, `PyMuPDF`, and `python-docx`.
- [ ] Add `ffmpeg-python` step to normalize audio inputs to 16kHz mono before Whisper processing.
- [ ] Test memory consumption during OCR and Audio transcription.

### 2. LLM JSON Extraction & Memory Management
- [ ] Implement `src/llm_transformer.py`.
- [ ] Load GGUF model via `llama-cpp-python`.
- [ ] **Critical**: Implement explicit `del model; gc.collect()` logic at the module boundary to ensure RAM is freed.

### 3. Encrypted SQLite Storage (SQLCipher + Dotenv)
- [ ] Implement `src/database.py` using `sqlmodel` (wrapping SQLite).
- [ ] Integrate `python-dotenv` so `SQLCIPHER_KEY` is loaded from a local `.env` file securely.
- [ ] Define `JSON` column in `sqlmodel` for the raw schema output.

### 4. Air-Gap Validation (Backend & DB)
- [ ] Inject a complex PDF and a Whiteboard image offline. Assert output is valid JSON.
- [ ] Verify SQLite encryption keys are working and insertion is lock-free.

---

## Member 2: CLI, UX & DevOps (4 Tasks)

### 5. Typer CLI Architecture
- [ ] Create `src/main.py` using standard Typer boilerplate. 
- [ ] Add `@app.command()` for `ingest`, `query`, and `status`. Provide proper routing to Member 1's `src/parsers.py`.

### 6. Rich UI & Graceful Error Handling
- [ ] Use `rich.table.Table` to output the database contents.
- [ ] Catch `MemoryError` gracefully.

### 7. Phase 3 Repo Audit (CI/CD & Binary)
- [ ] Implement 10+ strict CI checks (Ruff, Mypy, Bandit, Vulture, Pytest).
- [ ] Setup `.gitlab-ci.yml`.
- [ ] Write `build.spec` for PyInstaller. Run `pyinstaller --onefile src/main.py`.

### 8. Air-Gap Validation (CLI Output)
- [ ] Disable network adapters. 
- [ ] Run E2E test from CLI using a `.png` and `.wav` file, asserting 0 network requests.

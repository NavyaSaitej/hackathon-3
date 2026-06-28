# Task List

> *Aligned with GitLab Issues Tracker*

## Member 1: AI Core & Omni-Modal Data Pipeline (4 Tasks)

### 1. Unified Ingestion Router (Audio, OCR, Docs)
- [ ] Initialize Python virtual env (`uv venv`) and lock dependencies.
- [ ] Implement `src/parsers.py`. Abstract `faster-whisper`, `rapidocr`, `PyMuPDF`, and `python-docx` behind a generic `Ingestor` interface.
- [ ] Test memory consumption during OCR and Audio transcription using `memory_profiler`.

### 2. LLM JSON Extraction & Memory Management
- [ ] Implement `src/llm_transformer.py`.
- [ ] Load GGUF model via `llama-cpp-python`.
- [ ] **Critical**: Implement explicit `del model; gc.collect()` logic between the ingestion phase and the LLM extraction phase to stay under 6GB.

### 3. Encrypted SQLite Storage
- [ ] Implement `src/database.py` using `sqlmodel` (wrapping SQLite).
- [ ] Configure SQLite engine with `PRAGMA journal_mode=WAL;`.
- [ ] Define `JSON` column in `sqlmodel` for the raw schema output.

### 4. Air-Gap Validation (Backend & DB)
- [ ] Inject a complex PDF and a Whiteboard image offline. Assert output is valid JSON.
- [ ] Verify SQLite data insertion without locking errors.

---

## Member 2: CLI, UX & DevOps (4 Tasks)

### 5. Typer CLI Architecture
- [ ] Create `src/main.py` using standard Typer boilerplate. 
- [ ] Add `@app.command()` for `ingest`, `query`, and `status`. Provide proper routing to the Omni-Modal ingestor based on file extension.

### 6. Rich UI & Graceful Error Handling
- [ ] Use `rich.table.Table` to output the database contents in the `query` command.
- [ ] Catch `MemoryError` and OS interrupts (`Ctrl+C`) gracefully.
- [ ] Display rich spinners during the heavy OCR/LLM processing phases.

### 7. Phase 3 Repo Audit (CI/CD & Binary)
- [ ] Implement 10+ strict CI checks (Ruff, Mypy, Bandit, Vulture, Pytest).
- [ ] Setup `.gitlab-ci.yml`.
- [ ] Write `build.spec` for PyInstaller. Run `pyinstaller --onefile src/main.py`.

### 8. Air-Gap Validation (CLI & Resilience)
- [ ] Disable network adapters on the host machine. 
- [ ] Run full E2E test from CLI using a `.png` and `.wav` file, asserting 0 network requests.

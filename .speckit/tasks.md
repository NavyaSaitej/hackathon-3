# Task List

> *Aligned with GitLab Issues Tracker*

## Member 1: AI & Core Backend (4 Tasks)

### 1. Offline Audio Ingestion Pipeline
- [ ] Initialize Python virtual env (`uv venv`) and lock dependencies.
- [ ] Implement `src/audio_processor.py`. Abstract `faster-whisper` behind a `BaseTranscriber` interface.
- [ ] Test memory consumption during transcription using `memory_profiler`.

### 2. SLM JSON Grammar Extraction
- [ ] Implement `src/llm_transformer.py`.
- [ ] Load GGUF model via `llama-cpp-python`.
- [ ] Pass the strict JSON grammar string to the `create_chat_completion` call.

### 3. Encrypted SQLite Storage
- [ ] Implement `src/database.py` using `sqlmodel` (wrapping SQLite).
- [ ] Configure SQLite engine with `PRAGMA journal_mode=WAL;`.
- [ ] Define `JSON` column in `sqlmodel` for the raw schema output.

### 4. Air-Gap Validation (Backend & DB)
- [ ] Inject a highly confusing transcript offline. Assert output remains strictly valid JSON.
- [ ] Verify SQLite data insertion without locking errors.

---

## Member 2: CLI, UX & DevOps (4 Tasks)

### 5. Typer CLI Architecture
- [ ] Create `src/main.py` using standard Typer boilerplate. 
- [ ] Add `@app.command()` for `ingest`, `query`, and `status`.

### 6. Rich UI & Graceful Error Handling
- [ ] Use `rich.table.Table` to output the database contents in the `query` command.
- [ ] Catch `MemoryError` and OS interrupts (`Ctrl+C`) gracefully.

### 7. Phase 3 Repo Audit (CI/CD & Binary)
- [ ] Implement 10+ strict CI checks (Ruff, Mypy, Bandit, Vulture, Pytest).
- [ ] Setup `.gitlab-ci.yml`.
- [ ] Write `build.spec` for PyInstaller. Run `pyinstaller --onefile src/main.py`.

### 8. Air-Gap Validation (CLI & Resilience)
- [ ] Disable network adapters on the host machine. 
- [ ] Run full E2E test from CLI and assert 0 network requests and perfect Rich layout.

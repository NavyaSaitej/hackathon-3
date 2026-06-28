# Task List

> *Aligned with GitLab Issues Tracker*

## Member 1: AI Core Backend (1 Epic Task)

### 1. The Monolithic Backend (`src/backend.py`)
- [ ] Initialize Python virtual env (`uv venv`) and lock dependencies.
- [ ] **Ingestion Router**: Implement functions for `faster-whisper`, `rapidocr`, `PyMuPDF`, and `python-docx` inside `backend.py`.
- [ ] **LLM Extraction**: Implement `Phi-3-mini` logic via `llama-cpp-python` in `backend.py`.
- [ ] **Memory Manager**: Enforce `del model; gc.collect()` between parser and LLM steps.
- [ ] **Database**: Create `sqlmodel` + `SQLCipher` persistence logic inside `backend.py`.
- [ ] **Validation**: Run offline E2E backend validation to ensure no OOM crashes.

---

## Member 2: CLI, UX & DevOps (4 Tasks)

### 2. Typer CLI Architecture
- [ ] Create `src/main.py` using standard Typer boilerplate. 
- [ ] Add `@app.command()` for `ingest`, `query`, and `status`. Provide proper routing to Member 1's `backend.py` based on file extension.

### 3. Rich UI & Graceful Error Handling
- [ ] Use `rich.table.Table` to output the database contents in the `query` command.
- [ ] Catch `MemoryError` and OS interrupts (`Ctrl+C`) gracefully.
- [ ] Display rich spinners during the heavy OCR/LLM processing phases.

### 4. Phase 3 Repo Audit (CI/CD & Binary)
- [ ] Implement 10+ strict CI checks (Ruff, Mypy, Bandit, Vulture, Pytest).
- [ ] Setup `.gitlab-ci.yml`.
- [ ] Write `build.spec` for PyInstaller. Run `pyinstaller --onefile src/main.py`.

### 5. Air-Gap Validation (CLI & Resilience)
- [ ] Disable network adapters on the host machine. 
- [ ] Run full E2E test from CLI using a `.png` and `.wav` file, asserting 0 network requests.

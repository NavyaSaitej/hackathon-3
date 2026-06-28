# Task List

> *Amended by: [Tech Lead], [QA Engineer]*
> *V2 Refined by: [Junior Developer Proxy], [Database Admin]*

## Phase 1: Foundation
- [ ] **JD**: Run `uv venv` and `uv pip install typer rich pydantic sqlmodel llama-cpp-python faster-whisper`. Save to `requirements.txt`.
- [ ] **DBA**: Create `src/database.py`. Configure SQLite engine with `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;` for high concurrency and write speed.
- [ ] **JD**: Create `src/main.py` using standard Typer boilerplate. Add `@app.command()` for `ingest`.

## Phase 2: Transcription
- [ ] **JD**: Create `src/audio_processor.py`. Use `faster_whisper.WhisperModel("tiny.en", device="cpu", compute_type="int8")`.
- [ ] **QA**: Add tests passing corrupt audio files.
- [ ] **DBA**: Log transcription metadata (duration, processing time) to an `analytics_local` table for debugging without telemetry.

## Phase 3: SLM Extraction
- [ ] **JD**: Create `src/llm_transformer.py`. Download `Phi-3-mini-4k-instruct-q4.gguf` into a `models/` dir. 
- [ ] **JD**: Use `Llama(model_path="models/phi3.gguf", n_ctx=4096, n_threads=4)`.
- [ ] **DBA**: Define `JSON` column in `sqlmodel` for the raw schema output to ensure future flexibility if the schema changes. Add indexing on `title` and `timestamp`.

## Phase 4: Polish & Packaging
- [ ] **JD**: Use `rich.table.Table` to output the database contents in the `query` command.
- [ ] **DevOps**: Write `build.spec` for PyInstaller. Run `pyinstaller --onefile src/main.py`.
- [ ] **QA**: Disable network adapters and run the frozen executable.

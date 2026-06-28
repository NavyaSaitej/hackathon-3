# Development Plan

> *Amended by: [Project Manager], [Risk Assessor]*
> *V2 Refined by: [DevOps Engineer], [Agile Coach]*

This plan breaks down the project implementation into logical, tested milestones. 

## Phase 1: Basic Working Foundation & Infrastructure
- **Agile Scope**: 2 Hours. **Definition of Done**: DB initializes, CLI accepts commands and prints help.
- **Steps**:
  - Init `typer` CLI.
  - Implement SQLCipher connection.
  - **DevOps**: Setup `logging` module to write rotating logs to `~/.local/share/local-ai/logs/app.log`. Absolutely no stdout pollution unless asked.

## Phase 2: Ingestion & Transcription
- **Agile Scope**: 3 Hours. **Definition of Done**: Audio correctly converts to raw text in terminal.
- **Steps**:
  - Implement `faster-whisper`.
  - Add robust audio chunking.
  - **DevOps**: Wrap `ffmpeg` gracefully so the app auto-downloads the static binary if missing, ensuring seamless user experience.

## Phase 3: SLM Transformation
- **Agile Scope**: 4 Hours. **Definition of Done**: Raw text securely pipes into JSON and saves to DB.
- **Steps**:
  - Implement `llama-cpp-python` with strict JSON grammar.
  - Chain transcription text -> Prompt -> SLM -> DB.
  - **DevOps**: Implement memory garbage collection triggers between audio processing and SLM loading to prevent overlap memory spikes.

## Phase 4: Polish, Testing, & Binary Packaging
- **Agile Scope**: 3 Hours. **Definition of Done**: E2E tests pass, single executable generated.
- **Steps**:
  - **DevOps**: Use `PyInstaller` or `Nuitka` to freeze the entire Python application into a single standalone binary for Windows/Linux. This eliminates the need for users to have Python installed.
  - Run the `stress_eval_loop.py` to bombard the CLI.

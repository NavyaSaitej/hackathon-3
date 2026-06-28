# System Architecture

## Core Pipeline (Sequential Modular Execution)
Due to the strict 6GB memory ceiling, all models **must be loaded sequentially**. Loading Whisper, RapidOCR, and Phi-3 simultaneously will cause an Out-Of-Memory (OOM) crash on edge hardware. 

We maintain a modular backend structure, passing string outputs between stateless modules to ensure clean memory unloading.

1. **Configuration & Diagnostics (`src/config.py` & `src/logger.py`)**
   - **Config Validation**: Uses `pydantic-settings` to strictly validate all `.env` keys (e.g., `SQLCIPHER_KEY`, model paths) on startup. If a key is missing, the app halts immediately.
   - **Advanced Diagnostics**: Uses `loguru` to intercept all errors. Custom exceptions (`src/exceptions.py`) are logged to both `stderr` (colorized) and `logs/chronicle_errors.log` (full stack traces).
2. **Unified Ingestion Router (`src/parsers.py`)**
   - **Audio (`.wav`, `.mp3`)**: Pre-processed via `ffmpeg-python` (forced to 16kHz mono). Loads `faster-whisper`. Extracts text. Unloads Whisper.
   - **Images (`.png`, `.jpg`)**: Loads `rapidocr-onnxruntime`. Extracts text. Unloads RapidOCR.
   - **Documents (`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.md`, `.txt`)**: Uses `PyMuPDF`, `python-docx`, `python-pptx`, and `pandas`. 
3. **Context Normalization (`src/parsers.py`)**
   - The raw output from any parser is flattened into a single UTF-8 string buffer.
4. **Structured Extraction (`src/llm_transformer.py`)**
   - **LLM Initialization**: Loads `llama-cpp-python` with `Phi-3-mini-4k-instruct-q4.gguf`.
   - Passes the flattened string and the strict JSON Grammar to the LLM.
   - Unloads the LLM immediately upon completion.
5. **Persistence (`src/database.py`)**
   - Validated JSON payload is encrypted and committed to SQLite via `sqlmodel` + `SQLCipher`.
   - **Security**: Master database keys are never hardcoded. Injected securely via Config phase.

## IPC and Memory Management
- We use manual Garbage Collection (`import gc; gc.collect()`) after the `del` command inside the cross-module boundaries to aggressively free RAM.
- Typer (`src/main.py`) handles routing and Rich handles UX. There is no background threading for AI inference; everything is strictly blocking.

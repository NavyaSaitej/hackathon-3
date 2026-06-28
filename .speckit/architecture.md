# System Architecture

## Core Pipeline (Sequential Execution)
Due to the strict 6GB memory ceiling, all models **must be loaded sequentially**. Loading Whisper, RapidOCR, and Phi-3 simultaneously will cause an Out-Of-Memory (OOM) crash on edge hardware.

1. **Unified Ingestion Router**
   - **Audio (`.wav`, `.mp3`)**: Loads `faster-whisper`. Extracts text. Unloads Whisper.
   - **Images (`.png`, `.jpg`)**: Loads `rapidocr-onnxruntime`. Extracts text. Unloads RapidOCR.
   - **Documents (`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.md`, `.txt`)**: Uses `PyMuPDF`, `python-docx`, `python-pptx`, and `pandas`. (Negligible memory, but handles large docs via generators).
2. **Context Normalization**
   - The raw output from any parser is flattened into a single UTF-8 string buffer.
3. **Structured Extraction**
   - **LLM Initialization**: Loads `llama-cpp-python` with `Phi-3-mini-4k-instruct-q4.gguf`.
   - Passes the flattened string and the strict JSON Grammar to the LLM.
   - Unloads the LLM immediately upon completion.
4. **Persistence**
   - Validated JSON payload is encrypted and committed to SQLite via `sqlmodel` + `SQLCipher`.

## IPC and Memory Management
- We use manual Garbage Collection (`import gc; gc.collect()`) after the `del` command to aggressively free RAM between the Ingestion and Extraction phases.
- Typer handles routing and Rich handles UX. There is no background threading for AI inference; everything is strictly blocking.

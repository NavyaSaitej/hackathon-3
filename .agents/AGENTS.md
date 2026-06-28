# Chronicle.cpp — Agent Handoff Guide & Workspace Rules

## Project Overview
**Chronicle.cpp** is an offline-first, CPU-optimized application that transforms unstructured Omni-Modal data (Audio, Images, Documents) into structured JSON data.
It strictly adheres to the CPU-First Hackathon rules: **No GPU, 100% Offline (Air-Gapped), GPLv3 License**.

## Architecture Boundaries
- **Backend (Member 1)**: `faster-whisper` (Audio), `rapidocr-onnxruntime` (Images), `PyMuPDF`/`python-docx` (Docs). `llama-cpp-python` (Phi-3-mini GGUF) for JSON extraction, `sqlmodel` + `SQLCipher` for encrypted SQLite storage.
- **Frontend/CLI (Member 2)**: `Typer` for routing, `Rich` for UI components (spinners, tables).
- **DevOps (Member 2)**: Local GitLab runner, 10+ strict CI checks, `PyInstaller` for binary freezing.

---

## 🤖 Agent Role & Directives (Member 2 Focus)
If you are an agent assisting Member 2, your primary domain is **CLI, UX, and DevOps**. 
You are strictly forbidden from altering the AI Core Backend logic unless specifically requested.

**Your Critical Guidelines:**
1. **Strict CPU & Air-Gap Enforcement**: Never include network calls (e.g., `requests`, `urllib`) in your UI or CI scripts. The CI runner must test offline capabilities.
2. **UX Standards**: Use `Typer` for all CLI arguments. Use `Rich` for all terminal outputs (Progress bars, tables, spinners). Do not use standard `print()` statements. 
3. **File Type Routing**: The `Typer` CLI must properly identify the extension of the ingested file (e.g., `.pdf`, `.png`, `.mp3`) and pass it correctly to Member 1's Omni-Modal router.
4. **Phase 3 Audit Mastery**: You are responsible for configuring `.gitlab-ci.yml` and enforcing the following checks: `Ruff`, `Mypy`, `Bandit`, `Vulture`, `Pytest`. Ensure they are legitimate, strict configurations. No stubbing allowed.
5. **PyInstaller Freezing**: Write the `build.spec` file to compile the entire Python app into a single executable binary. Ensure all models and SQLite/CTranslate binaries are properly bundled.

---

## 📂 Required Reading 
Before generating any code for Member 2, read the following files:
1. `.speckit/constitution.md` (The non-negotiable rules)
2. `.speckit/design.md` (The UX/UI standards)
3. `.speckit/tasks.md` (Your specific tasks are Issues 5, 6, 7, and 8)

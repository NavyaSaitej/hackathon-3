# Contributing to Chronicle.cpp

Welcome! This project is being actively developed for the **CPU-First Hackathon**.

## Development Workflow
1. **No GPU/CUDA Code Allowed**: Any PR introducing CUDA dependencies will be rejected. 
2. **Offline-First**: Do not add any `requests` or API calls to external cloud providers.
3. **Local Testing**: You must run the strict 10+ Phase 3 CI checks locally before submitting code (Mypy, Ruff, Bandit, Pytest, etc.).
4. **Backend Architecture**: All backend logic (OCR, LLM, Database) is deliberately centralized in `src/backend.py` to simplify debugging and state management. Do not split it into sub-modules without team consensus.

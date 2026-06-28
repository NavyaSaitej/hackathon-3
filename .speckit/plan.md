# Development Plan

> *V3 Refined for Official Hackathon Deadlines*

## 📋 PHASE 1 — Plan & Spec (Deadline: Before 10 AM)
- **Goal**: Full project scaffolding and repository documentation.
- **Tasks**:
  - Finalize SpecKit (Done).
  - Write `README.md` outlining the Audio-to-Notes idea.
  - Create repository Issues with assignees, estimates, and due dates.
  - Draft the work-division plan.

## 🚀 PHASE 2 — MVP (Deadline: Before Lunch Break)
- **Goal**: Working CLI demo on real audio records.
- **Tasks**:
  - Implement Audio Ingestion (`faster-whisper`).
  - Implement SLM Transformation (`llama.cpp` + `Phi-3-mini`).
  - Implement SQLite Database storage via `sqlmodel`.
  - Compile the CLI build version.
  - Run the demo with Wi-Fi physically turned OFF.

## 🔍 PHASE 3 — Repo Audit (Deadline: Before 3 PM)
- **Goal**: Perfect repository health with 10+ real CI checks.
- **Tasks**:
  - Ensure `README`, `CONTRIBUTING`, and `CHANGELOG` are polished.
  - Set up local GitLab Runner `.gitlab-ci.yml`.
  - Implement at least 10 **legitimate** pre-commit & CI checks:
    1. Black/Ruff (Formatting)
    2. Flake8/Ruff (Linting)
    3. Mypy (Type-checking)
    4. Bandit (Security Scan)
    5. Vulture (Dead code)
    6. Pytest (Unit tests)
    7. Commitizen (Semantic commits check)
    8. Safety (Dependency vulnerability scan)
    9. Interrogate (Docstring coverage)
    10. Isort (Import sorting)
  - **CRITICAL**: No faking or stubbing jobs. All checks must execute real logic and pass.

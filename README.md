# 🧠 Chronicle.cpp - Offline Knowledge Distillation

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()
[![Architecture](https://img.shields.io/badge/Architecture-CPU%20Only-orange)]()
[![Network](https://img.shields.io/badge/Network-100%25%20Offline-success)]()

> **An enterprise-grade, offline-first, CPU-optimized CLI application built for the CPU-First Hackathon.**

---

## 🎯 Executive Summary
In high-security and enterprise environments, uploading sensitive meeting audio, confidential documents, or proprietary whiteboard images to cloud-based APIs (such as OpenAI or Anthropic) represents a severe data privacy violation. 

**Chronicle.cpp** mitigates this risk entirely by providing a hyper-optimized, air-gapped CLI tool that processes unstructured **Omni-Modal** data entirely on edge devices. 

Our application seamlessly:
1. **Configures Securely**: Validates all cryptographic `.env` variables via `pydantic-settings` before booting, preventing late-stage crashes.
2. **Ingests Omni-Modal Data**: Securely loads Audio (`.wav`, `.mp3`), Images (`.png`, `.jpg`), and Documents (`.pdf`, `.docx`, `.xlsx`, `.pptx`, `.md`, `.txt`).
3. **Normalizes via Local Parsers**: 
   - Audio is pre-processed (`ffmpeg-python`) and transcribed locally using a CTranslate2 backend (`faster-whisper`).
   - Images are scanned using CPU-optimized OCR (`rapidocr-onnxruntime`).
   - Documents are parsed using high-speed libraries (`PyMuPDF`, `python-docx`).
4. **Transforms**: The flattened text is converted into a strict, structured JSON schema (Summaries, Action Items, Key Decisions) using a local **Ollama** engine (`phi3` model). If Ollama is unavailable, the pipeline falls back to a 100% offline, zero-dependency Python **NLP Heuristics Engine**.
5. **Persists**: The extracted intelligence is saved into an encrypted SQLite database (`SQLCipher`), managed securely via `.env` keys within `local_assets/`.

All processing occurs sequentially with strict **manual garbage collection** to ensure a maximum memory footprint of 6GB RAM. Furthermore, the entire architecture is wrapped in **Advanced Error Tracing** (`loguru`), ensuring robust debugging capabilities in production.

---

## ⚙️ Core Technical Constraints (Hackathon Compliance)
This project strictly adheres to the official hackathon rubric:
- 🚫 **CPU-First**: Absolutely no GPU/CUDA dependencies. Inference relies solely on heavily optimized local engines (`ollama`, `whisper.cpp`) and ONNX Runtimes.
- 📴 **Offline-First**: Guaranteed air-gap resiliency. The core pipeline is guaranteed to function flawlessly with the host machine's Wi-Fi adapters physically disabled, thanks to local Ollama processing and Regex/NLP fallbacks.
- 🔓 **Free & Open Source**: The entire codebase is licensed under **GNU GPLv3** (Strong Copyleft), ensuring maximum open-source freedom and compliance.

---

## 📂 The SpecKit (Documentation Architecture)
Our engineering methodology, system architecture, UX design, and granular tasks are heavily documented in the `.speckit/` directory. 

| Document | Purpose |
|----------|---------|
| [📜 Constitution](.speckit/constitution.md) | Non-negotiable project rules (Air-gap, resource ceilings, licensing). |
| [📝 Feature Spec](.speckit/specify.md) | Detailed I/O constraints across all 10 file formats. |
| [🏗️ Architecture](.speckit/architecture.md) | The Unified Ingestion Router and Memory Management constraints. |
| [🎨 CLI Design](.speckit/design.md) | Elegant, cognitive-load tested UX/UI flows using `Typer` and `Rich`. |
| [📅 Dev Plan](.speckit/plan.md) | Strict timeline alignment to the Phase 1, 2, and 3 Hackathon deadlines. |
| [✅ Task List](.speckit/tasks.md) | Granular implementation checklist and acceptance criteria. |
| [🧪 Test Strategy](.speckit/testing_strategy.md) | Chaos engineering and air-gap E2E verification plans. |

---

## 📋 Work Division Plan
To ensure rapid execution across the strict Phase 2 and Phase 3 deadlines, the 2-person team structure is divided into distinct, non-blocking domains. 

*(Note: Individual tasks, time estimates, and due dates are actively tracked in the GitLab Issues board).*

| Domain | Primary Owner | Key Responsibilities |
|--------|--------------|----------------------|
| **AI & Core Backend** | **Member 1** | • Implement Diagnostics (`loguru`) & Omni-Modal Parsers (`whisper`, `rapidocr`, `PyMuPDF`).<br>• Enforce Garbage Collection (`gc.collect`) across backend module boundaries.<br>• Build the `OllamaOrchestrator` and NLP Fallback Engine.<br>• Design the `SQLModel` encrypted schema in `local_assets/`. |
| **CLI, UX & DevOps** | **Member 2** | • Develop the `Typer` (`frontend/cli.py`) interactive UI presentation.<br>• Implement robust exception handling and memory cleanup.<br>• Configure local GitLab CI Runner (10+ checks). |

---

## 🚀 Usage (MVP Demo)
*(To be compiled in Phase 2)*

The application is designed to be as intuitive as standard UNIX tools.

### Prerequisites
Before ingesting data, ensure your local Ollama engine has downloaded the Phi-3 model:
```bash
ollama pull phi3
```
*(If the model is missing or the server crashes, Chronicle automatically falls back to an offline Python NLP engine).*

### Basic Usage
```bash
# Process a meeting recording offline
chronicle ingest local_assets/dummy_files/confidential_meeting.mp3

# Process a whiteboard scan offline
chronicle ingest local_assets/dummy_files/architectural_diagram.png

# Process a slide deck offline
chronicle ingest local_assets/dummy_files/q3_planning.pptx

# View extracted structured notes in a terminal table
chronicle list

# View the raw JSON output for a specific ID
chronicle view 1
```

---

## 📜 License
Distributed under the **GNU General Public License v3.0 (GPLv3)**. See `LICENSE` for more information.

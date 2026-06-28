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
4. **Transforms**: The flattened text is converted into a strict, structured JSON schema (Summaries, Action Items, Key Decisions) using an aggressively quantized Small Language Model (`Phi-3-mini`) via constrained grammar decoding.
5. **Persists**: The extracted intelligence is saved into an encrypted SQLite database (`SQLCipher`), managed securely via `.env` keys.

All processing occurs sequentially with strict **manual garbage collection** to ensure a maximum memory footprint of 6GB RAM. Furthermore, the entire architecture is wrapped in **Advanced Error Tracing** (`loguru`), ensuring robust debugging capabilities in production.

---

## ⚙️ Core Technical Constraints (Hackathon Compliance)
This project strictly adheres to the official hackathon rubric:
- 🚫 **CPU-First**: Absolutely no GPU/CUDA dependencies. Inference relies solely on heavily optimized C++ backends (`llama.cpp`, `whisper.cpp`) and ONNX Runtimes.
- 📴 **Offline-First**: Guaranteed air-gap resiliency. The core pipeline is guaranteed to function flawlessly with the host machine's Wi-Fi adapters physically disabled.
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
| **AI & Core Backend** | **Member 1** | • Implement Diagnostics (`loguru`) & Omni-Modal Parsers (`whisper`, `rapidocr`, `PyMuPDF`).<br>• Enforce Garbage Collection (`gc.collect`) across backend module boundaries.<br>• Compile JSON Grammar for `llama.cpp` constrained decoding.<br>• Design the `SQLModel` encrypted schema and manage `.env` security. |
| **CLI, UX & DevOps** | **Member 2** | • Develop the `Typer` (`src/main.py`) interactive UI presentation.<br>• Implement robust exception handling and memory cleanup.<br>• Configure local GitLab CI Runner (10+ checks) & PyInstaller executable freezing. |

---

## 🚀 Usage (MVP Demo)
*(To be compiled in Phase 2)*

The application is designed to be as intuitive as standard UNIX tools.
```bash
# Process a meeting recording offline
chronicle ingest confidential_meeting.mp3

# Process a whiteboard scan offline
chronicle ingest architectural_diagram.png

# Process a slide deck offline
chronicle ingest q3_planning.pptx

# View encrypted structured notes in a terminal table
chronicle query --topic "Hackathon Planning"
```

---

## 📜 License
Distributed under the **GNU General Public License v3.0 (GPLv3)**. See `LICENSE` for more information.

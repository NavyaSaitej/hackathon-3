# Hackathon-3 Constitution

> This document defines the absolute, non-negotiable rules for the Local AI project. All development MUST adhere strictly to these principles.
> *Amended by: [Security Auditor], [Performance Optimizer], [Data Privacy Officer]*
> *V2 Refined by: [Edge-Computing Architect], [Open-Source Purist], [Accessibility Advocate]*

## 1. Offline First & Air-Gapped Resiliency
- **Absolute Air-Gap:** The application must operate flawlessly without an internet connection. Any HTTP/Socket requests attempting to reach external IPs will result in immediate build failure.
- **Dependency Sandboxing & OS Hygiene:** All libraries must bundle their own dependencies. App data and models must be stored in standard OS-specific localized directories (e.g., `~/.local/share/local-ai` or `%APPDATA%`), leaving zero footprint elsewhere. [Open-Source Purist]
- **Resilient Fallbacks:** If a model file is missing or corrupted, the system must degrade gracefully with a human-readable CLI prompt instructing the user on how to sideload the model.

## 2. CPU-Optimized Inference & Resource Ceilings
- **Strict CPU Bounds:** Code must prioritize execution on CPU. 
- **Thermal & Battery Awareness:** Dynamically detect available cores. Never use 100% of available CPU threads; reserve at least 1 core for OS stability. Implement thermal throttling safeguards (e.g., pause/yield during long processing). [Edge-Computing Architect]
- **Memory Ceiling:** The combined memory footprint of the ASR (Whisper) and SLM (Llama.cpp) must NEVER exceed 6.0 GB of RAM.
- **Quantization Mandate:** SLMs must use Q4_K_M or Q5_K_M GGUF quantization.
- **License Purity:** All models and dependencies MUST be strictly open-source (MIT, Apache 2.0, or Llama-3 Community License). No restrictive commercial wrappers. [Open-Source Purist]

## 3. Security, Privacy & Zero-Trust
- **Input Sanitization:** Audio files must be treated as hostile.
- **Zero-Retention Processing:** Temporary `.wav` chunks MUST be securely deleted immediately after processing.
- **Encrypted Rest State:** The SQLite database must use `SQLCipher` for local encryption at rest.

## 4. Universal Accessibility
- **Screen-Reader Compliance:** All CLI outputs must avoid complex ASCII art that breaks text-to-speech. Use semantic text labels (e.g., `[SUCCESS]`, `[ERROR]`) instead of relying solely on colors or emojis. [Accessibility Advocate]
- **Keyboard & Navigation:** Interactive CLI prompts must be fully traversable via standard keyboard inputs without mouse requirements. [Accessibility Advocate]

## 5. Simplicity and Code Integrity
- Choose simple, battle-tested solutions over complex architectures. 
- A fully working, bug-free simple feature scores higher than a broken complex feature.

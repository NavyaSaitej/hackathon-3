# Hackathon Overview: "Local AI"

This project focuses on building an *offline-first, CPU-optimized AI application* capable of transforming unstructured data (audio, text, documents, video, images) into highly structured, actionable datasets.

## Core Technical Constraints

*   **Offline-First App:** The application must function reliably without a persistent internet connection. All core processing, vectorization, and inference must occur locally on the user's device.
*   **CPU-First AI:** Models must be optimized for edge computing (e.g., ONNX, Quantized GGUF, or TensorFlow Lite). We are prioritizing efficiency and low-power hardware performance over cloud-based GPU scaling.

## App Flow & AI Workflow

1.  **Ingestion:** Support multi-modal inputs (Audio/Video via Transcribers, Documents/Images via OCR/VLM).
2.  **Processing:** Local normalization and feature extraction.
3.  **Transformation:** Using local small language models (SLMs) to map unstructured content to a defined JSON/Relational schema.
4.  **Storage:** Persistence via local SQLite/Vector less DB for retrieval.

## Hackathon Rules & Participation

*   **Code Integrity:** All AI inference must run locally. Use of external APIs (OpenAI, Anthropic) is strictly prohibited.
*   **Data Handling:** The system must demonstrate graceful failure and caching when input processing latency occurs.
*   **Dependency Limits:** Optimize for low-latency libraries (e.g., llama.cpp, transformers.js, Tesseract, or Whisper.cpp).

## Validation Criteria

Submissions will be evaluated based on:

1.  **Model Performance:** Accuracy of structured extraction versus original data fidelity.
2.  **Resource Efficiency:** CPU usage metrics and memory footprint during inference.
3.  **Offline Resiliency:** Stability of the application when the system is completely air-gapped.
4.  **Data Schema Alignment:** How well the unstructured input maps to the target structured output.

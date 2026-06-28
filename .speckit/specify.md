# Chronicle.cpp CLI App - Feature Specification

> *Amended by: [Product Manager], [UX Expert]*
> *V2 Refined by: [Machine Learning Engineer], [Compliance Officer]*

## 1. Overview & Value Proposition
A robust CLI application that ingests unstructured audio files, performs offline transcription, and uses a local SLM to extract structured data into an encrypted SQLite database. 

## 2. Detailed Input Specifications
- **Supported Formats**: `.wav`, `.mp3`, `.m4a`, `.ogg`.
- **Audio Pre-Processing Limits (ML Engineer)**: 
  - Audio MUST be downsampled to 16kHz mono internally before passing to Whisper to drastically reduce memory usage and hallucination rates.
  - VAD (Voice Activity Detection) must be applied to strip pure silence.
- **Validation Constraints**: Max file size: 500 MB. Max duration: 120 minutes.

## 3. Processing Pipeline & UX Flow
1. **Command Invocation**: User runs `chronicle ingest meeting.mp3`.
2. **Ingestion & UI**: `[STATUS] Validating and downsampling audio file...`
3. **Offline Transcription**: `faster-whisper` (CTranslate2).
4. **Information Extraction**:
   - Engine: `llama-cpp-python` (Phi-3-mini-4k-instruct.Q4_K_M.gguf).
   - **Generation Parameters (ML Engineer)**: `temperature=0.1` (highly deterministic), `max_new_tokens=1024`, `repetition_penalty=1.15`.
   - Mechanism: JSON Grammar constrained decoding.
5. **Storage, Feedback & Compliance**:
   - DB: SQLCipher (SQLite).
   - **Audit Trail (Compliance Officer)**: Every database entry must include a non-mutable timestamp of ingestion, original filename hash (SHA-256), and an auto-deletion flag (e.g., "Expires in 30 days").

## 4. Target Output Schema (Strict JSON)
```json
{
  "title": "String (Max 100 chars)",
  "summary": "String (3-4 sentences)",
  "action_items": [
    {
      "task": "String", 
      "assignee": "String (or 'Unassigned')", 
      "deadline": "String (Date or 'None')"
    }
  ],
  "key_decisions": ["String"]
}
```

## 5. CLI Command Signatures
- `chronicle ingest <filepath> [--model <model_path>] [--export-json]`
- `chronicle query [--topic <string>] [--assignee <string>]`
- `chronicle audit-log` (Compliance: Shows data access and deletion events)
- `chronicle status`

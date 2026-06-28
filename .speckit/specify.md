# Feature Specification

## Input / Output Constraints
- **Supported Inputs**: `.wav`, `.mp3`, `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.md`, `.txt`, `.png`, `.jpg`.
- **Output Mode**: Strictly formatted JSON written to an encrypted SQLite database.
- **Constraints**: 100% offline. Zero network calls after initial model bootstrap. Max 6GB Memory footprint.

## Unified Schema Target
All omni-modal inputs, regardless of source (Meetings, Spreadsheets, Whiteboard images, Slide decks) will be extracted into this deterministic schema:

```json
{
  "summary": "A concise 2-3 sentence overview of the provided data.",
  "action_items": [
    "List of implicit or explicit tasks identified."
  ],
  "key_entities": [
    "People, companies, metrics, or major technical terms mentioned."
  ]
}
```

## CLI Signature
```bash
chronicle ingest <filepath>
chronicle query --topic <string>
chronicle status
```

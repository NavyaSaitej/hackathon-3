# CLI Interface Design & UX Spec

> *Curated by: [UX Architect], [CLI Usability Researcher]*
> *V2 Refined by: [Cognitive Load Psychologist], [Color Theory Expert], [Data Visualization Specialist], [Gamification Lead]*

## 1. Core Design Philosophy
Inspired by tools like **Claude Code**, **Antigravity CLI**, and **Vercel CLI**, this application will prioritize:
1. **Minimalism & Cognitive Flow (Psychologist):** The human eye processes terminal output linearly. We must aggressively use whitespace (`\n\n`) and hierarchical indentations to guide the user's eye to the most critical data (Action Items) in under 2 seconds. Intermediate, noisy logs are strictly wiped from the buffer post-execution.
2. **Elegance:** Use of subtle, cohesive color palettes and unicode box-drawing characters for structure.
3. **Transparency:** The user must always know what the CPU is doing.
4. **Resilience:** Errors must be actionable, human-readable, and offer a direct "Next Step" command.

## 2. Technology Stack for UI
- **`Typer`**: For robust, easily discoverable commands.
- **`Rich`**: The gold-standard for Python CLI styling.
  - `Live`: To update progress in place.
  - `Panel`: To encapsulate outputs and errors.
  - `Table`: To display SQLite database queries cleanly.
- **`Textual` (Optional inclusion by Data Viz Specialist)**: If we ever need a full-screen Terminal User Interface (TUI) for browsing the SQLite DB without leaving the terminal.

## 3. Color Palette, Typography & Accessibility
> *Mandated by the Color Theory Expert*

Colors must not solely rely on Red/Green pairs to ensure full accessibility for Protanopia/Deuteranopia (color blindness).
- **Primary / Brand**: `cyan` (Hex `#00FFFF`) - High contrast against dark terminal backgrounds.
- **Processing States**: `magenta` or `purple` - Used for AI "thinking" states.
- **Accent / Info**: `bright_black` (Grey) - Used for metadata (timestamps, file paths).
- **Error**: `bold yellow` and `red` combinations - Emphasized with a bold `[!]` icon so shape, not just color, indicates failure.
- **Success**: `bold blue` and `green` combinations - Emphasized with a `[✓]` icon.

## 4. Interaction Flows & Data Visualization

### A. The "Ingest" Flow (Audio to JSON)
**Step 1: Initiation**
```text
[🌀] Initializing Chronicle.cpp engine... (Loading Whisper to RAM)
```

**Step 2: Processing (Live Progress Bar)**
We use a single, unified progress block with localized sub-status.
```text
╭──────────────────────────────────────────────╮
│ 🧠 Processing: meeting.mp3                   │
│                                              │
│ [████████████░░░░░░] 66% • 00:15 remaining   │
│                                              │
│ ❯ Phase: Transcribing (CPU Core 3 Active)    │
╰──────────────────────────────────────────────╯
```

**Step 3: Output Presentation (Gamification Lead)**
Upon completion, a subtle "reveal" animation prints the final panel, satisfying the user's wait time.
```text
╭─ ✨ Meeting Notes Extracted (0.8s SLM Latency) ─╮
│                                                 │
│ 📝 Title: Hackathon Planning Sync               │
│                                                 │
│ 🎯 Action Items:                                │
│  • Alice: Setup GitHub repo                     │
│  • Bob: Download Phi-3 model                    │
│                                                 │
│ 💡 Decision: We will use SQLCipher for DB.      │
│                                                 │
│ 💾 Saved to database successfully.              │
╰─────────────────────────────────────────────────╯
```

### B. The "Status" Flow (Data Viz Specialist)
Instead of just printing "RAM: 4GB", we use unicode sparklines to visualize real-time resource pressure.
When the user runs: `chronicle status`

```text
╭─ 📊 System Health ───────────────────────────╮
│                                              │
│ 💾 RAM Usage:  [4.2 / 16 GB]                 │
│    Trend:      ▂▃▄▅▇█▆▅▃▂                    │
│                                              │
│ 🌡️ CPU Load:   [35%]                         │
│    Trend:      ▃▃▃▃▅▅▃▃▃▃                    │
│                                              │
│ 📦 Models Cached:                            │
│  ✓ faster-whisper-tiny.en (140MB)            │
│  ✓ phi-3-mini-4k.Q4_K_M (2.2GB)              │
╰──────────────────────────────────────────────╯
```

## 5. Micro-Interactions
- **Smart Autocomplete**: Hitting `TAB` after `chronicle ingest` will automatically list `.wav` and `.mp3` files in the current directory.
- **Graceful Interrupts**: Hitting `Ctrl+C` does not print `KeyboardInterrupt`. It smoothly stops the progress bar and prints `[⏹] Process halted safely by user. Memory cleared.`

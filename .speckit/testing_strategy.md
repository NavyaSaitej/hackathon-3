# Testing Strategy

> *V2 Refined by: [Chaos Engineer]*

## 1. Unit Tests (Pytest)
- Mock `faster-whisper` and `llama-cpp-python` entirely to ensure tests run in milliseconds.
- Test Typer CLI argument parsing.
- Test DB schema validation (Pydantic).

## 2. Integration Tests
- Run with small dummy models (e.g., TinyLlama) to ensure the pipeline connects, but without the time penalty of 8B models.
- Verify DB writes occur correctly after an SLM pass.

## 3. "Air-Gap" E2E Test
- Run `ping 8.8.8.8` (or equivalent) to ensure failure, confirming offline state.
- Run the full ingest pipeline on a 30-second audio clip.
- Assert final DB state.

## 4. Resource Profiling & Chaos Testing (Chaos Engineer)
- **Memory Spiking**: Use `memory_profiler` during the E2E test. Fail the test if RAM spikes above 6GB.
- **Process Starvation**: Randomly limit CPU cycles using `cpulimit` (Linux) or simulate thread locking to ensure the pipeline gracefully queues processing rather than crashing.
- **I/O Interruptions**: Simulate a sudden disk-full error during SQLite commit to verify rollback mechanisms prevent database corruption.

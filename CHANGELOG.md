# Changelog

All notable changes to Chronicle.cpp will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Phase 3: Added missing multimedia parsers to `pyproject.toml` so `pip install -e .` handles all dependencies.
- Phase 3: Finalized GNU GPLv3 license tracking and GitLab CI/CD `.gitlab-ci.yml`.
- Phase 2: Built out `OllamaOrchestrator` for automated LLM provisioning via `winget`/`brew`/`curl`.
- Phase 2: Added `RuleBasedExtractor` fallback engine for offline air-gap resiliency.
- Phase 1: Complete Omni-Modal SpecKit.
- Phase 1: Strict `requirements.txt` and `bootstrap_offline_models.py`.
- Phase 1: Project scaffold and `AGENTS.md` handoff rules.

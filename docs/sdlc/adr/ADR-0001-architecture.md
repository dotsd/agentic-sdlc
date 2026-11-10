# ADR-0001: Foundational Architecture & Agentic SDLC Mode

- **Date**: 2026-11-10
- **Status**: Accepted
- **Project**: agentic-sdlc

## Context
Modern software and AI systems degrade rapidly under ad-hoc "vibe coding" due to context window drift, implicit assumptions, untested edge cases, and LLM self-grading bias.

## Decision
We adopt **Agentic SDLC (`full` mode)** with version-controlled living contracts in `docs/sdlc/`:
- **Primary Stack**: Python 3.11+ standard library, Hatchling, Markdown/JSON contracts
- **Model Strategy**: Model-agnostic (Gemini, Claude, OpenAI, Kimi, DeepSeek, Qwen, Mistral, Local)
- **Quality Gates**: Context-isolated architecture criticism (`spec-critic`), security auditing (`security-redteam`), and test/trajectory verification (`eval-verifier`).

## Consequences
- **Positive**: Deterministic handoffs across coding sessions, vendor/model portability, traceable requirements-to-tests coverage, and early detection of architectural or security flaws.
- **Trade-offs**: Requires keeping `docs/sdlc/` specifications and `TASK_PROGRESS.json` synchronized alongside code changes.

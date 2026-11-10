# ADR-0001: Foundational Architecture & Agentic SDLC Mode

- **Date**: {{DATE}}
- **Status**: Accepted
- **Project**: {{PROJECT_NAME}}

## Context
Modern software and AI systems degrade rapidly under ad-hoc "vibe coding" due to context window drift, implicit assumptions, untested edge cases, and LLM self-grading bias.

## Decision
We adopt **Agentic SDLC (`{{MODE}}` mode)** with version-controlled living contracts in `docs/sdlc/`:
- **Primary Stack**: {{STACK}}
- **Model Strategy**: {{LLM_PROVIDER}}
- **Quality Gates**: Context-isolated architecture criticism (`spec-critic`), security auditing (`security-redteam`), and test/trajectory verification (`eval-verifier`).

## Consequences
- **Positive**: Deterministic handoffs across coding sessions, vendor/model portability, traceable requirements-to-tests coverage, and early detection of architectural or security flaws.
- **Trade-offs**: Requires keeping `docs/sdlc/` specifications and `TASK_PROGRESS.json` synchronized alongside code changes.

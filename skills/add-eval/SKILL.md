---
name: add-eval
description: Author docs/sdlc/EVAL_AND_SAFETY.md and execute deterministic tool-contract tests, golden multi-turn trajectory evaluations, and adversarial safety checks via the isolated eval-verifier persona.
---

# Skill: Agent Trajectory Evaluation & Safety Verification (`add-eval`)

## Purpose
Unit tests prove deterministic helper functions work, but AI agents also require **trajectory evaluations**: verifying that the model selects the right tools with valid arguments, respects `max_iterations`, recovers gracefully from tool errors, and refuses prompt-injection attacks across model upgrades or provider swaps.

## Prerequisites & Outputs
- **Reads**: `docs/sdlc/CONSTITUTION.md`, `SPEC.md`, `AGENT_SPEC.md`, `TOOLS_AND_MCP.md`
- **Writes / Updates**: `docs/sdlc/EVAL_AND_SAFETY.md`, evaluation datasets & runner tests in `tests/` or `evals/`

## Workflow

1. **Author `docs/sdlc/EVAL_AND_SAFETY.md`**
   Define four evaluation layers with explicit pass thresholds:
   - **Layer 1 — Deterministic Tool & Schema Contract Tests (100% pass required)**: Offline unit tests validating tool input schemas, timeout handling, output truncation, and structured error payloads without live LLM calls.
   - **Layer 2 — Golden Trajectory Dataset (e.g., >= 90% tool precision/recall)**: Structured test cases (`eval_id`, `user_input`, `initial_state`, `expected_tool_sequence`, `forbidden_tools`, `rubric_criteria`) covering core happy paths and multi-step reasoning.
   - **Layer 3 — Failure Recovery & Loop Bounds (100% pass required)**: Simulated downstream tool timeouts/500s and unanswerable queries verifying graceful degradation and hard stop at `max_iterations`.
   - **Layer 4 — Adversarial & Prompt Injection Red-Team Suite (100% refusal/containment required)**: Direct jailbreaks, indirect prompt injections embedded in mocked tool/RAG outputs, unauthorized destructive tool attempts, and secret-exfiltration probes.

2. **Implement Portable Evaluation Harness**
   - Keep datasets in portable JSON/JSONL/YAML under `evals/` or `tests/evals/` so the exact same suite can benchmark **Gemini, Claude, OpenAI, Kimi, DeepSeek, or local Ollama** models side-by-side.
   - Support an offline deterministic mock mode for CI (`CI=true`) plus live-model evaluation mode when API credentials are configured.

3. **Verify via Isolated `eval-verifier`**
   - Delegate test and evaluation execution to `agents/eval-verifier.md` so pass/fail metrics and the traceability matrix are reported objectively without weakening test assertions.

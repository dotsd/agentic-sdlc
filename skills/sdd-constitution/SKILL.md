---
name: sdd-constitution
description: Establish or update docs/sdlc/CONSTITUTION.md and docs/sdlc/adr/ADR-0001-architecture.md to define non-negotiable engineering principles, language/runtime stack, model providers, cloud/deployment targets, testing gates, and security boundaries.
---

# Skill: Establish Project Constitution (`sdd-constitution`)

## Purpose
Define the immutable engineering guardrails for a repository **before** writing product specs, agent architectures, or production code. Works across any language, cloud hyperscaler (AWS, Azure, GCP, Kubernetes, on-prem), LLM provider (Gemini, Claude, OpenAI, Kimi, DeepSeek, Qwen, Mistral, Llama/Ollama), and agent framework.

## Outputs
- `docs/sdlc/CONSTITUTION.md`
- `docs/sdlc/adr/ADR-0001-architecture.md`

## Workflow

1. **Inspect Existing Repository Context**
   - Check package manifests (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `pom.xml`, `Dockerfile`, `.github/workflows/`) and existing docs to detect brownfield conventions.
   - If greenfield and critical stack choices are unspecified, ask up to 3 concise questions (runtime stack, deployment target, and LLM/agent runtime if building AI agents).

2. **Author `docs/sdlc/CONSTITUTION.md`**
   Include concrete, verifiable rules—never vague platitudes:
   - **Runtime & Stack**: Language version, package manager (`uv`, `pnpm`, `cargo`, `go`), web/API framework, database, and (if applicable) AI agent framework + model tier policy (fast routing tier vs. deep reasoning tier).
   - **Code Quality & Typing**: Strict static typing (`mypy`/`pyright`, `tsc --strict`), linting/formatting commands, modular file boundaries.
   - **Testing & Evaluation Gates**: Minimum automated test expectations (unit, contract, integration) and, for AI agents, golden trajectory pass-rate and tool-precision thresholds.
   - **Security & Privacy Guardrails**: Zero hardcoded secrets, `.env.example` documentation, parameterized queries, strict path/URL allowlists, `127.0.0.1` local dev binding, and human-in-the-loop confirmation for destructive operations.
   - **Operational & Cost Guardrails**: Structured logging/OpenTelemetry tracing, network timeouts on all external calls, and `max_iterations` bounds on any agentic loop.

3. **Record `docs/sdlc/adr/ADR-0001-architecture.md`**
   - Document the **Context**, **Decision** (SDD-only, ADD-only, or Unified SDD + ADD topology, plus core stack choices), **Alternatives Considered**, and **Consequences**.

4. **Verification Gate**
   - Confirm every build, lint, and test command listed in `CONSTITUTION.md` matches the repository's real toolchain and contains zero unresolved `[TODO]` placeholders.

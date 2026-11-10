# Project Constitution — {{PROJECT_NAME}}

> **Status**: Living Engineering Guardrails | **Mode**: `{{MODE}}` | **Initialized**: `{{DATE}}`

## 1. Runtime & Technology Stack
- **Primary Stack**: {{STACK}}
- **LLM / Model Provider Policy**: {{LLM_PROVIDER}} (externalized via environment variables; never hardcode model IDs in business logic)
- **Cloud / Deployment Target**: Cloud-agnostic container / serverless / local runtime (AWS, Azure, GCP, Kubernetes, or on-prem)

## 2. Engineering & Code Quality Principles
1. **Spec-Before-Code**: Update `docs/sdlc/` specifications before making architectural, schema, or agent-routing changes.
2. **Strict Typing & Validation**: Enforce static type annotations and runtime boundary validation on all external inputs, API payloads, and LLM tool arguments.
3. **Small, Test-Driven Increments**: Implement one task from `docs/sdlc/TASK_PROGRESS.json` at a time with automated tests passing before marking `"completed"`.

## 3. Security & Privacy Guardrails
- **Zero Hardcoded Secrets**: Load all API keys, credentials, endpoints, and DSNs from environment variables documented in `.env.example`.
- **Safe Defaults**: Bind local development servers to `127.0.0.1` by default; enforce parameterized queries, strict path traversal checks, and outbound network timeouts.
- **Human-in-the-Loop for High-Impact Actions**: Any destructive, financial, IAM, or production-mutating operation requires deterministic policy validation and explicit user confirmation.

## 4. AI Agent Guardrails (When `ADD` or `full` Mode Applies)
- **Bounded Loops**: Every agent loop or reflection cycle must enforce an explicit `max_iterations` cap and wall-clock timeout.
- **Typed Tool Contracts**: Every LLM tool and MCP integration must provide typed schemas, clear routing docstrings, timeouts, and structured error payloads.
- **Fresh-Context Verification**: Run `spec-critic`, `security-redteam`, and `eval-verifier` in isolated contexts rather than self-grading in the authoring session.

## 5. Verification Commands
- **Format / Lint**: `echo "Configure linter in CONSTITUTION.md"`
- **Unit & Contract Tests**: `pytest`
- **Agent Evaluations (if applicable)**: `pytest -m eval`

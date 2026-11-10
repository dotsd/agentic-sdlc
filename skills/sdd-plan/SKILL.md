---
name: sdd-plan
description: Generate docs/sdlc/PLAN.md translating docs/sdlc/SPEC.md and CONSTITUTION.md into concrete system architecture, Mermaid component/sequence diagrams, data models, API/interface contracts, and a test verification plan.
---

# Skill: Technical Architecture Plan (`sdd-plan`)

## Purpose
Bridge `docs/sdlc/SPEC.md` (**what** to build) and `docs/sdlc/TASKS.md` (**step-by-step execution**) by designing concrete modules, data schemas, API contracts, error semantics, and test strategies in `docs/sdlc/PLAN.md`.

> **Note**: If your system includes LLM reasoning loops, autonomous subagents, or MCP servers, pair `sdd-plan` (for deterministic services, databases, APIs, and UIs) with `add-architect` (for `AGENT_SPEC.md` and `TOOLS_AND_MCP.md`).

## Prerequisites & Outputs
- **Reads**: `docs/sdlc/CONSTITUTION.md`, `docs/sdlc/SPEC.md`
- **Writes**: `docs/sdlc/PLAN.md` (and additional ADRs in `docs/sdlc/adr/` for major architectural trade-offs)

## Workflow

1. **Verify Constitution Alignment**
   - Check every proposed library, database, cloud service, and pattern against `docs/sdlc/CONSTITUTION.md`. Document any justified exception in an ADR.

2. **Design System Architecture (`docs/sdlc/PLAN.md`)**
   - **Architecture Overview & Mermaid Diagrams**: Component topology diagram and key request/data-flow sequence diagram (quote Mermaid node labels containing parentheses or brackets).
   - **Repository & Module Layout**: Exact directory tree and single-responsibility boundaries for each module.
   - **Data Models & Persistence**: Entities, field types, indexes, constraints, state transitions, and migration strategy.
   - **API / CLI / Event Contracts**: Endpoints or command signatures, request/response schemas, authentication, pagination, idempotency, timeouts, and structured error codes.
   - **Security & Observability Design**: Input validation boundaries, secret injection via environment/secret manager, structured logs, metrics, and distributed trace propagation.
   - **Test & Verification Strategy**: Exact unit, contract, integration, and end-to-end test layers mapped back to `US-*` / `FR-*` IDs in `SPEC.md`.

3. **Verification Gate**
   - Confirm every `P0`/`P1` requirement in `SPEC.md` maps to a module, interface contract, and test layer in `PLAN.md`.

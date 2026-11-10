---
name: sdd-clarify
description: Audit docs/sdlc/SPEC.md (and AGENT_SPEC.md if present) for underspecified requirements, edge cases, security boundaries, and failure modes, ask up to 5 high-impact clarification questions, and encode answers back into the spec.
---

# Skill: Socratic Requirement Clarification (`sdd-clarify`)

## Purpose
Eliminate costly architectural rework by surfacing hidden assumptions in `docs/sdlc/SPEC.md` **before** technical planning or code generation begins.

## Prerequisites & Outputs
- **Reads**: `docs/sdlc/SPEC.md`, `docs/sdlc/CONSTITUTION.md`, and `docs/sdlc/AGENT_SPEC.md` (if present)
- **Updates**: `docs/sdlc/SPEC.md` (and `AGENT_SPEC.md` if applicable)

## Workflow

1. **Scan Across 6 Ambiguity Dimensions**
   - **Domain & Data**: Missing entity lifecycles, uniqueness rules, retention/deletion semantics, concurrency conflicts.
   - **Auth & Multi-Tenancy**: Who can read/mutate what? How is tenant isolation enforced?
   - **External Dependencies & Failure Modes**: Retries, idempotency keys, fallback behavior when an API, database, or LLM provider times out.
   - **Agent Autonomy Boundaries (if AI agents are in scope)**: Which actions may execute autonomously vs. require human confirmation? What is the fallback when confidence is low?
   - **Scale & Cost Budgets**: Expected data volume, latency ceiling, token/cost budget per request.
   - **Explicit `[NEEDS CLARIFICATION]` Markers**: Resolve any open tags from `sdd-specify`.

2. **Ask At Most 5 High-Impact Questions**
   - Prioritize questions that materially alter data models, API contracts, security posture, or multi-agent topology.
   - Do **not** ask trivial questions with obvious industry-standard defaults—state your recommended default alongside each question so the user can approve quickly.

3. **Encode Decisions Directly Into the Living Spec**
   - Append a dated `## Clarifications & Resolved Decisions` log in `docs/sdlc/SPEC.md`.
   - Update the affected functional requirements, Gherkin scenarios, and non-goals directly so zero `[NEEDS CLARIFICATION]` markers remain.

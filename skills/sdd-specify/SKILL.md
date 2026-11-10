---
name: sdd-specify
description: Create or update docs/sdlc/SPEC.md from natural-language requirements with prioritized user stories, Gherkin Given/When/Then acceptance criteria, edge cases, explicit non-goals, and measurable success metrics.
---

# Skill: Author Functional Specification (`sdd-specify`)

## Purpose
Translate an ambiguous feature idea or product brief into a testable, implementation-agnostic specification in `docs/sdlc/SPEC.md`. Focus strictly on **WHAT** the system or agent must accomplish and **WHY**, leaving implementation internals to `sdd-plan` and `add-architect`.

## Prerequisites & Outputs
- **Reads**: `docs/sdlc/CONSTITUTION.md` (if present)
- **Writes**: `docs/sdlc/SPEC.md`

## Workflow

1. **Extract Core Intent & Actors**
   - Identify primary users, API consumers, upstream/downstream systems, or human-in-the-loop operators.
   - Define the core problem statement and business value in 3–5 sentences.

2. **Write Prioritized User Stories & Critical User Journeys (CUJs)**
   - Assign clear IDs (`US-001`, `US-002`, ...) and priorities (`P0` Must-Have MVP, `P1` Important, `P2` Stretch).
   - Every `P0` and `P1` story must be independently testable.

3. **Define Gherkin Acceptance Criteria**
   - For each story, write explicit **Given / When / Then** scenarios covering:
     - Happy path behavior
     - Validation / malformed input rejection
     - Downstream failure, timeout, or rate-limit handling
     - Authorization / tenant boundary enforcement

4. **Specify Non-Functional Requirements & Non-Goals**
   - **SLOs & Constraints**: Latency budgets (p50/p95), throughput, payload limits, idempotency, accessibility, compliance/data residency.
   - **Explicit Non-Goals**: List out-of-scope features to prevent scope creep and hallucinated functionality during coding.
   - **Open Ambiguities**: Mark unresolved product decisions explicitly with `[NEEDS CLARIFICATION: ...]` so `sdd-clarify` can resolve them systematically.

5. **Verification Gate**
   - Ensure every functional requirement has a unique ID (`FR-001`, ...) and at least one deterministic acceptance scenario.

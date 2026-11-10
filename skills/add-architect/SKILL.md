---
name: add-architect
description: Design vendor-neutral single-agent or multi-agent architectures, subagent routing boundaries, session/memory state contracts, termination bounds, and LLM tool/MCP schemas in docs/sdlc/AGENT_SPEC.md and docs/sdlc/TOOLS_AND_MCP.md.
---

# Skill: AI Agent & Tool Architecture (`add-architect`)

## Purpose
Bring engineering determinism to non-deterministic AI agents across **any** LLM provider (Gemini, Claude, OpenAI, Kimi, DeepSeek, Qwen, Mistral, Llama/Ollama) and **any** agent framework (LangGraph, CrewAI, OpenAI Agents SDK, Anthropic Agent SDK, Google ADK, AutoGen, PydanticAI, custom ReAct loops, or MCP servers).

## Prerequisites & Outputs
- **Reads**: `docs/sdlc/CONSTITUTION.md`, `docs/sdlc/SPEC.md` (if present)
- **Writes**: `docs/sdlc/AGENT_SPEC.md`, `docs/sdlc/TOOLS_AND_MCP.md`

## Workflow

1. **Select Minimal Viable Agent Topology (`docs/sdlc/AGENT_SPEC.md`)**
   - Prefer the simplest topology that solves the problem reliably:
     1. **Deterministic Workflow + Structured LLM Step** (when control flow is known up front)
     2. **Single Tool-Using Agent** (up to ~10 cohesive tools)
     3. **Router / Supervisor + Specialized Subagents** (when tool count > 10 or distinct personas/context windows are needed)
     4. **Generator + Isolated Critic Loop** (bounded by `max_iterations`, typically 2–3)
   - Document in `AGENT_SPEC.md`:
     - **Mermaid Topology Diagram** (quote labels with parentheses/brackets).
     - **Agent & Subagent Registry**: Name, model tier (`fast` vs. `reasoning`, configured via env vars), role persona, exact routing trigger, and explicit **out-of-scope / non-trigger** rules so subagents never overlap.
     - **Session & Memory State Contract**: Exact state keys, types, single-writer ownership, and artifact URI/reference passing (never pass bloated raw chat transcripts across subagents).
     - **Termination & Cost Bounds**: `max_iterations` / `max_tool_calls`, wall-clock timeout, fallback behavior on exhaustion, and human-in-the-loop confirmation gates for mutating/high-risk actions.

2. **Specify LLM Tools & MCP Integrations (`docs/sdlc/TOOLS_AND_MCP.md`)**
   - Remember: **To an LLM, a tool's schema and docstring ARE its user interface.**
   - For every custom tool and external MCP server, specify:
     - **Tool ID & Signature**: Strictly typed parameters with JSON Schema / Pydantic / Zod constraints (enums, min/max, regex, defaults).
     - **LLM Routing Docstring**: *When to call*, *when NOT to call*, and expected output shape.
     - **Operational Bounds**: Timeout (ms/s), retry policy, idempotency, rate-limit behavior, and payload truncation limit so large outputs do not blow up context windows.
     - **Structured Error Contract**: Recoverable domain errors returned as structured JSON (`{"ok": false, "error_code": "...", "hint": "..."}`) so the model can self-correct instead of crashing on raw stack traces.
     - **Security & Trust Level**: `read_only`, `scoped_write`, or `destructive_requires_approval`.

3. **Verification Gate**
   - Confirm zero overlapping subagent triggers, zero unbounded loops, and 100% typed tool contracts before proceeding to `add-critic` and `sdd-tasks`.

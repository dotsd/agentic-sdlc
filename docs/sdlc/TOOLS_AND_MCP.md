# LLM Tools & MCP Server Contracts — agentic-sdlc

> **Track**: Agent-Driven Development (ADD) | **Last Updated**: `2026-11-10`
> **Golden Rule**: To an LLM, a tool's parameter schema, docstring, and structured error format *are* its user interface.

## 1. Custom Tool Registry

### `TOOL-001` — `example_lookup`
- **Trust Classification**: `read_only` (`read_only` | `scoped_write` | `destructive_requires_approval`)
- **Typed Parameters**:
  - `query: str` (non-empty, max 256 chars)
  - `limit: int = 10` (`1 <= limit <= 50`)
- **LLM Routing Docstring**:
  - *Call when*: Retrieving verified records matching a specific identifier or keyword.
  - *Do NOT call when*: Performing open-ended summarization that requires no external lookup.
- **Operational Bounds**: Timeout `5.0s`, max response payload `16 KB` (truncate with pagination cursor), idempotent `true`.
- **Structured Error Contract**:
  ```json
  {
    "ok": false,
    "error_code": "UPSTREAM_TIMEOUT",
    "message": "Lookup timed out after 5.0s",
    "retryable": true,
    "hint": "Narrow query scope or retry once."
  }
  ```

## 2. External MCP Server Integrations
| MCP Server Name | Transport (`stdio`/`streamable-http`) | Allowed Tools (Least Privilege) | Auth / Env Vars | Timeout |
| :--- | :--- | :--- | :--- | :--- |
| `none_configured` | N/A | Explicit allowlist only | `MCP_API_TOKEN` | `10s` |

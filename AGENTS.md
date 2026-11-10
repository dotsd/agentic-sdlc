# Agentic SDLC Instructions — agentic-sdlc

This repository follows **Agentic SDLC** in **`full`** mode (Unified SDD + ADD (Full-Stack Software + AI Agents)).
All architectural specifications, agent contracts, and task execution states live in `docs/sdlc/`.

- **Primary Stack**: Python 3.11+ standard library, Hatchling, Markdown/JSON contracts
- **Model / LLM Strategy**: Model-agnostic (Gemini, Claude, OpenAI, Kimi, DeepSeek, Qwen, Mistral, Local)

## Non-Negotiable Engineering Rules

1. **Specs Before Code**: Read `docs/sdlc/CONSTITUTION.md` before making changes. Keep `docs/sdlc/` specifications synchronized with code—never introduce undocumented APIs, state keys, or LLM tools.
2. **Incremental TDD Execution**: Work one task at a time from `docs/sdlc/TASK_PROGRESS.json` and `docs/sdlc/TASKS.md`. Write/update automated tests first, verify they pass, then mark the task `"completed"`.
3. **Zero Hardcoded Secrets & Safe Defaults**: Load credentials, model IDs, and endpoints from environment variables. Bind local development servers to `127.0.0.1` by default and enforce explicit timeouts and path/input validation.
4. **Bounded AI Loops (ADD)**: Every AI agent or tool loop must enforce `max_iterations`, typed tool schemas, timeouts, and structured error payloads as specified in `docs/sdlc/AGENT_SPEC.md` and `docs/sdlc/TOOLS_AND_MCP.md`.
5. **Context-Isolated Review**: Do not self-certify specifications or security in the authoring context. Use isolated fresh-context reviewers (`spec-critic`, `security-redteam`, `eval-verifier`).

## Available Skills

| Skill | Purpose |
| :--- | :--- |
| `add-architect` | Design vendor-neutral single-agent or multi-agent architectures, subagent routing boundaries, session/memory state contracts, termination bounds, and LLM tool/MCP schemas in docs/sdlc/AGENT_SPEC.md and docs/sdlc/TOOLS_AND_MCP.md. |
| `add-critic` | Run a context-isolated Quality & Security Gate by delegating docs/sdlc/ specs, prompts, tools, and source code to fresh-context spec-critic and security-redteam subagents (or clean review sessions), then remediate all P0 and P1 defects. |
| `add-deploy` | Validate production readiness, container/serverless packaging, secret hygiene, OpenTelemetry observability, and rollback safety for software services, AI agents, and MCP servers across AWS, Azure, GCP, Kubernetes, or on-prem runtimes. |
| `add-eval` | Author docs/sdlc/EVAL_AND_SAFETY.md and execute deterministic tool-contract tests, golden multi-turn trajectory evaluations, and adversarial safety checks via the isolated eval-verifier persona. |
| `sdd-clarify` | Audit docs/sdlc/SPEC.md (and AGENT_SPEC.md if present) for underspecified requirements, edge cases, security boundaries, and failure modes, ask up to 5 high-impact clarification questions, and encode answers back into the spec. |
| `sdd-constitution` | Establish or update docs/sdlc/CONSTITUTION.md and docs/sdlc/adr/ADR-0001-architecture.md to define non-negotiable engineering principles, language/runtime stack, model providers, cloud/deployment targets, testing gates, and security boundaries. |
| `sdd-converge` | Audit the implemented codebase and test suite against docs/sdlc/SPEC.md, PLAN.md, AGENT_SPEC.md, and TOOLS_AND_MCP.md, identify unbuilt or partially verified requirements, and append delta tasks to TASKS.md and TASK_PROGRESS.json until 100% converged. |
| `sdd-implement` | Execute pending engineering tasks from docs/sdlc/TASK_PROGRESS.json and docs/sdlc/TASKS.md incrementally using test-driven development (TDD), updating living state after every verified task. |
| `sdd-plan` | Generate docs/sdlc/PLAN.md translating docs/sdlc/SPEC.md and CONSTITUTION.md into concrete system architecture, Mermaid component/sequence diagrams, data models, API/interface contracts, and a test verification plan. |
| `sdd-specify` | Create or update docs/sdlc/SPEC.md from natural-language requirements with prioritized user stories, Gherkin Given/When/Then acceptance criteria, edge cases, explicit non-goals, and measurable success metrics. |
| `sdd-tasks` | Decompose docs/sdlc/PLAN.md and/or docs/sdlc/AGENT_SPEC.md + TOOLS_AND_MCP.md into small, dependency-ordered TDD engineering tasks in docs/sdlc/TASKS.md and machine-readable state in docs/sdlc/TASK_PROGRESS.json. |
| `sdlc-sync` | Onboard existing brownfield software or AI agent repositories by reverse-engineering docs/sdlc/ living specifications from code, or synchronize docs/sdlc/ artifacts when code and specs drift apart. |

## Context-Isolated Personas

| Persona | Role |
| :--- | :--- |
| `eval-verifier` | Isolated fresh-context Test & Agent Trajectory Verifier. Executes unit/integration suites, tool-contract tests, and golden/adversarial AI agent trajectory evaluations against SPEC.md and EVAL_AND_SAFETY.md without mutating production code. |
| `sdlc-orchestrator` | Lead Agentic SDLC coordinator combining Spec-Driven Development (SDD) for deterministic software engineering and Agent-Driven Development (ADD) for deterministic AI agent engineering. Enforces living state contracts in docs/sdlc/ and delegates audits to fresh-context reviewer subagents. |
| `security-redteam` | Isolated fresh-context Application & AI Agent Security Red-Team Auditor. Audits specs, system prompts, tools, MCP configs, and source code against OWASP Web/API Top 10 and OWASP Top 10 for LLM & Agentic Applications. |
| `spec-critic` | Isolated fresh-context Software & AI Agent Architecture Critic. Audits docs/sdlc/ specifications and source code in read-only mode for requirement gaps, API/schema mismatches, multi-agent routing overlaps, state collisions, unbounded loops, and tool schema defects. |

## CLI Quick Check

- Check progress: `asdlc status`
- Validate `docs/sdlc/` contracts & task graph: `asdlc validate`

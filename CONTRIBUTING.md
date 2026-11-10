# Contributing to `agentic-sdlc`

Thank you for helping make **Spec-Driven Development (SDD)** and **Agent-Driven Development (ADD)** open, practical, and accessible across every LLM, agent framework, and cloud!

## Core Design Principles

1. **Vendor, Cloud & Model Neutrality**:
   - Skills, templates, and subagent personas must remain hyperscaler-agnostic (AWS, Azure, GCP, on-prem, or local) and LLM-agnostic (Gemini, Claude, OpenAI, Kimi, DeepSeek, Qwen, Mistral, Llama, Ollama, etc.).
2. **Zero Runtime Bloat**:
   - The `asdlc` CLI uses only the Python 3.11+ standard library so anyone can install and run it in milliseconds without dependency conflicts.
3. **Strict Context Separation**:
   - Authoring skills write to version-controlled `docs/sdlc/` markdown/JSON state; critic, security, and verification personas operate in fresh, isolated contexts.

## Running Tests Locally

```bash
python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m agentic_sdlc.cli validate .
```

## Submitting Pull Requests

1. Fork the repository and create a feature branch.
2. Add or update tests in `tests/` for any CLI, template, or adapter changes.
3. Ensure `python3 -m unittest discover -s tests -v` passes with zero warnings.
4. Open a Pull Request with a clear summary of the problem solved.

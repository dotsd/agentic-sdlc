---
name: add-deploy
description: Validate production readiness, container/serverless packaging, secret hygiene, OpenTelemetry observability, and rollback safety for software services, AI agents, and MCP servers across AWS, Azure, GCP, Kubernetes, or on-prem runtimes.
---

# Skill: Cloud-Agnostic Production Readiness & Deployment (`add-deploy`)

## Purpose
Ensure software services and AI agent workloads meet production reliability, security, cost-control, and observability standards before shipping to **any** target environment:
- **AWS**: Bedrock Agents / ECS Fargate / EKS / Lambda
- **Azure**: Azure AI Foundry / Container Apps / AKS / Functions
- **Google Cloud**: Vertex AI Agent Engine / Cloud Run / GKE
- **Cloud-Neutral & On-Prem**: Kubernetes (Helm/Kustomize), Docker Compose, bare-metal, or local stdio/SSE/Streamable-HTTP MCP servers

## Workflow

1. **Pre-Flight Gate Verification**
   - Confirm `TASK_PROGRESS.json` has zero `pending` or `in_progress` P0/P1 tasks.
   - Confirm deterministic test suite and `EVAL_AND_SAFETY.md` checks pass.
   - Confirm `add-critic` security and architecture gates have zero open P0/P1 findings.

2. **Production Packaging & Runtime Checklist**
   - **Configuration & Secrets**: Every model name, provider base URL, API key, database DSN, and cloud identifier is loaded via environment variables or secret manager; `.env.example` documents every required/optional variable without real secrets; `.gitignore` and `.dockerignore` exclude `.env*`, credentials, and local artifacts.
   - **Container & Process Hardening**: Pin base images and dependency lockfiles; run containers as non-root user; expose explicit `/healthz` and `/readyz` endpoints; bind local dev servers to `127.0.0.1` and container entrypoints cleanly via configurable `HOST`/`PORT`.
   - **Observability & Cost Telemetry**: Emit structured JSON logs (redacting PII/secrets) and OpenTelemetry spans/metrics capturing request latency, tool latency/error rates, model token usage, and loop iteration counts.
   - **Resilience & Rollback**: Enforce outbound HTTP/LLM/MCP timeouts, rate limiting, concurrency caps, and document a single-command rollback procedure.

3. **Explicit User Confirmation Before Live Mutation**
   - Generate/validate deployment manifests (`Dockerfile`, IaC, CI/CD workflows) safely locally first.
   - Always request explicit user confirmation before executing live production deployments, database migrations, or cloud resource mutations.

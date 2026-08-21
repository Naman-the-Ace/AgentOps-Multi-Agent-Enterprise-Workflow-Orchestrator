<div align="center">

# 🚀 AgentOps

### Multi-Agent Enterprise Workflow Orchestrator

**Built a production-oriented multi-agent orchestration platform using LangGraph to coordinate specialized AI agents across research, analysis, and execution workflows, with MCP-based tool integration, persistent workflow state, human-in-the-loop approvals, RBAC, and fault-tolerant execution.**

[![CI](https://github.com/Naman-the-Ace/AgentOps-Multi-Agent-Enterprise-Workflow-Orchestrator/actions/workflows/ci.yml/badge.svg)](https://github.com/Naman-the-Ace/AgentOps-Multi-Agent-Enterprise-Workflow-Orchestrator/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.60+-1c7d4d.svg)](https://langchain-ai.github.io/langgraph/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple.svg)](https://modelcontextprotocol.io)
[![React 19](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev)
[![Docker](https://img.shields.io/badge/docker-compose-2496ed.svg)](https://docker.com)
[![Tests](https://img.shields.io/badge/tests-344%20passing-brightgreen.svg)](tests/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

[Quickstart](#-quickstart) · [Architecture](#-architecture) · [Features](#-features) · [API](#-api-reference) · [Deployment](#-deployment) · [Docs](docs/) · [Roadmap](#-roadmap) · [Contributing](#-contributing)

![AgentOps Console](docs/images/dashboard.png)

</div>

---

## 📖 Table of Contents

- [What is AgentOps?](#-what-is-agentops)
- [Why AgentOps?](#-why-agentops)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Quickstart](#-quickstart)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Workflows & Connectors](#-workflows--connectors)
- [API Reference](#-api-reference)
- [Security](#-security)
- [Performance & Scalability](#-performance--scalability)
- [Deployment](#-deployment)
- [Developer Guide](#-developer-guide)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧭 What is AgentOps?

**AgentOps** is an open-source platform for building, running, and operating **multi-agent AI workflows** in the enterprise. Instead of a single monolithic prompt, AgentOps orchestrates a **supervisor agent** that routes work to a team of specialists — a researcher, an analyzer, and an executor — each grounded in real tools and real data, and gated by **human approval** before any high-impact side effect.

It ships three named workflow domains out of the box:

| Workflow | Pipeline | Status | Connector |
|---|---|---|---|
| **`sales_ops`** | qualify → research → analyze → propose → **approve** → execute | ✅ **Production** | HubSpot CRM (upsert-by-email, idempotent deals, 429 backoff) |
| **`support_ops`** | triage → investigate → respond → escalate → resolve | ⚠️ Template scaffold | Pairs with Jira / ServiceNow |
| **`finance_recon`** | ingest → match → flag variance → approve → post | ⚠️ Template scaffold | Pairs with QuickBooks / SAP |

> `support_ops` and `finance_recon` are honest scaffolds — they raise on `.run()` unless `dry_run=True` or `AGENTOPS_ALLOW_TEMPLATE_WORKFLOWS=1` is set. `sales_ops` is the fully-wired reference path.

### The problem it solves

Most "agent demos" collapse the moment they meet production reality: there's no audit trail, no cost ceiling, no way to pause for a human, secrets leak into prompts, a single flaky API takes down the whole run, and swapping a mock tool for a real one means rewriting the agent. **AgentOps** is the **opinionated reference implementation** of everything that sits *around* the LLM call to make agentic automation safe to deploy:

- **Durable state** — every node is checkpointed to PostgreSQL, so any worker can resume any run after a crash.
- **Human-in-the-loop** — workflows pause via LangGraph `interrupt_before` and resume on an approve/reject webhook or Slack button.
- **Pluggable tools** — agents talk to the world through the **Model Context Protocol (MCP)**, so you swap a mock CRM for HubSpot without touching agent code.
- **Defense in depth** — PII redaction, prompt-injection guards, SSRF protection, untrusted-tool-output quarantine, and an outbound-email allowlist.
- **Cost & resilience controls** — per-run budget guard, circuit breakers, retry-with-backoff, and token-level cost tracking.
- **Full observability** — LangSmith / Phoenix / Langfuse tracing, Prometheus metrics, immutable audit log, and LLM-as-judge evaluation.

### Who it's for

| Audience | What AgentOps gives you |
|---|---|
| **Platform / ML engineers** | A batteries-included blueprint for shipping agents with checkpointing, RBAC, observability, and connectors already wired. |
| **Enterprises** | Human approvals, audit trails, cost ceilings, multi-tenancy, and on-prem / air-gapped deployment paths. |
| **OSS contributors** | A clean, typed, well-tested (344 tests) codebase with clear extension points — connectors, MCP tools, and workflow templates. |
| **Recruiters & evaluators** | A demonstration of production agentic-AI engineering: LangGraph, MCP, A2A, Kubernetes, Terraform, and a polished React 19 console. |

---

## 💎 Why AgentOps?

- 🧠 **Supervisor multi-agent orchestration** — deterministic, auditable hub-and-spoke routing built on LangGraph `StateGraph`.
- 🔌 **8 real enterprise connectors** — HubSpot, Salesforce, Jira, ServiceNow, GitHub, SAP S/4HANA, QuickBooks Online, and Microsoft Graph — all behind a single resilient connector base.
- 🛡️ **Security-first by design** — see [SECURITY_AUDIT.md](SECURITY_AUDIT.md) for the full threat model and the fixes that close each finding.
- 🔁 **Provider-agnostic** — OpenAI, Anthropic Claude, or a fully local **Ollama** daemon (privacy / air-gapped mode).
- 📊 **Operate it, don't just run it** — a 13-view React console for runs, approvals, cost, audit, memory, agents, and evaluations.
- 🚢 **Deploy anywhere** — Docker Compose, Kubernetes, Helm, Terraform (AWS), Fly.io, and an offline bundle for air-gapped sites.

---

## ✨ Features

<details open>
<summary><b>🤖 AI-Powered Multi-Agent Orchestration</b></summary>

- **Supervisor agent** emits a structured `RoutingDecision` (never calls tools directly) so routing stays deterministic and auditable
- **Researcher agent** — web search + URL scraping + enrichment, with SSRF-guarded fetches
- **Analyzer agent** — 0–10 ICP scoring with risk flags and a recommended action
- **Executor agent** — drafts proposals, writes to the CRM, and sends pinned-recipient email
- **Pluggable LLM providers** — OpenAI (default), Anthropic Claude, or local Ollama via a single `get_model()` factory
- **Agent-to-Agent (A2A) protocol** — JSON-RPC 2.0, `AgentCard` capability discovery, and an in-workflow dispatch registry

</details>

<details>
<summary><b>🔄 Workflow Automation & Orchestration</b></summary>

- **LangGraph `StateGraph`** with PostgreSQL checkpointing — every node persisted, any worker resumes any `thread_id`
- **Human-in-the-loop** via `interrupt_before` + approve/reject webhooks and Slack deep-link buttons
- **Approval escalation** — a background job ratchets stale approvals through level 1 → 2 → auto-reject
- **SSE streaming** — stream agent reasoning + tool calls live with `astream()` over `StreamingResponse`
- **Event-driven mode** — consume **Redis Streams** or **Kafka** events into a shared `EventDispatcher`
- **Dry-run simulation** — run the full LLM plan with all side effects (CRM writes, emails, Slack) skipped
- **Workflow template marketplace** — file-based registry with a `manifest.yaml` schema and a CLI validator

</details>

<details>
<summary><b>🧪 Testing, Evaluation & Validation</b></summary>

- **344 tests** across unit + integration suites
- **LLM-as-judge evaluation** — faithfulness, relevance, coherence, and hallucination detection in one pass
- **Eval regression gate in CI** — `.github/workflows/eval.yml` checks scores against a baseline
- **HubSpot pre-flight validator** — probes your real CRM end-to-end before deploy
- **Type + lint gates** — `ruff` (E/F/I/UP/B/SIM/ANN) and `mypy` enforced in CI

</details>

<details>
<summary><b>🛡️ Security (Defense in Depth)</b></summary>

- **PII redactor** — conservative regex scrubbing of common identifiers
- **Prompt-injection guard** — heuristic risk scoring on inbound text
- **SSRF guard** — blocks private IPs, IMDS, and non-http(s) schemes on every agent-controlled URL
- **Tool-output quarantine** — wraps tool results in an `<UNTRUSTED_TOOL_OUTPUT>` envelope to defeat 2nd-order injection
- **Outbound-email allowlist** — pins recipients so an LLM can't exfiltrate via `email_send`
- **JWT + RBAC**, immutable partitioned **audit log**, **rate limiting**, and a CORS allowlist (never `*`)

</details>

<details>
<summary><b>📈 Observability & Cost Control</b></summary>

- **Tracing** — pick LangSmith, Phoenix, Langfuse, or none via `TRACING_PROVIDER`; OTel auto-configures for OTLP backends
- **Prometheus** — `/metrics/prometheus` exposition endpoint
- **Cost tracking** — `tiktoken`-based token counting with a per-model cost table and per-agent breakdown
- **Budget guard** — halts a workflow before projected spend exceeds `BUDGET_LIMIT_USD`
- **Circuit breaker** — CLOSED/OPEN/HALF_OPEN state machine stops cascading failures
- **Opt-in anonymous telemetry** — off by default, PII-clean allowlist

</details>

<details>
<summary><b>🏢 Enterprise & Platform</b></summary>

- **Multi-tenancy** — `workspaces` as the tenant root with a nullable `workspace_id` on every tenant-scoped row
- **Multi-modal input** — PDF text extraction + vision-LLM image description
- **Semantic memory** — pgvector cosine recall, namespace-scoped
- **Deployment targets** — Docker Compose, Kubernetes, Helm, Terraform (AWS), Fly.io, and an air-gapped offline bundle

</details>

---

## 🏗️ Architecture

AgentOps is a **hub-and-spoke** system: a FastAPI control plane drives a checkpointed LangGraph state machine, agents reach the outside world only through an MCP tool server, and a React console operates the whole thing.

```mermaid
graph TB
    subgraph Client["🖥️ Presentation"]
        Console["React 19 Console :8501<br/>13 views · landing · architecture"]
    end

    subgraph ControlPlane["⚙️ Control Plane — FastAPI :8000"]
        API["REST + SSE API"]
        MW["Middleware stack<br/>RBAC · RateLimit · Security · Audit"]
        Jobs["Escalation job · Event dispatcher"]
    end

    subgraph Orchestration["🧠 Orchestration — LangGraph"]
        Supervisor["Supervisor Agent<br/>structured routing"]
        Researcher["Researcher"]
        Analyzer["Analyzer"]
        Executor["Executor"]
        Human["⏸ Human Approval<br/>interrupt_before"]
    end

    subgraph Tools["🔌 MCP Tool Server :8001 — FastMCP"]
        Search["Web search"]
        Connectors["8 connectors:<br/>HubSpot · Salesforce · Jira ·<br/>ServiceNow · GitHub · SAP ·<br/>QuickBooks · MS Graph"]
        MultiModal["PDF · Image tools"]
    end

    subgraph Data["💾 State & Memory"]
        PG["PostgreSQL 16 + pgvector<br/>checkpoints · audit · memory · tenants"]
    end

    subgraph Observe["📊 Observability"]
        Trace["LangSmith / Phoenix / Langfuse"]
        Prom["Prometheus"]
    end

    Console -->|nginx proxy /api/*| API
    API --> MW --> Supervisor
    Jobs --> Supervisor
    Supervisor -->|qualify| Researcher
    Supervisor -->|analyze| Analyzer
    Supervisor -->|propose| Executor
    Supervisor -->|await| Human
    Human -->|approve| Executor
    Researcher --> Tools
    Executor --> Tools
    Connectors --> External["External SaaS APIs"]
    Orchestration -->|checkpoint every node| PG
    Researcher -->|semantic recall| PG
    API --> Observe
    Orchestration --> Observe
```

### Data flow (the `sales_ops` happy path)

```
POST /workflows/run ─┐
                     ▼
            RBAC → RateLimit → Security → Audit middleware
                     ▼
            LangGraph compiled graph (PostgreSQL-checkpointed)
                     ▼
   QUALIFY ── Researcher ─► MCP: web_search / scrape_url (SSRF-guarded)
                     ▼
   ANALYZE ── Analyzer ──► ICP score 0–10 + risk flags
                     │  score < 4.0 ─► DISQUALIFIED
                     ▼  score ≥ 4.0
   PROPOSE ── Executor ──► draft_proposal (LLM) ─► PostgreSQL proposals
                     ▼
   APPROVE ── Human ─────► ⏸ interrupt_before → Slack card / POST /approvals/{token}/approve
                     │  rejected ─► DONE
                     ▼  approved
   EXECUTE ── Executor ──► MCP: send_email (pinned) + CRM upsert ─► mark "proposed"
                     ▼
                   DONE  (cost tracked · evaluated · audited · traced)
```

### Key design decisions

| Decision | Choice | Why |
|---|---|---|
| Orchestration | **LangGraph** | Built-in `interrupt_before`, PostgreSQL checkpointing, and streaming — production-proven |
| Tool discovery | **MCP** | Swap backends without touching agent code; a fast-growing open standard |
| Agent comms | **A2A (JSON-RPC 2.0)** | Capability-based discovery; swappable to gRPC for scale |
| Memory | **PostgreSQL + pgvector** | Co-locate semantic + transactional data; one datastore to operate |
| Evaluation | **LLM-as-judge** | Faithfulness, relevance, coherence, and hallucination in a single pass |
| Resilience | **Circuit breaker + tenacity** | Stops cascading failures at the API boundary |
| Frontend | **React 19 + Vite + nginx** | Single-origin SPA, reverse-proxied `/api/*`, hand-authored CSS with oklch tokens |

---

## 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| **Orchestration** | LangGraph · LangChain Core · langgraph-checkpoint-postgres |
| **LLM providers** | OpenAI · Anthropic Claude · Ollama (local) |
| **Tools** | MCP (FastMCP, streamable-HTTP) · langchain-mcp-adapters · Tavily |
| **API** | FastAPI · Uvicorn · Pydantic v2 · pydantic-settings |
| **Data** | PostgreSQL 16 · pgvector · asyncpg · psycopg3 · Alembic |
| **Frontend** | React 19 · Vite · TanStack Router + Query · TypeScript |
| **Resilience** | tenacity · custom circuit breaker · budget guard |
| **Observability** | LangSmith · OpenTelemetry · Phoenix · Langfuse · Prometheus · tiktoken |
| **Security** | PyJWT · custom RBAC · PII / prompt / SSRF / tool-output guards |
| **Events** | Redis Streams · Kafka (aiokafka) |
| **Infra** | Docker Compose · Kubernetes · Helm · Terraform (AWS) · Fly.io |
| **Quality** | pytest · pytest-asyncio · ruff · mypy |

---

## 🚀 Quickstart

### Prerequisites

- **Docker** + **Docker Compose**
- **An LLM provider** — one of:
  - an OpenAI API key (default), or
  - an Anthropic API key, or
  - a local [Ollama](https://ollama.com) daemon (privacy / air-gapped mode)
- *(Optional)* a Tavily API key for real web search, and a LangSmith key for tracing

### 1. Clone and configure

```bash
git clone https://github.com/Naman-the-Ace/AgentOps-Multi-Agent-Enterprise-Workflow-Orchestrator.git
cd AgentOps-Multi-Agent-Enterprise-Workflow-Orchestrator
cp .env.example .env
# Edit .env — at minimum set OPENAI_API_KEY, API_SECRET_KEY, POSTGRES_PASSWORD, DEV_LOGIN_PASSWORD
```

> Generate a strong secret with `openssl rand -hex 32` for `API_SECRET_KEY`. Startup fails fast without it.

### 2. Run migrations + start all services

```bash
docker compose --profile migration run --rm migrate   # apply Alembic migrations once
docker compose up                                      # start the stack
```

| Service | URL | Description |
|---|---|---|
| **React Console** | http://localhost:8501 | Landing page + 13-view operations console (nginx, proxies `/api/*`) |
| **FastAPI** | http://localhost:8000/docs | REST API + interactive OpenAPI UI |
| **MCP Server** | http://localhost:8001 | Tool server for agents |
| **PostgreSQL** | localhost:5432 | Database + pgvector |

### 3. Run the demo

Every API call requires a bearer JWT. With `DEV_LOGIN_ENABLED=true`, mint one
from `/auth/login` using a seeded demo user (`rep-1` has the `sales_rep` role),
then trigger a run:

```bash
# 1. Get a token
TOKEN=$(curl -s http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "rep-1", "password": "change-me-locally-only"}' | jq -r .access_token)

# 2. Trigger a workflow
curl -X POST http://localhost:8000/workflows/run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lead_data": {"company_name": "Stripe"}, "workflow_type": "sales_ops"}'
```

### 4. Verify

```bash
curl http://localhost:8000/health
# → {"status":"healthy","database":"connected","graph":"compiled"}
```

Then open **http://localhost:8501** and watch the run land in `/console/runs`. 🎉

---

## ⚙️ Configuration

All configuration is environment-based and loaded through Pydantic Settings. Copy `.env.example` to `.env` — the key knobs:

| Variable | Default | Purpose |
|---|---|---|
| `LLM_PROVIDER` | `openai` | `openai` · `ollama` · `anthropic` |
| `OPENAI_API_KEY` | — | Required when `LLM_PROVIDER=openai` |
| `API_SECRET_KEY` | — | **Required.** Signs JWTs — generate with `openssl rand -hex 32` |
| `POSTGRES_PASSWORD` | — | **Required** by docker-compose |
| `DEV_LOGIN_ENABLED` / `DEV_LOGIN_PASSWORD` | `true` / — | Demo `/auth/login`. Set `false` in production |
| `DOCS_ENABLED` | `true` | Disable `/docs` + `/redoc` in production |
| `CORS_ALLOW_ORIGINS` | `localhost:5173,8501` | Comma-separated allowlist — never `*` |
| `BUDGET_LIMIT_USD` | `5.0` | Per-workflow spend ceiling enforced by the budget guard |
| `TRACING_PROVIDER` | `langsmith` | `langsmith` · `phoenix` · `langfuse` · `none` |
| `TAVILY_API_KEY` | — | Real web search (optional) |
| `SLACK_BOT_TOKEN` | — | HITL approval cards in Slack (optional) |

---

## 📚 Usage Examples

### Run a workflow synchronously

```bash
curl -X POST http://localhost:8000/workflows/run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "lead_data": {"company_name": "Acme Corp", "industry": "fintech"},
        "workflow_type": "sales_ops"
      }'
```

### Stream agent reasoning live (SSE)

```bash
curl -N -X POST http://localhost:8000/workflows/stream \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lead_data": {"company_name": "Stripe"}, "workflow_type": "sales_ops"}'
```

### Approve a paused proposal (human-in-the-loop)

```bash
MGR=$(curl -s http://localhost:8000/auth/login -H "Content-Type: application/json" \
  -d '{"user_id": "manager-1", "password": "change-me-locally-only"}' | jq -r .access_token)

curl -X POST http://localhost:8000/approvals/<token>/approve \
  -H "Authorization: Bearer $MGR" \
  -H "Content-Type: application/json" \
  -d '{"note": "Good fit, proceed"}'
```

---

## 🔗 Workflows & Connectors

| Connector | Pairs with | Notes |
|---|---|---|
| **HubSpot** | `sales_ops` | Upsert-by-email contacts, idempotent `agentops_run_id` deals |
| **Salesforce** | `sales_ops` | Leads + opportunities + SOQL |
| **Jira Cloud** | `support_ops` | Issue create + transitions |
| **ServiceNow** | Incident mgmt | Table API incidents + change requests |
| **GitHub** | DevOps / PR review | Issues, PRs, releases, repo metadata |
| **SAP S/4HANA** | `finance_recon` | OData v2 + CSRF for orders + invoices |
| **QuickBooks Online** | `finance_recon` | Ledger + journal entries (OAuth 2.0) |
| **Microsoft Graph** | HITL approvals | Teams / Outlook / Calendar (Slack alternative) |

---

## 🔐 API Reference

Interactive OpenAPI docs live at **http://localhost:8000/docs**. Core endpoints:

<details open>
<summary><b>Workflows</b></summary>

```
POST  /workflows/run               Trigger a workflow (sync)
POST  /workflows/stream            Trigger with SSE streaming
GET   /workflows/{id}              Run status + state
GET   /workflows/{id}/trace        Per-agent execution traces
```
</details>

<details>
<summary><b>Approvals · Agents · Memory</b></summary>

```
GET   /approvals/pending           Proposals awaiting review
POST  /approvals/{token}/approve   Resume (approved)
POST  /approvals/{token}/reject    Resume (rejected)

GET   /agents                      Registered A2A agents
POST  /agents/{id}/message         Send an A2A message

POST  /memory/store                Store semantic memory
GET   /memory/search?q=            Cosine similarity search
DELETE /memory/{id}                Delete a memory
```
</details>

<details>
<summary><b>Metrics · Audit · Marketplace · Auth</b></summary>

```
GET   /metrics/                    System KPIs
GET   /metrics/cost                Cost by agent
GET   /metrics/prometheus          Prometheus exposition

GET   /audit/search                Filterable, paginated audit log

GET   /marketplace/templates       List installable templates

POST  /auth/login                  Issue access + refresh tokens
POST  /auth/refresh                Rotate refresh token
POST  /auth/logout                 Revoke tokens
POST  /auth/mfa/enroll             Begin TOTP MFA enrollment
POST  /auth/oidc/exchange          Exchange external IdP id_token
```
</details>

---

## 🛡️ Security

AgentOps ships a documented threat model and the controls that close each finding — see **[SECURITY_AUDIT.md](SECURITY_AUDIT.md)**.

- **Prompt-injection guard** scores inbound text; **tool-output guard** wraps every tool result in an `<UNTRUSTED_TOOL_OUTPUT>` envelope.
- **SSRF guard** rejects private IPs, cloud metadata (IMDS), and non-http(s) schemes.
- **PII redactor** scrubs common identifiers (conservative — prefers over-redaction).
- **Outbound-email allowlist** pins recipients so the LLM can't choose where mail goes.
- **JWT + RBAC**, an **immutable partitioned audit log**, **rate limiting**, and a strict **CORS allowlist** (never `*`).

---

## ⚡ Performance & Scalability

| Concern | Approach |
|---|---|
| **Horizontal scaling** | The API is stateless — workers share one PostgreSQL checkpointer, so any worker resumes any `thread_id`. |
| **Memory at scale** | `ivfflat` cosine index works well for <1M vectors; switch to **HNSW** for higher recall at scale. |
| **Cost control** | `BudgetGuard` blocks an LLM call before projected spend exceeds `BUDGET_LIMIT_USD`. |
| **Resilience** | Circuit breaker + tenacity retries isolate flaky upstreams; `Retry-After` honored on 429s. |

### Evaluation results

| Metric | Score |
|---|---|
| Faithfulness | 0.91 |
| Relevance | 0.88 |
| Coherence | 0.93 |
| Hallucination rate | 3.2% |
| Avg cost / run | $0.042 |
| Avg latency | 12.4s |

---

## 🚢 Deployment

| Target | Notes |
|---|---|
| **Docker Compose** | Local + single-host production |
| **Kubernetes** | StatefulSet + Deployments + HPAs + NetworkPolicies + Ingress |
| **Helm** | Templated chart with an Alembic pre-upgrade hook |
| **Terraform (AWS)** | VPC + EKS + RDS PG16 (pgvector) + Secrets Manager + ECR + IRSA |
| **Fly.io** | 3 apps + managed Postgres + 6PN networking |
| **Air-gapped** | Offline bundle builder |

---

## 👩‍💻 Developer Guide

```bash
# Install dev dependencies
pip install -e '.[dev]'

# Quality gates
make lint                          # ruff + mypy
make fmt                           # ruff format
make test                          # full suite with coverage
make test-unit                     # fast unit tests only

# Start just the DB for local API dev
docker compose up postgres

# Run the API locally (hot-reload)
uvicorn agentops.api.main:app --reload

# Run the React console (Vite dev server)
cd frontend && npm install && npm run dev   # → http://localhost:5173
```

### Extension points

| Extend… | Pattern |
|---|---|
| A new **connector** | `agentops/connectors/github.py` → `Connector` subclass + MCP tool router |
| A new **MCP tool** | any router in `agentops/mcp/server/tools/` → mount in `agentops/mcp/server/main.py` |
| A new **workflow** | `agentops/workflows/sales_ops/` → `models.py`, `prompts.py`, `stages.py`, `pipeline.py` + `manifest.yaml` |
| A new **LLM provider** | `agentops/models/provider.py` → lazy-imported branch in `get_model()` |
| A new **tracing backend** | `agentops/observability/tracing_provider.py` → a `TRACING_PROVIDER` branch |

---

## 📂 Project Structure

```
agentops/
├── agents/           # Supervisor, Researcher, Analyzer, Executor
├── graph/            # LangGraph StateGraph wiring + PostgreSQL checkpointer
├── state/            # Shared WorkflowState schema
├── mcp/              # FastMCP server (14 tool routers) + MCP client adapter
├── connectors/       # 8 enterprise connectors on a resilient base
├── a2a/              # A2A protocol, registry, transport, dispatcher
├── memory/           # pgvector semantic store + relational store
├── workflows/        # sales_ops · support_ops · finance_recon pipelines
├── api/              # FastAPI app, routers, schemas, dependencies
├── middleware/       # RBAC + JWT, audit, rate limiter, security
├── auth/ · rbac/     # JWT issuance + role policies
├── security/         # PII · prompt · SSRF · tool-output · email guards
├── resilience/       # Retry (tenacity), circuit breaker, budget guard
├── observability/    # Tracing providers, cost tracker, metrics, Prometheus
├── evaluation/       # LLM judge, metrics, dataset, eval runner
├── events/           # Redis Streams + Kafka consumers + dispatcher
├── jobs/             # Approval escalation background job
├── marketplace/      # File-based template registry
├── multimodal/       # PDF + image ingestion
├── telemetry/        # Opt-in anonymous usage emitter
└── notifications/    # Slack HITL cards

frontend/             # React 19 + Vite SPA (13 console views + landing + architecture)
tests/                # unit/ + integration/ (344 tests)
scripts/              # seed_db · run_demo · run_eval · validate_hubspot · deploy_fly · marketplace
alembic/              # 9 migrations (schema · pgvector · RBAC · escalation · multi-tenant · auth hardening)
k8s/ · helm/ · terraform/ · fly/   # Deployment targets
templates/            # Built-in + community workflow templates
docs/                 # Production runbook · air-gapped guide · images
```

---

## 🗺️ Roadmap

**✅ Shipped** — supervisor multi-agent core · PostgreSQL checkpointing · MCP tool server · A2A protocol · pgvector memory · JWT + RBAC + audit · cost tracking + budget guard · circuit breaker · LLM-as-judge evals · 8 enterprise connectors · Prometheus + OTel + Phoenix/Langfuse tracing · Slack HITL · approval escalation · event-driven mode (Redis/Kafka) · multi-modal (PDF + images) · template marketplace · React 19 console · K8s/Helm/Terraform(AWS)/Fly.io/air-gapped deploys.

**🚧 In progress / next**

- [ ] **Multi-tenant query scoping** — extend `workspace_id` filtering to all tenant-scoped endpoints.
- [ ] **Embeddings provider abstraction** — `get_embeddings()` factory for Ollama/Cohere/Voyage to unblock 100%-offline mode.
- [ ] **Terraform for GCP & Azure** — mirror the AWS module with GKE/Cloud SQL and AKS/Flexible Server.
- [ ] **Voice / Whisper transcription** — `transcribe_audio` MCP tool alongside the PDF/image pipeline.

---

## 🤝 Contributing

Contributions are welcome! Start with **[CONTRIBUTING.md](CONTRIBUTING.md)** and the **[Code of Conduct](CODE_OF_CONDUCT.md)**.

1. **Fork & branch** — `git checkout -b feat/your-feature`
2. **Set up** — `pip install -e '.[dev]'` and `docker compose up postgres`
3. **Code to the standards** — keep it typed; `make lint` (ruff + mypy) and `make fmt` must pass
4. **Test** — add tests next to the suite; `make test` must stay green
5. **Open a PR** — describe the change, link any issue, and ensure CI is green

---

## 📄 License

Licensed under the **[Apache License 2.0](LICENSE)**.

<div align="center">

---

**Built for the bleeding edge of agentic AI deployment.**

⭐ Star the repo if AgentOps helps you ship agents to production.

[Report a bug](https://github.com/Naman-the-Ace/AgentOps-Multi-Agent-Enterprise-Workflow-Orchestrator/issues) · [Request a feature](https://github.com/Naman-the-Ace/AgentOps-Multi-Agent-Enterprise-Workflow-Orchestrator/issues)

</div>

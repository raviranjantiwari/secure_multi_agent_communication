# Secure Multi-Agent Framework (SMAF)

An enterprise-grade, zero-trust coordination framework for autonomous multi-agent networks designed to mitigate systemic vulnerabilities such as prompt injections, cascade failures, lateral privilege escalation, and memory poisoning. 

This repository implements the production-ready reference pattern detailed in the architectural paper **"Security Challenges and Architectural Solutions in Multi-Agent Systems (MAS)"** using **LangGraph**, **Pydantic**, and out-of-band asymmetric verification loops.

---

## 🏗️ Core Architecture & Security Pillars

The architecture physically and logically decouples agent execution loops from security validation through four hardened defensive components:

1. **Zero-Trust Inter-Agent Mesh Topology:** Every agent is provisioned with a cryptographic identity. Inter-agent messages are structurally bound using scoped JSON Web Tokens (JWT) and Mutual TLS (mTLS) principles. Lateral agent movement is disallowed via strict communication schemas.
2. **Heuristic Ingress Guardrails:** Inbound workflows undergo deterministic validation to neutralize immediate prompt overrides before payload propagation.
3. **Asymmetric Out-of-Band Orchestration:** The execution network never polices itself. An independent, read-only **Overseer Agent** layer monitors telemetry and internal state fields out-of-band to catch indirect prompt injections introduced during runtime tool or scraper phases.
4. **Hardened Ephemeral Sandboxing:** Inbound tools, third-party integrations, and scrapers execute inside non-privileged, stateless sandboxed execution spaces where resources are wiped post-transaction.
5. **Cascade Collapse Safeguards:** A structural loop-count execution cap (strictly bounded at 10 hops) eliminates infinite messaging loops and resource exhaustion vectors.

---

## 📂 Repository Layout

```text
secure_mas/
│
├── schema.py          # State Matrix and Type-safe Reducer Schemas
├── security.py        # Token Validation and Ephemeral Sandboxing Logic
├── nodes.py           # Core System Nodes (Guardrails, Scraper, Overseer, Execution)
├── pipeline.py        # LangGraph Workflow compilation and topology configuration
└── main.py            # Automated Simulation and Verification Entry Point
```

---

## 🛡️ Implementation Details

### State Accumulation and Reducers
In standard `LangGraph` architectures, returning an updated state field overrides previous values. This framework implements a type-safe `Pydantic` runtime state schema combined with an additive reducer (`operator.add`). This approach guarantees that `message_history` and `quarantine_logs` act as **immutable, append-only operational audit trails**.

### Node Decoupling
Nodes take partial state dictionaries as inputs and return only the target fields intended to be merged or mutated. This ensures clean separation of concerns and complies with production graph compilation requirements.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- `langgraph`
- `pydantic`

### Installation
Clone the repository layout and install dependencies:
```bash
pip install langgraph pydantic
```

### Running the Verification Suite
Execute the testing suite to simulate standard operations alongside adversarial attacks (token forgery and indirect injections):
```bash
python main.py
```

---

## 📊 Architectural Verification Matrix

| Verification Domain | Target Vulnerability Vector | Framework Mitigation Pattern | Production Output Verification Check |
| :--- | :--- | :--- | :--- |
| **Identity & Ingress Access** | Impersonation / Stolen Tokens / Unauthorized Lateral Inter-agent Movement. | Scoped token peer verification paired with strict agent topological boundary checks. | Messages lacking valid token signatures are dropped by the `guardrail` node, halting processing immediately. |
| **Tool Execution & Ingestion** | Indirect Prompt Injection via external web scrapers, data parsers, or API connectors. | Micro-segmented sandboxing simulation combined with Asymmetric Out-of-Band Overseer monitoring. | Anomaly markers inside untrusted fields are detected by the `overseer` node, redirecting the pipeline to a quarantine state. |
| **System Resiliency & Agility** | Infinite Messaging Loops / Cascade Network and Compute Exhaustion. | Out-of-band telemetry monitoring tracking state-graph traversal bounds. | Processing loops reaching depth thresholds (>10 hops) trigger structural system self-healing invalidation. |

---

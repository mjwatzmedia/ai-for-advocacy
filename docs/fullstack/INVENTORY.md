# Technical inventory — November 12, 2026

Baseline: `fff100988e400672788f7615b100a9e8ccc8b009`.
The original source remains in `public/`, `server.py`, `tests/`.

Implemented baseline: template-based four-stage planning, editable source notes,
actions, correspondence, Word/Markdown export, versioned JSON save/restore.
Not implemented at baseline: search/retrieval, claim evidence checks, structured
research synthesis, jurisdiction modules, independently hosted research API.
The existing Python draft adapter cannot browse and is loopback-only.
The existing interface is vanilla JavaScript, not React. No database is required.

Smallest extension: independent FastAPI services + the existing browser workspace,
curated authoritative-source retrieval without a paid search service, configurable
server-side AI adapters. Keep the original interface at `/`; preserve the original standalone server.
No autonomous agent framework, vector database, accounts or narrative persistence.

Implementation increments:
1. Typed jurisdiction, retrieval, evidence and provider services.
2. Request-limited REST API and a typed adapter for the existing workspace.
3. Deterministic tests, live retrieval probe, reproducible builds and documentation.
4. Reviewed GitHub branch; live LLM acceptance gated on approved credentials/model/budget.

Public repository approved by MJ Watz November 12. Publication does not select a
license, authorize hosted paid endpoints, publish private management conversations
or change repository ownership.

# Contributing to AI for Advocacy

Thanks for your interest in building accessible, evidence-grounded civic technology.

## Current stage
This is a public experimental planning and bounded-retrieval foundation.
The new research runtime is on `feat/fullstack-research-engine-20261112` in draft PR #5,
not merged into `main`. Live AI is off; applicable-law/decision-maker explanations and
conversational clarification remain incomplete. Nothing is submitted or sent.
See [developer handoff](docs/fullstack/DEVELOPER-HANDOFF.md) for accurate status and setup.
A final license has not been approved.

## Before starting
1. Read [README.md](README.md), [architecture](docs/ARCHITECTURE.md), [product plan](docs/product/conversational-ux-plan.md), and [security policy](SECURITY.md).
2. Discuss substantial changes with the maintainer in an issue or agreed project channel before coding.
3. Never add real advocacy cases, personal information, credentials, tokens, or private correspondence to commits, issues, tests, or PRs.
4. Use fictional or synthetic data for demonstrations and tests.

## Local development

For the research foundation, follow [clone, run and test instructions](docs/fullstack/DEVELOPER-HANDOFF.md). The commands below run the legacy planner only.
Requirements: Python 3.10+, Node 22.12+, npm, Playwright Chromium.

```sh
npm ci
npx playwright install chromium
npm test
PORT=8080 python3 server.py
```

Visit http://localhost:8080. On Linux, Playwright may require system libraries (see README). Application runtime has no third-party packages; npm dependencies are development-only.

## Change workflow
- Create a feature/fix/docs branch from current `main`; do not commit directly to `main`.
- Keep changes scoped; update documentation and tests with behavior changes.
- Run `npm test` and `npm run test:foundation` after `uv sync --locked` in `backend/`, and report results honestly. Browser checks are not a full security audit.
- Open a pull request explaining motivation, changes, privacy/security implications, testing, and any deployment/migration impact.
- Wait for maintainer review. A passing CI check does not authorize merge or deployment.
- No external API integrations, paid services, user-data persistence, permission changes, or production deployment without explicit maintainer approval.

## Civic-information standards
Clearly separate user allegations, verified facts, interpretations, and unknowns. Never invent officials, contact details, deadlines, laws, procedures, citations, or source verification. Keep regional rules and sources separate from reusable application logic. No automated outreach or filing without the user's informed confirmation.

## License and ownership
A final open-source license has **not** been approved. Public visibility alone does not grant permission to reuse the code. The `ISC` field in package metadata is historical initialization metadata and is under review; see [LICENSE-STATUS.md](LICENSE-STATUS.md). Do not assume incoming contributions will be accepted under a particular future license; coordinate with the maintainer first.


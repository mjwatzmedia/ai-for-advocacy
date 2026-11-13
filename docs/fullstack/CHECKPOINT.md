# Research-workspace foundation — checkpoint, November 12, 2026

**Historical pre-merge checkpoint.** PR #5 was subsequently merged by MJ Watz on
November 12, 2026 (America/Los_Angeles); this foundation is included in `main`.
The results below describe the checkpoint tests, not a new production launch.
See [TEAM-START-HERE.md](../../TEAM-START-HERE.md) for the current entry point.

This increment retains the existing interface instead of rebuilding it. The research
API returns typed source, institution, claim, option and action fields. A deterministic
adapter maps these to the existing boxes. The browser validates the entire proposal,
requires a preview/review step, and preserves existing notes, drafts and completed
actions. Malformed responses and responses to a changed workspace are not applied.

## Recreate the foundation

Install Python 3.11+ and [uv](https://docs.astral.sh/uv/). From the repository:

```sh
cd backend
uv sync --locked
uv run uvicorn advocacy.api:app --host 127.0.0.1 --port 8080 --no-access-log
```

Open **http://127.0.0.1:8080**. Describe a fictional concern, goal and location.
In the plan tab, explicitly consent to source retrieval and click **Research advocacy
avenues**. Review the source records/options, then add reviewed proposals to the
workspace. Sources, institutions, options and actions populate their respective
sections. Use the campaign control for an editable public-comment, petition proposal,
representative call script or information-request template. Nothing is sent, signed
or called. Save/download a case file before closing; there is no automatic persistence.

No AWS account, PromptQL runtime, Gmail grant or ChatGPT subscription is needed.
The old `python3 server.py` planner remains available, but its new research controls
require the FastAPI server above. The legacy free-text AI button is not connected to
the research server; use the structured research controls instead.

## Research and AI limits

- Curated US civic starting points and an Arizona/Tucson pilot, or up to three
  selected public HTTPS URLs. **Not a general search engine.**
- Live retrieval on November 12 succeeded for USA.gov elected-officials and the
  Arizona legislative page listed in `live-retrieval-probe.json`.
- “VERIFIED SOURCE” in backend metadata means a recognized publisher page was
  retrieved, not that its claims, applicability, currentness or legal interpretation
  were verified. Workspace suggestions remain **needs review**.
- No actual current petition, hearing, representative phone number or deadline is
  promised. Generic options are explicitly candidate avenues to investigate.
- Provider adapters exist with mocked tests. **No live AI generation was tested.**
  AI is disabled by default: credentials, model, call limits, estimated cost budget
  and positive model pricing settings must all be explicitly configured in the
  server environment, along with each user's separate AI consent.
- This is not yet an open-ended conversational assistant. It is a concern intake,
  bounded research, structured-plan review and campaign-draft foundation.

## Run tests

Node 22.12+ and Playwright Chromium are needed for browser tests:

```sh
npm ci
npx playwright install chromium
python3 -m unittest discover -s tests -p 'test_*.py'
npm test
node tests/workspace-adapter.cjs
(cd backend && uv run python -m pytest -q)
node tests/research.cjs
```

Local results on November 12:
- Existing Python HTTP/provider suite: **3 passed**.
- Backend suite: **22 passed** (one dependency deprecation warning).
- Existing browser/accessibility/privacy/export/case-file suites: **passed**.
- New strict mapping/preservation/reference-validation checks: **passed**.
- Real FastAPI/browser integration with synthetic retrieval: **passed**, including
  review, stale edits, malformed response rejection, draft/export and reset.
- Two live source retrieval probes: **passed**; **live AI: not run**.

Automated tests are not a full security, accessibility, legal or model-quality audit.
CI for the new backend/browser suite still needs wiring.

## Security and remaining work

Local-development defaults only. HTTPS URL and DNS/address checks, bounded downloads,
origin/request checks, request limits and payload validation are present; they are not
a production security certification. Before remote deployment, review authentication,
TLS, per-user budgets and abuse controls, outbound egress policies, PDF/parser resource
isolation, provider privacy terms and jurisdiction accuracy. A configured bearer token
is only a basic API gate, not user accounts or production access management. Use one
local process; in-memory limits are not distributed or durable billing controls.

No case database or case logging was added. Source sites receive URL requests, while
an explicitly enabled/consented AI provider receives the concern and evidence excerpts.
Exports are unencrypted. Don't commit real cases, secrets, tokens or private conversations.

Next increments: complete reproduction/security documentation and CI; test an approved
live model with a budget and fictional cases; add conversational clarification and a
better review experience; evaluate broader participation coverage; independently review
and approve any deployment. Do not merge or deploy this checkpoint automatically.

# Developer handoff — November 12, 2026

## Start here

The research foundation is included in **`main`** after MJ Watz merged
[PR #5](https://github.com/mjwatzmedia/ai-for-advocacy/pull/5) on November 12, 2026
(America/Los_Angeles). Start new work from `main`, not the historical checkpoint branch.
[TEAM-START-HERE.md](../../TEAM-START-HERE.md) covers setup and contribution steps.
A merged prototype is not a public production deployment.

Install Git, Python 3.11+ and [uv](https://docs.astral.sh/uv/).
Node 22.12+ and Chromium are only needed for browser development/tests.

```sh
git clone --branch main \
  https://github.com/mjwatzmedia/ai-for-advocacy.git
cd ai-for-advocacy/backend
uv sync --locked
uv run uvicorn advocacy.api:app --host 127.0.0.1 --port 8080 --no-access-log
```

Open **http://127.0.0.1:8080**. Stop with Ctrl+C.
No AWS account, PromptQL integration, Gmail access, ChatGPT subscription or model
API key is required for the baseline. `/health` and `/ready` expose readiness.
`/docs` provides the generated API documentation. Readiness is not a promise
that an external source website is reachable.

### Five-minute fictional smoke test

1. Enter a fictional concern, desired outcome and location (e.g. safer street crossings in Tucson).
2. In the plan tab, consent to public-page retrieval. Leave AI consent off.
3. Click **Research advocacy avenues**, inspect source status and candidate options.
4. Click **Add reviewed proposals**. Inspect sources, institutions, options and actions.
5. Create an editable comment, petition proposal or call-script template.
6. Download JSON, refresh, and restore it. Exports are unencrypted.
   Nothing is sent, signed, filed or called.

Try malformed inputs and edited workspaces: a failed or stale response must not
replace existing notes or drafts. Use synthetic cases only.

## What works and what does not

| Capability | Foundation status |
|---|---|
| Intake, editable workspace, Word/Markdown/JSON export and JSON restore | Implemented |
| Curated/selected public HTTPS page retrieval | Implemented, bounded; network can fail |
| Structured source/institution/option/action mapping | Implemented with validation and review before application |
| Comment/petition/call/information drafts | Editable templates, not researched assertions |
| AI adapters | Mock-tested; disabled by default; no live model acceptance test |
| Identify the actual responsible institution/person for an arbitrary concern | Not completed |
| Determine which law/rule applies and explain authority in beginner-friendly terms | Not completed |
| Find a current applicable comment period, petition, deadline or contact | Not completed |
| Open-ended clarification chat | Not completed |
| Production accounts, secure case storage or multi-user hosting | Not implemented |

Source IDs connect records and evidence; `workspace.py` translates validated
research to case fields and `workspace-adapter.js` checks/merges those fields.
The model does not directly mutate UI state. A recognized-publisher page being
retrieved is not proof of a legal interpretation or of an available opportunity.

### Repository map

- `backend/advocacy/api.py`: request boundaries, endpoints, and serving the existing UI.
- `models.py`, `workspace.py`: validated contracts and deterministic field mapping.
- `jurisdiction.py`: initial curated institutions/source registry and location heuristics.
- `retrieval.py`: bounded HTTPS retrieval, address checks, HTML/PDF text extraction.
- `providers.py`, `evidence.py`, `engine.py`: optional AI, quote checks and orchestration.
- `public/case-model.js`: versioned case format and import validation.
- `public/workspace-adapter.js`: preserve edits, validate and apply reviewed additions.
- `public/research-workspace.js`: explicit requests, preview, stale-response guards.
- `server.py`: legacy standalone planner; not the new research runtime.
- `backend/tests/`, `tests/`: synthetic/mocked service, browser and regression checks.

The browser keeps the case in memory; no case database or automatic persistence.
The backend fetches URLs only after consent. A separately configured and consented
AI provider receives the issue and retrieved excerpts. No model calls occur by default.

## Reproduce tests

From the repository root:

```sh
npm ci
npx playwright install chromium
(cd backend && uv sync --locked)
python3 -m unittest discover -s tests -p 'test_*.py'
npm test
npm run test:foundation
```

Linux browser installations may need `npx playwright install --with-deps chromium`.
The foundation test command runs backend unit tests, strict adapter checks and
a real FastAPI/browser test using synthetic retrieval. It does not use live AI.
Legacy tests use their isolated original server. Do not test with real case information.

See [CHECKPOINT.md](CHECKPOINT.md) for dated results and limitations. These commands
are not a security certification. The existing GitHub workflow runs legacy tests;
wiring all foundation tests into CI remains a follow-up.

## Next implementation priority: authority and explanation

MJ Watz's principal requirement is:
**concern → responsible institutions/individuals → governing laws/rules →
where influence is possible → understandable explanation → advocacy plan.**

Start with one bounded jurisdiction and concern type, not claims of nationwide
coverage. The following is a recommended implementation sequence, not shipped functionality:

1. Collect missing location, institution and decision details through clarification.
2. Define typed authority records with institution/office, actual decision power,
   governing rule, source passage, effective/retrieved date, plain-language meaning,
   available influence channel and explicit unknowns.
3. Retrieve primary official documents and distinguish candidates from evidence-backed
   applicability. A quote existing in a document alone does not establish applicability.
4. Explain who can change what and why the user would approach them, without jargon.
5. Confirm participation rules, contacts and deadlines against current notices.
   Do not invent them when sources are unavailable.
6. Produce a human-reviewed game plan, preserving editable notes and evidence links.
7. Evaluate fictional positive, ambiguous, wrong-jurisdiction, stale-source,
   unavailable-source and prompt-injection cases before calling this capability complete.

Optional AI activation needs an explicitly approved provider/model, server-side key,
pricing estimates, call limits, budget and separate user consent. See the disabled
[configuration example](../../backend/.env.example). An API key is not an authority
research engine: evidence quality and applicability tests are still required.

## Contribution and release gates

Small changes should be tested, committed and pushed to a review branch as they go.
Do not merge, deploy, change permissions or enable paid model usage without approval.
Never commit keys, private management chats, real cases or identity information.

The repository is public, but a final license remains undecided. Coordinate
contribution/reuse terms with the maintainer; public visibility alone is not an
approved open-source license. See LICENSE-STATUS.md.

Before remote exposure, review authentication, TLS, user isolation, rate/spend
controls, provider privacy, source injection, PDF parsing isolation and outbound
network policies. The local preview is not a production service.

# AI for Advocacy — First interaction prototype

**Repository status:** Public, as authorized by MJ Watz on November 12, 2026. Public visibility does not select a license or authorize deployment. Contributor onboarding documents are in [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). No final open-source license has been approved; see [LICENSE-STATUS.md](LICENSE-STATUS.md).

## Development checkpoint — structured research foundation

This development branch adds a FastAPI research backend and a validated adapter
for the **existing interface**. See [checkpoint, run instructions, tests and limits](docs/fullstack/CHECKPOINT.md).
Live source retrieval is implemented for bounded curated/selected pages; live AI
generation remains disabled and untested. This is not a completed conversational
product or a deployed service. The legacy descriptions below describe the original
standalone `server.py` planner; use the FastAPI instructions for new research controls.

## Previous implementation increment — case-file return

This branch depends on draft PR #3 (base `60f2de37410ac310cc25ebad297634797d3fe1cb`); it does not merge or deploy it. See the [executable launch backlog](docs/product/functional-ai-launch-plan.md), [case format](docs/development/case-files.md), [runtime capabilities](docs/operations/runtime-capabilities.md), [proposed pilot](docs/product/pilot-scope.md) and [inactive staging plan](docs/operations/staging.md).

Use **Download case file (.json)** to save a lossless, versioned backup to your device. After closing/reloading, choose **Restore case file**. Restore validates schema/version/size/references, asks before replacing the page, and never restores AI sharing consent. Sources and suggestions stay unverified. These files are **not encrypted** and may contain private writing; keep them out of Git/issues/chat. Word and Markdown are readable documents, not importable backups. No accounts, automatic browser saving, or server case storage is introduced.

## Status

A session-only planning prototype with editable Word (.docx) and Markdown downloads, a copyable prompt for ChatGPT/Gemini, and optional local OpenAI/Gemini API assistance. The starting roadmap still uses transparent keyword matching and guided templates. No source verification, live web research, automatic sending, legal service, or production AI hosting is provided. User-added sources and AI suggestions remain explicitly unverified.

## Features

- Three-question intake: concern, desired outcome, location.
- Editable planning workspace: possible institutional roles, evidence checklist, strategy options, contacts and notes.
- Source add/edit/remove with HTTP(S)-only links and plain-text rendering.
- Actions, completion state, optional user-entered dates with required source/basis, response notes.
- Editable information-request draft; no sending or filing.
- Browser-generated Word (.docx) and Markdown exports with notes, sources, actions, draft and optional AI suggestions.
- Copy a case-specific prompt into your existing ChatGPT/Gemini account, or generate suggestions on a locally configured installation.
- Clear-workspace confirmation, fictional example.
- Responsive layout and keyboard-accessible forms/tabs.

## Privacy and permissions

The guided planner and document exports run entirely in page memory. No analytics, storage, cookies, shared database, or automatic provider calls are used. Clicking Generate AI suggestions requires explicit sharing consent; the current workspace then passes through the local server to the chosen configured provider. Copy prompt sends no data automatically, but pasting it elsewhere shares it under that service's policies. The server does not save cases or log requests. OpenAI requests use `store: false`; that is not a promise of zero provider retention. Provider, hosting, device, browser and extension policies still apply. Source URLs are never fetched by this integration. Exports stay on the user's device. Do not enter sensitive details.

The web service does not use PromptQL platform tokens or request visitor permissions. Publishing the app artifact is a separate operator action, not an application capability. The artifact is available to authorized viewers of its owning PromptQL bot, not an unrestricted public website.

## Run

Python 3.10+; application runtime has no third-party dependencies.

```sh
PORT=8080 python3 server.py
```

Open http://localhost:8080. GET /readyz returns 204. For PromptQL publication use an enabled persistent systemd service; the provisioned deployment uses advocacy-app.service.

## Tests

Requires Node **22.12+**, npm, Python **3.10+**, and Playwright Chromium.

```sh
npm ci
npx playwright install chromium
npm test
```

On a new Linux machine, Chromium may need OS libraries. Use the Playwright installation
instructions (or `npx playwright install --with-deps chromium` with appropriate OS permissions).
`npm test` starts and stops its own **isolated loopback server on an ephemeral port**,
serving a temporary copy of the assets with the real Python handler. It does not reuse
or change a running prototype. It removes `PROMPTQL_*` variables from test subprocesses.
No external account, API key, PromptQL installation, or running application server is required. Tests exclude provider credentials and use synthetic fixtures/mocked provider replies.

**Pull request CI:** `.github/workflows/tests.yml` runs `npm ci`, installs Chromium and
its Linux dependencies, then runs `npm test` on GitHub-hosted Ubuntu for opened, updated
and reopened pull requests. It uses read-only repository permissions and no application
or deployment secrets. Failed tests fail the check; no deployment occurs. Branch-protection
requirements are not configured by this workflow.

Python provider/HTTP tests: `python3 -m unittest discover -s tests -p 'test_*.py'`.

A preinstalled Chromium can be selected with `TEST_BROWSER_EXECUTABLE=/absolute/path/to/chromium`.

Individual suites: `npm run test:smoke`, `npm run test:views`, `npm run test:privacy`.
To invoke the runner from another directory, use `node /path/to/repository/tests/run.cjs`.
Set `PYTHON` if the Python executable is not named `python3`.
Screenshots/reports go into ignored `test-results/`; `TEST_OUTPUT_DIR` can select another
output directory. These files contain synthetic test data, not actual advocacy cases.
Do not run suite files directly: they require the runner's private test-server URL.

Coverage includes existing intake/source/action/draft/export behavior, validation, injection-safe
rendering, non-US fallback, reset, no storage, browser errors, mobile layout, and axe accessibility
scans (desktop/mobile plus three panels at four widths). Axe violations fail the test run.
A dedicated privacy regression verifies cancel leaves the case intact; confirmed clearing
removes state, form values, rendered entries, hidden summaries, source/action handlers and counts;
a subsequent case/export does not contain the prior case. Its request monitor rejects
unexpected external requests, query-string requests and non-GET requests. Automated checks
are not a complete accessibility or security audit.

Clearing is an in-page reset, **not secure erasure** of browser memory, device backups,
downloaded exports, clipboard contents or browser extensions. Existing exports are not deleted.

## Versioned baseline

The original preservation commit is `da96749944d6cc302ecfe2ddcca93dca91ca07ce`.
The manifests and evidence under `docs/audit/` describe that historical commit, not later
modified files. See [recovery instructions](docs/operations/recovery.md) and
[cleanup review notes](docs/development/privacy-test-cleanup.md).

## For prospective collaborators

This repository is public. Propose changes through a reviewed pull request; maintainer approval is still required to merge. Start with [CONTRIBUTING.md](CONTRIBUTING.md); use synthetic cases and open a reviewed pull request. No merge, deployment, paid integration, or sensitive-data processing is implied by repository access.

## Next design decisions

The first proposed research pilot is bounded Tucson/Pima public participation using fictional cases; it is not enabled jurisdiction coverage. The functional launch backlog records authorized reversible work and the live-provider/spending/hosting approval gates. Session-only plus explicit case files is the return default; no accounts are planned for M1.


## Optional AI assistance

Without any setup, use **Copy prompt for ChatGPT or Gemini**, review it, paste it into your chosen service, then paste useful output into **Editable AI suggestions**. Those suggestions are included in exports. This app does not log into or reuse your ChatGPT/Google account.

For local in-app generation, configure one provider using environment variables:

- OpenAI: `OPENAI_API_KEY` and `OPENAI_MODEL`.
- Google Gemini: `GEMINI_API_KEY` and `GEMINI_MODEL` (model identifier only).

Choose a text-generation model supported by your provider account. Example variable names are in `.env.example`; this file is documentation, not an automatically loaded secrets file. Set variables in your shell/service environment; never commit real keys or put them in browser code. Start `python3 server.py` and open `http://127.0.0.1:8080`.

The AI endpoint permits only loopback clients and loopback Host headers, exact same-origin requests, JSON with the app's request header, explicit consent, a bounded payload, and one generation at a time. It is a local development integration, not a public AI service. Remote/PromptQL visitors can use prompt copying and local Word downloads. A hosted AI service requires authentication, per-user abuse/budget controls, approved provider/data policies and deployment work before removing these restrictions. No remote AI deployment is part of this change.

API requests use OpenAI Responses or Gemini generateContent, no tools or browsing. AI output is unverified editable text, separate from the original roadmap; existing notes/actions are not replaced. Timeouts, missing configuration and provider failures preserve the workspace. Clearing/starting a changed story cancels the browser request and clears suggestions. An already dispatched provider call may still complete or incur charges.

A provider API key/model with usable quota is required for in-app AI. Account access and live model quality must be checked by the operator; automated tests use mocks and do not establish live provider availability.

Official API references:
- https://developers.openai.com/api/docs/guides/text
- https://developers.openai.com/api/docs/guides/migrate-to-responses
- https://ai.google.dev/api/generate-content

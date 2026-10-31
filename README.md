# AI for Advocacy — First interaction prototype

Built from mjwatzmedia's AI for Advocacy brief at Malithi's request.

## Status

A functional, session-only planning prototype. This is NOT a live AI service, source-verification engine, legal service, or production launch. The roadmap uses a transparent keyword match plus guided templates. No actual office, deadline, legal requirement, or procedure is verified. User-added sources remain explicitly unverified.

## Features

- Three-question intake: concern, desired outcome, location.
- Editable planning workspace: possible institutional roles, evidence checklist, strategy options, contacts and notes.
- Source add/edit/remove with HTTP(S)-only links and plain-text rendering.
- Actions, completion state, optional user-entered dates with required source/basis, response notes.
- Editable information-request draft; no sending or filing.
- Markdown export, clear-workspace confirmation, fictional example.
- Responsive layout and keyboard-accessible forms/tabs.

## Privacy and permissions

Concern text never leaves page JavaScript memory. No API calls, analytics, storage, cookies, shared database, AI provider, or background requests are used by application code. External source links open only at the user's direction. Files explicitly exported are saved by the browser. Reloading or closing the page clears entries, subject to browser session behavior. The server serves only static assets and a readiness endpoint; HTTP access logging is disabled. The PromptQL hosting platform and user's device retain their own privacy considerations. Do not enter sensitive details.

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
No external account, API key, PromptQL installation, or running application server is required.

**Pull request CI:** `.github/workflows/tests.yml` runs `npm ci`, installs Chromium and
its Linux dependencies, then runs `npm test` on GitHub-hosted Ubuntu for opened, updated
and reopened pull requests. It uses read-only repository permissions and no application
or deployment secrets. Failed tests fail the check; no deployment occurs. Branch-protection
requirements are not configured by this workflow.

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

## Next design decisions

Confirm the first country/region, initial testers and first real issue, and privacy/retention rules before integrating live AI, jurisdiction-specific primary-source retrieval, or durable accounts. Nothing in this list is implemented or a committed delivery schedule.

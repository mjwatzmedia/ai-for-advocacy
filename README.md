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

```sh
npm ci
npx playwright install chromium
node tests/smoke.cjs
```

Tests assume the server is on localhost:8080. The generated deployment tests use /workspace/advocacy/tests for output. Run in the deployment workspace or adjust paths for local use.

Smoke coverage includes validation, example intake, roadmap routing, source creation/editing and injection safety, date-basis validation, action completion, draft, Markdown export content, non-US fallback, reset, mobile layout, no storage, no data POSTs, and browser errors. Automated axe scans cover desktop roadmap and mobile intake. Passing scans are not a complete accessibility audit.

## Next design decisions

Confirm the first country/region, initial testers and first real issue, and privacy/retention rules before integrating live AI, jurisdiction-specific primary-source retrieval, or durable accounts. Nothing in this list is implemented or a committed delivery schedule.

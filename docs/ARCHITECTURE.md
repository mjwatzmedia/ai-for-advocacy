# Baseline architecture and roadmap status

## Implemented baseline

- public/index.html, style.css, app.js and favicon.svg: browser-only HTML/CSS/JavaScript.
- server.py: Python standard-library static server, readiness endpoint and security headers.
- Browser state plus DOM-held notes: concern/goal/location, keyword-based candidate roles,
  evidence checklist, manually added unverified sources, options, actions, notes and drafts.
- Browser-only OOXML Word (.docx) and Markdown exports, prompt copying and optional local provider requests. No automatic filing, sending, reminders or background jobs.
- Dev-only Playwright/axe tests; package-lock.json pins transitive versions.
- Optional publish.py operator utility is platform-specific; runtime is not.

Optional explicit-consent local OpenAI Responses/Gemini generateContent invocation is implemented in server.py. No retrieval/index/vector service, source verification,
jurisdiction rules database, durable cases, accounts or production AI backend is implemented.
Do not describe missing services as present or introduce misleading empty implementation files.

## Committed product direction; implementation approval pending

See product/master-development-specification.md and product/conversational-ux-plan.md.
The UX direction is conversation-first with an editable/exportable Advocacy Game Plan;
four advocacy capabilities become primarily internal, not mandatory navigation.
That direction does not alter what this baseline implements. The separately named full
UX architecture specification still needs to be supplied for full-text reconciliation.

The conversational plan's GitHub-unverified snapshot is historical (before this baseline).
See audit/BASELINE.md and the post-push handoff for the preservation results; nothing in
this backup authorizes the proposed implementation, provider changes or deployment.

## Approval boundaries and maintenance

MJ Watz is founder/primary maintainer. Official repository is currently private and invitation-only; any future visibility change requires authorization.
No final license, invitations, paid services, permissions changes, production migrations,
provider/model selection, major replacement or deployment without explicit authorization.
Development follows reviewed branches, tests, commits, push and PRs. Merge and release
require their own approval. Keep secrets, confidential cases and unnecessary personal
history out of Git. Regional source knowledge must stay separate from reusable logic.

Until UX implementation is approved, the next work is resolving the full specification,
first jurisdiction, return/privacy policy and approved model/research budget.


## Current AI boundary

See README Optional AI assistance for server configuration and limitations. Provider secrets remain server-side. The local-only JSON endpoint limits request/response sizes, enforces same origin and serializes provider calls. DOCX generation happens in browser memory without libraries or uploading case data. No automatic provider call is made on page load, intake or export.

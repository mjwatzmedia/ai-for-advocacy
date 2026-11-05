# Functional AI launch plan — executable backlog

Updated 2026-11-04. MJ Watz authorized reversible isolated implementation, branch pushes and review PRs in the supplied functional-launch specification. No merge, paid activation, public release, license/permission change, real sensitive cases or replacement of the live application is authorized.

## Current truth and shortest path
- Private repository: https://github.com/mjwatzmedia/ai-for-advocacy . Current main: `d1adb168b4db7c04d0641ce5d15d59fb9945e950`.
- Draft PR3 `codex/word-roadmap-ai-assistance` head `60f2de37410ac310cc25ebad297634797d3fe1cb` already implements browser Word/Markdown, prompt copying and optional **local-only, unverified** OpenAI/Gemini suggestions. Reuse it; do not merge it implicitly.
- This increment branch `feat/case-file-roundtrip` starts from PR3's exact head. A PR against PR3 is stacked: PR3 must be reviewed/merged or its dependency resolved explicitly before main integration. Main-level comparison will include PR3 until then.
- Live PromptQL service `advocacy-app.service` on port8080 runs `/workspace/advocacy/server.py`, serving that directory's public assets, not this checkout. It remains the earlier static prototype. Its application/server source matches the preservation baseline; not a deployed Git checkout, so deployment identity is established by file hashes, not an invented release SHA. Git pushes do not publish this service.
- Pulls, local branches and commits work. Read access and Git object uploads work; earlier native push/ref writes timed out. Recheck actual branch/PR results; never call a local commit synchronized. No automatic deployment configured in this repository's workflow; external deployment hooks were not fully inspectable.
- A source-only snapshot is retained outside Git with no credentials or private case data. Baseline: npm test four suites and three Python mocked/HTTP tests pass on this VM. No live model call or retrieved official material was evaluated.

## Milestones and acceptance gates
1. **M1 useful without live research (current):** reuse Word; one validated case; lossless user-controlled JSON return; inherited planner/notes/actions/reset/exports preserved; CI fixtures pass. Not a functional researched AI release.
2. **M2 evidence-grounded vertical slice:** one provider, one Tucson/Pima published-proposal participation workflow, curated original texts, claim-linked evidence, necessary questions, editable user-selected plan. A URL existing is not proof of support.
3. **M3 hosted invited testing:** explicit authorized users, secrets, measured cost limits and private staging, current-document live evaluation and tested rollback. Separate exposure/spend approval.
4. **M4 expand only from observed needs:** more jurisdictions/documents/collaboration; no vector database or autonomous agent fleet without a demonstrated need.

## Executable work packages
Statuses distinguish implemented code from tested behavior. Blocked live work does not stop independent tasks. File additions below are plans unless present in this branch.

### WP1 — Baseline and preservation
- **Priority/dependency:** P0; none. **Status:** tested.
- **Current:** Baseline browser/Python tests pass; main d1adb168; PR3 60f2de3 open draft; live service older, separate.
- **Build:** Record main/PR/deployed fingerprints and preserve isolated recovery snapshot; never overwrite live files.
- **Reuse/add:** Reuse server.py, tests/, docs/operations; add this plan and baseline evidence.
- **Acceptance:** Exact main/base/live fingerprints recorded; clean isolated branch; inherited tests pass.
- **Verify:** Git reads, hashes, npm test, Python unittest.
- **Service/credential/decision:** GitHub repository access (working); no new account.
- **Complete here:** Yes.

### WP2 — Runtime capability routes
- **Priority/dependency:** P0; 1. **Status:** tested.
- **Current:** VM/systemd/app publication supported; no app model API verified.
- **Build:** Document development-vs-visitor runtime capabilities and smallest portable fallbacks.
- **Reuse/add:** Reuse server.py/publish.py; add docs/operations/runtime-capabilities.md.
- **Acceptance:** Every required capability has documented route, limits or blocker.
- **Verify:** Product API/App Artifacts docs + service inspection; no secret-value inspection.
- **Service/credential/decision:** Later deployment decision; do not borrow operator token.
- **Complete here:** Yes: capability matrix, not live service activation.

### WP3 — Bounded pilot
- **Priority/dependency:** P1; 1. **Status:** in progress.
- **Current:** No bounded researched pilot; manual US directories only.
- **Build:** Propose Tucson/Pima published-proposal/public-comment demo with fictional case; source ownership/process review gate.
- **Reuse/add:** Reuse notes/source UI; add docs/product/pilot-scope.md.
- **Acceptance:** Scope, unsupported routes and minimum documents explicit; no invented authority or deadline.
- **Verify:** Review fictional demo and inspect primary sources in M2 before registry acceptance.
- **Service/credential/decision:** Proposed local pilot; source verification still needed.
- **Complete here:** Yes: scope now; current official documents in M2.

### WP4 — Real provider
- **Priority/dependency:** P1; 2,3. **Status:** blocked.
- **Current:** PR3 local OpenAI/Gemini text adapter; no real call verified.
- **Build:** Prefer OpenAI adapter initially; check current official docs, typed output, request/output/call budget caps, timeout/cancel, bounded retry, sanitized usage; leave local gate.
- **Reuse/add:** Reuse server.py provider_plan and UI failure handling; add provider adapter/tests only in M2.
- **Acceptance:** Authorized staging real request succeeds; malformed/quota/timeout safe; manual planner survives; measured cost within cap.
- **Verify:** Deterministic mocked tests then separately approved live evaluation.
- **Service/credential/decision:** Owner-controlled OpenAI API quota/model and small spend cap via host secret manager or systemd credential; never chat.
- **Complete here:** Code yes; live testing blocked until secure credential and cost approval.

### WP5 — Structured case model
- **Priority/dependency:** P0; 1. **Status:** tested.
- **Current:** Data split between JS arrays and DOM.
- **Build:** Versioned validated case for story/preferences/jurisdiction/facts/research/institutions/sources/claims/options/actions/notes/suggestions/revisions and draft buffers; preserve user vs generated content.
- **Reuse/add:** Reuse public/app.js and fields; add public/case-model.js, tests/case-model.cjs.
- **Acceptance:** Every supported editable value survives round-trip; unsafe/versioned data rejected atomically; goal/location corrections mark generated material for review.
- **Verify:** Schema unit tests + browser conversion/restore; no network/storage.
- **Service/credential/decision:** None.
- **Complete here:** Yes.

### WP6 — Conversation
- **Priority/dependency:** P1; 5,4. **Status:** not started.
- **Current:** Three-field intake; no conversation.
- **Build:** Conversation composer, one/two material questions, unknown/correction handling, visible interpretation, accessible cancel/retry.
- **Reuse/add:** Reuse intake and manual tools; add conversational functions/UI and fixture tests.
- **Acceptance:** Natural fictional concern reaches draft plan without mandatory stage screens; answers not repeated.
- **Verify:** Deterministic conversation fixtures, keyboard/mobile tests; live behavior separately.
- **Service/credential/decision:** Provider route for real conversation; no credential needed for fixtures.
- **Complete here:** Yes for code/mocks; live provider blocked.

### WP7 — Official-source registry
- **Priority/dependency:** P1; 3. **Status:** not started.
- **Current:** No source registry; user labels unverified.
- **Build:** Small institutional-ownership checked registry, allowlisted exact locations, topics/types/dates/checks/limitations/refresh; no trust-by-domain heuristic.
- **Reuse/add:** Reuse source UI; add jurisdictions/pima-pilot/sources.json and source validation docs/tests when verified.
- **Acceptance:** Each entry ownership checked against actual official publisher; contributor validation documented.
- **Verify:** Fetch/read primary pages and record check date/hash; review process/jurisdiction coverage.
- **Service/credential/decision:** Access to public official documents; no paid service necessary.
- **Complete here:** Yes; no entries called verified before checking.

### WP8 — Retrieval
- **Priority/dependency:** P1; 7. **Status:** not started.
- **Current:** No retrieval; source links not fetched.
- **Build:** Curated-first fetch/rank, HTML and text-PDF extraction, passages/page labels/hash cache; block private IPs and revalidate redirects/DNS; size/time/count/type caps; OCR honest fallback.
- **Reuse/add:** Reuse Python server boundary; add retrieval module/tests/public-source cache path outside case state.
- **Acceptance:** Fictional case gets original passages; no-source/scan/redirect/network failures yield partial result; SSRF fixtures blocked.
- **Verify:** Deterministic HTTP/PDF fixtures + separate approved live official-doc evaluation.
- **Service/credential/decision:** Optional search connector later; PDF library pinned when needed.
- **Complete here:** Yes; web search not necessary for curated first slice.

### WP9 — Claim-level citations
- **Priority/dependency:** P1; 5,8. **Status:** not started.
- **Current:** No verified findings or claim links.
- **Build:** Claim/source-version/passage/location/jurisdiction/check-date contract; separate allegation/text/support/interpretation/lead/question; deterministic reference checks.
- **Reuse/add:** Reuse case records; add citation validator and source-open UI/tests.
- **Acceptance:** Users see exact support and limitations; fabricated IDs/snippet-only claims rejected; unsupported findings unverified.
- **Verify:** Hostile/superseded/conflicting/reference fixtures.
- **Service/credential/decision:** None beyond source content.
- **Complete here:** Yes.

### WP10 — Civic orchestration
- **Priority/dependency:** P1; 4,6,8,9. **Status:** not started.
- **Current:** Keywords/templates, not civic reasoning.
- **Build:** Single bounded orchestrator: understand, jurisdiction, questions, retrieve, supported findings/options, gaps, user choices, plan; deterministic date/status/authority checks.
- **Reuse/add:** Reuse describeIssue as fallback lead only; add orchestrator module and tests.
- **Acceptance:** No invented legal date/contact/authority; adviser vs decision-maker/proposal vs adopted and target vs deadline explicit; bounded partial return.
- **Verify:** Grounding/correction/timeout/loop budget fixtures.
- **Service/credential/decision:** Runtime provider/budget for live path.
- **Complete here:** Yes code; live end-to-end blocked on 4.

### WP11 — Collaborative choices
- **Priority/dependency:** P1; 6,9,10. **Status:** not started.
- **Current:** Manual strategy checkboxes and notes.
- **Build:** Present lawful options with effort/evidence/limits, ask preferences/time/resources, let user stop/change course; categories not invented endorsements.
- **Reuse/add:** Reuse strategy-list/actions/notes, case preferences/options.
- **Acceptance:** Same evidence can produce two user-chosen plans; official rules distinct from strategy suggestions.
- **Verify:** Two-choice fixtures + user-control regressions.
- **Service/credential/decision:** No political goal selected by app.
- **Complete here:** Yes.

### WP12 — Editable Game Plan
- **Priority/dependency:** P1; 5,9,10,11. **Status:** not started.
- **Current:** Editable manual roadmap, suggestions text.
- **Build:** Game Plan includes goal/context/institutions/evidence/gaps/choices/actions/date basis/correspondence/progress; proposed updates accept/reject; preserve edits/completed actions.
- **Reuse/add:** Reuse renderPlan, drafts/actions, case-model; add update review UI/tests.
- **Acceptance:** New evidence never silently overwrites user writing; changed goal/jurisdiction flags affected conclusions.
- **Verify:** Update-diff and preservation fixtures; mobile/keyboard.
- **Service/credential/decision:** None additional.
- **Complete here:** Yes; evidence-backed slice depends on 4/8.

### WP13 — Downloads and return
- **Priority/dependency:** P0; 5. **Status:** tested.
- **Current:** PR3 real DOCX and Markdown already pass; no lossless restore.
- **Build:** Reuse Word, retain Markdown, add browser-only validated versioned JSON export/import with limits and explicit replace confirmation; readable exports cover case records.
- **Reuse/add:** Reuse makeRoadmapDocx/buildMarkdown; add case controls, tests/casefile.cjs.
- **Acceptance:** Export/close/reopen/import recovers all supported fields; invalid/oversized/version/malicious/cancelled import leaves case intact; consent never restored.
- **Verify:** Unit/browser roundtrip and DOCX ZIP/XML/content checks.
- **Service/credential/decision:** None; unencrypted local files require user care.
- **Complete here:** Yes.

### WP14 — Staging and hosting
- **Priority/dependency:** P2; 2,4,8,12,13,15. **Status:** blocked.
- **Current:** Live original static prototype; no hosted AI or staging.
- **Build:** Prepare inactive staging/access/secret/HTTPS/rate/concurrency/cost/logging/health/rollback guide; do not expose local AI by removing checks; publish only after approval.
- **Reuse/add:** Reuse service example/health/provider local gate; add docs/operations/staging.md.
- **Acceptance:** Invited tester completes full browser flow with approved budget/credentials/auth; rollback tested; logs exclude raw case text.
- **Verify:** Mock auth/budget tests then approved hosted evaluation.
- **Service/credential/decision:** Provider secret, allowed testers, maximum spend, hosting/exposure approval.
- **Complete here:** Preparation yes; activation blocked by approval/configuration.

### WP15 — Quality and user control
- **Priority/dependency:** P0 ongoing; each relevant task. **Status:** in progress.
- **Current:** Existing smoke/privacy/views/Word/HTTP mocks pass.
- **Build:** Preserve tests; add structured case and restore now; M2 grounding/jurisdiction/source attacks/errors/cancel/edit preservation; M3 isolation/live rubric.
- **Reuse/add:** Reuse tests/CI; add case unit/browser fixtures and later grounded pilot evaluation report.
- **Acceptance:** Every milestone fixture passes; any invented official deadline/contact/authority/citation blocks AI release; no undefined accuracy score.
- **Verify:** npm test, Python unittest, future separately budgeted live dataset with model/prompt/doc hashes/date/cost.
- **Service/credential/decision:** No credentials for CI; live eval requires 4/14 approvals.
- **Complete here:** Yes deterministic; live blocked.

## Minimum owner inputs — not blockers for M1
For real AI/live hosted evaluation: supply an operator-controlled provider API account/model via an approved server secret facility (never chat), approve a small explicit maximum spend and confirm invited staging users/hosting. Recommend OpenAI first with the existing adapter, but no paid provider/model is activated by this proposal. Tucson/Pima published-proposal/public-comment is the conservative proposed pilot; mines may require state/federal/tribal review and are outside scope unless specific authority is established. Session-only plus explicit JSON files is the selected default from this specification, not a request to introduce accounts.

## Truthful reporting
Record each increment's files, actual local/remote tests, branch/SHA/PR, dependency, limitations and blockers. An unrun live call, unopened PR, failed push or unpublished revision is not successful. Current provider assistance is unverified text without retrieval and must not be marketed as a functional source-grounded pilot.

## M1 increment verification (2026-11-04)
Schema v1 and browser-only JSON save/restore implemented and tested on the PR3-dependent branch. Five browser suites pass, including source editing, actions, Word/Markdown, provider mocks, privacy and case-file restoration; 24 schema checks pass and three Python provider/HTTP mocked tests pass. No live provider, real official retrieval or staging verification is claimed. WP5/WP13 are tested for this first contract, not completion of future research/update UX. WP15 continues across M2/M3. Actual branch publication/CI result is recorded separately in the handoff; a local test is not a GitHub check.

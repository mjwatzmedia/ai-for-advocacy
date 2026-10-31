# AI for Advocacy — Conversational UX Requirements and Incremental Implementation Plan

**Planning revision: October 31, 2026. Status: proposed implementation; no application changes authorized or performed.**

## Decision summary

Replace mandatory stage-based navigation with a conversational entry point and a personalized, editable **Advocacy Game Plan**. Keep the four advocacy stages as reusable internal research/analysis capabilities rather than four screens users must complete. Users retain access to evidence, uncertainty, options and the ability to change their plan; internal orchestration must not become an unexplained black box.

The requirements below incorporate MJ Watz’s October 31 message. The separate full document titled **“User Experience Architecture — Internal Research, Externalized Game Plans”** was not attached to that message and was not found in the previously supplied master specification or initial brief. The entire named document cannot yet be certified as incorporated. Supply its full text for a gap comparison before implementation approval. The four stage names below are confirmed in the existing master specification, not guessed.

This plan and the accompanying wiki proposal are reviewable requirements/roadmap artifacts. They have **not** been committed to GitHub, and the revised UI has not been built or deployed.

## 1. Preservation and version-control gate — BLOCKED

| Check performed for this plan | Observed result |
|---|---|
| Authenticated GitHub identity | `mjwatzmedia` |
| Visible GitHub App installations | 0 |
| Intended lookup `mjwatzmedia/ai-for-advocacy` | 404: inaccessible or absent; cannot distinguish |
| Confirmed current repository URL | **UNKNOWN**; the intended name is not a verified repository |
| Baseline Git commit | **NOT VERIFIED**; no local Git repository exists |
| Preservation of current VM files | All 17 files match the pre-audit SHA-256 manifest |
| Existing downloadable source ZIP | Previously verified 12-file export, not a GitHub backup |

**I cannot confirm that the prototype has been preserved in GitHub.** The last authorization covers checking for an existing repository, private creation if necessary, and a first sanitized baseline commit. That authorization does not authorize implementing or deploying this UX revision.

Before modifying application code: grant selected repository access, identify an existing repository or confirm none exists, complete the authorized private backup, verify ownership/privacy/remote contents and record the exact baseline commit SHA. If a repository already has history, inspect and preserve it rather than force-push or replace it. Include the working code, dependency lockfile, tests, sanitized operating instructions and deliberately selected product requirements; exclude credentials, private case data and unrelated chat history. Account for the audit’s missing deployment/context files. Preserve source faithfully in the baseline and document unapproved generated ISC metadata rather than silently choosing a license.

After UX implementation approval and baseline verification, fetch/check the current repository and create a dedicated branch, proposed name **`feat/conversational-game-plan`**, from the agreed baseline/updated base. No such branch has been created.

## 2. Confirmed revised product requirements

| ID | Requirement | Acceptance evidence planned |
|---|---|---|
| UX-01 | Users describe their situation conversationally; mandatory navigation through four stages is removed. | A user reaches a draft plan from conversation without completing stage screens. |
| UX-02 | The assistant asks necessary clarifying questions about the situation, outcome, jurisdiction and other material gaps. | It uses supplied answers, avoids redundant questions, handles corrections/unknown answers, and does not silently infer a missing jurisdiction. |
| UX-03 | Four stages primarily operate internally: identify who can act, build a case, explore options, take the next step. | Structured outputs can run/revisit as needed, with task status and useful evidence summaries rather than mandatory sequential forms. |
| UX-04 | Research informs a personalized Advocacy Game Plan with verified sources, relevant institutions, available options and concrete next steps. | Each consequential factual assertion has supporting evidence and applicable jurisdiction/status; unverified or unavailable material is explicitly labeled, not manufactured. |
| UX-05 | The plan is editable and exportable. | User changes to goals, options, actions, notes and drafts survive exports and subsequent accepted updates. |
| UX-06 | Users return with new information and continue progressing on their plan. | A supported restoration method recovers the plan and progress; later updates do not erase accepted user edits. Persistence mechanism remains a decision. |
| UX-07 | Existing useful functionality and user information are preserved. | Source editing, action tracking, notes, drafts and export regressions pass; no destructive migration or silent draft replacement. |
| UX-08 | Revision follows GitHub control and review. | Verified baseline; dedicated branch after approval; tests, commits, pushed branch and review PR with exact SHAs; no unapproved merge/deploy. |

Research can fail, be incomplete or lack primary evidence. In those cases the system must explain what remains unverified, ask an appropriate question or offer a research next step. It must not call an unsupported institution, option or deadline verified merely to fill a game-plan section. User-facing explanation means concise findings, evidence, assumptions and uncertainty—not exposing private model reasoning traces.

## 3. Reusing the four-stage workflow

The original master specification names these four stages. The implementation contains related templates/cards and an actions panel, **not a functioning four-stage research engine**. Its sidebar’s four entries—story, roadmap, sources, actions—are navigation, not evidence of four implemented research services.

| Existing conceptual stage | Reusable prototype pieces | Proposed internal responsibility | Work still required |
|---|---|---|---|
| Identify who can act | `describeIssue()`, candidate-role cards, authority notes | Resolve jurisdiction and candidate institution/remit; connect supported claims to sources | Keyword categories remain fallback leads only; actual institutional research/verification is new |
| Build a case | Evidence checklist, source add/edit/remove, source notes | Organize allegations versus supported facts; record provenance, contradictions, missing evidence | No ingestion/retrieval/citation verification exists; user-entered source type is not proof |
| Explore options | Strategy choices and free-text approach notes | Compare supported avenues, applicability, limits and user preferences | Procedures, eligibility and deadlines require source-grounded validation; no political-position steering |
| Take the next step | Actions, completion state, optional dates/bases, response notes, editable draft | Produce a chosen first step, monitor recorded progress and propose follow-ups | No reminders, automatic filings or submissions added by this revision; none exists today |

Reuse content, validation and UI behaviors; extract testable functions only as needed rather than rewrite the app. Internal work should be revisitable in any order when a user changes a goal/location or supplies new evidence. Do not ask the user to complete artificial stages just because the internal pipeline has four conceptual capabilities.

## 4. Interface modification map

| Component / source | Proposed change | Preserve |
|---|---|---|
| Intake, `index.html`, `submitIntake()` | Introduce conversation composer, history, clarifications and visible cancel/retry/research status. Existing concern/goal/location become case facts, not a mandatory three-field screen. | Ability to inspect/correct all supplied facts; minimal personal-data collection |
| Sidebar, `activeNav()`, `setTab()` | Conversation and Game Plan become primary destinations; sources/actions accessible as tools/details, not required steps. | Keyboard navigation and access to existing evidence/actions |
| Roadmap, `renderPlan()` | Editable Game Plan with goal/context, institutions, evidence, options, first step, actions/progress and open questions. | Notes, warnings, user-selected approach and explicit unverified status |
| Source workspace, `renderSources()` etc. | Reuse CRUD; add provenance, claim associations, dates/status and research results when real retrieval exists. | Existing manually entered notes/links; safe URL/text rendering |
| Actions and draft | Embed or link inside Game Plan; proposed edits separated from user-approved content. | Completed items, date basis, response history, editable correspondence and human control over sending |
| State currently split between `state` and DOM | Introduce a versioned case/game-plan model and snapshot before conversion. | All story/source/action data and DOM-only notes/checks/draft—not just current arrays |
| `exportMarkdown()` | Maintain human-readable export; add plan metadata/uncertainty and progress. | Existing content and truthful verification/privacy notices |
| Return/resume flow | Add restoration after privacy choice; proposed portable structured export/import is one option, private accounts/storage another. | Existing session-only mode until storage is approved; no quiet localStorage/server retention |
| Privacy/limits, `clearWorkspace()` | Explain actual storage/provider transfers; repair the known hidden-DOM reset residue through a scoped reviewed change. | No invented privacy guarantees; manual downloads remain user-controlled |
| Server/headers | Backend introduced only for approved real model/retrieval functionality; current server stays intact for baseline. | Secure server-side secrets; current network-blocking CSP not loosened without review |

## 5. Proposed game-plan contract — for design review

A versioned `case` contains user story, goal, jurisdiction and clarified facts; source records and claim-to-source associations; institution candidates and verification state; options with applicability/limits; selected approach; editable action items and completion; response notes; correspondence; open questions; verification/check dates; and revision/update metadata. Conversation history should be retained only to the extent the user’s approved privacy choice requires.

Separate user-authored material from generated suggestions. A new answer/research result proposes a diff: show which facts/options/actions changed and why, let the user accept/reject, and preserve earlier user edits/completed actions. A changed jurisdiction invalidates affected conclusions for review rather than carrying them over as verified. Source verification is scoped to a claim, jurisdiction, document version and check date—not a universal trust badge.

**Proposed initial export:** continue Markdown for reading/sharing; a versioned JSON export/import could support returning without a hosted account. These are design proposals, not features implemented or approved storage choices. Structured imports need schema/size validation, safe text rendering and migration tests. Existing Markdown exports are not a lossless serialized case; importing them cannot be promised to reconstruct all state automatically. Existing in-page sessions cannot be read centrally or resurrected after closure. Users must export before closing/reloading; any controlled transition needs an explicit snapshot/restore mechanism before replacing a loaded page.

## 6. Incremental roadmap and approval gates

### Gate 0 — Requirements and verified baseline
- Obtain the full named UX specification and compare it to UX-01–08; keep missing details explicit.
- Resolve GitHub identity/access/existence, complete authorized private baseline backup and record repo URL + full commit SHA.
- Review this plan, first jurisdiction, return/privacy approach and AI/research scope.
- Exit: owner approves UX implementation; no code changes until preservation is verified.

### Increment 1 — Branch, safety harness and compatibility model
- Create the dedicated development branch only after approval; work in an isolated clone/worktree, not the running app directory.
- Make existing tests portable and fix the failing npm test entry point; add conversion fixtures for all existing data, including DOM-held fields.
- Introduce a case/game-plan contract and compatibility adapter; address reset residue with regression coverage.
- Exit: old workflow and export still pass, snapshot/restore round-trip passes, no live service or data alteration.

### Increment 2 — Conversation and editable Game Plan shell
- Implement conversational intake, correction/clarification behavior and editable plan presentation using deterministic test doubles.
- Reuse source/actions/draft tools, and keep the old workspace available for regression/rollback during development.
- Exit: user can describe a concern, answer only missing questions, edit an explicitly simulated plan and export it. Simulation cannot be marketed as live AI research.

### Increment 3 — Approved AI and evidence pipeline
- After provider/model/research and spend approval, add backend provider adapters, retrieval/provenance and structured-output validation.
- Run four internal capabilities adaptively; show useful evidence/status and source limitations, not stage gates.
- Add timeout/cancellation/retry, cost/rate controls, injection defenses, source failure and unsupported-claim behavior.
- Exit: supported factual content is traceable; missing evidence causes qualified/incomplete outputs, not fabricated answers. Existing manual workflow remains usable on provider failure.

### Increment 4 — Return, progress and controlled plan updates
- Implement the approved return method; do not quietly introduce persistence while claiming session-only privacy.
- New information produces a reviewable update without destroying user changes or completion history; maintain export and schema migrations.
- Exit: close/reopen/restore and new-information tests pass for the chosen method; consent/privacy language matches actual behavior.

### Increment 5 — Reviewable GitHub delivery
- Run existing regressions and new tests; document versions, limitations, migrations, provider configuration and rollback.
- Commit and push branch changes; open a PR with baseline/head SHA, test evidence, risks and preserved-functionality checklist. Keep changes reviewable; split into multiple PRs if appropriate.
- Exit: owner review/merge approval. **No automatic deployment, production replacement or revised-interface release.** Deployment requires separate authorization and a tested rollback process.

## 7. Required tests — planned, not newly executed

| Area | Minimum scenarios |
|---|---|
| Conversation | Complete initial story; missing goal/location; unknown jurisdiction; user correction; mixed issues; no repeated questions; cancelled request; non-English/unsupported locale disclosure |
| Internal orchestration | Four capability outputs valid; missing evidence; follow-up reruns affected work only; no forced stage navigation |
| Plan generation | Evidence-linked institution/options/actions; unsupported laws/officials/deadlines not invented; no evidence means explicitly incomplete plan; dates distinguish personal target vs supported official date |
| Editing/progress | Notes/draft/selected strategy/user edits survive updates; accepted/rejected diffs; completed actions preserved; revised jurisdiction removes stale verified status |
| Return/export | Markdown content coverage; structured round-trip if selected; version migration; invalid/malicious/oversized import; controlled restore retains every baseline data field |
| Security/privacy | Cross-user isolation if storage chosen; no secrets/client credentials; safe rendering/URLs; hostile retrieved text is not an instruction; clear purges visible/hidden DOM; provider consent and retention match behavior |
| Research/provider errors | Outdated/conflicting/unavailable source; timeout/rate limits/cost cap; malformed model JSON; cancellation and retry without duplicated actions or silent content loss |
| Accessibility/regression | Keyboard/screen reader focus and announcements, accessible streaming/research status, mobile layout, source CRUD, draft-copy fallback, action tracking, export, sample, privacy dialogue and reset |
| Delivery | Clean install/test, independent-clone setup, verified commit/remote parity, no production deploy side effects; stable old entry point until release approved |

CI should use deterministic fixtures/mocks and no live personal data. Gated real-provider evaluation is separate from repeatable unit/browser tests and must report its exact model/source versions, costs and limits. Passing template tests alone cannot establish factual research quality.

## 8. Dependencies, limitations and decisions

1. **Blocking:** no verified GitHub repository/baseline SHA; selected repository access or confirmation none exists is still required.
2. **Blocking for full-spec sign-off:** supply the complete named UX architecture specification; only the message’s requirements are available for this revision.
3. **Before live research:** choose first jurisdiction, model/provider, official sources/search service, backend hosting, spend limits and credential owner. None of these runtime services exists in the prototype.
4. **Before a promise of returning users:** decide portable user-controlled files versus private saved cases. Account/storage/authentication, retention/deletion, consent, backup and access controls cannot be assumed.
5. **Before implementation:** owner approval of scope/branch and preservation verified. Before deployment: separate approval, HTTPS/access controls, privacy review and rollback. Existing backup approval is not permission for all these actions.
6. No new functional tests were run for this planning task. Read-only GitHub checks and original-file hash verification were performed; previous audit test results are historical, not newly claimed successes.

## Requested next input

Please provide the full **“User Experience Architecture — Internal Research, Externalized Game Plans”** text. Complete GitHub’s selected-repository access step and provide the existing repository URL, or confirm that no repository has been created. These inputs let us finalize requirements and complete the already-authorized baseline before seeking UX implementation approval.

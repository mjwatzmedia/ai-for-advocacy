Help me turn AI for Advocacy into a functioning, source-grounded AI application that collaborates with users to develop an editable Advocacy Game Plan.

I am MJ Watz, the founder and maintainer. I am building without a software engineering background. Make routine implementation decisions, explain meaningful tradeoffs plainly, and identify exactly what requires my input. Produce a prioritized implementation backlog, then begin the authorized reversible development work. Do not stop after writing another architecture proposal.

PROJECT AND SOURCE OF TRUTH

Repository:
https://github.com/mjwatzmedia/ai-for-advocacy

Existing draft pull request:
https://github.com/mjwatzmedia/ai-for-advocacy/pull/3

Branch containing that work:
codex/word-roadmap-ai-assistance

Read:
- README.md
- CONTRIBUTING.md
- GOVERNANCE.md
- SECURITY.md
- docs/ARCHITECTURE.md
- docs/product/master-development-specification.md
- docs/product/conversational-ux-plan.md
- public/index.html
- public/app.js
- public/style.css
- server.py
- Tests, dependency files, deployment instructions, and open pull requests.

Inspect the actual current revisions before relying on this description. Some product documents contain historical statements that repository access or backup is blocked. Verify current conditions and update stale statements.

KNOWN STARTING POINT

At the last check:

- main contained a browser-based, session-only planning prototype.
- Intake collected concern, desired outcome, and location.
- Roadmap suggestions used keyword matching and templates.
- Users could organize sources, notes, actions, and correspondence.
- Sources were manually entered and unverified.
- No official-source retrieval or verified civic reasoning pipeline existed.
- PR #3 added real browser-generated Word downloads, retained Markdown, added prompt copying for ChatGPT/Gemini, and added optional local OpenAI/Gemini API assistance.
- The PR’s AI endpoint was deliberately restricted to local installations. It is not a hosted research service.
- No live provider call or deployed AI integration had been verified.
- The repository was private and licensing remained undecided.

Verify these facts. Do not rebuild existing work unnecessarily. Inspect PR #3 for reuse; do not merge it without approval. If appropriate, base a new development branch on its head and clearly document that dependency.

PRODUCT EXPERIENCE

The user should be able to say something like:

“A mine is proposed near my neighborhood. I’m concerned about water impacts and want our community to participate in the decision.”

The application should:

1. Understand the concern and desired outcome.
2. Ask only necessary clarifying questions.
3. Establish the jurisdiction and relevant decision.
4. Research applicable official sources.
5. Explain who can act and what remains uncertain.
6. Help the user compare available approaches.
7. Collaboratively develop a practical advocacy campaign.
8. Produce an editable, downloadable Advocacy Game Plan.
9. Incorporate new information without destroying the user’s work.

The four underlying capabilities are:
- Identify who can act.
- Build a case.
- Explore options.
- Take the next step.

These should guide the internal workflow, rather than force the user through four mandatory forms.

FIRST DELIVERABLE: AN EXECUTABLE BACKLOG

Create docs/product/functional-ai-launch-plan.md and a concise summary.

For every task, include:
- Priority and dependency.
- Current state.
- Exact functionality to build.
- Existing files to reuse and proposed files to add.
- Acceptance criteria.
- Verification method.
- Required service, credential, or decision.
- Whether you can complete it in this environment.
- Status: not started, in progress, implemented, tested, or blocked.

Order work around a small functioning release. Avoid spending the entire effort on restructuring, governance, or infrastructure that the first release does not need.

Use the following work packages.

1. VERIFY THE WORKSPACE AND PRESERVE THE BASELINE

To do:
- Identify the repository’s current main SHA, open PRs, and deployed revision.
- Locate the actual running PromptQL application and service configuration.
- Establish whether this environment can pull, branch, commit, push, and open PRs.
- Determine whether GitHub changes automatically reach the running app or require publication.
- Run existing tests and record the baseline.
- Create an isolated development branch and recoverable snapshot.
- Preserve existing source editing, notes, actions, correspondence, reset, and downloads.

Done when:
There is a documented baseline, a working development environment, and a clear distinction between repository changes and deployed behavior.

2. VERIFY PROMPTQL’S ACTUAL CAPABILITIES

Determine whether PromptQL provides supported application-runtime capabilities for:
- Server-side model calls.
- Secret storage.
- Internet search.
- Fetching official webpages and PDFs.
- Background processing.
- Authentication and access control.
- Hosting a persistent application service.
- Downloading generated files.
- Operational logging and usage limits.

Distinguish tools available to you during development from tools that the deployed application can invoke for visitors.

Do not assume that because this conversation can research or call a model, the hosted app automatically can.

Use native capabilities where suitable and documented. Where unavailable, identify the smallest portable replacement and implement what you can.

Done when:
Each required capability has a verified implementation route or an explicit blocker and fallback.

3. DEFINE THE FIRST SUPPORTED PILOT

Propose a narrow Tucson/Pima County pilot, using fictional cases and a small verified collection of official sources.

Start with a bounded public-participation workflow, such as understanding a published proposal and preparing public comments. Avoid claiming to handle every agency, legal process, or jurisdiction.

To do:
- Define supported users, issues, jurisdictions, and outputs.
- Specify what the first release can research reliably.
- Identify unsupported scenarios and useful fallback responses.
- Define a single end-to-end demonstration.
- Identify the minimum official documents needed.

The mine example can remain the promotional scenario, but the app must acknowledge when relevant authority is state, federal, tribal, or outside the pilot’s supported coverage.

Done when:
A user can understand the pilot’s scope and limitations before relying on its output.

4. CONNECT A REAL MODEL PROVIDER

Reuse and improve the provider work in PR #3 where appropriate.

To do:
- Identify a supported model/provider available to the application runtime.
- Prefer one provider for the first release; retain a clean adapter boundary for alternatives.
- Check current official provider documentation before implementation.
- Keep credentials server-side in a supported secret store.
- Use configurable model identifiers.
- Add input/output limits, timeouts, cancellation, bounded retries, and clear errors.
- Track usage and enforce a small configurable budget.
- Validate structured outputs before changing application state.
- Preserve the manual planner when the provider is unavailable.

Explain exactly what credential or account configuration I must supply. Use a secure configuration flow, not chat or source files.

Do not expose the existing local endpoint publicly by merely removing its loopback checks. Build appropriate access controls and spending protections first.

Done when:
An authorized staging user can make a real model request, receive useful output, and recover safely from failure. Report live testing separately from simulated testing.

5. CREATE ONE STRUCTURED CASE MODEL

Consolidate information currently split between JavaScript state and DOM fields.

The versioned case model should include:
- User’s concern, goal, and preferences.
- Location and jurisdiction status.
- Clarified facts and user corrections.
- User reports and allegations.
- Research questions.
- Institutions and their supported responsibilities.
- Sources and extracted passages.
- Claims and supporting source references.
- Options and applicability.
- Selected approach.
- Actions, owners, completion, and date basis.
- Correspondence and response notes.
- Open questions.
- AI suggestions awaiting review.
- Revision information.

Separate user-authored content from generated suggestions. Avoid collecting names, addresses, or sensitive details unless needed.

Done when:
Existing data survives conversion and editing, research, export, and restoration use the same validated case representation.

6. BUILD CONVERSATIONAL INTAKE

To do:
- Add a conversation interface connected to the case model.
- Extract concern, outcome, jurisdiction, and material missing information.
- Ask one or two useful questions at a time.
- Allow “I don’t know.”
- Avoid repeating answered questions.
- Let users inspect and correct the assistant’s understanding.
- Identify distinct issues instead of forcing everything into one category.
- Clearly distinguish user statements from researched findings.
- Provide accessible loading, cancellation, retry, and error states.

Done when:
A user can describe a situation naturally and reach a useful initial plan without completing mandatory stage screens.

7. BUILD A CURATED OFFICIAL-SOURCE REGISTRY

Create a jurisdiction/source configuration rather than hardcoding local knowledge throughout the application.

For each registered source, record:
- Owning institution and jurisdiction.
- Official domain and allowed retrieval locations.
- Relevant topics and document types.
- Source URL.
- Publication or effective date when available.
- Last retrieval/check date.
- Known limitations and refresh policy.

Begin with a small, inspectable collection of official agency pages, meeting records, adopted policies, and public-participation guidance.

An official-looking domain, search result, or user-selected “official” label must not automatically establish authority or accuracy.

Done when:
The pilot’s sources are traceable, their institutional ownership is checked, and a contributor can add a source through documented validation.

8. IMPLEMENT ACTUAL SEARCH AND RETRIEVAL

Build the path from a user’s question to relevant original documents.

To do:
- Search the curated collection first.
- Add constrained official-domain search if a supported service is available.
- Retrieve actual content rather than relying on search snippets.
- Extract text from HTML and text-based PDFs.
- Preserve headings, page references, document dates, and source URLs.
- Detect scans that need OCR and report unsupported extraction.
- Handle redirects, inaccessible pages, changed URLs, and empty documents.
- Deduplicate documents and record document versions or content hashes.
- Start with simple search and ranking; add embeddings or a vector database only if evaluation demonstrates a need.
- Cache public documents separately from private case information.

Protect retrieval:
- Block localhost, private networks, cloud metadata endpoints, and unsupported URL schemes.
- Revalidate redirects and resolved destinations.
- Set size, time, document-count, and file-type limits.
- Treat retrieved text as untrusted evidence, never as instructions.
- Do not access private systems, bypass restrictions, or send personal case details in search queries unnecessarily.

Done when:
A fictional supported case retrieves relevant original passages with usable references. Retrieval failure produces an honest partial result.

9. BUILD CLAIM-LEVEL CITATIONS AND CHECKS

For each consequential finding, keep:
- The claim.
- Source and document version.
- Supporting passage.
- Page, section, or heading when available.
- Applicable jurisdiction.
- Check date.
- Any conflict or limitation.

Distinguish:
- User-reported information.
- Retrieved official text.
- A claim supported by a specific passage.
- AI interpretation.
- A research lead.
- An unresolved question.

Checking that a URL exists is not citation verification. An official source does not automatically support every claim made about it.

Done when:
Users can open the source and see why it supports the associated finding. Unsupported findings remain visibly unverified.

10. ADD CIVIC LOGIC AND BOUNDED ORCHESTRATION

Use one understandable orchestrator initially. Separate responsibilities into testable functions; multiple autonomous agents are not required.

Workflow:
- Understand the case and missing information.
- Resolve supported jurisdiction.
- Generate targeted research questions.
- Retrieve relevant official material.
- Extract evidence-linked findings.
- Evaluate institutional authority and applicable options.
- Identify contradictions or gaps.
- Ask the user about material choices.
- Propose a Game Plan.
- Validate it before presentation.

Use deterministic checks for source IDs, jurisdiction compatibility, dates, required fields, and document status where possible.

Distinguish:
- Decision-maker versus adviser.
- Adopted rule versus proposal.
- Public comment versus complaint, appeal, or records request.
- General guidance versus case-specific applicability.
- Personal target date versus official deadline.

Do not invent deadlines or calculate legal deadlines from ambiguous rules. Show source-backed dates with their basis and flag uncertainty.

Set limits on research iterations, model calls, elapsed time, and spending. Return partial findings when limits are reached.

Done when:
The system produces a useful supported plan or explains precisely what prevents completion.

11. MAKE PLANNING COLLABORATIVE

The app should help users make choices rather than select their political position.

To do:
- Present plausible approaches with evidence, effort, limitations, and dependencies.
- Ask about the user’s priorities, available time, resources, and preferred participation.
- Offer manageable actions and an option to stop or change direction.
- Identify supporters or partner categories without inventing endorsements.
- Distinguish campaign strategy suggestions from official procedural requirements.
- Explain recommendations briefly through evidence and assumptions, without exposing private model reasoning traces.

Done when:
Two users with the same issue can select different lawful approaches and receive plans reflecting their choices.

12. BUILD THE EDITABLE ADVOCACY GAME PLAN

Include:
- Desired outcome and scope.
- Current understanding of the situation.
- Relevant institutions and supported responsibilities.
- Evidence summary and source references.
- Unknowns and conflicting information.
- Options considered and chosen approach.
- A concrete first action.
- A short action sequence.
- Official dates and personal targets, clearly distinguished.
- Draft correspondence or public comment.
- Progress, responses, and next questions.

New research should propose changes. Let the user accept or reject substantive updates. Preserve their writing and completed actions.

A changed jurisdiction or goal should mark affected conclusions for review rather than silently carrying them forward as verified.

Done when:
The plan is specific to the user’s answers and retrieved evidence, remains editable, and survives subsequent updates.

13. FINISH DOWNLOAD AND RETURN SUPPORT

Reuse the Word export in PR #3.

To do:
- Export the actual current Game Plan to a real editable .docx.
- Include full source URLs, supporting references, uncertainty, actions, notes, and correspondence.
- Retain Markdown.
- Offer a print-friendly view if practical.
- Add versioned JSON export/import for user-controlled return sessions.
- Validate imported schema, size, version, and content.
- Preserve every supported field in a round trip.
- Clearly explain that Word and Markdown are readable exports, not necessarily lossless backups.

Keep session-only operation as the default. Do not silently introduce accounts, browser persistence, or server case storage. If saved accounts become necessary, propose retention, deletion, authorization, and backup behavior before implementing them.

Done when:
A user can download a useful document, close the app, and restore their work through the supported case-file mechanism.

14. MAKE STAGING AND HOSTING FUNCTIONAL

To do:
- Prepare a private staging environment.
- Configure secrets and authorized-user access.
- Use HTTPS and appropriate request/session protections.
- Add per-user rate limits, global concurrency limits, and cost controls.
- Keep operational logs free of raw case content.
- Add health checks and actionable error monitoring.
- Update privacy language to match actual provider transfers and storage.
- Identify which parts depend on PromptQL and document independent startup.
- Test the complete workflow through the hosted browser interface.
- Document deployment and rollback commands.

Done when:
An authorized tester can use the hosted app without needing localhost, developer tools, or manual server intervention.

Prepare staging configuration and deployment instructions now. Ask before exposing a service, activating paid usage, or replacing the live application.

15. TEST RESEARCH QUALITY AND USER CONTROL

Retain existing tests and add:

- Missing or corrected jurisdiction.
- User changes their goal.
- Unsupported location or process.
- Relevant official source found.
- No source found.
- Outdated, proposed, superseded, or conflicting documents.
- Search snippets that do not support a conclusion.
- PDF extraction failure.
- Source contains hostile instructions.
- Fabricated model source IDs or unsupported citations.
- Model timeout, quota failure, invalid JSON, and cancelled requests.
- No loss of edits or completed actions.
- Export completeness and case-file restoration.
- Clear-workspace behavior and cross-user isolation where applicable.
- Keyboard, screen-reader, and mobile behavior.
- No communication sent without a separate explicit user action.

Use deterministic fixtures for CI. Conduct a separate, budgeted live evaluation with current official documents and record model, prompt, source versions, date, outcome, and cost.

Treat any invented official deadline, contact, authority, or citation as a release-blocking failure in pilot evaluation. Do not invent an overall “accuracy score” without a defined dataset and rubric.

IMPLEMENTATION ORDER

Milestone 1 — Useful without live research:
Reuse existing work, finish Word export, establish the case model, add lossless case-file export/import, and preserve baseline behavior.

Milestone 2 — Real evidence-grounded vertical slice:
One model provider, one supported jurisdiction/process, a small official-source collection, actual retrieval, claim-linked citations, conversational clarifications, and an editable Game Plan.

Milestone 3 — Hosted invited testing:
Authenticated staging, configured credentials, usage limits, full browser workflow, live evaluation, and rollback.

Milestone 4 — Broader coverage:
Additional source types, jurisdictions, research capabilities, and collaboration features based on observed needs.

Do not attempt every milestone simultaneously. Complete a small end-to-end path before expanding.

WHAT I AUTHORIZE NOW

- Repository and environment inspection.
- Updating stale documentation.
- Creating a dedicated development branch.
- Reversible implementation and tests in an isolated environment.
- Staging preparation.
- Commits, branch pushes, and reviewable pull requests.

Do not merge, publish the repository, choose a final license, activate paid services, change collaborator permissions, retain real sensitive cases, or deploy over the live application without my approval.

If credentials or a product decision block one task, continue independent work and bundle the blockers into a short list. Make conservative recommendations instead of asking me to resolve ordinary engineering details.

FIRST RESPONSE AND ONGOING REPORTING

First:
1. State what exists in the current repository and deployment.
2. Identify the shortest path to a genuinely functioning pilot.
3. Show the prioritized checklist with acceptance criteria.
4. Explain what PromptQL can supply natively and what must be built.
5. Identify the minimum decisions or credentials needed from me.
6. Begin the first unblocked implementation task.

After each increment, report:
- What now works.
- Changed files.
- Tests actually run and results.
- Branch, commit, and PR.
- What remains.
- Any cost, credential, hosting, or approval blocker.

Do not call the product functional solely because it can produce fluent text. The first functional AI release must retrieve relevant official material, connect consequential findings to evidence, collaborate with the user, preserve their edits, and export a useful Advocacy Game Plan.
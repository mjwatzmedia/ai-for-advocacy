# AI for Advocacy — Master Development, GitHub, Collaboration, and Open-Source Infrastructure Specification

## Project mission

You are helping develop **AI for Advocacy**, an independent civic technology initiative founded and led by MJ Watz.

AI for Advocacy is an AI-assisted platform intended to make civic participation, institutional accountability, and government processes more accessible.

The application helps people:

1. **Identify who can act:** Locate relevant government institutions, officials, oversight bodies, and decision-makers.
2. **Build a case:** Organize evidence, distinguish verified information from assumptions, identify missing information, and preserve source references.
3. **Explore options:** Understand available civic participation, reporting, information-request, and accountability pathways.
4. **Take the next step:** Develop action plans, track follow-through, and prepare correspondence for human review.

The long-term goal is a **reproducible, extensible, open-source civic technology framework** that individuals and organizations can adapt to their own cities, states, countries, and institutions.

The intended development model resembles Mozilla: a maintained core project, transparent technical standards, community contributions, and independently adaptable implementations.

### Founding principles

- MJ Watz remains the founding project lead and primary maintainer of the official AI for Advocacy project.
- GitHub is the authoritative source of application code, documentation, configuration, and development history.
- PromptQL is a development environment, not the sole repository of essential product knowledge.
- The application must eventually operate independently of PromptQL.
- Contributors may help develop the project without receiving unrestricted administrative control over the official repository.
- Regional adaptations should be possible without rewriting the entire application.
- Every material architectural decision must be documented.
- Existing functionality must be preserved unless changes are explicitly approved.
- The repository remains private until public release is authorized.
- Do not select a final open-source license, publish the repository, invite collaborators, or deploy new infrastructure without authorization.

**Primary objective:** Preserve the complete existing application in a private GitHub repository under my ownership, establish a safe collaborative development workflow, and make every component of the product reproducible from documented source code and external dependencies.

---

# Phase 1 — Complete Technical Audit

Before changing the application, inspect the current project and produce a comprehensive technical inventory.

## 1.1 Application source code

Identify and document:

- All frontend source code.
- All backend source code.
- Application routing and navigation.
- UI components and design systems.
- State management.
- Forms, validation, and user interactions.
- Application workflows and orchestration.
- Server-side functions.
- Background jobs and scheduled processes.
- Build scripts and generated artifacts.
- Third-party components and libraries.

Record programming languages, frameworks, package managers, exact dependency versions, and runtime requirements.

## 1.2 AI model infrastructure

Identify:

- Current AI providers.
- Exact model identifiers and versions.
- API endpoints.
- Model parameters, including temperature, token limits, and relevant generation settings.
- System prompts, developer instructions, workflow prompts, and templates.
- Prompt construction and context assembly.
- Structured output schemas.
- Model invocation and orchestration logic.
- Tool-calling mechanisms.
- Error handling, retries, rate limits, and timeouts.
- Model usage and cost tracking.
- Model fallback behavior.
- Whether model providers can be substituted.

Document whether the application uses a single model, multiple models, or platform-managed AI functionality.

Do not assume an AI architecture exists unless it can be verified.

## 1.3 Retrieval and information infrastructure

Identify:

- All government and institutional information sources.
- Search APIs and providers.
- Web retrieval methods.
- Document ingestion processes.
- File parsing and text extraction.
- Indexing methods.
- Vector databases or embedding services, if any.
- Embedding model identifiers and versions.
- Keyword, semantic, or hybrid retrieval.
- Chunking strategies.
- Retrieval ranking and reranking.
- Metadata filtering.
- Citation generation.
- Source provenance tracking.
- Source refresh schedules.
- Handling of inaccessible, outdated, or conflicting documents.

Explain the complete information flow from a user's question to the sources used in the generated answer.

## 1.4 Civic decision logic

Identify:

- Existing rules and conditional workflows.
- Government authority mapping.
- Jurisdiction identification.
- Institutional responsibility mapping.
- Procedural guidance.
- Eligibility and deadline logic.
- Escalation and referral pathways.
- Evidence validation.
- Distinctions between deterministic logic and AI-generated interpretation.

Identify which civic decisions are currently implemented, simulated, hardcoded, or absent.

## 1.5 Data and storage

Document:

- Database providers.
- Database schemas and tables.
- Data relationships.
- Migrations.
- User records and sessions.
- Evidence workspace storage.
- Action tracker storage.
- Source registries.
- Document storage.
- Retention and deletion behavior.
- Backups and recovery procedures.
- Any third-party storage services.

## 1.6 Security and privacy

Identify:

- Authentication and authorization.
- User roles and permissions.
- API credential management.
- Secret storage.
- Session security.
- Data encryption.
- Access controls.
- Logging and monitoring.
- Personal information handling.
- Confidential case material handling.
- Data retention.
- Third-party data transmission.
- Potential prompt-injection and retrieval security risks.

## 1.7 Hosting and external dependencies

Document:

- Current hosting provider.
- Build and deployment procedures.
- Domain and DNS configuration.
- Environment variables.
- External APIs.
- Platform-managed services.
- Infrastructure dependencies.
- Usage limits and paid-service requirements.
- Monitoring and incident recovery.

## 1.8 Audit classifications

For every identified component, report:

- Component name.
- Purpose.
- Current implementation.
- Source file or configuration location.
- Dependencies.
- Reproducibility status.
- Security considerations.
- Missing documentation.
- Recommended next action.

Classify each component as:

**IMPLEMENTED / PARTIALLY IMPLEMENTED / SIMULATED / PLANNED / UNKNOWN**

Do not invent missing functionality or describe proposed components as already implemented.

---

# Phase 2 — GitHub Repository and Backup

## 2.1 Repository creation

Check whether a GitHub repository already exists for AI for Advocacy.

Report:

1. Repository URL.
2. Repository owner.
3. Visibility.
4. Default branch.
5. Current commit.
6. Existing collaborators.
7. Repository permissions.
8. Branch protection settings.
9. Existing GitHub Actions.
10. Existing deployment integrations.

If no repository exists, prepare to create a private repository named:

`ai-for-advocacy`

The repository must be owned by my personal GitHub account unless I explicitly authorize another ownership arrangement.

Request authorization before creating the repository or changing permissions.

Do not create duplicate repositories.

## 2.2 Preserve the existing prototype

Before restructuring the application:

- Create a recoverable snapshot of the existing project.
- Export all accessible source code.
- Preserve current application behavior.
- Record the current deployment configuration.
- Preserve prompts and application instructions.
- Record external service dependencies.
- Document anything that cannot be exported.
- Establish a baseline commit and identifiable backup version.

Do not delete, overwrite, or replace the current working prototype.

## 2.3 Security before committing

Scan the project for:

- API keys.
- Access tokens.
- Passwords.
- Private credentials.
- Personally identifiable information.
- Confidential user data.
- Private case records.
- Unnecessary generated files.
- Sensitive logs.

Do not commit secrets or sensitive records.

Create:

- `.gitignore`
- `.env.example`
- Secret management documentation.
- Instructions for configuring credentials locally and in deployment environments.

If secrets have already been committed, report the exposure and recommend credential rotation and appropriate history remediation.

## 2.4 Verify the backup

Confirm that the repository contains the actual application source, not merely screenshots, generated summaries, or deployment links.

Provide the exact commit identifier and an inventory of exported files.

Do not claim a successful backup unless the repository contents have been verified.

---

# Phase 3 — Complete Reproducibility

The application must eventually be reconstructable by an independent developer without relying on undocumented PromptQL state or this conversation.

## 3.1 Required repository structure

Adapt the structure to the actual technology stack, but aim for the following organization:

```text
ai-for-advocacy/
├── src/
│   ├── frontend/
│   ├── backend/
│   ├── ai/
│   │   ├── providers/
│   │   ├── prompts/
│   │   ├── schemas/
│   │   └── orchestration/
│   ├── retrieval/
│   │   ├── ingestion/
│   │   ├── indexing/
│   │   ├── search/
│   │   └── citations/
│   ├── civic/
│   │   ├── jurisdictions/
│   │   ├── authorities/
│   │   └── workflows/
│   └── safety/
├── jurisdictions/
│   └── examples/
├── database/
│   ├── schemas/
│   └── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── evaluation/
│   └── security/
├── docs/
│   ├── architecture/
│   ├── product/
│   ├── integrations/
│   ├── jurisdictions/
│   └── operations/
├── scripts/
├── .github/
│   ├── workflows/
│   └── ISSUE_TEMPLATE/
├── .env.example
├── .gitignore
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── GOVERNANCE.md
├── CHANGELOG.md
└── LICENSE
```

Do not create empty or misleading implementation files merely to make the structure appear complete.

## 3.2 Reproducible configuration

Document:

- Required operating systems and runtimes.
- Exact dependency versions and lockfiles.
- Installation commands.
- Local startup commands.
- Environment variables.
- Database setup.
- API integration.
- AI provider setup.
- Retrieval service setup.
- Source ingestion.
- Testing.
- Production build.
- Deployment.
- Backup and restoration.

Where practical, provide containerized development infrastructure or equivalent reproducible setup.

## 3.3 AI configuration portability

Design the AI layer so that providers and models can eventually be changed through configuration.

Document:

- Provider adapters.
- Model identifiers.
- API authentication.
- Input and output formats.
- Prompt versions.
- Context limits.
- Cost considerations.
- Failure behavior.
- Compatibility requirements.

Do not silently change the model or provider currently used.

## 3.4 PromptQL independence

Identify which parts of the current application rely on proprietary or platform-managed PromptQL functionality.

For each dependency, document:

- What it does.
- Whether its source is exportable.
- Whether an independent replacement is needed.
- How difficult migration would be.
- Whether equivalent behavior can be tested outside PromptQL.

Provide a portability plan.

**Long-term requirement:** A developer must be able to clone the repository, configure supported services, and run the application without needing access to the original PromptQL workspace.

---

# Phase 4 — Modular AI Architecture

Separate the application into independently understandable components.

## 4.1 Core application

Responsible for:

- User interface.
- Guided advocacy workflow.
- Evidence organization.
- Action tracking.
- Correspondence drafting.
- User settings.
- Application state.

## 4.2 AI model layer

Responsible for:

- Model provider integration.
- Prompt management.
- Context assembly.
- Structured responses.
- Model routing.
- Output validation.
- Error handling.

## 4.3 Retrieval layer

Responsible for:

- Finding official information.
- Ingesting documents.
- Indexing content.
- Searching sources.
- Ranking evidence.
- Producing verifiable citations.
- Tracking source freshness.

## 4.4 Civic logic layer

Responsible for:

- Identifying jurisdictions.
- Mapping institutional authority.
- Distinguishing government responsibilities.
- Validating procedural requirements.
- Organizing possible advocacy pathways.
- Identifying unresolved questions.

Use deterministic rules where authoritative information can be formally represented and verified.

Do not allow AI-generated assumptions to become authoritative procedural rules.

## 4.5 Safety and verification layer

Responsible for:

- Unsupported-claim detection.
- Citation validation.
- Uncertainty handling.
- Source provenance.
- Privacy safeguards.
- Prompt-injection resistance.
- Human approval before consequential actions.

## 4.6 Architecture documentation

Create diagrams and technical documentation showing:

- System components.
- Data flow.
- Model calls.
- API connections.
- Retrieval processes.
- Storage.
- Security boundaries.
- Deployment infrastructure.

Record significant architecture decisions in version-controlled decision records.

---

# Phase 5 — Jurisdiction Adaptation Framework

AI for Advocacy must be adaptable to different geographic and institutional environments.

The core application should not assume that every jurisdiction has the same government structure.

## 5.1 Jurisdiction packs

Develop a configurable jurisdiction system describing:

- Jurisdiction name.
- Geographic scope.
- Government structure.
- Institutions and agencies.
- Official websites.
- Decision-makers and offices.
- Oversight bodies.
- Public participation processes.
- Information request procedures.
- Complaint and reporting pathways.
- Relevant laws and regulations.
- Official forms and procedural requirements.
- Source update schedules.
- Local terminology.
- Language and accessibility requirements.

## 5.2 Separation of code and local knowledge

Keep reusable application logic separate from jurisdiction-specific data.

Do not hardcode Tucson, Arizona, or United States procedures into the core framework.

## 5.3 Example jurisdiction

Prepare a documented example jurisdiction configuration using a limited, verified set of official sources.

The initial example may focus on Tucson and Pima County, Arizona, but the architecture must support additional regions.

Do not populate example configurations with unverified agency responsibilities or invented procedures.

## 5.4 Regional adaptation documentation

Provide instructions for another developer to:

1. Create a new jurisdiction pack.
2. Register official government sources.
3. Configure institutional relationships.
4. Define verified procedural rules.
5. Configure retrieval and source updates.
6. Test the jurisdiction pack.
7. Deploy a regional instance.
8. Maintain and update local information.

---

# Phase 6 — Civic AI Reliability and Safety

The application must be designed for responsible use in potentially consequential civic and institutional matters.

## 6.1 Required behavior

The system should:

- Ground factual claims in identifiable sources.
- Provide links to original documents when available.
- Distinguish verified facts from interpretations.
- Clearly identify uncertainty.
- Avoid inventing officials, agencies, laws, deadlines, or procedures.
- Recognize conflicting information.
- Identify outdated sources.
- Avoid presenting speculative advice as an official requirement.
- Preserve user agency.
- Require human review before external correspondence or action.

## 6.2 Evidence integrity

Maintain distinctions between:

- User-provided allegations.
- Independently verified facts.
- Documentary evidence.
- Inferences.
- Unresolved questions.
- Suggested actions.

Do not automatically transform allegations into established facts.

## 6.3 Privacy

Support privacy-conscious development, including:

- Data minimization.
- Session-based workflows where appropriate.
- Secure handling of evidence.
- Explicit retention rules.
- User-controlled exports.
- Secure deletion procedures.
- Separation of public government sources from private user materials.

## 6.4 Automated evaluation

Develop test cases covering:

- Fabricated agencies.
- Invented laws.
- Incorrect deadlines.
- Unsupported citations.
- Conflicting sources.
- Outdated government information.
- Incorrect jurisdiction selection.
- Sensitive personal information.
- Prompt injection in retrieved documents.
- Missing or unavailable official sources.

Document test results and known limitations.

---

# Phase 7 — GitHub Collaboration Infrastructure

GitHub must serve as the authoritative record of development.

PromptQL may remain a primary development interface, but collaborators should not be required to use it if they can work safely through GitHub-compatible tools.

## 7.1 Verify PromptQL synchronization

Determine whether PromptQL supports:

- Exporting complete source code.
- Connecting to a private GitHub repository.
- Creating real Git commits.
- Pulling remote changes.
- Pushing local changes.
- Creating branches.
- Opening pull requests.
- Resolving merge conflicts.
- Multiple collaborators.
- Separate development environments.
- Role-based access controls.

Distinguish native functionality from functionality requiring external tools.

If synchronization is only one-way, explain the limitations and propose a safe alternative workflow.

Do not assume bidirectional synchronization exists.

## 7.2 Development workflow

For every development task:

1. Confirm the current repository state.
2. Pull the latest changes.
3. Create a dedicated development branch.
4. Implement the requested feature or fix.
5. Update documentation.
6. Add or update tests.
7. Run automated checks.
8. Commit changes.
9. Push the branch.
10. Open a pull request.
11. Summarize the changes and test results.
12. Request review.
13. Merge into `main` only after approval.

Do not directly overwrite the main branch with experimental work.

## 7.3 Branch protection

Configure, subject to my authorization:

- Protected default branch.
- Required pull requests.
- Required automated checks.
- Restrictions on force pushes.
- Restrictions on branch deletion.
- Appropriate review requirements.
- Limited administrative access.

Do not grant collaborators repository ownership or administrative permissions by default.

## 7.4 GitHub Actions

Create appropriate continuous integration workflows for:

- Dependency installation.
- Linting.
- Type checking.
- Unit tests.
- Integration tests.
- Security checks.
- Build verification.
- Civic AI evaluation tests where feasible.

Report failures rather than bypassing checks.

## 7.5 Deployment

Prepare a deployment workflow in which approved changes merged into `main` can trigger automated deployment.

Do not activate automatic production deployment until the hosting environment has been verified and I authorize it.

Prefer a staging environment for testing changes before public release.

## 7.6 Recovery

Document how to:

- Restore an earlier commit.
- Revert a problematic pull request.
- Recover from failed deployment.
- Restore databases from backups.
- Rebuild the application from the repository.
- Continue development if PromptQL becomes unavailable.

---

# Phase 8 — Collaborator Onboarding and Permissions

I expect to meet new technical and nontechnical collaborators and want to support meaningful contributions while maintaining clear project leadership and security.

## 8.1 Founder and maintainer role

MJ Watz is the founding project lead and primary maintainer of the official AI for Advocacy project.

The official repository should remain under my administrative control.

Contributors should receive only the permissions necessary for their work.

## 8.2 Technical collaborators

Technical collaborators may contribute through:

- GitHub branches.
- Pull requests.
- Local development environments.
- VS Code or equivalent tools.
- PromptQL, where safe collaboration is supported.
- Issue assignments.
- Architecture proposals.
- Code reviews.

Avoid multiple contributors editing the same unversioned live application state.

## 8.3 Nontechnical collaborators

Nontechnical collaborators may contribute through:

- Prototype testing.
- User experience research.
- Civic process research.
- Source verification.
- Accessibility reviews.
- Jurisdiction configuration.
- Documentation.
- Product feedback.

Provide appropriate access without exposing unnecessary source code, credentials, or private user data.

## 8.4 Contributor permissions

Define access levels for:

- Project founder/administrator.
- Trusted maintainers.
- Technical contributors.
- Documentation contributors.
- Researchers and testers.
- External reviewers.

Recommend the minimum required permissions for each role.

## 8.5 Contribution workflow

Use GitHub Issues to organize work.

Provide issue templates for:

- Feature requests.
- Bugs.
- Documentation.
- Jurisdiction additions.
- Source corrections.
- Security concerns.
- Architecture proposals.

Create contributor onboarding instructions explaining:

- How to obtain access.
- How to run the application.
- How to choose an issue.
- How to create a branch.
- How to submit a pull request.
- How reviews work.
- How contributions are credited.
- How licensing and intellectual property are handled.

Do not invite collaborators or modify permissions without my authorization.

---

# Phase 9 — Open-Source Licensing and Governance

The repository must remain private during initial development.

Prepare the project for an eventual public release.

## 9.1 Required documentation

Create or prepare:

- `README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `GOVERNANCE.md`
- `CHANGELOG.md`
- `LICENSE`
- Architecture documentation.
- Deployment documentation.
- API integration documentation.
- Jurisdiction adaptation guide.
- Contributor onboarding guide.
- Project roadmap.

Do not select or activate a final license without my approval.

## 9.2 Licensing analysis

Compare established open-source licenses, including:

- Mozilla Public License 2.0.
- Apache License 2.0.
- MIT License.

Explain:

- Rights to copy and modify.
- Rights to distribute.
- Commercial use.
- Patent provisions.
- Requirements for publishing modified source.
- Attribution requirements.
- Compatibility considerations.
- Implications for regional adaptations.

Do not invent a custom open-source license without discussing the consequences.

## 9.3 Contributor intellectual property

Recommend a contribution policy that:

- Respects contributors' ownership of their original work.
- Gives the project sufficient permission to maintain and distribute accepted contributions.
- Clarifies the license under which contributions are submitted.
- Addresses third-party code and dependencies.
- Prevents unauthorized incorporation of proprietary or confidential material.
- Explains attribution and contribution history.

Evaluate whether a Developer Certificate of Origin, contributor license agreement, or another established approach is appropriate.

Do not assume contributors automatically transfer ownership to the founder.

## 9.4 Project governance

Document:

- Founder and maintainer responsibilities.
- Contribution review procedures.
- Release approval.
- Security decision-making.
- Project roadmap management.
- Dispute resolution.
- Maintainer appointments.
- Governance changes.
- Community participation.

The goal is to preserve coherent stewardship of the official project while enabling legitimate open-source development and independent regional adaptations.

## 9.5 Project identity

Recommend ways to distinguish the official AI for Advocacy project from independent forks or regional implementations.

Consider naming, attribution, branding, and trademark questions separately from software copyright and licensing.

Do not claim trademark protection has been established unless verified.

---

# Phase 10 — Collaboration Readiness Audit

Before inviting collaborators, verify the following.

1. **Private repository:** Does the repository exist under my GitHub ownership, with the actual source code committed?
2. **Complete export:** Are frontend, backend, prompts, retrieval components, configuration, and dependencies included?
3. **Bidirectional synchronization:** Can PromptQL pull and push GitHub changes without overwriting collaborators' work?
4. **Isolated development:** Can contributors work on separate branches or development environments?
5. **Protected main branch:** Are pull request review and appropriate protections enabled?
6. **Automated testing:** Are GitHub Actions configured and passing?
7. **Secrets management:** Are credentials securely managed outside version control?
8. **Independent setup:** Can another developer clone and run the application?
9. **Recovery:** Can the project be restored from GitHub without PromptQL?
10. **Access control:** Can contributors receive restricted permissions while I retain administration?
11. **Paid requirements:** Which capabilities require paid plans or additional services?
12. **Deployment safety:** Can proposed changes be tested without affecting the live prototype?
13. **Contribution policy:** Are collaboration expectations and intellectual property terms documented?
14. **Documentation:** Can a new contributor understand the architecture and setup without relying on private conversations?

For each item, report:

**VERIFIED / NOT CONFIGURED / UNKNOWN**

Provide supporting evidence, relevant links, configuration references, and recommended remediation.

Do not report a capability as verified based solely on assumptions.

---

# Phase 11 — Development Task Reporting

For every future development task, provide a concise technical report.

Include:

**Task:** What was requested.

**Files changed:** Which source files or configurations were modified.

**Architecture impact:** Whether the change affects AI models, retrieval, civic logic, databases, APIs, security, or deployment.

**Tests:** Which tests were run and their results.

**GitHub:** Branch name, commit identifier, and pull request URL when available.

**Documentation:** What was updated.

**Dependencies:** Any new services, credentials, costs, or configuration requirements.

**Limitations:** Anything incomplete, unverified, or dependent on PromptQL.

**Next action:** What needs review or approval.

Do not claim that code was tested, synchronized, deployed, or independently reproduced unless those operations actually succeeded.

---

# Required Initial Deliverables

Begin with an audit, not a redesign.

Produce the following:

## Deliverable A — Technical Inventory

A complete inventory of the existing application, including source code, AI models, prompts, retrieval, civic logic, data, APIs, hosting, and security.

## Deliverable B — GitHub Status Report

Identify the current repository, owner, visibility, default branch, commit history, synchronization capabilities, and missing configuration.

## Deliverable C — Reproducibility Gap Analysis

Explain precisely what prevents an independent developer from reconstructing the application.

Distinguish missing source code, undocumented configuration, unavailable credentials, proprietary dependencies, and unimplemented features.

## Deliverable D — Proposed Repository Architecture

Recommend a repository structure appropriate to the existing technology stack and long-term modular design.

## Deliverable E — Collaboration Readiness Report

Evaluate whether technical and nontechnical collaborators can safely begin contributing.

Identify required permission controls, branch protections, testing, and synchronization capabilities.

## Deliverable F — Prioritized Implementation Roadmap

Organize the remaining work into manageable milestones:

1. Audit and preservation.
2. Private GitHub repository and verified backup.
3. Independent reproducibility.
4. Safe collaboration infrastructure.
5. Modular AI and retrieval architecture.
6. Jurisdiction adaptation.
7. Civic reliability and security testing.
8. Open-source licensing and governance.
9. Public release preparation.

For each milestone, identify dependencies, risks, acceptance criteria, and any decisions requiring my approval.

## Deliverable G — Verified Export Report

Confirm what has actually been exported and committed to GitHub.

Include the repository URL, commit identifier, exported components, and any missing materials.

---

# Operating Rules and Approval Boundaries

**You may immediately:**

- Inspect the existing project.
- Audit the application.
- Analyze current GitHub integration.
- Identify dependencies.
- Prepare documentation and implementation proposals.
- Recommend repository structure.
- Run safe, read-only checks.
- Identify missing functionality and risks.

**Request my approval before:**

- Creating or changing repository ownership.
- Changing repository permissions.
- Inviting collaborators.
- Publishing code or making the repository public.
- Changing AI providers or models.
- Replacing major architectural components.
- Modifying production databases.
- Activating deployment automation.
- Incurring paid service costs.
- Choosing a final open-source license.
- Making destructive or irreversible changes.

Do not request approval repeatedly for ordinary read-only auditing or documentation.

If an operation is unsupported, inaccessible, or requires authorization, report that clearly and propose the next action.

Do not pretend to have completed an operation that was not performed.

---

# Final Success Criteria

The infrastructure is successful when:

1. The full application is preserved in a private GitHub repository under my control.
2. An independent developer can reconstruct and run the application from documented source code and external dependencies.
3. Every AI model, prompt, retrieval process, API integration, and civic decision component is accounted for.
4. The application can eventually run without PromptQL.
5. Contributors can work independently without overwriting one another's changes.
6. Changes are reviewed, tested, and recorded through GitHub.
7. Secrets and private user data remain protected.
8. Jurisdiction-specific configurations can be developed independently of the core application.
9. The project has a documented path toward responsible open-source licensing and community governance.
10. I retain administrative control and stewardship of the official AI for Advocacy project while contributors can meaningfully participate.

**Begin now with Phase 1 and the read-only portions of Phase 10. Establish the current technical and GitHub state, identify gaps, and present the audit results before making structural changes. Preserve the existing prototype and request authorization before creating the repository or performing the first backup commit. Do not attempt all phases simultaneously.**
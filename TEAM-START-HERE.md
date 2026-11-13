# NEW TEAM MEMBERS — START HERE

**Active project: Advocacy Assistant research foundation.**
**Start from `main`.** PR #5 was merged by MJ Watz on November 12, 2026
(America/Los_Angeles), preserving the backend and interface work here.

This is a development prototype, not a complete AI product or production service.

## 1. Understand the goal

Help a person describe a concern, understand who can act on it and which rules
govern it, then build an evidence-informed campaign to make their voice heard.

**Works:** concern intake, editable workspace, bounded public-page retrieval,
structured research proposals with review-before-apply, campaign draft templates,
Word/Markdown/JSON export and JSON restore.

**Still needs work:** reliable issue-specific institutions/individuals and law
applicability, plain-language authority explanations, clarification chat and live
AI acceptance testing. AI is disabled by default. Suggestions are not legal advice
or proof that a particular comment period, petition or deadline exists.

[Detailed developer handoff and architecture map](docs/fullstack/DEVELOPER-HANDOFF.md)
· [Contribution rules](CONTRIBUTING.md)
· [Security](SECURITY.md)
· [License status](LICENSE-STATUS.md)

## 2. Run it locally

Install Git, Python 3.11+ and [uv](https://docs.astral.sh/uv/).
From a terminal:

```sh
git clone --branch main https://github.com/mjwatzmedia/ai-for-advocacy.git
cd ai-for-advocacy/backend
uv sync --locked
uv run uvicorn advocacy.api:app --host 127.0.0.1 --port 8080 --no-access-log
```

Open **http://127.0.0.1:8080**. Stop with Ctrl+C.
The FastAPI command above serves the existing interface and research API.
`python3 server.py` is the older standalone planner, not the research backend.

No AWS, PromptQL account, Gmail, ChatGPT subscription or model key is needed for
baseline testing. Use fictional concerns, explicitly consent to source retrieval,
review proposals before adding them, and download JSON before closing/refreshing.
No campaign is sent, petition signed or official called by the application.

## 3. Find your first task

Agree on one small issue with MJ before substantial coding. Suggested starting
tasks (not already assigned):

- Add a fictional authority-mapping test case for one jurisdiction.
- Improve how the interface explains candidate versus confirmed authority.
- Extend an official-source registry with documented jurisdiction limits.
- Wire the existing foundation test suite into CI.

Do not invent a decision-maker, law, phone number or deadline. New findings need
official sources and clear unknowns. Keep regional facts separate from reusable
logic. See the handoff for the larger authority/explanation milestone.

## 4. Make a contribution — never edit `main` directly

### If you have write access

From the repository root, with a clean working tree:

```sh
git switch main
git pull --ff-only origin main
git switch -c feat/short-task-name
# Make a small change. Add tests and update relevant documentation.
git add path/to/changed-file path/to/changed-test
git commit -m "Explain the change"
git push -u origin feat/short-task-name
```

On GitHub, select **Compare & pull request**. Set **base: main** and
**compare: your feature branch**. Explain the change, actual test results,
limitations and any privacy/security/cost impact. Request MJ's review.

### If you do not have write access

1. Discuss contribution and licensing terms with MJ first.
2. Use GitHub's **Fork** button, then clone your fork:
   ```sh
   git clone https://github.com/YOUR-GITHUB-USERNAME/ai-for-advocacy.git
   cd ai-for-advocacy
   git remote add upstream https://github.com/mjwatzmedia/ai-for-advocacy.git
   git fetch upstream
   git switch -c feat/short-task-name upstream/main
   # Make and test your change.
   git add path/to/changed-file
   git commit -m "Explain the change"
   git push -u origin feat/short-task-name
   ```
3. Open a PR to **mjwatzmedia/ai-for-advocacy**, base **main**, from your fork branch.

Push small checkpoints as you go, but never commit credentials or real case data.
Avoid broad `git add .` until you have inspected all files being included.
Do not force-push shared branches. A passing test does not authorize merge,
deployment, new paid services or permission changes.

## 5. Test before requesting review

Install Node 22.12+ for browser development. From the repository root:

```sh
npm ci
npx playwright install chromium
(cd backend && uv sync --locked)
python3 -m unittest discover -s tests -p 'test_*.py'
npm test
npm run test:foundation
```

Linux may need `npx playwright install --with-deps chromium`.
`test:foundation` uses synthetic retrieval and mocked AI; it does not validate a
live model. Report any tests you did not run. The existing CI workflow covers
legacy checks; foundation CI wiring is still unfinished.

## 6. Handoff checklist

- [ ] Small agreed scope and linked issue.
- [ ] No sensitive cases, secrets, private chats or credentials.
- [ ] Tests and documentation updated; actual results recorded.
- [ ] Existing notes/drafts/actions and exports preserved.
- [ ] Uncertainty and jurisdiction limitations stated.
- [ ] Pull request targets `main`; MJ reviews before merge.
- [ ] No paid usage, production deployment or permission changes without approval.

The repository is public, but the final license is undecided. Visibility is not
permission for unrestricted reuse or a settled contribution agreement.

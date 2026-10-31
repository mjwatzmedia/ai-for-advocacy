# Recovering and running the baseline

The private repository is the versioned source baseline. Clone it using your own GitHub access:

```sh
git clone https://github.com/mjwatzmedia/ai-for-advocacy.git
cd ai-for-advocacy
PORT=8080 python3 server.py
```

Open http://localhost:8080. GET /readyz returns 204. Use Python 3.10+;
Python 3.14.4 was used for baseline verification. Application runtime has no
third-party Python requirements, database, API key, PromptQL client library or AI provider.
Use HTTPS on a real host: browser cryptographic APIs may not work on plain non-localhost HTTP.
The Python server is a prototype static server, not a hardened production launch configuration.

## Test dependencies and limitations

Use Node >=22.12 (the locked axe wrapper requires this), npm and Chromium.
The initial verification machine used Node 24.22.0 and npm 11.19.0.
`npm ci` installs the locked Playwright 1.64.1 and axe packages (4.14.0).
The original `npm test` is a failing generated placeholder, not the test runner.
The preserved direct CJS scripts assume port 8080 and absolute deployment output paths.
Do not run them unchanged against the live service or overwrite its test artifacts.
The baseline verifier documented in `../audit/BASELINE.md` runs a temporary copy,
changes only test URL/output paths there, installs dependencies and checks the same workflows.
A later approved development branch should make tests portable and repair npm test.

## What independence means

The runtime needs only public/ and server.py (or any equivalent static host).
The separate publish.py utility uses PromptQL environment variables to publish
artifacts; it is optional, is NOT imported by server.py, and must not run during normal startup.
Never put actual environment credentials into source control or browser code.
The systemd unit example is included for reference; no unit is installed and no deployment
is activated by cloning or pushing this repository.

## User data and recovery limits

The prototype has no case database, accounts or server-side session persistence.
User entries exist only in each visitor's open page. Git does not back up that memory,
private chat/wiki history or user-downloaded files. Users must export before closing/reloading.
The current Markdown export is not a lossless importable serialized case.
Do not add actual case files to this repository.

## Source fidelity and known defects

`../audit/preserved-source-manifest.json` lists the original source-file SHA-256 hashes.
All original application/test/package files were copied without modification.
The known reset defect leaves previously rendered source text in hidden DOM until reload.
Do not use sensitive real data. The ISC metadata and test limitations above are known,
not fixed in this preservation commit. No claim of verified civic/legal guidance is made.

## Rollback and synchronization

The first pushed commit is the preservation baseline; its full SHA is recorded in the
post-push handoff, not self-referentially inside that commit. Keep it available in history.
Future code changes use approved task branches and pull requests; no force push,
unapproved rewrite or deployment. Fetch and inspect remote changes before each task.
Connecting GitHub alone does not continuously synchronize the PromptQL workspace.
No workflow, webhook, hosting integration or automatic deployment is configured by this baseline.
External account-side deployment settings were not fully inspectable through the GitHub App.

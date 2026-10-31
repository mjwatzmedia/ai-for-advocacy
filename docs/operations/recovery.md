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

## Test dependencies and execution

Use Node >=22.12, npm, Python3.10+ and Playwright Chromium. From a fresh checkout:

```sh
npm ci
npx playwright install chromium
npm test
```

Tests start an ephemeral loopback server using a temporary asset copy; no running server
or fixed deployment path is needed. Reports go to ignored `test-results/` by default.
Individual suites and platform prerequisites are documented in the root README.
There is no newly configured GitHub Actions workflow; tests must be run explicitly.

The preservation commit `da96749944d6cc302ecfe2ddcca93dca91ca07ce` intentionally
retains the original failing npm placeholder and nonportable scripts. Historical audit files
and `run-baseline-verification.py` apply to that original revision only. For baseline recovery,
use a **separate** checkout at that SHA rather than replacing an active working tree:

```sh
git clone https://github.com/mjwatzmedia/ai-for-advocacy.git baseline-recovery
cd baseline-recovery
git checkout --detach da96749944d6cc302ecfe2ddcca93dca91ca07ce
python3 docs/audit/run-baseline-verification.py
```

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

## Source fidelity and reset behavior

`../audit/preserved-source-manifest.json` lists the **original baseline** source hashes.
Later approved development commits deliberately change some of those files; their hashes
are not expected to match the historical manifest. The initial reset defect was hidden DOM
residue; the cleanup branch explicitly clears rendered case content as well as state and
adds a reproducing regression test. It does not add durable case storage or data migration.
Clearing the page cannot delete downloaded exports, clipboard contents, browser backups,
or copies held by extensions, and is not a secure-erasure guarantee. Do not use sensitive real data.
The generated ISC metadata remains unchanged; final licensing still requires approval.
No claim of verified civic/legal guidance is made.

## Rollback and synchronization

The first pushed commit is the preservation baseline; its full SHA is recorded in the
post-push handoff, not self-referentially inside that commit. Keep it available in history.
Future code changes use approved task branches and pull requests; no force push,
unapproved rewrite or deployment. Fetch and inspect remote changes before each task.
Connecting GitHub alone does not continuously synchronize the PromptQL workspace.
No workflow, webhook, hosting integration or automatic deployment is configured by this baseline.
External account-side deployment settings were not fully inspectable through the GitHub App.

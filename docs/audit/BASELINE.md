# Preservation baseline — October 31, 2026

**Historical evidence:** this document, manifest and verifier describe preservation commit
`da96749944d6cc302ecfe2ddcca93dca91ca07ce`, not subsequent development.
Run its verifier only in a separate checkout of that commit; see
[recovery instructions](../operations/recovery.md). For a development checkout use `npm test`.

Approved scope: first sanitized backup of the existing prototype, selected product requirements
and reproducible operating context. Repository mjwatzmedia/ai-for-advocacy was already private
and empty: branches [], commits API 409 Git Repository is empty, contents empty.
No existing history was replaced and no duplicate repository was created.

All 11 preserved application/operator/test/README/package source files are byte-identical
to the working prototype; see preserved-source-manifest.json. All 17 pre-audit live files
also matched their original hashes before preparation. Generated screenshot/reports,
archives, dependencies and unrelated history are intentionally excluded from this commit.
No user cases, API keys, token values or chat transcript is included.

The original brief, complete user-supplied master development specification and the
conversation-first plan are selected product documentation, not a dump of workspace history.
The UX plan is a proposal with identified unresolved inputs, not implementation approval.

## Verification scope

Baseline functional and layout testing uses an isolated temporary copy on the same VM,
without PROMPTQL_* environment variables. It installs fresh npm dependencies from the lock,
changes only the copied test URLs/output locations, and runs the original smoke and
views scripts against the copy. It is not an independent-machine reproduction. The
original failing npm test placeholder and known reset defect remain documented, not repaired.
Test results will be recorded in verification.json after execution; no CI, deploy or
conversational-workflow tests are being introduced by the preservation commit.

The verifier source is run-baseline-verification.py. From the repository root:

```sh
python3 docs/audit/run-baseline-verification.py
```

It produces results under a new temporary directory, prints its location, and leaves
repository source untouched. Browser dependency setup may require an administrator on
another machine. Existing system Chromium support on the verification VM is not a
claim that a new OS has been bootstrapped.

## Secret review

A conservative token/private-key/email scan and explicit path/content review occur before
staging. Pattern scanning is not a guarantee that all possible sensitive information can
be recognized. Scripts reference environment variable NAMES only; credentials remain
outside source and Git configuration. No live credential is exported.

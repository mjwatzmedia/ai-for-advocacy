# Privacy reset and portable tests — review notes

## Approved scope

MJ Watz approved a dedicated cleanup branch and pull request, without merge or deployment.
Base: `da96749944d6cc302ecfe2ddcca93dca91ca07ce`; branch: `fix/privacy-reset-portable-tests`.

## Application change

Only `clearWorkspace` in `public/app.js` changes application behavior. A confirmed reset
clears the case state, summaries, dynamic authority/source/action/research/strategy containers,
form values, checkboxes, counts, validation errors, edit state and notes/draft. It resets tabs
and focuses intake. Cancel leaves the case and editable work unchanged. Removing rendered
cards also removes their attached handlers from the page. There is no persistence/database
schema change, live case migration, UI redesign or AI integration.

The reset message clarifies that downloaded files and copied text are not deleted.
This is not secure erasure from the browser/device or a promise to clear extensions/backups.

## Test infrastructure

`npm test` runs smoke, view/accessibility and privacy suites against an ephemeral loopback
server using copied assets and the real Python handler. No production port or absolute
workspace output paths are required. Test output is ignored; the runner strips platform
variables from children and stops its test server. Browser handles close on suite failure.
The smoke accessibility scan now fails on violations rather than merely reporting them.
Node22.12+ requirement is made explicit without changing locked dependency versions.
The license field is unchanged; no final license is selected by this task.

## Review evidence

Before the reset fix, `npm run test:privacy` failed with “Cleared case remains in hidden
DOM/attributes”. With the reset fix it passes. The full `npm test` passed with zero browser
errors or unexpected requests in the exercised privacy flow, and zero reported axe violations
in desktop/mobile scans and the 12 viewport/panel combinations. These are automated checks,
not an independent security/accessibility audit. A fresh `npm ci --ignore-scripts` in a separate temporary directory passed, and all three
suites passed when the runner was invoked from an unrelated working directory with no
`PROMPTQL_*` variables. Failure injection in that temporary copy proved that low-contrast
CSS causes smoke tests to fail and a missing Python executable fails startup promptly.
These checks used the same VM and cached browser binary; no independent-machine
reproduction is implied.

Historical baseline manifests/test evidence remain intact and apply to their original commit.

## Release boundary

This branch is review-only. No workflow, hook, deploy integration, dependency service,
credential, billing, repository permission or production service is changed.
Do not merge or deploy without separate approval. The conversation-first product revision
is out of scope and still requires its own implementation approval and test plan.

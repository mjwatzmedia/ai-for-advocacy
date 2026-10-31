# Security policy

## Project status
AI for Advocacy is an experimental, session-only planning prototype, **not** a secure case-management service, legal service, live AI engine, or emergency reporting channel. Do not enter or upload sensitive case details, minors' information, private correspondence, secrets, or real identity records.

## Reporting a vulnerability
**Do not disclose exploitable details in a public GitHub issue or pull request.** Contact the repository owner through a private GitHub message/channel or use GitHub's private vulnerability reporting feature **if it is enabled**. The maintainer should publish a dedicated security contact before inviting outside testers. If no private reporting channel is available, request one without including exploit details.

Please include affected version/commit, reproducible steps using synthetic data, impact, and any suggested mitigation. Avoid testing against other users, production services, or systems you do not control.

## Current controls and limitations
- Browser-only state; no app-side account, database, analytics, model, or retrieval service.
- Text-only rendering for user entries, HTTP(S) source-link validation, and server security headers.
- Automated privacy regression, smoke and accessibility tests.
- Clearing a workspace removes app state and rendered case content; it is **not** secure deletion from device memory, downloads, clipboard, backups, or extensions.
- Hosting platform, browser, device, network, and third-party links have independent risks.
- Tests and a limited historical credential scan do not establish comprehensive security assurance.

## Required review before adding AI or persistence
Threat-model prompt injection, untrusted source content, sensitive-data transfer to model providers, authorization between users, retention/deletion, secrets management, external links, rate limiting, abuse prevention, provenance and auditability. No real-case beta until those risks have documented mitigations and informed user guidance.

Security fixes should use a reviewed branch and tests; coordinate disclosure before publishing details.

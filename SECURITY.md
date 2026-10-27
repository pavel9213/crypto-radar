# Security Policy

## Supported project

Security fixes are welcome for the current default branch.

## Reporting a vulnerability

Please do not publish credentials, private data, or exploit details in a public issue. Use GitHub's private vulnerability reporting feature for this repository if it is enabled. If it is unavailable, contact the repository maintainer privately through GitHub before sharing technical details publicly.

## Secret handling

- Store API credentials in GitHub Actions repository secrets.
- Never place a Bearer Token in source files, issues, screenshots, or commit messages.
- Rotate any token that may have been exposed.
- The collector should continue to run without an X API token; do not replace this optional behavior with a hard-coded credential.

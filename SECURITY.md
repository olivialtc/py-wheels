# Security policy

These wheels are built by GitHub Actions from hash-pinned PyPI sdists (`requirements.txt`)
and published with a `SHA256SUMS` file per platform. Only the current `cp315` release is
supported.

## Reporting a vulnerability

Report it privately through GitHub: **Security → Report a vulnerability** on this repository.
Do not open a public issue. Expect an acknowledgement within 7 days.

A vulnerability in duckdb or pyyaml itself belongs upstream. Report it here only when it
comes from how these wheels are built or served, such as a hash mismatch, a tampered
release asset, or a workflow that could be abused.

## What protects this repository

- **`main` is ruleset-protected**: changes land by pull request; force-pushes and deletion are
  blocked.
- **Release tags are immutable** once pushed. Rebuilding a published platform would change
  its wheel hashes and break every `uv.lock` that pinned them.
- Secret scanning with push protection, Dependabot security updates, and private
  vulnerability reporting are enabled.

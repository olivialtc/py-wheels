# py-wheels

CPython 3.15 wheels for open-source packages that do not publish 3.15 wheels on PyPI yet.

Every wheel here is built by `.github/workflows/build.yml`, on GitHub-hosted runners, from the
package's own PyPI source release, pinned by version and by PyPI's sha256 in `requirements.txt`.
Nothing is patched. The packages keep their own licenses (shipped inside each wheel): DuckDB (MIT),
PyYAML (MIT).

| release tag | contents |
|---|---|
| `cp315` | duckdb 1.5.6, pyyaml 6.0.3 for Linux x86_64 and aarch64 (manylinux) and macOS arm64 |

## Use with uv

```toml
[tool.uv]
find-links = ["https://olivialtc.github.io/py-wheels/cp315/"]
```

That page (`index.yml`, GitHub Pages) is a hashed flat index: for each pinned package it lists
EVERY file PyPI has for that version, with PyPI's sha256, plus the cp315 wheels from the release,
with the hash the build recorded. Those wheels are served from the Pages site itself
(`/<tag>/files/`), copied only after their hash matches: a release-asset download redirects to a
host the Claude cloud sandbox cannot reach (2026-10-15). For a version listed here, uv takes the distributions from this
page, which is why PyPI's own files are listed too: every other interpreter and platform stays
installable, and `uv.lock` stays fully hashed. A newer version on PyPI still wins when a lock is
upgraded, so this pins nothing.

Adding or bumping a package: edit `requirements.txt` (version and PyPI's sdist sha256), then run
`build.yml`, then `index.yml`. Adding a platform: run `build.yml` with `runners` naming ONLY the new
runner (rebuilding a published platform changes its hashes and breaks the repos' locks), then
`index.yml`, then re-lock each repo. Retire a package once PyPI ships a cp315 wheel for the version the
repos lock (markupsafe was retired 2026-10-16: 3.0.4 ships its own cp315 wheels on PyPI; its 3.0.3 builds stay in the
release but are no longer indexed).

# py-wheels

CPython 3.15 wheels for open-source packages that do not publish 3.15 wheels on PyPI yet.

Every wheel here is built by `.github/workflows/build.yml`, on GitHub-hosted runners, from the
package's own PyPI source release, pinned by version and by PyPI's sha256 in `requirements.txt`.
Nothing is patched. The packages keep their own licenses (shipped inside each wheel): DuckDB (MIT),
PyYAML (MIT), MarkupSafe (BSD-3-Clause).

| release tag | contents |
|---|---|
| `cp315` | duckdb 1.5.6, pyyaml 6.0.3, markupsafe 3.0.3 for Linux x86_64 (manylinux) and macOS arm64 |

## Use with uv

```toml
[tool.uv]
find-links = ["https://olivialtc.github.io/py-wheels/cp315/"]
```

That page (`index.yml`, GitHub Pages) is a hashed flat index: for each pinned package it lists
EVERY file PyPI has for that version, with PyPI's sha256, plus the cp315 wheels from the release,
with the hash the build recorded. uv takes a package it finds there from there alone, which is
why PyPI's files are listed too: every other interpreter and platform stays installable from
PyPI's own wheels or sdist, and `uv.lock` stays fully hashed.

The cost of that: a listed package is pinned to the version listed here. Bumping one means
editing `requirements.txt` (version and PyPI sdist hash), then running `build.yml` and `index.yml`.
Retire a package once PyPI ships a cp315 wheel for the version you lock.

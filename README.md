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
find-links = ["https://github.com/olivialtc/py-wheels/releases/expanded_assets/cp315"]
```

uv still prefers PyPI's own wheel whenever one exists for the interpreter; this only fills the gap.
Retire an entry once PyPI ships a cp315 wheel for that version.

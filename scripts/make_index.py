"""Write site/<tag>/index.html: a hashed flat index for the packages in requirements.txt.

Each package lists EVERY file PyPI has for its pinned version (sdist and wheels, with PyPI's
sha256) plus the cp315 wheels this repo's release adds (with the sha256 the build recorded).
uv takes a package found here from here alone, so the PyPI files keep every other interpreter
and platform installable, and the hashes keep `uv.lock` hash-checked. Stdlib only.

usage: python3 scripts/make_index.py <tag> <dir holding SHA256SUMS-*.txt> [<dir holding the wheels>]

With the wheels dir, the built wheels are served FROM THIS SITE (site/<tag>/files/), each
copied only after its sha256 matches the build's record: a GitHub release asset redirects to
objects.githubusercontent.com, which the Claude cloud sandbox's egress proxy answers with
401, so uv in a cloud session could not download one (measured 2026-10-15).
"""

import hashlib
import html
import json
import pathlib
import re
import sys
import urllib.request

REPO = "olivialtc/py-wheels"
PAGES = "https://olivialtc.github.io/py-wheels"


def pins(path: pathlib.Path) -> list[tuple[str, str, str]]:
    out = []
    for line in path.read_text().splitlines():
        m = re.match(r"^([A-Za-z0-9_.-]+)==(\S+)\s+--hash=sha256:([0-9a-f]{64})", line)
        if m:
            out.append(m.groups())
    return out


def ours(tag: str, sums_dir: pathlib.Path, wheels: pathlib.Path | None = None) -> dict[str, list[tuple[str, str]]]:
    got: dict[str, list[tuple[str, str]]] = {}
    for f in sorted(sums_dir.glob("SHA256SUMS-*.txt")):
        for line in f.read_text().splitlines():
            digest, name = line.split()
            if wheels is None:
                url = f"https://github.com/{REPO}/releases/download/{tag}/{name}"
            else:
                blob = (wheels / name).read_bytes()
                if hashlib.sha256(blob).hexdigest() != digest:
                    raise SystemExit(f"make_index: {name}: sha256 differs from the build's record")
                dest = pathlib.Path("site") / tag / "files" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(blob)
                url = f"{PAGES}/{tag}/files/{name}"
            got.setdefault(name.split("-")[0].lower(), []).append((name, f"{url}#sha256={digest}"))
    return got


def main(tag: str, sums_dir: str, wheels_dir: str | None = None) -> int:
    built = ours(tag, pathlib.Path(sums_dir), pathlib.Path(wheels_dir) if wheels_dir else None)
    rows = []
    for name, version, sdist_sha in pins(pathlib.Path("requirements.txt")):
        with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=60) as r:
            files = json.load(r)["urls"]
        sdists = [f for f in files if f["packagetype"] == "sdist"]
        if [f["digests"]["sha256"] for f in sdists] != [sdist_sha]:
            print(f"make_index: {name} {version}: PyPI's sdist hash is not the pinned one", file=sys.stderr)
            return 1
        for f in files:
            rp = f.get("requires_python") or ""
            attr = f' data-requires-python="{html.escape(rp)}"' if rp else ""
            rows.append(f'<a href="{f["url"]}#sha256={f["digests"]["sha256"]}"{attr}>{f["filename"]}</a><br>')
        mine = built.get(name.lower().replace("-", "_"), []) + built.get(name.lower(), [])
        if not mine:
            print(f"make_index: no built wheel for {name} in {sums_dir}", file=sys.stderr)
            return 1
        rows += [f'<a href="{u}">{n}</a><br>' for n, u in dict(mine).items()]
    out = pathlib.Path("site") / tag / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("<!DOCTYPE html>\n<html><body>\n" + "\n".join(rows) + "\n</body></html>\n")
    print(f"make_index: {len(rows)} file(s) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))

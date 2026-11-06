#!/usr/bin/env python3
"""Fail when tracked paths use common secret-bearing filenames."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRET_PATH_RE = re.compile(r"(^|/)(?:\.env(?:\..*)?|id_rsa|id_ed25519|[^/]*\.(?:pem|key))$")


def is_secret_path(path: str) -> bool:
    """Return whether a tracked path resembles a secret-bearing file."""
    return Path(path).name != ".env.example" and SECRET_PATH_RE.search(path) is not None


def tracked_secret_paths(root: Path = ROOT) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"git ls-files failed: {result.stderr.decode(errors='replace').strip()}")
    paths = result.stdout.decode("utf-8", errors="surrogateescape").split("\0")
    return sorted(path for path in paths if path and is_secret_path(path))


def main() -> int:
    try:
        paths = tracked_secret_paths()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if paths:
        for path in paths:
            print(f"Potential secret-bearing path: {path}", file=sys.stderr)
        return 1
    print("No tracked paths match common secret-bearing filenames.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

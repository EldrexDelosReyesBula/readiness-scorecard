"""
scanner.py — Python file discovery for the Production Readiness Scorecard.

Walks a directory tree (or accepts a single file) and yields all .py files,
skipping common noise directories: .venv, venv, __pycache__, .git, node_modules.
"""

import os
from pathlib import Path
from typing import Iterator

# Directories that are never meaningful scan targets
_SKIP_DIRS = {".venv", "venv", "__pycache__", ".git", "node_modules", ".mypy_cache", ".tox"}


def discover_files(target: str) -> Iterator[Path]:
    """
    Yield absolute Path objects for every .py file under *target*.

    *target* may be:
      - A single .py file  → yields that file only (if it exists).
      - A directory        → walks recursively, honouring _SKIP_DIRS.

    Raises FileNotFoundError if *target* does not exist.
    """
    root = Path(target).resolve()

    if not root.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    if root.is_file():
        if root.suffix == ".py":
            yield root
        return

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skipped directories in-place (modifies os.walk's traversal)
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS and not d.startswith(".")]

        for filename in filenames:
            if filename.endswith(".py"):
                yield Path(dirpath) / filename

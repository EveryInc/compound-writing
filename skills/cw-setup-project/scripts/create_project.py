#!/usr/bin/env python3
"""Create the canonical Compound Writing writing-home structure without overwriting files."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create VOICE.md, STYLE.md, examples/, and drafts/ for one writing home."
    )
    parser.add_argument("target", type=Path, help="Writing-home folder to create or initialize")
    parser.add_argument(
        "--add-missing",
        action="store_true",
        help="Add only missing template items to a non-empty existing folder",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target.expanduser().resolve()
    template = Path(__file__).resolve().parents[3] / "defaults" / "project-template"

    if not template.is_dir():
        raise SystemExit(f"Project template not found: {template}")
    if target.exists() and not target.is_dir():
        raise SystemExit(f"Target exists and is not a folder: {target}")

    existing = list(target.iterdir()) if target.exists() else []
    if existing and not args.add_missing:
        raise SystemExit(
            "Target folder is not empty. Inspect it first, then rerun with --add-missing "
            "to create absent items without overwriting anything."
        )

    target.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    skipped: list[str] = []

    for source in sorted(template.rglob("*")):
        relative = source.relative_to(template)
        destination = target / relative
        if source.is_dir():
            if not destination.exists():
                destination.mkdir(parents=True)
                created.append(f"{relative}/")
            continue
        if destination.exists():
            skipped.append(str(relative))
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        created.append(str(relative))

    print(f"Writing home ready: {target}")
    if created:
        print("Created:")
        for item in created:
            print(f"  - {item}")
    if skipped:
        print("Preserved existing:")
        for item in skipped:
            print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

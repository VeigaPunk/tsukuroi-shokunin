#!/usr/bin/env python3
"""Count only KR rows satisfying the round-69 frozen evidence clauses.

Reads Git objects and snapshot files only; creates no temporary files.
"""
import argparse
from collections import Counter
import hashlib
from pathlib import Path
import re
import subprocess
import sys

NOTE = "corpus/knowledge/kernel-taint-plane-r69.md"
REGISTRY = "corpus/SOURCES.md"


def unfenced(text):
    """Yield lines outside CommonMark backtick/tilde fences (0-3 spaces)."""
    fence = None
    for line in text.splitlines():
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) +
                            "{" + str(fence[1]) + r",}[ \t]*", line):
                fence = None
            continue
        opening = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", line)
        if opening and (opening[1][0] != "`" or "`" not in opening[2]):
            fence = (opening[1][0], len(opening[1]))
            continue
        yield line


def registry_ids(text):
    ids = set()
    in_registry = False
    for line in unfenced(text):
        heading = re.match(r" {0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            if heading[2] == "Registry":
                in_registry = True
                level = len(heading[1])
            elif in_registry and len(heading[1]) <= level:
                in_registry = False
        if in_registry:
            row = re.match(r" {0,3}\|\s*(S[0-9]{3,})\s*\|", line)
            if row:
                ids.add(row[1])
    return ids


def git(lane, *args):
    return subprocess.run(["git", "-C", str(lane), *args],
                          capture_output=True, text=True, encoding="utf-8")


def default_lane():
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    return Path(__file__).resolve().parent.parent


def evaluate(note, sources, snapshots):
    rows = []
    for line in unfenced(note):
        if line.startswith("| KR"):
            cells = [cell.strip() for cell in line.split("|")[1:]]
            if cells and not cells[-1]:
                cells.pop()
            rows.append(cells)
    counts = Counter(cells[0] for cells in rows)
    verified = 0
    results = []
    for cells in rows:
        ident = cells[0]
        clause = None
        if len(cells) != 6:
            clause = "cells"
        elif not re.fullmatch(r"KR[0-9]+", ident):
            clause = "id"
        elif counts[ident] != 1:
            clause = "unique-id"
        elif len(cells[1].split()) < 12:
            clause = "statement"
        elif not re.fullmatch(r"source=S[0-9]{3,}", cells[2]) or cells[2][7:] not in sources:
            clause = "source"
        else:
            name = cells[3].removeprefix("snapshot=")
            if (not cells[3].startswith("snapshot=") or not name or
                    name in (".", "..") or Path(name).name != name):
                clause = "snapshot"
            else:
                try:
                    data = (snapshots / name).read_bytes()
                except OSError:
                    clause = "snapshot"
                else:
                    digest = cells[4].removeprefix("digest=")
                    if (not cells[4].startswith("digest=") or
                            not re.fullmatch(r"[0-9a-f]{64}", digest) or
                            hashlib.sha256(data).hexdigest() != digest):
                        clause = "digest"
                    else:
                        quote = re.fullmatch(r'quote="(.*)"', cells[5])
                        if not quote or not 1 <= len(quote[1].split()) <= 25:
                            clause = "quote"
                        else:
                            try:
                                text = data.decode("utf-8")
                            except UnicodeError:
                                clause = "quote"
                            else:
                                if " ".join(quote[1].split()) not in " ".join(text.split()):
                                    clause = "quote"
        if clause is None:
            verified += 1
        results.append(f"KR_ROW {ident} " + ("ok" if clause is None else f"fail:{clause}"))
    print(f"KR_ROWS={len(rows)} KR_VERIFIED={verified}")
    print("\n".join(results), end="\n" if results else "")
    return 0 if len(rows) == verified and verified >= 5 else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--lane", type=Path, default=default_lane())
    parser.add_argument("--snapshots", type=Path)
    args = parser.parse_args()
    snapshots = args.snapshots or args.lane / ".ufo/waves/round-69/before/src"
    try:
        revision = git(args.lane, "rev-parse", "--verify", "--end-of-options", args.revision + "^{commit}")
        if revision.returncode:
            raise ValueError("missing revision: " + revision.stderr.strip())
        commit = revision.stdout.strip()
        registry = git(args.lane, "show", commit + ":" + REGISTRY)
        if registry.returncode:
            raise ValueError("unreadable registry: " + registry.stderr.strip())
        if not snapshots.is_dir():
            raise ValueError("missing snapshot directory: " + str(snapshots))
        # Iteration checks directory readability without creating temporary files.
        next(snapshots.iterdir(), None)
        note = git(args.lane, "show", commit + ":" + NOTE)
        if note.returncode:
            present = git(args.lane, "cat-file", "-e", commit + ":" + NOTE)
            if present.returncode == 0:
                raise ValueError("unreadable note: " + note.stderr.strip())
            return evaluate("", registry_ids(registry.stdout), snapshots)
        return evaluate(note.stdout, registry_ids(registry.stdout), snapshots)
    except (OSError, UnicodeError, ValueError) as error:
        print("KR_ERROR " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

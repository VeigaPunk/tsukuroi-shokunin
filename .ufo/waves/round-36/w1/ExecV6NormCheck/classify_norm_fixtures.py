#!/usr/bin/env python3
"""Classify round-35 v6 normalization debt fixtures and print expected canonical forms."""
import re
import sys

ROOT = r"/fast/scratch/hyaku/s[0-9a-f]{12}-[A-Za-z0-9]+/r[0-9a-f]{12}/t[0-9a-f]{12}"
FIXTURE = re.compile(rf"^{ROOT}/adjacency-git-[A-Za-z0-9]{{8}}/fixture-tree$")
CEILING = re.compile(rf"^{ROOT}$")
HOME_DERIVED = re.compile(rf"^{ROOT}/adjacency-git-[A-Za-z0-9]{{8}}/home/\.config$")
SHORT_HASH = re.compile(r"^[0-9a-f]{7,39}$")


def classify(name, value):
    if name == "SHORT_HASH" and SHORT_HASH.fullmatch(value):
        return "short-hash", "<SHORT_HASH>"
    if name == "FIXTURE_PATH" and FIXTURE.fullmatch(value):
        return "fixture/scratch-path-components", "<RUN_ROOT>/<RUN>/<TMP>/adjacency-git-<FIXTURE>/fixture-tree"
    if name == "GIT_CEILING_DIRECTORIES" and CEILING.fullmatch(value):
        return "GIT_CEILING_DIRECTORIES-run-TMPDIR", "<RUN_TMPDIR>"
    if name == "XDG_CONFIG_HOME" and HOME_DERIVED.fullmatch(value):
        return "HOME-derived-config-path", "<TARGET_HOME>/.config"
    return "UNCLASSIFIED", "<no expected normalization>"


def main(path):
    count = 0
    for number, raw in enumerate(open(path, encoding="utf-8"), 1):
        pair = raw.rstrip("\n")
        if not pair or pair.startswith("#"):
            continue
        name, sep, value = pair.partition("=")
        if not sep:
            raise SystemExit(f"{path}:{number}: expected NAME=VALUE")
        label, canonical = classify(name, value)
        print(f"{label}\t{name}\t{value}\t=>\t{canonical}")
        if label == "UNCLASSIFIED":
            count += 1
    return 1 if count else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} norm-fixtures.txt")
    raise SystemExit(main(sys.argv[1]))

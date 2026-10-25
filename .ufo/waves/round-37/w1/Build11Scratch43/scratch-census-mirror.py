#!/usr/bin/env python3
"""scratch-census-mirror.py — tsukuroi round-37 design item 11/12.

Scratch census mirror gate: validate-before-append for corpus/SOURCES.md.

Contract (mirror design, derived from the round-36 verifier closure and the
fleet-wide sources-census.sh contract):

  BEFORE the first real registry append, the candidate rows (the "after"
  state of the registry) must be validated in an isolated scratch mirror:

      a copy of corpus/ plus the append block, then
      scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md
      must exit 0 (warnings allowed).

This tool performs exactly that, in that order. The lane corpus is opened
read-only: the mirror is what receives the appended rows. `used-by` paths
are resolved by sources-census.sh against the parent of the file's parent
(= the mirror root), so the whole corpus is copied and every used-by target
must exist inside the mirror on disk.

The gate MUST FAIL on the unchanged baseline: an empty/no-op append block is
a hard refusal (exit 1), never a silent green. A vacuous pass would be
indistinguishable from "no change", so the design binds the before-count
(--expect-rows-before, default 199 = the row count of lane HEAD 0e5f70f)
and requires at least one appended id that is not already in the registry.

Measured after-state (the receipt):
  rows_before / rows_appended / rows_after, ids_appended,
  rows_sha256 (append block), source_registry_sha256 (lane bytes, re-checked
  after the build), mirror_registry_sha256 (after-state bytes), and the
  validate findings (E/W) with W04 duplicate-url advisory counts before vs
  after the append.

Sandbox rules: dest must live under a fresh mktemp fixture repo or inside
the lane's .ufo/waves/round-37/w1/<seat> directory (never the lane worktree
itself); the fixture repo is git-initialized and its top-level is verified
equal to the fixture root before any commit; no git/jj writes ever happen in
the lane, fleet, or sibling repos; the source corpus is never written (its
digest is re-checked after the build).

Usage:
  python3 -B scratch-census-mirror.py --rows-file FILE
      [--corpus DIR] [--dest DIR] [--validate SCRIPT]
      [--today YYYY-MM-DD] [--expect-rows-before N] [--force] [--commit]
      [--fixture] [--verbose]

  --rows-file          candidate append block: one Markdown row per line
                       (11 cells => NF=13 on '|' split). An empty file is
                       refused: unchanged baseline has no after state.
  --corpus             source corpus to mirror (default: <lane>/corpus).
  --dest               mirror root (default: fresh mktemp fixture repo).
                       Must be under /var/tmp, /tmp, or the seat directory.
  --validate           sources-census.sh path (default: the fleet script).
  --today              ISO date for the census (default: UTC today).
  --expect-rows-before N  registry rows required before the append; default
                       199 = lane HEAD 0e5f70f row count; 0 disables.
  --force              replace a previous mirror this tool built (marker-checked).
  --commit             create one commit in the fixture repo after a clean
                       validation (top-level verified before the commit).
  --fixture            bootstrap a synthetic corpus (no real lane corpus).
  --verbose            also print the validate command line.

Exit: 0 mirror built and validate exited 0; 1 build/integrity refusal;
2 usage/environment; otherwise the validate exit code, also printed as
`validate_exit=<n>`.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
DEFAULT_CORPUS = LANE / "corpus"
DEFAULT_VALIDATE = Path("/home/vgpnk/Projects/shokunin/scripts/sources-census.sh")
SEAT = Path(__file__).resolve().parent

MARKER = ".tsukuroi-scratch-census-mirror"
DEFAULT_EXPECT_ROWS_BEFORE = 199  # lane HEAD 0e5f70f (round-36 tip + r37 capability commits)

KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book",
         "community", "own-work"}
TIERS = {"A", "B", "C"}
STATUSES = {"queued", "mined", "rejected"}
ID_RE = re.compile(r"^S[0-9]{3,}$")
ISO_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
CADENCE_RE = re.compile(r"^([0-9]+d|[A-Za-z][A-Za-z0-9 _-]*)$")
ROW_RE = re.compile(r"^ {0,3}\|(.*)\|[ \t]*$")
HEADING_RE = re.compile(r"^ {0,3}##[ \t]+Registry[ \t]*$")
ANY_HEADING_RE = re.compile(r"^ {0,3}#{1,6}[ \t]")
ID_SCAN_RE = re.compile(r"^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|")

warnings: list[str] = []


def die_usage(msg: str) -> None:
    print(f"scratch-census-mirror: {msg}", file=sys.stderr)
    raise SystemExit(2)


def die_build(msg: str) -> None:
    print(f"scratch-census-mirror: REFUSED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iso_ok(s: str, today: datetime.date) -> bool:
    if not ISO_RE.match(s):
        return False
    try:
        d = datetime.date.fromisoformat(s)
    except ValueError:
        return False
    return d <= today


def parse_rows(path: Path, today: datetime.date) -> list[list[str]]:
    """Strictly parse the append block; return the 11 cell lists per row."""
    rows: list[list[str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for lineno, line in enumerate(lines, 1):
        if not line.strip():
            continue
        m = ROW_RE.match(line)
        if not m:
            die_build(f"{path}:{lineno}: row must start and end with '|'")
        body = m.group(1)
        cells = [c.strip() for c in body.split("|")]
        if len(cells) != 11:
            die_build(f"{path}:{lineno}: NF={len(cells) + 2} (want 13)")
        if any("\\|" in c for c in cells):
            die_build(f"{path}:{lineno}: escaped pipe inside a cell")
        rows.append(cells)
    return rows


def check_row_static(rows: list[list[str]], today: datetime.date) -> None:
    seen: set[str] = set()
    for cells in rows:
        rid, source, kind, tier, _scope, _anchor, teaches, status, opened, recheck, usedby = cells
        if not ID_RE.match(rid):
            die_build(f"{rid}: id not S[0-9]{{3,}}")
        if rid in seen:
            die_build(f"{rid}: duplicate id in the append block")
        seen.add(rid)
        if kind not in KINDS:
            die_build(f"{rid}: kind={kind!r} not in the census enum")
        if tier not in TIERS:
            die_build(f"{rid}: tier={tier!r} not in {{A,B,C}}")
        if status not in STATUSES:
            die_build(f"{rid}: status={status!r} not in {{queued,mined,rejected}}")
        if not iso_ok(opened, today):
            die_build(f"{rid}: opened={opened!r} is not a past/present ISO date")
        if not CADENCE_RE.match(recheck):
            die_build(f"{rid}: recheck={recheck!r} is not ISO/NNd/symbolic")
        if not usedby or usedby == "—":
            continue
        for p in usedby.split(","):
            p = p.strip()
            if p and p != "—" and not p.startswith("corpus/"):
                die_build(f"{rid}: used-by {p!r} is not under corpus/")
    if not seen:
        die_build("no appended rows: unchanged baseline has no after state; "
                  "the mirror gate refuses a vacuous pass")


def scan_ids(lines: list[str]) -> list[str]:
    ids: list[str] = []
    in_registry = False
    for ln in lines:
        if HEADING_RE.match(ln):
            in_registry = True
            continue
        if ANY_HEADING_RE.match(ln):
            in_registry = False
            continue
        if not in_registry:
            continue
        m = ID_SCAN_RE.match(ln)
        if m:
            ids.append(m.group(1))
    return ids


def insert_rows(lines: list[str], rows: list[list[str]]) -> list[str]:
    """Insert rows after the separator line of the ## Registry table."""
    positions = [i for i, ln in enumerate(lines) if HEADING_RE.match(ln)]
    if not positions:
        die_build("source registry has no '## Registry' section")
    # find the separator line (the second table line: id | ... | then ---)
    start = positions[0]
    sep = None
    for i in range(start + 1, len(lines)):
        if not lines[i].strip():
            continue
        if lines[i].lstrip().startswith("|"):
            sep = i
            break
    if sep is None:
        die_build("source registry has no table header row")
    # The separator is the line after header: '|---|---|...'
    if not re.match(r"^ {0,3}\|[-:| ]+\|", lines[sep + 1]):
        die_build("source registry has no separator row after the header")
    anchor = sep + 1
    rendered = ["| " + " | ".join(cells) + " |\n" for cells in rows]
    return lines[:anchor + 1] + rendered + lines[anchor + 1:]


def resolve_dest(dest: Path, corpus: Path) -> Path:
    r = dest.resolve()
    allowed = (Path("/var/tmp"), Path("/tmp"), SEAT, corpus.resolve().parents[1])
    if not any(str(r).startswith(str(a)) for a in allowed):
        die_build(
            f"dest {r} is outside /var/tmp, /tmp, the seat directory, "
            f"and the lane (hard bound)")
    return r


def prepare_dest(dest: Path, force: bool) -> None:
    if dest.exists():
        if not force and (dest / MARKER).exists():
            die_build(f"dest {dest} holds a previous mirror; pass --force to replace")
        if not force and any(dest.iterdir()):
            die_build(f"dest {dest} is non-empty and carries no {MARKER} marker")
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    # Fixture Git: fresh mktemp repo; top-level must equal the fixture root.
    subprocess.run(["git", "init", "-q", "-b", "main", str(dest)],
                   check=True, capture_output=True)
    toplevel = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "--show-toplevel"],
        check=True, capture_output=True, text=True).stdout.strip()
    if Path(toplevel) != dest:
        die_build(f"fixture git top-level {toplevel} != fixture root {dest}")


def fixture_corpus(tmp: Path) -> Path:
    """Build a synthetic corpus (no real lane bytes) shaped like the lane's."""
    corpus = tmp / "fixture-lane" / "corpus"
    (corpus / "knowledge").mkdir(parents=True)
    (corpus / "knowledge" / "fixture.md").write_text(
        "# Fixture knowledge\n\nground: F1\n", encoding="utf-8")
    (corpus / "SOURCES.md").write_text(
        "# SOURCES — fixture\n\n## Registry\n\n"
        "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
        "| S990 | Fixture row — https://fixture.invalid/s990 | docs | B | fixture | §1 | fixture row | mined | 2026-10-01 | 90d | corpus/knowledge/fixture.md |\n"
        "\n## Paths\n\n", encoding="utf-8")
    return corpus


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--rows-file", required=True)
    ap.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    ap.add_argument("--dest", default="")
    ap.add_argument("--validate", default=str(DEFAULT_VALIDATE))
    ap.add_argument("--today", default="")
    ap.add_argument("--expect-rows-before", type=int, default=DEFAULT_EXPECT_ROWS_BEFORE)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--fixture", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    today = datetime.date.today()
    if args.today:
        try:
            today = datetime.date.fromisoformat(args.today)
        except ValueError:
            die_usage(f"--today not an ISO date: {args.today}")

    rows_file = Path(args.rows_file).resolve()
    validate = Path(args.validate).resolve()
    if not rows_file.is_file():
        die_usage(f"--rows-file not found: {rows_file}")
    if not validate.is_file():
        die_usage(f"--validate script not found: {validate}")

    with tempfile.TemporaryDirectory(prefix="scratch-census-mirror-") as tmpd:
        tmp = Path(tmpd)
        corpus = fixture_corpus(tmp) if args.fixture else Path(args.corpus).resolve()
        if not (corpus / "SOURCES.md").is_file():
            die_usage(f"no corpus/SOURCES.md under {corpus}")

        dest = resolve_dest(Path(args.dest) if args.dest else tmp / "mirror", corpus)
        rows = parse_rows(rows_file, today)
        check_row_static(rows, today)

        source_digest = sha256(corpus / "SOURCES.md")
        source_lines = (corpus / "SOURCES.md").read_text(encoding="utf-8").splitlines(keepends=True)
        before_ids = scan_ids(source_lines)
        if args.expect_rows_before and len(before_ids) != args.expect_rows_before:
            die_build(
                f"registry holds {len(before_ids)} rows, not the frozen base literal "
                f"{args.expect_rows_before}; build the mirror from the base bytes "
                f"(pass --expect-rows-before 0 only to disable this binding)")
        clash = sorted(set(before_ids) & {c[0] for c in rows})
        if clash:
            die_build(f"append block repeats registry ids: {clash}")

        prepare_dest(dest, args.force)
        (dest / MARKER).write_text(
            "tsukuroi round-37 scratch census mirror; built by "
            "scratch-census-mirror.py\n"
            f"source_corpus={corpus}\nrows_file={rows_file}\n", encoding="utf-8")

        lane_root = corpus.parent

        # Mirror the tree that sources-census.sh's --file mode resolves used-by
        # against (the mirror root): the corpus plus every top-level entry named
        # by any used-by cell (today: corpus/, tools/, SKILL.md). A corpus-only
        # mirror would report E11 for every tools//SKILL.md row.
        def top_level(path: str) -> str:
            return path.split("/", 1)[0]

        needed_roots: set[str] = {"corpus"}

        def scan_usedby_roots(lines_: list[str]) -> None:
            in_registry = False
            for ln in lines_:
                if HEADING_RE.match(ln):
                    in_registry = True
                    continue
                if ANY_HEADING_RE.match(ln):
                    in_registry = False
                    continue
                if not in_registry:
                    continue
                m = ROW_RE.match(ln)
                if not m:
                    continue
                cells = [c.strip() for c in m.group(1).split("|")]
                if len(cells) != 11:
                    continue
                if all(re.fullmatch(r":?-+:?", c) for c in cells):
                    continue
                if cells[0] == "id":
                    continue
                usedby = cells[10]
                if not usedby or usedby == "—":
                    continue
                for p in usedby.split(","):
                    p = p.strip()
                    if p:
                        needed_roots.add(top_level(p))

        scan_usedby_roots(source_lines)   # existing rows (tools/, SKILL.md, corpus/)
        for cells in rows:                # candidate rows
            usedby = cells[10]
            if not usedby or usedby == "—":
                continue
            for p in usedby.split(","):
                p = p.strip()
                if p:
                    needed_roots.add(top_level(p))
        for root in sorted(needed_roots):
            src = lane_root / root
            if not src.exists():
                die_build(f"used-by root {root!r} missing from the lane root "
                          f"{lane_root}")
            dst = dest / root
            if src.is_dir():
                shutil.copytree(src, dst, symlinks=True)
            else:
                shutil.copy2(src, dst)

        # E11 pre-check: every used-by path of the append block must exist in
        # the mirror now.
        for cells in rows:
            usedby = cells[10]
            if not usedby or usedby == "—":
                continue
            for p in usedby.split(","):
                p = p.strip()
                if p and p != "—" and not (dest / p).exists():
                    die_build(f"{cells[0]}: used-by {p!r} missing in the mirror")

        registry = dest / "corpus" / "SOURCES.md"
        after_lines = insert_rows(source_lines, rows)
        registry.write_text("".join(after_lines), encoding="utf-8")

        if sha256(corpus / "SOURCES.md") != source_digest:
            die_build(f"source registry changed during the build: {corpus}")

        appended_ids = [c[0] for c in rows]
        # W04 advisory count before the append: read-only validate on the source.
        w04_before = 0
        try:
            pre = subprocess.run(
                ["bash", str(validate), "validate", "--file", str(corpus / "SOURCES.md"),
                 "--today", today.isoformat()],
                capture_output=True, text=True, timeout=300)
            w04_before = sum(1 for ln in pre.stdout.splitlines() if "\tW04\t" in ln)
        except (subprocess.TimeoutExpired, OSError):
            warnings.append("source W04 advisory count unavailable")

        if args.verbose:
            print(f"validate_cmd=bash {validate} validate --file {registry} "
                  f"--today {today.isoformat()}")

        proc = subprocess.run(
            ["bash", str(validate), "validate", "--file", str(registry),
             "--today", today.isoformat()],
            capture_output=True, text=True, timeout=300)
        w04_after = sum(1 for ln in proc.stdout.splitlines() if "\tW04\t" in ln)
        e_findings = sum(1 for ln in proc.stdout.splitlines() if "\tE" in ln)

        if args.commit:
            subprocess.run(["git", "-C", str(dest), "add", "-A"],
                           check=True, capture_output=True)
            subprocess.run(
                ["git", "-C", str(dest), "commit", "-q", "-m",
                 f"scratch census mirror after-state: +{len(rows)} rows "
                 f"({','.join(appended_ids)})"],
                check=True, capture_output=True)

        print(f"mirror={dest}")
        print(f"source_corpus={corpus}")
        print(f"rows_before={len(before_ids)}")
        print(f"rows_appended={len(rows)}")
        print(f"rows_after={len(scan_ids(after_lines))}")
        print(f"ids_appended={','.join(appended_ids)}")
        print(f"rows_sha256={sha256(rows_file)}")
        print(f"source_registry_sha256={source_digest}")
        print(f"mirror_registry_sha256={sha256(registry)}")
        print(f"w04_before={w04_before}")
        print(f"w04_after={w04_after}")
        print(f"e_findings={e_findings}")
        for warning in warnings:
            print(f"WARN {warning}")
        if proc.stdout:
            sys.stdout.write(proc.stdout)
        if proc.stderr:
            sys.stderr.write(proc.stderr)
        print(f"validate_exit={proc.returncode}")
        return 0 if proc.returncode == 0 else proc.returncode


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except BrokenPipeError:
        sys.exit(1)

#!/usr/bin/env python3
# round-76 C1 strict row counter (frozen by the round-76 declaration, before any note exists).
#
# Counts only JD rows of corpus/knowledge/journald-retention-plane-r76.md that satisfy every frozen
# clause below, plus the note's effective-limit block. Reads Git objects (--revision) or a fixture
# mirror (--fixture); the self-test builds synthetic snapshots under one $TMPDIR root and writes
# nothing outside it, so the tool carries no copy of the real corpus and no answer key (round-74
# K1Critic D3 defect). The aggregate prints its verdict line only in the direction the exit code
# proves: a failing self-test prints SELFTEST: FAIL and exits 3 (round-74 routed limit).
#
# Frozen clauses per row: id unique and contiguous from 1; statement >= 12 words; >= 6 distinct
# non-stopword tokens (length >= 4) shared with the row's snapshot text AND shared/total >= 0.5;
# source=S### resolves to a registry row at the same revision; that row's kind is a source kind and
# is not own-work (QUALITY 86); the registry contains NO duplicate S-IDs; snapshot=<name> exists
# under .ufo/waves/round-76/before/src with sha256 == digest; the row's digest equals the digest
# recorded for that snapshot in src/SOURCES.json AND the registry row's source cell contains that
# map URL; the registry row's anchor cell contains the snapshot's basename; quote <= 25 words,
# contains no pipe, and is located verbatim (whitespace-normalized) in the snapshot. Any JD-shaped
# line that does not parse is a malformed-row finding. No snapshot may be cited more than four
# times (half of the eight rows; the rule keeps one file from grounding the whole table).
# The note must also carry the effective-limit block: the heading `## Effective limits on this host`
# followed, before the next `## ` heading, by the literals `SystemMaxUse=256M`,
# `/etc/systemd/journald.conf.d/size.conf`, `effective_limit=256M`, `SystemMaxFileSize=32M`,
# `148.6M` and `.ufo/waves/round-76/before/host.txt`.
# Target: rows == 8 and verified == 8 and distinct sources >= 4 and distinct snapshots >= 4 and the
# effective-limit block present.
#
# Exit map: 0 target met; 1 target missed (including JD_MAP malformed); 3 self-test failed;
# 128 JD_NOTE, JD_REGISTRY or JD_MAP absent. An absent data file in --revision/--fixture mode is
# 128, not 1, so a revision that predates the note reads absent rather than scored.
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

NOTE = "corpus/knowledge/journald-retention-plane-r76.md"
REGISTRY = "corpus/SOURCES.md"
SNAPDIR = ".ufo/waves/round-76/before/src"
MAP = SNAPDIR + "/SOURCES.json"
TARGET_ROWS = 8
TARGET_SOURCES = 4
TARGET_SNAPSHOTS = 4
MIN_WORDS = 12
MIN_TOKENS = 6
MIN_SHARE = 0.5
MIN_QUOTE_WORDS = 4
MAX_QUOTE_WORDS = 25
MAX_SNAPSHOT_REUSE = 4
HOST_HEADING = "## Effective limits on this host"
HOST_LITERALS = [
    "SystemMaxUse=256M",
    "/etc/systemd/journald.conf.d/size.conf",
    "effective_limit=256M",
    "SystemMaxFileSize=32M",
    "148.6M",
    ".ufo/waves/round-76/before/host.txt",
]
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community"}

ROW_RE = re.compile(
    r'^\| JD(?P<n>[0-9]+) \| (?P<stmt>[^|]+) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[^ |]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')
CAND_RE = re.compile(r'^\s*\|\s*JD[0-9]+\s*\|')
SROW_RE = re.compile(r'^\|\s*S(?P<n>[0-9]{3,})\s*\|')
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}")
STOP = set("""
that this with from into than then them they their there these those which while where when
have has had been being were was are its it's not but for and the a an of to in on at by as or
is are do does did can could would should may might must shall will one two three also such
more most less least other others same different only over under about across after before
each every both all any some no nor own same very just even still yet because since until
""".split())


def tokenize(text):
    return {w.lower() for w in WORD_RE.findall(text)} - STOP


def normalize_ws(s):
    return " ".join(s.split())


def parse_registry(text):
    rows = {}
    dups = set()
    for line in text.splitlines():
        line = line.rstrip()
        m = SROW_RE.match(line)
        if not m:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 13:
            continue
        sid = f"S{int(m.group('n')):03d}"
        if sid in rows:
            dups.add(sid)
        rows[sid] = {
            "kind": parts[3],
            "source_cell": parts[2],
            "anchor": parts[6],
        }
    return rows, dups


def load_file(repo, path, revision=None, fixture=None):
    if fixture:
        p = Path(fixture) / path
        if not p.is_file():
            return None
        return p.read_bytes()
    if revision:
        cmd = ["git", "-C", str(repo), "show", f"{revision}:{path}"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            return None
        return res.stdout
    p = Path(repo) / path
    if not p.is_file():
        return None
    return p.read_bytes()


def check_host_block(note_text):
    lines = note_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.rstrip() == HOST_HEADING:
            start = i
            break
    if start is None:
        return [f"host block missing heading {HOST_HEADING}"]
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    block = "\n".join(lines[start:end])
    return [f"host block missing literal {lit}" for lit in HOST_LITERALS if lit not in block]


def evaluate(repo, revision=None, fixture=None):
    raw_map = load_file(repo, MAP, revision, fixture)
    if raw_map is None:
        return 128, "JD_MAP absent", []
    try:
        source_map = json.loads(raw_map.decode("utf-8"))
        if not isinstance(source_map, dict):
            return 1, "JD_MAP malformed: root is not a dict", []
    except Exception as e:
        return 1, f"JD_MAP malformed: {e}", []

    raw_reg = load_file(repo, REGISTRY, revision, fixture)
    if raw_reg is None:
        return 128, "JD_REGISTRY absent", []
    reg_rows, reg_dups = parse_registry(raw_reg.decode("utf-8", errors="replace"))
    if reg_dups:
        return 1, f"JD_REGISTRY duplicate id: {sorted(reg_dups)}", []

    raw_note = load_file(repo, NOTE, revision, fixture)
    if raw_note is None:
        return 128, "JD_NOTE absent", []
    note_text = raw_note.decode("utf-8", errors="replace")

    findings = []
    parsed_rows = []
    seen_ids = set()
    reuse_count = {}
    sources_used = set()
    snapshots_used = set()

    for line_no, line in enumerate(note_text.splitlines(), start=1):
        if not CAND_RE.match(line):
            continue
        m = ROW_RE.match(line)
        if not m:
            findings.append((line_no, "malformed row shape"))
            continue
        n = int(m.group("n"))
        stmt = m.group("stmt").strip()
        src = m.group("src")
        snap = m.group("snap")
        digest = m.group("digest")
        quote = m.group("quote")

        if n in seen_ids:
            findings.append((line_no, f"duplicate JD id {n}"))
        seen_ids.add(n)

        if len(stmt.split()) < MIN_WORDS:
            findings.append((line_no, f"short statement ({len(stmt.split())} < {MIN_WORDS})"))

        if snap not in source_map:
            findings.append((line_no, f"unknown snapshot {snap}"))
            continue
        snap_info = source_map[snap]
        if not isinstance(snap_info, dict) or snap_info.get("sha256") != digest:
            findings.append((line_no, f"digest mismatch for {snap}"))
            continue

        raw_snap = load_file(repo, f"{SNAPDIR}/{snap}", revision, fixture)
        if raw_snap is None:
            findings.append((line_no, f"missing snapshot file {snap}"))
            continue
        if hashlib.sha256(raw_snap).hexdigest() != digest:
            findings.append((line_no, f"snapshot {snap} byte mismatch"))
            continue

        snap_text = raw_snap.decode("utf-8", errors="replace")
        stmt_tokens = tokenize(stmt)
        shared = stmt_tokens & tokenize(snap_text)
        if len(shared) < MIN_TOKENS:
            findings.append((line_no, f"too few shared tokens ({len(shared)} < {MIN_TOKENS})"))
        if stmt_tokens and (len(shared) / len(stmt_tokens)) < MIN_SHARE:
            findings.append((line_no, f"shared share too low ({len(shared)/len(stmt_tokens):.2f} < {MIN_SHARE})"))

        if src not in reg_rows:
            findings.append((line_no, f"source {src} not in registry"))
        else:
            rinfo = reg_rows[src]
            if rinfo["kind"] not in KINDS:
                findings.append((line_no, f"source {src} invalid kind {rinfo['kind']}"))
            map_url = snap_info.get("url", "")
            if map_url and map_url not in rinfo["source_cell"]:
                findings.append((line_no, f"registry row {src} does not cite URL {map_url}"))
            if snap not in rinfo["anchor"]:
                findings.append((line_no, f"registry row {src} does not anchor {snap}"))

        qwords = quote.split()
        if not (MIN_QUOTE_WORDS <= len(qwords) <= MAX_QUOTE_WORDS):
            findings.append((line_no, f"quote length out of bounds ({len(qwords)})"))
        if "|" in quote:
            findings.append((line_no, "quote contains pipe"))
        quote_norm = normalize_ws(quote)
        if quote_norm and quote_norm not in normalize_ws(snap_text):
            findings.append((line_no, f"quote not located in snapshot {snap}"))

        reuse_count[snap] = reuse_count.get(snap, 0) + 1
        if reuse_count[snap] > MAX_SNAPSHOT_REUSE:
            findings.append((line_no, f"snapshot {snap} cited {reuse_count[snap]} > {MAX_SNAPSHOT_REUSE}"))

        sources_used.add(src)
        snapshots_used.add(snap)
        parsed_rows.append(n)

    if parsed_rows != list(range(1, len(parsed_rows) + 1)):
        findings.append((0, f"non-contiguous IDs: {parsed_rows}"))

    host_findings = check_host_block(note_text)
    findings.extend((0, f) for f in host_findings)

    verified = len(parsed_rows) if not findings else 0
    met = (
        len(parsed_rows) == TARGET_ROWS
        and len(findings) == 0
        and len(sources_used) >= TARGET_SOURCES
        and len(snapshots_used) >= TARGET_SNAPSHOTS
        and not host_findings
    )
    summary = {
        "JD_ROWS": len(parsed_rows),
        "JD_VERIFIED": verified,
        "JD_SOURCES": len(sources_used),
        "JD_SNAPSHOTS": len(snapshots_used),
        "JD_HOST": 1 if not host_findings else 0,
        "JD_MALFORMED": len(findings),
        "met": 1 if met else 0,
    }
    return (0 if met else 1), summary, findings


def run_selftest():
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        snap_dir = tdp / SNAPDIR
        snap_dir.mkdir(parents=True, exist_ok=True)

        s1_text = ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu "
                   "nu xi omicron pi rho sigma tau upsilon phi chi psi omega.")
        s2_text = ("The manager merges job types and drops redundant entries before applying "
                   "the transaction across dependency edges and ordering constraints.")
        s3_text = ("Job collapse maps try restart onto restart while the unit stays active or "
                   "activating, otherwise onto nop, and reload variants follow the same shape.")
        s4_text = ("Vacuum removes the oldest archived journal files until the disk space they "
                   "use falls below the specified size, and rotate archives active files first.")

        snaps = {"syn-alpha.c": s1_text, "syn-beta.c": s2_text,
                 "syn-gamma.h": s3_text, "syn-delta.xml": s4_text}
        source_map = {}
        for name, text in snaps.items():
            (snap_dir / name).write_text(text, encoding="utf-8")
            source_map[name] = {
                "url": f"https://example.org/test/{name}",
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "tag": "vtest",
                "bytes": len(text),
            }
        (snap_dir / "SOURCES.json").write_text(json.dumps(source_map), encoding="utf-8")

        def row(n, stmt, src, snap, quote):
            return (f'| JD{n} | {stmt} | source={src} | snapshot={snap} | '
                    f'digest={source_map[snap]["sha256"]} | quote="{quote}" |')

        reg_lines = [
            "# SOURCES",
            "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
            f"| S501 | Syn Alpha code — https://example.org/test/syn-alpha.c | code | A | scope | syn-alpha.c lines 1-10 | test | mined | 2026-11-04 | on-release | {NOTE} |",
            f"| S502 | Syn Beta code — https://example.org/test/syn-beta.c | code | A | scope | syn-beta.c lines 1-10 | test | mined | 2026-11-04 | on-release | {NOTE} |",
            f"| S503 | Syn Gamma header — https://example.org/test/syn-gamma.h | code | A | scope | syn-gamma.h lines 1-10 | test | mined | 2026-11-04 | on-release | {NOTE} |",
            f"| S504 | Syn Delta xml — https://example.org/test/syn-delta.xml | docs | A | scope | syn-delta.xml lines 1-10 | test | mined | 2026-11-04 | on-release | {NOTE} |",
        ]
        host_block = [
            "",
            HOST_HEADING,
            "",
            "SystemMaxUse=256M from `/etc/systemd/journald.conf.d/size.conf`; effective_limit=256M;",
            "SystemMaxFileSize=32M; observed 148.6M; receipt `.ufo/waves/round-76/before/host.txt`.",
            "",
        ]
        control_rows = [
            row(1, "transaction alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu", "S501", "syn-alpha.c", "alpha beta gamma delta epsilon zeta"),
            row(2, "transaction alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu omega", "S501", "syn-alpha.c", "iota kappa lambda mu nu xi"),
            row(3, "The manager merges job types and drops redundant entries before applying the transaction", "S502", "syn-beta.c", "merges job types and drops redundant entries"),
            row(4, "The manager merges job types and drops redundant entries across dependency edges and ordering", "S502", "syn-beta.c", "applying the transaction across dependency edges"),
            row(5, "Job collapse maps try restart onto restart while the unit stays active or activating otherwise", "S503", "syn-gamma.h", "maps try restart onto restart while"),
            row(6, "Job collapse maps try restart onto restart while the unit stays active or activating likewise", "S503", "syn-gamma.h", "reload variants follow the same shape"),
            row(7, "Vacuum removes the oldest archived journal files until the disk space they use falls below", "S504", "syn-delta.xml", "removes the oldest archived journal files until the disk space"),
            row(8, "Vacuum removes the oldest archived journal files until the disk space they use falls short", "S504", "syn-delta.xml", "rotate archives active files first"),
        ]
        note_path = tdp / NOTE
        reg_path = tdp / REGISTRY
        note_path.parent.mkdir(parents=True, exist_ok=True)
        reg_path.parent.mkdir(parents=True, exist_ok=True)

        def reset():
            note_path.write_text("\n".join(control_rows + host_block) + "\n", encoding="utf-8")
            reg_path.write_text("\n".join(reg_lines) + "\n", encoding="utf-8")
            (snap_dir / "SOURCES.json").write_text(json.dumps(source_map), encoding="utf-8")

        cases = []
        cases.append(("CONTROL", reset, 0))
        cases.append(("SHORT-STMT", lambda: note_path.write_text(
            "\n".join([control_rows[0].replace(
                "transaction alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu",
                "transaction alpha beta gamma delta")] + control_rows[1:] + host_block) + "\n",
            encoding="utf-8"), 1))
        cases.append(("ABSENT-QUOTE", lambda: note_path.write_text(
            "\n".join([control_rows[0].replace(
                'quote="alpha beta gamma delta epsilon zeta"', 'quote="no such words here"')]
                + control_rows[1:] + host_block) + "\n", encoding="utf-8"), 1))
        cases.append(("QUOTE-TOO-LONG", lambda: note_path.write_text(
            "\n".join([control_rows[0].replace(
                'quote="alpha beta gamma delta epsilon zeta"',
                'quote="' + " ".join(["word"] * 26) + '"')]
                + control_rows[1:] + host_block) + "\n", encoding="utf-8"), 1))
        cases.append(("NON-CONTIGUOUS", lambda: note_path.write_text(
            "\n".join([control_rows[0].replace("| JD1 |", "| JD2 |")] + control_rows[1:] + host_block) + "\n",
            encoding="utf-8"), 1))
        cases.append(("UNREGISTERED-SRC", lambda: note_path.write_text(
            "\n".join([control_rows[0].replace("source=S501", "source=S999")] + control_rows[1:] + host_block) + "\n",
            encoding="utf-8"), 1))
        cases.append(("SNAPSHOT-REUSE-5", lambda: note_path.write_text(
            "\n".join(control_rows[:4] + [
                control_rows[4].replace(
                    "| source=S503 | snapshot=syn-gamma.h | digest=" + source_map["syn-gamma.h"]["sha256"] + ' | quote="maps try restart onto restart while"',
                    "| source=S501 | snapshot=syn-alpha.c | digest=" + source_map["syn-alpha.c"]["sha256"] + ' | quote="alpha beta gamma delta epsilon zeta"')
            ] + control_rows[5:] + host_block) + "\n", encoding="utf-8"), 1))
        cases.append(("UNGROUNDED", lambda: note_path.write_text(
            "\n".join([control_rows[0].replace(
                "transaction alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu",
                "completely arbitrary words sharing nothing with the synthetic file")] + control_rows[1:] + host_block) + "\n",
            encoding="utf-8"), 1))
        cases.append(("MALFORMED-ROW", lambda: note_path.write_text(
            "\n".join(["| JD1 | malformed line without fields |"] + control_rows[1:] + host_block) + "\n",
            encoding="utf-8"), 1))
        cases.append(("DIGEST-SWAP", lambda: note_path.write_text(
            "\n".join([control_rows[0].replace(
                source_map["syn-alpha.c"]["sha256"], "0" * 64)] + control_rows[1:] + host_block) + "\n",
            encoding="utf-8"), 1))
        cases.append(("OWN-WORK-SOURCE", lambda: reg_path.write_text(
            "\n".join([l.replace("| code |", "| own-work |") if "S501" in l else l for l in reg_lines])
            + "\n", encoding="utf-8"), 1))
        cases.append(("DUPLICATE-REGISTRY-ID", lambda: reg_path.write_text(
            "\n".join(reg_lines + [reg_lines[-1].replace("S504", "S501")]) + "\n",
            encoding="utf-8"), 1))
        cases.append(("HOST-BLOCK-MISSING", lambda: note_path.write_text(
            "\n".join(control_rows) + "\n", encoding="utf-8"), 1))
        cases.append(("NON-MAP-MAPFILE", lambda: (snap_dir / "SOURCES.json").write_text(
            '["not", "a", "map"]', encoding="utf-8"), 1))

        passed = 0
        failures = []
        for name, setup, expected_rc in cases:
            reset()
            setup()
            rc, summary, _ = evaluate(tdp, fixture=tdp)
            if rc == expected_rc:
                passed += 1
            else:
                failures.append(f"{name}: expected rc {expected_rc}, got {rc} ({summary})")

        if failures:
            for f in failures:
                print(f"SELFTEST-FAIL {f}", file=sys.stderr)
            print(f"SELFTEST: FAIL ({len(cases)} cases, {passed} passed, {len(failures)} failed)")
            return 3

        print(f"SELFTEST: PASS ({len(cases)} cases, {passed} passed, 0 failed)")
        return 0


def main():
    parser = argparse.ArgumentParser(description="round-76 C1 row counter")
    parser.add_argument("--revision", help="git revision to inspect")
    parser.add_argument("--fixture", help="fixture directory to inspect")
    parser.add_argument("--selftest", action="store_true", help="run hermetic self-test")
    parser.add_argument("--repo", default=".", help="repo directory")
    args = parser.parse_args()

    if args.selftest:
        sys.exit(run_selftest())

    rc, summary, findings = evaluate(args.repo, args.revision, args.fixture)
    if isinstance(summary, str):
        print(summary)
        sys.exit(rc)
    print(" ".join(f"{k}={v}" for k, v in summary.items()))
    for line_no, msg in findings:
        print(f"  line {line_no}: {msg}", file=sys.stderr)
    sys.exit(rc)


if __name__ == "__main__":
    main()

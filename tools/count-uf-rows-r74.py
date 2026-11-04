#!/usr/bin/env python3
# round-74 C1 strict row counter (frozen by the round-74 declaration, before any note exists).
#
# Counts only UF rows of corpus/knowledge/systemd-unit-fragment-plane-r74.md that satisfy every
# frozen clause below. Reads Git objects (--revision) or a fixture mirror (--fixture); the
# self-test creates synthetic snapshots into one $TMPDIR root and writes nothing outside it
# (answering K1Critic D2: no real-corpus answer key inside the tool).
#
# Frozen clauses per row: id unique and contiguous from 1; statement >= 12 words; >= 6 distinct
# non-stopword tokens (length >= 4) shared with the row's snapshot text AND shared/total >= 0.5;
# source=S### resolves to a registry row at the same revision; that row's kind is a source kind
# and is not own-work (QUALITY 86: an own-work row grounds host observations, never a rule);
# the registry contains NO duplicate S-IDs (answering E1Counter §D2); snapshot=<name> exists under
# .ufo/waves/round-74/before/src with sha256 == digest; the row's digest equals the digest recorded
# for that snapshot in src/SOURCES.json AND the registry row's source cell contains that map URL;
# the registry row's anchor cell contains the snapshot's basename; quote <= 25 words, contains no
# pipe, and is located verbatim (whitespace-normalized) in the snapshot. Any UF-shaped line that
# does not parse is a malformed-row finding. No snapshot may be cited more than twice.
# Target: rows == 6 and verified == 6 and distinct sources >= 3 and distinct snapshots >= 3.
#
# Exit map: 0 target met; 1 target missed (including UF_MAP malformed); 2 cannot evaluate under
# --selftest only ($TMPDIR names no directory, or is /tmp); 3 self-test failed; 128 UF_NOTE,
# UF_REGISTRY or UF_MAP absent. An absent data file in --revision/--fixture mode is 128, not 2.
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

NOTE = "corpus/knowledge/systemd-unit-fragment-plane-r74.md"
REGISTRY = "corpus/SOURCES.md"
SNAPDIR = ".ufo/waves/round-74/before/src"
MAP = SNAPDIR + "/SOURCES.json"
TARGET_ROWS = 6
TARGET_SOURCES = 3
TARGET_SNAPSHOTS = 3
MIN_WORDS = 12
MIN_TOKENS = 6
MIN_SHARE = 0.5
MIN_QUOTE_WORDS = 4
MAX_QUOTE_WORDS = 25
MAX_SNAPSHOT_REUSE = 2
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community"}
BASE_URL = "https://raw.githubusercontent.com/systemd/systemd/v262/"

ROW_RE = re.compile(
    r'^\| UF(?P<n>[0-9]+) \| (?P<stmt>[^|]+) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[^ |]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')
CAND_RE = re.compile(r'^\s*\|\s*UF[0-9]+\s*\|')
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
            "title": parts[2],
            "kind": parts[3],
            "tier": parts[4],
            "location": parts[6],
            "status": parts[8],
            "anchor": parts[6],
            "source_cell": parts[2],
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


def evaluate(repo, revision=None, fixture=None):
    raw_map = load_file(repo, MAP, revision, fixture)
    if raw_map is None:
        return 128, "UF_MAP absent", {}
    try:
        source_map = json.loads(raw_map.decode("utf-8"))
        if not isinstance(source_map, dict):
            return 1, "UF_MAP malformed: root is not a dict", {}
    except Exception as e:
        return 1, f"UF_MAP malformed: {e}", {}

    raw_reg = load_file(repo, REGISTRY, revision, fixture)
    if raw_reg is None:
        return 128, "UF_REGISTRY absent", {}
    reg_rows, reg_dups = parse_registry(raw_reg.decode("utf-8", errors="replace"))
    if reg_dups:
        return 1, f"UF_REGISTRY duplicate id: {sorted(reg_dups)}", {}

    raw_note = load_file(repo, NOTE, revision, fixture)
    if raw_note is None:
        return 128, "UF_NOTE absent", {}
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
            findings.append((line_no, f"duplicate UF id {n}"))
        seen_ids.add(n)

        words = stmt.split()
        if len(words) < MIN_WORDS:
            findings.append((line_no, f"short statement ({len(words)} < {MIN_WORDS})"))

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
        actual_digest = hashlib.sha256(raw_snap).hexdigest()
        if actual_digest != digest:
            findings.append((line_no, f"snapshot {snap} byte mismatch"))
            continue

        snap_text = raw_snap.decode("utf-8", errors="replace")
        snap_norm = normalize_ws(snap_text)

        stmt_tokens = tokenize(stmt)
        snap_tokens = tokenize(snap_text)
        shared = stmt_tokens & snap_tokens
        if len(shared) < MIN_TOKENS:
            findings.append((line_no, f"too few shared tokens ({len(shared)} < {MIN_TOKENS})"))
        if stmt_tokens and (len(shared) / len(stmt_tokens)) < MIN_SHARE:
            findings.append((line_no, f"shared share too low ({len(shared)/len(stmt_tokens):.2f} < {MIN_SHARE})"))

        if src not in reg_rows:
            findings.append((line_no, f"source {src} not in registry"))
        else:
            rinfo = reg_rows[src]
            if rinfo["kind"] not in KINDS or rinfo["kind"] == "own-work":
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
        if quote_norm and quote_norm not in snap_norm:
            findings.append((line_no, f"quote not located in snapshot {snap}"))

        reuse_count[snap] = reuse_count.get(snap, 0) + 1
        if reuse_count[snap] > MAX_SNAPSHOT_REUSE:
            findings.append((line_no, f"snapshot {snap} cited {reuse_count[snap]} > {MAX_SNAPSHOT_REUSE}"))

        sources_used.add(src)
        snapshots_used.add(snap)
        parsed_rows.append(n)

    if parsed_rows != list(range(1, len(parsed_rows) + 1)):
        findings.append((0, f"non-contiguous IDs: {parsed_rows}"))

    verified = len(parsed_rows) if not findings else 0
    met = (
        len(parsed_rows) == TARGET_ROWS
        and len(findings) == 0
        and len(sources_used) >= TARGET_SOURCES
        and len(snapshots_used) >= TARGET_SNAPSHOTS
    )
    summary = {
        "UF_ROWS": len(parsed_rows),
        "UF_VERIFIED": verified,
        "UF_SOURCES": len(sources_used),
        "UF_SNAPSHOTS": len(snapshots_used),
        "UF_MALFORMED": len(findings),
        "met": 1 if met else 0,
        "findings": findings,
    }
    rc = 0 if met else 1
    return rc, summary, findings


def run_selftest():
    # Synthetic test fixture (addressing K1Critic D2: no real answer key in tool)
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        snap_dir = tdp / SNAPDIR
        snap_dir.mkdir(parents=True, exist_ok=True)

        s1_text = "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau."
        s2_text = "The manager shall resolve lookup paths in priority order rejecting alias cycles and loops."
        s3_text = "Systemd units define execution parameters masks and socket activation dependencies across directories and lookup paths."

        snaps = {
            "syn-alpha.c": s1_text,
            "syn-beta.c": s2_text,
            "syn-gamma.h": s3_text,
        }
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

        reg_lines = [
            "# SOURCES",
            "| ID | Title | Kind | Tier | Scope | Location | Summary | Status | Date | Recheck | Used-by | Notes |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|",
            f"| S401 | Syn Alpha docs — https://example.org/test/syn-alpha.c | code | A | scope | syn-alpha.c lines 1-10 | test | mined | 2026-11-04 | on-release | {NOTE} | |",
            f"| S402 | Syn Beta code — https://example.org/test/syn-beta.c | code | A | scope | syn-beta.c lines 1-10 | test | mined | 2026-11-04 | on-release | {NOTE} | |",
            f"| S403 | Syn Gamma header — https://example.org/test/syn-gamma.h | code | A | scope | syn-gamma.h lines 1-10 | test | mined | 2026-11-04 | on-release | {NOTE} | |",
        ]
        reg_path = tdp / REGISTRY
        reg_path.parent.mkdir(parents=True, exist_ok=True)
        reg_path.write_text("\n".join(reg_lines) + "\n", encoding="utf-8")

        control_rows = [
            f'| UF1 | Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron | source=S401 | snapshot=syn-alpha.c | digest={source_map["syn-alpha.c"]["sha256"]} | quote="Alpha beta gamma delta epsilon" |',
            f'| UF2 | Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi pi rho | source=S401 | snapshot=syn-alpha.c | digest={source_map["syn-alpha.c"]["sha256"]} | quote="zeta eta theta iota kappa" |',
            f'| UF3 | The manager shall resolve lookup paths in priority order rejecting alias cycles | source=S402 | snapshot=syn-beta.c | digest={source_map["syn-beta.c"]["sha256"]} | quote="resolve lookup paths in priority" |',
            f'| UF4 | The manager shall resolve lookup paths in priority order rejecting loops cleanly | source=S402 | snapshot=syn-beta.c | digest={source_map["syn-beta.c"]["sha256"]} | quote="order rejecting alias cycles and" |',
            f'| UF5 | Systemd units define execution parameters masks and socket activation dependencies across directories and lookup paths | source=S403 | snapshot=syn-gamma.h | digest={source_map["syn-gamma.h"]["sha256"]} | quote="units define execution parameters masks" |',
            f'| UF6 | Systemd units define execution parameters masks and socket activation dependencies across directories and lookup cleanly | source=S403 | snapshot=syn-gamma.h | digest={source_map["syn-gamma.h"]["sha256"]} | quote="and socket activation dependencies" |',
        ]
        note_path = tdp / NOTE
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text("\n".join(control_rows) + "\n", encoding="utf-8")

        cases = [
            ("CONTROL", None, 0),
            ("SHORT-STMT", lambda lines: [lines[0].replace("Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron", "Alpha beta gamma delta")] + lines[1:], 1),
            ("ABSENT-QUOTE", lambda lines: [lines[0].replace('quote="Alpha beta gamma delta epsilon"', 'quote="Not in snapshot text"')] + lines[1:], 1),
            ("QUOTE-TOO-LONG", lambda lines: [lines[0].replace('quote="Alpha beta gamma delta epsilon"', 'quote="' + ' '.join(['word']*26) + '"')] + lines[1:], 1),
            ("NON-CONTIGUOUS", lambda lines: [lines[0].replace("UF1", "UF2")] + lines[1:], 1),
            ("UNREGISTERED-SRC", lambda lines: [lines[0].replace("source=S401", "source=S999")] + lines[1:], 1),
            ("SNAPSHOT-REUSE-3", lambda lines: lines[:4] + [lines[4].replace("syn-gamma.h", "syn-alpha.c").replace(source_map["syn-gamma.h"]["sha256"], source_map["syn-alpha.c"]["sha256"]).replace("source=S403", "source=S401").replace('quote="units define execution parameters masks"', 'quote="Alpha beta gamma delta epsilon"')] + lines[5:], 1),
            ("UNGROUNDED", lambda lines: [lines[0].replace("Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron", "completely arbitrary words that share nothing with the underlying synthetic file contents")] + lines[1:], 1),
            ("MALFORMED-ROW", lambda lines: ["| UF1 | malformed line without fields |"] + lines[1:], 1),
            ("DIGEST-SWAP", lambda lines: [lines[0].replace(source_map["syn-alpha.c"]["sha256"], "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")] + lines[1:], 1),
            ("OWN-WORK-SOURCE", None, 1),
            ("DUPLICATE-REGISTRY-ID", None, 1),
            ("NON-MAP-MAPFILE", None, 1),
        ]

        passed = 0
        failed = 0
        for name, mutator, expected_rc in cases:
            if name == "CONTROL":
                note_path.write_text("\n".join(control_rows) + "\n", encoding="utf-8")
                reg_path.write_text("\n".join(reg_lines) + "\n", encoding="utf-8")
                (snap_dir / "SOURCES.json").write_text(json.dumps(source_map), encoding="utf-8")
                rc, summary, _ = evaluate(tdp, fixture=tdp)
            elif name == "OWN-WORK-SOURCE":
                bad_reg = [l.replace("| code |", "| own-work |") if "S401" in l else l for l in reg_lines]
                reg_path.write_text("\n".join(bad_reg) + "\n", encoding="utf-8")
                note_path.write_text("\n".join(control_rows) + "\n", encoding="utf-8")
                rc, summary, _ = evaluate(tdp, fixture=tdp)
                reg_path.write_text("\n".join(reg_lines) + "\n", encoding="utf-8")
            elif name == "DUPLICATE-REGISTRY-ID":
                bad_reg = reg_lines + [reg_lines[-1].replace("S403", "S401")]
                reg_path.write_text("\n".join(bad_reg) + "\n", encoding="utf-8")
                note_path.write_text("\n".join(control_rows) + "\n", encoding="utf-8")
                rc, summary, _ = evaluate(tdp, fixture=tdp)
                reg_path.write_text("\n".join(reg_lines) + "\n", encoding="utf-8")
            elif name == "NON-MAP-MAPFILE":
                (snap_dir / "SOURCES.json").write_text("[\"not\", \"a\", \"map\"]", encoding="utf-8")
                rc, summary, _ = evaluate(tdp, fixture=tdp)
                (snap_dir / "SOURCES.json").write_text(json.dumps(source_map), encoding="utf-8")
            else:
                mut_lines = mutator(control_rows)
                note_path.write_text("\n".join(mut_lines) + "\n", encoding="utf-8")
                rc, summary, _ = evaluate(tdp, fixture=tdp)
                note_path.write_text("\n".join(control_rows) + "\n", encoding="utf-8")

            if rc == expected_rc:
                passed += 1
            else:
                failed += 1
                print(f"CASE {name}: expected rc {expected_rc}, got {rc} (summary={summary})", file=sys.stderr)

        print(f"SELFTEST: PASS ({len(cases)} cases, {passed} passed, {failed} failed)")
        return 0 if failed == 0 else 3


def main():
    parser = argparse.ArgumentParser(description="round-74 C1 row counter")
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
    s_line = " ".join(f"{k}={v}" for k, v in summary.items() if k != "findings")
    print(s_line)
    if findings:
        for lno, msg in findings:
            print(f"  line {lno}: {msg}", file=sys.stderr)
    sys.exit(rc)


if __name__ == "__main__":
    main()

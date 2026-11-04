#!/usr/bin/env python3
# round-76 C2 routed-and-drift checker (frozen by the round-76 declaration, before any repair exists).
#
# Closes the six routed defects the round-75 non-author closure filed for this lane's next round
# (`corpus/lessons/round-75-verifier-spotcheck.md` section 7 items 1-6) plus the two stale journald
# negative claims this round's host probe found (`journal-boot-plane.md` r3 `[unknown]` and
# `degraded-triage-r4.md` "no retention policy configured anywhere"). Each item is one appended
# record in committed bytes; the checker reads only committed text (--revision) or a fixture mirror
# (--root) and never writes.
#
# Item 1  R76-S314-SUPERSEDE   a SOURCES.md row whose teaches cell opens `supersedes S314 —` and
#         names both PROPAGATE_STOP and the graceful branch; the round-76 lesson names the row.
# Item 2  R76-JT5-COUNT        the round-75 note carries an erratum block naming eight
#         comma-separated items, ten labels and the split method.
# Item 3  R76-R75-MISTAKE-COUNT the round-76 lesson names five `## Mistakes` rows plus two owed,
#         and `corpus/lessons/round-75.md` has exactly five `- **R75-` rows.
# Item 4  R76-R75-RECEIPT-REPOINT the round-76 lesson names both `e5f5ca9e` and `bd0acc44`, and
#         `.ufo/waves/round-76/before/recheck-r75-at-tip.txt` carries `met=1` and `ROUTED_OK=4/4`.
# Item 5  R76-WAVE-MARKERS     the seven carried wave markers exist in the revision.
# Item 6  R76-QUALITY-WORDING  the round-76 lesson carries the narrowed sentence (no admitted
#         knowledge entry left failing its own re-check).
# Item 7  R76-JD-CONFIG-DRIFT  `journal-boot-plane.md`, `degraded-triage-r4.md` and `boot-plane.md`
#         each carry an appended block naming the size.conf drop-in, SystemMaxUse=256M and the token.
# Item 8  R76-QUALITY-109      `corpus/QUALITY.md` carries criterion 109 naming round-76.md and a
#         recheck command plus cadence for negative host-state claims.
#
# Block rule (frozen): an item's block is the token's own line plus the 80 lines that follow it in
# the same file. A token placed further than 80 lines above its content is a stale finding, not a
# pass. Every token block must also carry a supersede verb (supersede/superseded/supersedes/
# superseding, erratum, correction, corrected, replaced), except item 5 (a file-presence item) and
# item 8 (a criterion definition, not a correction).
#
# Exit map: 0 every item satisfied (`ROUTED_STALE=0 ROUTED_OK=8/8`); 1 one or more stale, with a
# finding line per item and `reason=` one of `absent`, `token`, `need`, `verb`, `rows`, `count`,
# `markers`; 3 self-test failed. An absent file is a stale finding (rc 1), never rc 2.
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WINDOW = 80
VERBS = ("supersede", "superseded", "supersedes", "superseding",
         "erratum", "correction", "corrected", "replaced")
LESSON = "corpus/lessons/round-76.md"
LESSON75 = "corpus/lessons/round-75.md"
NOTE75 = "corpus/knowledge/systemd-job-transaction-plane-r75.md"
REGISTRY = "corpus/SOURCES.md"
QUALITY = "corpus/QUALITY.md"
RECEIPT = ".ufo/waves/round-76/before/recheck-r75-at-tip.txt"
MARKERS = [
    ".ufo/waves/round-66/w1.ready.dispatched",
    ".ufo/waves/round-67/w1.ready.dispatched",
    ".ufo/waves/round-73/w1-run.stderr",
    ".ufo/waves/round-73/w1.ready.dispatched",
    ".ufo/waves/round-74/w1.ready.dispatched",
    ".ufo/waves/round-75/w1.ready",
    ".ufo/waves/round-75/w1.ready.dispatched",
]


def load(root, path, revision=None):
    if revision:
        res = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{path}"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.stdout.decode("utf-8", "replace") if res.returncode == 0 else None
    p = Path(root) / path
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None


def exists(root, path, revision=None):
    if revision:
        res = subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"{revision}:{path}"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0
    return (Path(root) / path).exists()


def token_block(text, token):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if token in line:
            return "\n".join(lines[i:i + WINDOW + 1])
    return None


def has_verb(block):
    low = block.lower()
    return any(v in low for v in VERBS)


def check_block(root, revision, path, token, need_all=(), need_any=(), verb=True):
    text = load(root, path, revision)
    if text is None:
        return f"absent path={path}"
    block = token_block(text, token)
    if block is None:
        return f"token path={path}"
    low = block.lower()
    for item in need_all:
        if item.lower() not in low:
            return f"need path={path} missing={item}"
    for group in need_any:
        if not any(alt.lower() in low for alt in group):
            return f"need path={path} missing_any={group}"
    if verb and not has_verb(block):
        return f"verb path={path}"
    return None


def item1(root, revision):
    text = load(root, REGISTRY, revision)
    if text is None:
        return "absent path=corpus/SOURCES.md"
    found = None
    for line in text.splitlines():
        if not line.startswith("| S"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 13:
            continue
        teaches = parts[7]
        if teaches.lower().startswith("supersedes s314"):
            if "propagate_stop" in line.lower() and "graceful" in line.lower():
                found = parts[1]
            break
    if not found:
        return "rows path=corpus/SOURCES.md missing=supersedes S314 row"
    return check_block(root, revision, LESSON, "R76-S314-SUPERSEDE", need_all=(found,))


def item2(root, revision):
    return check_block(root, revision, NOTE75, "R76-JT5-COUNT",
                       need_all=("eight comma-separated items", "ten labels", "split"))


def item3(root, revision):
    lesson75 = load(root, LESSON75, revision)
    if lesson75 is None:
        return "absent path=corpus/lessons/round-75.md"
    lines = lesson75.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.rstrip() == "## Mistakes":
            start = i
            break
    if start is None:
        return "absent path=corpus/lessons/round-75.md heading=## Mistakes"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    count = sum(1 for line in lines[start:end] if line.startswith("- **R75-"))
    if count != 5:
        return f"count path=corpus/lessons/round-75.md rows={count}"
    return check_block(root, revision, LESSON, "R76-R75-MISTAKE-COUNT",
                       need_all=("five", "two owed"))


def item4(root, revision):
    receipt = load(root, RECEIPT, revision)
    if receipt is None:
        return f"absent path={RECEIPT}"
    for lit in ("met=1", "ROUTED_OK=4/4"):
        if lit not in receipt:
            return f"need path={RECEIPT} missing={lit}"
    return check_block(root, revision, LESSON, "R76-R75-RECEIPT-REPOINT",
                       need_all=("e5f5ca9e", "bd0acc44"))


def item5(root, revision):
    missing = [p for p in MARKERS if not exists(root, p, revision)]
    if missing:
        return f"markers missing={missing[0]}"
    return None


def item6(root, revision):
    return check_block(root, revision, LESSON, "R76-QUALITY-WORDING",
                       need_all=("no admitted knowledge entry is left failing its own re-check",))


def item7(root, revision):
    need = ("/etc/systemd/journald.conf.d/size.conf", "SystemMaxUse=256M", "R76-JD-CONFIG-DRIFT")
    for path in ("corpus/knowledge/journal-boot-plane.md", "corpus/knowledge/degraded-triage-r4.md",
                 "corpus/knowledge/boot-plane.md"):
        reason = check_block(root, revision, path, "R76-JD-CONFIG-DRIFT", need_all=need)
        if reason:
            return reason
    return None


def item8(root, revision):
    text = load(root, QUALITY, revision)
    if text is None:
        return "absent path=corpus/QUALITY.md"
    block = token_block(text, "109.")
    if block is None:
        return "token path=corpus/QUALITY.md"
    low = block.lower()
    for lit in ("round-76.md", "recheck", "cadence"):
        if lit not in low:
            return f"need path=corpus/QUALITY.md missing={lit}"
    return None


ITEMS = [
    ("R76-S314-SUPERSEDE", item1),
    ("R76-JT5-COUNT", item2),
    ("R76-R75-MISTAKE-COUNT", item3),
    ("R76-R75-RECEIPT-REPOINT", item4),
    ("R76-WAVE-MARKERS", item5),
    ("R76-QUALITY-WORDING", item6),
    ("R76-JD-CONFIG-DRIFT", item7),
    ("R76-QUALITY-109", item8),
]


def evaluate(root, revision=None):
    findings = []
    for name, fn in ITEMS:
        reason = fn(root, revision)
        if reason:
            findings.append((name, reason))
    stale = len(findings)
    ok = len(ITEMS) - stale
    summary = {"ROUTED_STALE": stale, "ROUTED_OK": f"{ok}/{len(ITEMS)}"}
    return (0 if stale == 0 else 1), summary, findings


def run_selftest():
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        control = {
            "corpus/lessons/round-76.md": "\n".join([
                "# Round 76",
                "",
                "## r75 routed repairs",
                "R76-S314-SUPERSEDE supersedes S322 — the PROPAGATE_STOP branch is scoped; the graceful branch may enqueue a direct JOB_RESTART.",
                "R76-JT5-COUNT correction: the JT5 row has eight comma-separated items; ten labels after the split method.",
                "R76-R75-MISTAKE-COUNT correction: round-75.md carries five ## Mistakes rows plus two owed rows.",
                "R76-R75-RECEIPT-REPOINT correction: receipts re-run at bd0acc44 after the e5f5ca9e receipt.",
                "R76-QUALITY-WORDING correction: no admitted knowledge entry is left failing its own re-check.",
                "",
            ]),
            "corpus/lessons/round-75.md": "\n".join([
                "# Round 75", "## Mistakes",
                "- **R75-A** x", "- **R75-B** x", "- **R75-C** x", "- **R75-D** x", "- **R75-E** x",
            ]),
            "corpus/knowledge/systemd-job-transaction-plane-r75.md": "\n".join([
                "# note",
                "R76-JT5-COUNT erratum: the row has eight comma-separated items and ten labels; the split method splits the two compound items.",
            ]),
            "corpus/knowledge/journal-boot-plane.md": "\n".join([
                "# plane",
                "R76-JD-CONFIG-DRIFT erratum: `/etc/systemd/journald.conf.d/size.conf` sets SystemMaxUse=256M.",
            ]),
            "corpus/knowledge/degraded-triage-r4.md": "\n".join([
                "# triage",
                "R76-JD-CONFIG-DRIFT correction: `/etc/systemd/journald.conf.d/size.conf` sets SystemMaxUse=256M.",
            ]),
            "corpus/knowledge/boot-plane.md": "\n".join([
                "# boot",
                "R76-JD-CONFIG-DRIFT erratum: `/etc/systemd/journald.conf.d/size.conf` sets SystemMaxUse=256M.",
            ]),
            "corpus/QUALITY.md": "\n".join([
                "# QUALITY",
                "109. **A negative host-state claim names its recheck command and cadence (R76-JD-CONFIG-DRIFT):** the criterion cites corpus/lessons/round-76.md and requires a recheck command with a cadence.",
            ]),
            "corpus/SOURCES.md": "\n".join([
                "# SOURCES",
                "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
                "|---|---|---|---|---|---|---|---|---|---|---|",
                "| S322 | systemd v262 transaction.c — https://example.org/t.c | code | A | PROPAGATE_STOP and the graceful branch | t.c lines 1-2 | supersedes S314 — scopes restart propagation to PROPAGATE_STOP and names the graceful branch | mined | 2026-11-04 | on-release | corpus/lessons/round-76.md |",
            ]),
            RECEIPT: "count-jt-rows-r75.py at bd0acc44: met=1\ncheck-r74-routed-r75.py at bd0acc44: ROUTED_OK=4/4\n",
        }
        for path, body in control.items():
            p = tdp / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body + "\n", encoding="utf-8")
        for path in MARKERS:
            p = tdp / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("{}\n", encoding="utf-8")

        def reset():
            for path, body in control.items():
                p = tdp / path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body + "\n", encoding="utf-8")
            for path in MARKERS:
                p = tdp / path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("{}\n", encoding="utf-8")

        def mutate(path, old, new):
            def fn():
                p = tdp / path
                text = p.read_text(encoding="utf-8")
                assert old in text, (path, old)
                p.write_text(text.replace(old, new), encoding="utf-8")
            return fn

        cases = [
            ("CONTROL", reset, 0),
            ("S314-ROW-MISSING", mutate("corpus/SOURCES.md", "supersedes S314", "supersedes S399"), 1),
            ("JT5-COUNT-MISSING", mutate("corpus/knowledge/systemd-job-transaction-plane-r75.md", "eight comma-separated items", "nine comma items"), 1),
            ("MISTAKE-COUNT-WRONG", mutate("corpus/lessons/round-75.md", "- **R75-E** x\n", ""), 1),
            ("RECEIPT-MISSING", mutate(RECEIPT, "ROUTED_OK=4/4", "ROUTED_OK=3/4"), 1),
            ("MARKER-ABSENT", lambda: (tdp / MARKERS[0]).unlink(), 1),
            ("QUALITY-WORDING-WRONG", mutate("corpus/lessons/round-76.md", "no admitted knowledge entry is left failing its own re-check", "no admitted artifact is left failing its own re-check"), 1),
            ("DRIFT-ONE-CARRIER", mutate("corpus/knowledge/degraded-triage-r4.md", "R76-JD-CONFIG-DRIFT", "OTHER"), 1),
            ("QUALITY-109-MISSING", mutate("corpus/QUALITY.md", "cadence", "schedule"), 1),
            ("DECOY-DISTANT", lambda: (
                (tdp / "corpus/lessons/round-76.md").write_text(
                    "R76-S314-SUPERSEDE\n" + "\n" * 120 + control["corpus/lessons/round-76.md"] + "\n",
                    encoding="utf-8")), 1),
        ]

        passed = 0
        failures = []
        for name, setup, expected_rc in cases:
            reset()
            setup()
            rc, summary, _ = evaluate(tdp)
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
    parser = argparse.ArgumentParser(description="round-76 C2 routed-and-drift checker")
    parser.add_argument("--revision", help="git revision to inspect")
    parser.add_argument("--root", help="fixture root to inspect")
    parser.add_argument("--selftest", action="store_true", help="run hermetic self-test")
    parser.add_argument("--repo", default=".", help="repo directory")
    args = parser.parse_args()

    if args.selftest:
        sys.exit(run_selftest())

    root = args.root or args.repo
    rc, summary, findings = evaluate(root, args.revision)
    print(" ".join(f"{k}={v}" for k, v in summary.items()))
    for name, reason in findings:
        print(f"  {name} reason={reason}", file=sys.stderr)
    sys.exit(rc)


if __name__ == "__main__":
    main()

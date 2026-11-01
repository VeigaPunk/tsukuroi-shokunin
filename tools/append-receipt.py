#!/usr/bin/env python3
"""append-receipt — verify that record-file changes between two revisions are pure appends.

Round 60, C3 (calibration). The routed r59 closure carry-in named the class: the round-55..59
plumbing landed SCORECARD.md / SKILL.md / corpus/SOURCES.md with their line endings rewritten
(all-LF bases became CRLF or mixed), inflating byte diffs and sha pins while the CONTENT was
append-only modulo CR. The fleet precedent is tameshi r63's tools/additivity-receipt.py (the
convention routed by the r59 closure); this is tsukuroi's own implementation over its own record
files — tameshi keeps no gate ownership here (ADJ-07: method advice, not gate transfer).

Contract
  python tools/append-receipt.py --repo <dir> --base <rev> --tip <rev> --file P [--file P2 ...]
        [--require-raw] [--json]
    Reads the base and tip blobs by git plumbing (cat-file; the worktree is never consulted)
    and reports, per file:
      old_only_raw / old_only_norm   members of the base line multiset absent from the tip's,
                                     CR-sensitive and CR-normalized; EMPTY LINES ARE DROPPED ON
                                     BOTH SIDES before these counts (an inserted blank line is
                                     not a content member — the tameshi r63 erratum's set-member
                                     rule). Multiset, not set: duplicating a base line is
                                     new_only, dropping one is old_only.
      new_only_raw / new_only_norm   members of the tip line multiset absent from the base's,
                                     same normalization.
      prefix_ok                      tip bytes start with the base bytes (true byte append;
                                     a mid-file insert reports False with old_only still 0 —
                                     the SOURCES.md id-position row-insert case).
      eol_rewrite_disclosed          old_only_raw > 0 with old_only_norm == 0: the base
                                     content is all there, but its line endings moved.
    Exit map: 0 every file old_only_norm == 0 (and, under --require-raw, old_only_raw == 0 too —
    a disclosed rewrite is still a rewrite); 1 violation (content altered, deleted, or — under
    --require-raw — endings rewritten); 2 could-not-evaluate (usage, bad revision, a file absent
    from BOTH revisions, or a file DELETED at the tip — a deletion arm reports per-file and
    exits 1).

  python tools/append-receipt.py --selftest
    Hermetic arms over a plumbing-built fixture repository (hash-object/mktree/commit-tree/
    update-ref only — the index is never touched, the git-index-is-unreliable host rule):
    clean LF append; CRLF append on a CRLF file; whole-file EOL rewrite (disclosed by default,
    exit 1 under --require-raw); content alteration (exit 1); deletion (exit 1). Prints
    APPEND_RECEIPT_SELFTEST: PASS/FAIL (N cases, N passed, N failed) and exits 0/1.

Write scope: none on the target repo (plumbing reads only); the selftest writes only its own
temporary fixture directory. Spell `python`, not `python3`, on this host (Store alias stub
exits 49 — drift register D8). Owner: tsukuroi.
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import datetime
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2


def die(msg: str, code: int = CANNOT) -> int:
    print(f"append-receipt: {msg}", file=sys.stderr)
    return code


def git(repo: str, *args: str, inp: bytes | None = None) -> bytes:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, input=inp)
    if r.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args[:2])} failed: {r.stderr.decode(errors='replace').strip()[:300]}"
        )
    return r.stdout


def blob(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{rev}:{path}"],
        capture_output=True,
    )
    if r.returncode != 0:
        return None
    return git(repo, "cat-file", "-p", f"{rev}:{path}")


def members(data: bytes) -> collections.Counter:
    """Non-empty line members, as written (CR-sensitive)."""
    return collections.Counter(
        ln for ln in data.split(b"\n") if ln != b""
    )


def members_norm(data: bytes) -> collections.Counter:
    """Non-empty line members after CR normalization (trailing \\r stripped)."""
    return collections.Counter(
        ln[:-1] if ln.endswith(b"\r") else ln
        for ln in data.split(b"\n")
        if (ln[:-1] if ln.endswith(b"\r") else ln) != b""
    )


def diff_counts(base: collections.Counter, tip: collections.Counter) -> tuple[int, int]:
    """old_only (in base, missing from tip) and new_only, multiset semantics."""
    old_only = sum((base - tip).values())
    new_only = sum((tip - base).values())
    return old_only, new_only


def receipt_for(base_bytes: bytes | None, tip_bytes: bytes | None) -> dict:
    if tip_bytes is None:
        return {
            "deleted_at_tip": True,
            "old_only_raw": sum(members(base_bytes or b"").values()),
            "old_only_norm": sum(members_norm(base_bytes or b"").values()),
            "new_only_raw": 0,
            "new_only_norm": 0,
            "prefix_ok": False,
            "eol_rewrite_disclosed": False,
            "clean": False,
        }
    if base_bytes is None:
        return {
            "new_file": True,
            "old_only_raw": 0,
            "old_only_norm": 0,
            "new_only_raw": sum(members(tip_bytes).values()),
            "new_only_norm": sum(members_norm(tip_bytes).values()),
            "prefix_ok": False,
            "eol_rewrite_disclosed": False,
            "clean": True,
        }
    o_raw, n_raw = diff_counts(members(base_bytes), members(tip_bytes))
    o_norm, n_norm = diff_counts(members_norm(base_bytes), members_norm(tip_bytes))
    return {
        "old_only_raw": o_raw,
        "old_only_norm": o_norm,
        "new_only_raw": n_raw,
        "new_only_norm": n_norm,
        "prefix_ok": tip_bytes.startswith(base_bytes),
        "eol_rewrite_disclosed": o_raw > 0 and o_norm == 0,
        "clean": o_norm == 0,
    }


def run_receipt(repo: str, base: str, tip: str, files: list[str], require_raw: bool, as_json: bool) -> int:
    try:
        git(repo, "rev-parse", "--verify", "--quiet", base + "^{commit}")
        git(repo, "rev-parse", "--verify", "--quiet", tip + "^{commit}")
    except RuntimeError as exc:
        return die(str(exc))
    records = {}
    violations = []
    for path in files:
        base_bytes = blob(repo, base, path)
        tip_bytes = blob(repo, tip, path)
        if base_bytes is None and tip_bytes is None:
            return die(f"{path}: absent from both revisions", CANNOT)
        rec = receipt_for(base_bytes, tip_bytes)
        records[path] = rec
        if not rec["clean"] or (require_raw and rec["old_only_raw"] > 0):
            violations.append(path)
        if as_json:
            continue
        flag = "new-file" if rec.get("new_file") else ("DELETED" if rec.get("deleted_at_tip") else "pair")
        print(
            f"{path}: [{flag}] old_only raw={rec['old_only_raw']} norm={rec['old_only_norm']} "
            f"new_only raw={rec['new_only_raw']} norm={rec['new_only_norm']} "
            f"prefix_ok={str(rec['prefix_ok']).lower()} "
            f"eol_rewrite_disclosed={str(rec['eol_rewrite_disclosed']).lower()}"
        )
    code = FAIL if violations else PASS
    if as_json:
        print(json.dumps({"base": base, "tip": tip, "require_raw": require_raw,
                          "files": records, "violations": violations,
                          "status": "PASS" if code == PASS else "FAIL"},
                         sort_keys=True, separators=(",", ":")))
    else:
        verdict = "PASS" if code == PASS else "FAIL"
        extra = " (--require-raw)" if require_raw else ""
        print(f"APPEND_RECEIPT: {verdict}{extra} ({len(files)} files, {len(files) - len(violations)} clean, "
              f"{len(violations)} violation)")
    return code


# --- selftest: a plumbing-only fixture repository -------------------------------------------

def fixture_commit(repo: Path, files: dict[str, bytes], message: str) -> str:
    entries = []
    for name, data in files.items():
        p = subprocess.run(["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                           capture_output=True, input=data)
        if p.returncode != 0:
            raise RuntimeError(p.stderr.decode(errors="replace")[:200])
        entries.append(f"100644 blob {p.stdout.decode().strip()}\t{name}")
    inp = ("\n".join(entries)).encode() + b"\n"
    t = subprocess.run(["git", "-C", str(repo), "mktree"], capture_output=True, input=inp)
    if t.returncode != 0:
        raise RuntimeError(t.stderr.decode(errors="replace")[:200])
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    env = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local",
               GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@local",
               GIT_AUTHOR_DATE=now, GIT_COMMITTER_DATE=now)
    c = subprocess.run(["git", "-C", str(repo), "commit-tree", t.stdout.decode().strip(), "-m", message],
                       capture_output=True, env=env)
    if c.returncode != 0:
        raise RuntimeError(c.stderr.decode(errors="replace")[:200])
    return c.stdout.decode().strip()


def selftest() -> int:
    failures: list[str] = []
    total = 0
    with tempfile.TemporaryDirectory(prefix="append-receipt-selftest-") as td:
        repo = Path(td)
        if subprocess.run(["git", "init", "--quiet", "-b", "master", str(repo)],
                          capture_output=True).returncode != 0:
            return die("git init failed in the selftest sandbox")
        rf = str(repo)

        def check(name: str, got: int, want: int, extra_ok=None) -> None:
            nonlocal total
            total += 1
            if got != want or (extra_ok is not None and not extra_ok):
                failures.append(f"{name}: exit {got}, wanted {want}"
                                + ("" if extra_ok is None or extra_ok else " (payload check failed)"))

        def quiet_run(*args) -> int:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                return run_receipt(*args)

        c1 = fixture_commit(rf, {"log.md": b"alpha\nbeta\n"}, "base LF")
        c2 = fixture_commit(rf, {"log.md": b"alpha\nbeta\ngamma\n"}, "clean append")
        check("clean-LF-append", quiet_run(rf, c1, c2, ["log.md"], False, True), PASS)

        c3 = fixture_commit(rf, {"log.md": b"a\r\nb\r\n"}, "base CRLF")
        c4 = fixture_commit(rf, {"log.md": b"a\r\nb\r\nc\r\n"}, "CRLF append")
        check("CRLF-append", quiet_run(rf, c3, c4, ["log.md"], False, True), PASS)

        c5 = fixture_commit(rf, {"log.md": b"a\nb\n"}, "base LF 2")
        c6 = fixture_commit(rf, {"log.md": b"a\r\nb\r\nc\r\n"}, "whole-file EOL rewrite + append")
        # one declared arm with two binding exits: disclosed (exit 0) by default and a
        # violation (exit 1) under --require-raw — the arm passes only when BOTH hold
        rewrite_default = quiet_run(rf, c5, c6, ["log.md"], False, True)
        rewrite_raw = quiet_run(rf, c5, c6, ["log.md"], True, True)
        check("rewrite-disclosed-then-require-raw",
              PASS if (rewrite_default == PASS and rewrite_raw == FAIL) else FAIL,
              PASS)

        c7 = fixture_commit(rf, {"log.md": b"a\nb\n"}, "base LF 3")
        c8 = fixture_commit(rf, {"log.md": b"a\nX\n"}, "content altered")
        check("alteration", quiet_run(rf, c7, c8, ["log.md"], False, True), FAIL)

        c9 = fixture_commit(rf, {"log.md": b"a\nb\nc\n"}, "base LF 4")
        c10 = fixture_commit(rf, {"log.md": b"a\n"}, "line deleted")
        check("deletion", quiet_run(rf, c9, c10, ["log.md"], False, True), FAIL)

    if failures:
        print(f"APPEND_RECEIPT_SELFTEST: FAIL ({total} cases, {total - len(failures)} passed, "
              f"{len(failures)} failed)")
        for f in failures:
            print(f"  {f}")
        return FAIL
    print(f"APPEND_RECEIPT_SELFTEST: PASS ({total} cases, {total} passed, 0 failed)")
    return PASS


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--base")
    ap.add_argument("--tip")
    ap.add_argument("--file", action="append", dest="files")
    ap.add_argument("--require-raw", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(sys.argv[1:] if argv is None else argv)
    if a.selftest:
        if a.repo or a.base or a.tip or a.files:
            return die("--selftest takes no other arguments")
        return selftest()
    if not (a.repo and a.base and a.tip and a.files):
        return die("--repo, --base, --tip and at least one --file are required")
    return run_receipt(a.repo, a.base, a.tip, a.files, a.require_raw, a.json)


if __name__ == "__main__":
    sys.exit(main())

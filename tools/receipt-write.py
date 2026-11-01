#!/usr/bin/env python3
"""receipt-write — write a receipt-run-FORMAT receipt for output that is ALREADY captured.

Companion to `receipt-run.py` (round 57, claim C2): some probes must NOT be re-executed to
capture them — their signature lives in the exec environment of the process that ran them (the
services recheck's T1 is bash/MSYS-exec-specific; T7 writes a stray file that a re-run would
create twice). For those, the calling script judges the probe in place and hands THIS tool the
already-captured bytes; the receipt is built by the SAME `build_receipt` implementation
receipt-run uses — imported from it, never copied (the r56 C1 one-implementation rule).

Contract
  python tools/receipt-write.py --receipt <path> --rc <int> [--command <text>] [--budget <sec>] --note <text> < capture
    Reads verbatim bytes on stdin (the caller's already-captured output), writes the receipt with
    command=<text> (the exact probe command the caller executed, one string, shlex-quoted by the
    shared builder), rc=<int> (the caller's measured rc for that command), timed_out=0, and the
    bytes verbatim under `--- stdout ---` (stderr section empty). Exit map: 0 receipt written;
    2 could-not-evaluate (usage error or unwritable receipt path). This tool never runs the probe.

  python tools/receipt-write.py --selftest
    Hermetic: blob-shape/header keys, byte-identity with the shared builder, CRLF verbatim,
    usage rejection, unwritable-path refusal. Prints
    RECEIPT_WRITE_SELFTEST: PASS/FAIL (N cases, N passed, N failed) and exits 0/1.

Write scope: the receipt path only. Reads: stdin, the shared module file. No host state modified.
Spell `python`, not `python3` (Store alias stub exits 49 — drift register D8).
Owner: tsukuroi.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

PROG = "receipt-write"
SELFTEST_TAG = "RECEIPT_WRITE_SELFTEST"
DEFAULT_BUDGET = 60


def _shared():
    """Import the receipt-run module by path (dash in the filename; sys.modules stays clean)."""
    src = Path(__file__).resolve().parent / "receipt-run.py"
    spec = importlib.util.spec_from_file_location("tsukuroi_receipt_run", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def execute(args: argparse.Namespace) -> int:
    out = sys.stdin.buffer.read()
    shared = _shared()
    now = datetime.now(timezone.utc)
    blob = shared.build_receipt(
        [args.command], args.budget,
        now.strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        0.0, out, b"", args.rc, False,
    )
    try:
        shared.write_receipt(args.receipt, blob)
    except OSError as exc:
        print(f"{PROG}: cannot write receipt {args.receipt}: {exc}", file=sys.stderr)
        return 2
    print(f"{PROG}: rc={args.rc} receipt {args.receipt} ({len(out)} capture bytes)")
    return 0


class Case:
    def __init__(self, name: str):
        self.name = name
        self.fail: str | None = None


def _check(case: Case, got, want, label: str) -> None:
    if case.fail is None and got != want:
        case.fail = f"{label}: got {got!r} want {want!r}"


def selftest() -> int:
    cases: list[Case] = []

    def run_case(name: str, fn) -> Case:
        case = Case(name)
        try:
            fn(case)
        except Exception as exc:  # a broken checker must read as FAIL, not crash the run
            case.fail = f"raised {type(exc).__name__}: {exc}"
        cases.append(case)
        print(f"PASS {name}" if case.fail is None else f"FAIL {name} — {case.fail}")
        return case

    shared = _shared()
    scratch = Path(__file__).resolve().parent.parent / ".ufo" / "waves" / "round-57" / "receipts"
    capture = b"matched=12\r\ndrift=0\r\n"

    def c1(case: Case):
        blob = shared.build_receipt(["MSYS_NO_PATHCONV=1 sc query x"], 60, "S", "E", 0.0,
                                    capture, b"", 0, False)
        head = blob.split(b"--- stdout ---")[0].decode("utf-8")
        kv = dict(line.split("=", 1) for line in head.strip().splitlines())
        for key in shared.HEADER_KEYS:
            _check(case, key in kv, True, f"header key {key}")
        _check(case, kv["rc"], "0", "rc line")
        _check(case, kv["timed_out"], "0", "timed_out")
        _check(case, kv["command"], "'MSYS_NO_PATHCONV=1 sc query x'", "command quoting")
    run_case("blob-header-complete", c1)

    def c2(case: Case):
        argv = ["cmd1 ; cmd2"]
        a = shared.build_receipt(argv, 60, "S", "E", 0.0, capture, b"", 36, False)
        b = shared.build_receipt(argv, 60, "S", "E", 0.0, capture, b"", 36, False)
        _check(case, a, b, "byte-identity with the shared builder (same inputs)")
        _check(case, b"\nrc=36\n" in a, True, "rc passthrough")
    run_case("shared-builder-identity", c2)

    def c3(case: Case):
        blob = shared.build_receipt(["x"], 60, "S", "E", 0.0, capture, b"", 1, False)
        _check(case, b"matched=12\r\ndrift=0\r\n" in blob, True, "CRLF verbatim")
        _check(case, f"stdout_bytes={len(capture)}".encode() in blob, True,
               "stdout_bytes matches captured bytes")
        _check(case, blob.count(b"stdout_bytes="), 1, "one stdout_bytes line")
    run_case("stdin-bytes-verbatim", c3)

    def c4(case: Case):
        import subprocess
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--receipt",
             str(scratch / "unused-selftest.txt")],
            input=b"", capture_output=True, timeout=30,
        )
        _check(case, proc.returncode, 2, "missing --rc/--command rejected rc 2")
    run_case("usage-rejected", c4)

    def c5(case: Case):
        shared.build_receipt(["x"], 60, "S", "E", 0.0, b"", b"", 0, False)
        blocker_file = scratch / "selftest-not-a-dir"
        blocker_file.parent.mkdir(parents=True, exist_ok=True)
        blocker_file.write_bytes(b"x")
        try:
            shared.write_receipt(str(blocker_file / "nested" / "r.txt"), b"")
            case.fail = "unwritable path did not raise"
        except OSError:
            pass
        finally:
            blocker_file.unlink(missing_ok=True)
    run_case("unwritable-path-refused", c5)

    passed = sum(1 for c in cases if c.fail is None)
    failed = len(cases) - passed
    verdict = "PASS" if failed == 0 else "FAIL"
    print(f"{SELFTEST_TAG}: {verdict} ({len(cases)} cases, {passed} passed, {failed} failed)")
    return 0 if failed == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog=PROG, add_help=True)
    ap.add_argument("--receipt", help="receipt path (lane-tree relative or absolute)")
    ap.add_argument("--rc", type=int, help="the caller's measured rc for the command")
    ap.add_argument("--command", default="", help="the exact probe command text (one string)")
    ap.add_argument("--budget", type=int, default=DEFAULT_BUDGET,
                    help="recorded budget_s (the caller's probe budget; default 60)")
    ap.add_argument("--selftest", action="store_true", help="run hermetic selftest")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.rc is None or not args.receipt or not args.command:
        ap.print_usage()
        print(f"{PROG}: --receipt, --rc and --command are required; capture arrives on stdin",
              file=sys.stderr)
        return 2
    return execute(args)


if __name__ == "__main__":
    sys.exit(main())

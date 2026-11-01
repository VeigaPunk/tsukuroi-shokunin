#!/usr/bin/env python3
"""receipt-run — run a command under a wall-clock budget and write a raw receipt into the lane tree.

Closes the round-53 routed defect class "raw receipts lived in scratch and were deleted with it"
(closure 5cbcb06e defect 3, register rows D7/W5): a host-state measurement is only citable if its
raw output is committed, so this instrument writes the receipt file itself, at a lane-tree path the
caller names. Scratch is never involved.

Contract
  python tools/receipt-run.py --budget <seconds> --receipt <path> -- <command> [args...]
    Runs the command with subprocess (no shell), kills it when the budget expires, and writes the
    receipt file with verbatim stdout/stderr. Exit map: 0 command completed within budget; 1 budget
    expired (timed out); 2 could-not-evaluate (usage error, unwritable receipt path). The child's
    own exit code is recorded in the receipt, not mirrored by this tool.

  python tools/receipt-run.py --selftest
    Hermetic cases over the injected runner (logic) plus one real sleeping-child timeout (the
    interpreter running this tool spawns itself; nothing else on the host is required). Prints
    RECEIPT_RUN_SELFTEST: PASS/FAIL (N cases, N passed, N failed) and exits 0/1.

Receipt format (key=value header, then verbatim captured streams):
  receipt_run=1
  command=<argv, shell-quoted>
  budget_s=<int>
  start_utc=<ISO-8601 Z>
  end_utc=<ISO-8601 Z>
  duration_s=<seconds, one decimal>
  timed_out=0|1
  rc=<child exit int, or the string timeout when timed_out=1>
  timeout_after_s=<int, only when timed_out=1>
  stdout_bytes=<int>
  stderr_bytes=<int>
  --- stdout ---
  <verbatim stdout bytes>
  --- stderr ---
  <verbatim stderr bytes>

Write scope: the receipt path only. Reads: the child's streams. No host state is modified.
Spell `python`, not `python3`, on this host (Store alias stub exits 49 — drift register D8).
Owner: tsukuroi.
"""
from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

PROG = "receipt-run"
SELFTEST_TAG = "RECEIPT_RUN_SELFTEST"
HEADER_KEYS = (
    "receipt_run", "command", "budget_s", "start_utc", "end_utc", "duration_s",
    "timed_out", "rc", "stdout_bytes", "stderr_bytes",
)


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_command(argv: list[str], budget: float) -> tuple[bytes, bytes, int | None, bool]:
    """Run argv with a budget. Returns (stdout, stderr, rc, timed_out). Injected in the selftest."""
    proc = subprocess.Popen(
        argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
    )
    try:
        out, err = proc.communicate(timeout=budget)
    except subprocess.TimeoutExpired:
        # Surface whatever the child produced before the cut, then make sure it is gone.
        try:
            out, err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
        return out or b"", err or b"", None, True
    return out or b"", err or b"", proc.returncode, False


def build_receipt(
    argv: list[str], budget: int, start: str, end: str, duration: float,
    out: bytes, err: bytes, rc: int | str, timed_out: bool,
) -> bytes:
    lines = [
        "receipt_run=1",
        f"command={shlex.join(argv)}",
        f"budget_s={budget}",
        f"start_utc={start}",
        f"end_utc={end}",
        f"duration_s={duration:.1f}",
        f"timed_out={1 if timed_out else 0}",
        f"rc={rc}",
    ]
    if timed_out:
        lines.append(f"timeout_after_s={budget}")
    lines.append(f"stdout_bytes={len(out)}")
    lines.append(f"stderr_bytes={len(err)}")
    blob = ("\n".join(lines) + "\n").encode("utf-8")
    blob += b"--- stdout ---\n" + out
    if out and not out.endswith(b"\n"):
        blob += b"\n"
    blob += b"--- stderr ---\n" + err
    if err and not err.endswith(b"\n"):
        blob += b"\n"
    return blob


def write_receipt(path: str, blob: bytes) -> None:
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as fh:
        fh.write(blob)


def execute(args: argparse.Namespace) -> int:
    start = utcnow()
    t0 = time.monotonic()
    out, err, rc, timed_out = run_command(list(args.command), float(args.budget))
    duration = time.monotonic() - t0
    end = utcnow()
    blob = build_receipt(
        list(args.command), args.budget, start, end, duration, out, err,
        "timeout" if timed_out else rc, timed_out,
    )
    try:
        write_receipt(args.receipt, blob)
    except OSError as exc:
        print(f"{PROG}: cannot write receipt {args.receipt}: {exc}", file=sys.stderr)
        return 2
    if timed_out:
        print(f"{PROG}: timed out after {args.budget}s; receipt {args.receipt}")
        return 1
    print(f"{PROG}: rc={rc} in {duration:.1f}s; receipt {args.receipt}")
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
    py = sys.executable or "python"

    def run_case(name: str, fn) -> Case:
        case = Case(name)
        try:
            fn(case)
        except Exception as exc:  # a broken checker must read as FAIL, not crash the run
            case.fail = f"raised {type(exc).__name__}: {exc}"
        cases.append(case)
        print(f"PASS {name}" if case.fail is None else f"FAIL {name} — {case.fail}")
        return case

    # Injected-runner cases (pure logic, no host dependency beyond this interpreter).
    fake_out = (b"PASS one\nPASS two\n", b"", 0, False)

    def c1(case: Case):
        blob = build_receipt(["echo", "hi"], 10, "S", "E", 0.2, *fake_out[:2], 0, False)
        head = blob.split(b"--- stdout ---")[0].decode("utf-8")
        kv = dict(line.split("=", 1) for line in head.strip().splitlines())
        for key in HEADER_KEYS:
            _check(case, key in kv, True, f"header key {key}")
        _check(case, kv["rc"], "0", "rc")
        _check(case, kv["timed_out"], "0", "timed_out")
        _check(case, kv["command"], "echo hi", "command quoting")
    run_case("rc0-header-complete", c1)

    def c2(case: Case):
        blob = build_receipt(["x"], 5, "S", "E", 1.0, b"out", b"err", 3, False)
        _check(case, b"\nrc=3\n" in blob, True, "rc line")
        _check(case, b"stdout_bytes=3" in blob, True, "stdout bytes")
        _check(case, b"--- stderr ---\nerr\n" in blob, True, "stderr verbatim")
    run_case("rc3-streams-verbatim", c2)

    def c3(case: Case):
        blob = build_receipt(["slow"], 7, "S", "E", 7.1, b"partial", b"", "timeout", True)
        _check(case, b"\nrc=timeout\n" in blob, True, "rc=timeout")
        _check(case, b"timeout_after_s=7" in blob, True, "timeout_after_s")
        _check(case, b"timed_out=1" in blob, True, "timed_out")
    run_case("timeout-receipt-shape", c3)

    def c4(case: Case):
        blob = build_receipt(["a b", "c"], 1, "S", "E", 0.1, b"", b"", 0, False)
        head = blob.split(b"--- stdout ---")[0].decode("utf-8")
        kv = dict(line.split("=", 1) for line in head.strip().splitlines())
        _check(case, kv["command"], "'a b' c", "shlex quoting of spaces")
    run_case("argv-quoting", c4)

    def c5(case: Case):
        blob = build_receipt(["x"], 2, "S", "E", 0.1, b"no newline end", b"", 0, False)
        _check(case, blob.count(b"--- stdout ---"), 1, "one stdout marker")
        _check(case, b"no newline end\n--- stderr ---" in blob, True, "newline separation")
    run_case("stream-separation", c5)

    # Real subprocess cases (this interpreter spawning itself; budget far above spawn cost).
    scratch = Path(__file__).resolve().parent.parent / ".ufo" / "waves" / "round-54" / "after"

    def c6(case: Case):
        receipt = scratch / "receipt-run-selftest-ok.txt"
        argv = [py, "-c", "print('PASS ok'); raise SystemExit(0)"]
        out, err, rc, timed_out = run_command(argv, 30)
        blob = build_receipt(argv, 30, utcnow(), utcnow(), 0.3, out, err, rc, timed_out)
        write_receipt(str(receipt), blob)
        _check(case, (rc, timed_out), (0, False), "child rc/timed_out")
        # Verbatim means the child's own line ending survives: print() emits CRLF on Windows.
        _check(case, b"PASS ok\r\n" in blob or b"PASS ok\n" in blob, True,
               "stdout verbatim in receipt file")
        _check(case, f"stdout_bytes={len(out)}".encode("utf-8") in blob, True,
               "stdout_bytes matches captured bytes")
        receipt.unlink(missing_ok=True)
    run_case("live-child-rc0", c6)

    def c7(case: Case):
        receipt = scratch / "receipt-run-selftest-timeout.txt"
        argv = [py, "-c", "import time; print('PASS early', flush=True); time.sleep(30)"]
        out, err, rc, timed_out = run_command(argv, 1)
        blob = build_receipt(argv, 1, utcnow(), utcnow(), 1.1, out, err, "timeout" if timed_out else rc, timed_out)
        write_receipt(str(receipt), blob)
        _check(case, timed_out, True, "timed_out flag")
        _check(case, b"rc=timeout" in blob, True, "rc=timeout line")
        _check(case, b"PASS early" in blob, True, "partial stdout preserved")
        receipt.unlink(missing_ok=True)
    run_case("live-child-timeout", c7)

    passed = sum(1 for c in cases if c.fail is None)
    failed = len(cases) - passed
    verdict = "PASS" if failed == 0 else "FAIL"
    print(f"{SELFTEST_TAG}: {verdict} ({len(cases)} cases, {passed} passed, {failed} failed)")
    return 0 if failed == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog=PROG, add_help=True)
    ap.add_argument("--budget", type=int, help="wall-clock budget in seconds")
    ap.add_argument("--receipt", help="receipt path (lane-tree relative or absolute)")
    ap.add_argument("--selftest", action="store_true", help="run hermetic selftest")
    ap.add_argument("command", nargs="*", help="command to run, after --")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.budget or args.budget <= 0 or not args.receipt or not args.command:
        ap.print_usage()
        print(f"{PROG}: --budget, --receipt and a command after -- are required", file=sys.stderr)
        return 2
    return execute(args)


if __name__ == "__main__":
    sys.exit(main())

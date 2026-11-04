#!/usr/bin/env python3
"""Semantic cross-check: does the upstream PROSE entail each table cell?

Reads the Restart= prose paragraphs from the pinned XML and checks the table
cells against the prose definitions, so that a transcription error in the
frozen expected object is detectable independently of the table itself.

Prose rules (as written in v262 systemd.service.xml):
  on-success : restarted only when the process exits cleanly
                (exit code 0; for non-oneshot, SIGHUP/SIGINT/SIGTERM/SIGPIPE;
                 anything in SuccessExitStatus=)
  on-failure : non-zero exit code, terminated by a signal (incl. core dump,
                excluding the four clean signals), an operation timing out, or
                the watchdog timeout triggering
  on-abnormal: terminated by a signal (incl. core dump, excluding the four
                clean signals), an operation timing out, or the watchdog timeout
                triggering
  on-abort   : only if the process exits due to an uncaught signal that is not
                specified as a clean exit status
  on-watchdog: only if the watchdog timeout expires
  always     : regardless of clean/unclean exit, abnormal signal, or timeout
  no         : never restarted
"""
import json
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
i = text.find("Configures whether the service shall be restarted")
j = text.find("</table>", i)
prose = re.sub(r"<[^>]+>", " ", text[i:j])
prose = re.sub(r"\s+", " ", prose)

matrix = json.load(open(sys.argv[2]))
rows = {r["cause"]: r["restart"] for r in matrix["rows"]}
settings = matrix["settings"]

CLEAN_SIGNALS = {"SIGHUP", "SIGINT", "SIGTERM", "SIGPIPE"}


def cell(cause, setting):
    return rows[cause][settings.index(setting)]


checks = []


def chk(name, got, want, note=""):
    checks.append((name, got == want, got, want, note))


# --- 'no' column: the prose says "the service will not be restarted".
for cause in rows:
    chk(f"no/{cause}", cell(cause, "no"), False)

# --- 'always' column: "restarted regardless of whether it exited cleanly or
#     not, got terminated abnormally by a signal, or hit a timeout".
#     Every cause in the table is one of those, so always is true for all six.
for cause in rows:
    chk(f"always/{cause}", cell(cause, "always"), True)

# --- on-success: true only for the clean-exit row.
chk("on-success/Clean exit code or signal", cell("Clean exit code or signal", "on-success"), True)
for cause in ["Unclean exit code", "Unclean signal", "Timeout", "Watchdog", "Termination due to OOM"]:
    chk(f"on-success/{cause}", cell(cause, "on-success"), False)

# --- on-failure: non-zero exit code, unclean signal, operation timeout,
#     watchdog timeout. NOT a clean exit.
chk("on-failure/Unclean exit code", cell("Unclean exit code", "on-failure"), True)
chk("on-failure/Unclean signal", cell("Unclean signal", "on-failure"), True)
chk("on-failure/Timeout", cell("Timeout", "on-failure"), True)
chk("on-failure/Watchdog", cell("Watchdog", "on-failure"), True)
chk("on-failure/Clean exit code or signal", cell("Clean exit code or signal", "on-failure"), False)

# --- on-abnormal: unclean signal, operation timeout, watchdog timeout.
#     NOT a non-zero exit code (prose does not list exit codes for on-abnormal),
#     NOT a clean exit.
chk("on-abnormal/Unclean signal", cell("Unclean signal", "on-abnormal"), True)
chk("on-abnormal/Timeout", cell("Timeout", "on-abnormal"), True)
chk("on-abnormal/Watchdog", cell("Watchdog", "on-abnormal"), True)
chk("on-abnormal/Unclean exit code", cell("Unclean exit code", "on-abnormal"), False)
chk("on-abnormal/Clean exit code or signal", cell("Clean exit code or signal", "on-abnormal"), False)

# --- on-abort: uncaught signal that is not a clean exit status.
chk("on-abort/Unclean signal", cell("Unclean signal", "on-abort"), True)
chk("on-abort/Clean exit code or signal", cell("Clean exit code or signal", "on-abort"), False)
chk("on-abort/Unclean exit code", cell("Unclean exit code", "on-abort"), False)
chk("on-abort/Timeout", cell("Timeout", "on-abort"), False)
chk("on-abort/Watchdog", cell("Watchdog", "on-abort"), False)

# --- on-watchdog: only the watchdog row.
chk("on-watchdog/Watchdog", cell("Watchdog", "on-watchdog"), True)
for cause in ["Clean exit code or signal", "Unclean exit code", "Unclean signal", "Timeout", "Termination due to OOM"]:
    chk(f"on-watchdog/{cause}", cell(cause, "on-watchdog"), False)

# --- OOM row: the upstream table marks on-failure and on-abnormal, but not
#     on-abort and not on-watchdog. The prose does not mention OOM at all, so
#     the OOM row is table-only content: it is NOT prose-entailed, and its
#     on-abort=False / on-watchdog=False cells are the upstream table's own
#     choices. Recorded as table-sourced, not prose-derived.
oom_note = "OOM row is not described in the Restart= prose; cell values are table-sourced"

bad = [c for c in checks if not c[1]]
for name, ok, got, want, note in checks:
    if not ok:
        print(f"MISMATCH {name}: table={got} prose-implies={want} {note}")
print(f"prose-entailment checks: {len(checks)}  mismatches: {len(bad)}")
print("OOM row note:", oom_note)
sys.exit(1 if bad else 0)
